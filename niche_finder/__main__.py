"""CLI: seed | add | update | evaluate | status | top | report"""
import argparse
import json
import sys

from . import config, report, state
from .seeds import START_SEEDS


def _print_stop_status(store) -> bool:
    """Zeigt Stopp-Kriterien an; True = ein Stopp-Kriterium ist erreicht."""
    win = state.winners(store)
    iters = store.get("iterations", 0)
    remaining = state.remaining_today()
    print(f"Gewinner (Score >= {config.TARGET_SCORE}): {len(win)}/{config.TARGET_COUNT}")
    print(f"Iterationen: {iters}/{config.MAX_ITERATIONS}")
    print(f"Quota heute: {state.used_today()}/{config.DAILY_QUOTA} verbraucht, "
          f"{remaining} übrig (Stopp bei < {config.QUOTA_STOP_THRESHOLD})")
    if len(win) >= config.TARGET_COUNT:
        print(f"\n=> ZIEL ERREICHT: {config.TARGET_COUNT} Nischen >= {config.TARGET_SCORE}. "
              "Jetzt `python -m niche_finder report`.")
        return True
    if iters >= config.MAX_ITERATIONS:
        print("\n=> STOPP: 30 Iterationen erreicht. Report erstellen.")
        return True
    if remaining < config.QUOTA_STOP_THRESHOLD:
        print("\n=> QUOTA-STOPP: morgen nahtlos fortsetzen (Checkpoint vorhanden).")
        return True
    return False


def cmd_seed(_args):
    store = state.load_store()
    added, rejected = state.add_candidates(store, [dict(s) for s in START_SEEDS])
    state.save_store(store)
    print(f"Seeds angelegt: {len(added)}, bereits vorhanden: {len(rejected)}")


def cmd_add(args):
    candidates = json.loads(open(args.file, encoding="utf-8").read())
    required = {"id", "name", "topic", "audience", "format", "queries_en", "queries_de",
                "rpm_category_usd", "affiliate_potential", "needs_us_context",
                "feasibility_10_15h", "de_transferability", "energiepilot_synergy"}
    for cand in candidates:
        missing = required - set(cand)
        if missing:
            sys.exit(f"Kandidat {cand.get('id', '?')}: Felder fehlen: {sorted(missing)}")
    store = state.load_store()
    added, rejected = state.add_candidates(store, candidates)
    state.save_store(store)
    print(f"Hinzugefügt: {added}")
    if rejected:
        print(f"Abgelehnt (schon geprüft/vorhanden – nichts doppelt prüfen): {rejected}")


def cmd_update(args):
    store = state.load_store()
    if args.id not in store["niches"]:
        sys.exit(f"Unbekannte Nische: {args.id}")
    patch = json.loads(open(args.file, encoding="utf-8").read())
    store["niches"][args.id].update(patch)
    state.save_store(store)
    print(f"{args.id} aktualisiert: {sorted(patch)}")


def cmd_evaluate(args):
    from .evaluate import evaluate_candidate
    from .youtube_client import YouTubeClient
    try:
        from googleapiclient.errors import HttpError
    except ImportError:  # pragma: no cover
        HttpError = ()

    store = state.load_store()
    if _print_stop_status(store):
        return
    todo = state.pending(store)
    if args.limit:
        todo = todo[:args.limit]
    if not todo:
        print("Keine offenen Kandidaten. Neue generieren: siehe CLAUDE.md, dann `add`.")
        return

    yt = YouTubeClient()
    print(f"\nBewerte {len(todo)} Kandidaten ...")
    for cand in todo:
        if len(state.winners(store)) >= config.TARGET_COUNT:
            print("Ziel erreicht – Bewertung gestoppt.")
            break
        try:
            evaluate_candidate(yt, cand)
        except state.QuotaExceeded as exc:
            state.write_checkpoint(str(exc), [c["id"] for c in state.pending(store)])
            print(f"\nQUOTA-STOPP: {exc}\nCheckpoint geschrieben – morgen fortsetzen.")
            break
        except HttpError as exc:
            if "quota" in str(exc).lower():
                state.write_checkpoint(str(exc), [c["id"] for c in state.pending(store)])
                print(f"\nQUOTA-STOPP (API-Fehler): {exc}\nCheckpoint geschrieben.")
                break
            cand["status"] = "error"
            cand["error"] = str(exc)
            print(f"  FEHLER {cand['id']}: {exc}")
        else:
            state.clear_checkpoint()
            if cand["status"] == "killed":
                print(f"  KILL  {cand['id']}: {', '.join(cand['kill_reasons'])}")
            else:
                print(f"  SCORE {cand['id']}: {cand['score']}/100")
        store["niches"][cand["id"]] = cand
        state.save_store(store)
    print()
    _print_stop_status(store)


def cmd_status(_args):
    store = state.load_store()
    counts = {}
    for n in store["niches"].values():
        counts[n.get("status", "?")] = counts.get(n.get("status", "?"), 0) + 1
    print(f"Kandidaten gesamt: {len(store['niches'])}  {counts}")
    _print_stop_status(store)
    if config.CHECKPOINT_FILE.exists():
        cp = json.loads(config.CHECKPOINT_FILE.read_text(encoding="utf-8"))
        print(f"\nCheckpoint vom {cp['written_at']}: {cp['reason']}")
        print(f"Offen: {cp['pending_ids']}")


def cmd_top(args):
    store = state.load_store()
    ranked = state.scored(store)[:args.n]
    if not ranked:
        print("Noch keine bewerteten Nischen.")
        return
    print("Top-Scorer (Muster als Seeds für die nächste Generation):\n")
    for n in ranked:
        print(f"  {n['score']:>3}  {n['name']}  "
              f"[{n.get('topic')} × {n.get('audience')} × {n.get('format')}]")


def cmd_report(_args):
    store = state.load_store()
    report.write(store)
    print(f"Report geschrieben: {config.REPORT_FILE}")


def main():
    p = argparse.ArgumentParser(prog="niche_finder",
                                description="YouTube-Nischen-Finder (EN->DE-Arbitrage)")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("seed", help="Start-Seeds anlegen").set_defaults(fn=cmd_seed)
    sp = sub.add_parser("add", help="Kandidaten aus JSON-Datei anlegen")
    sp.add_argument("file")
    sp.set_defaults(fn=cmd_add)
    sp = sub.add_parser("update", help="Nische mit JSON-Patch aktualisieren (z. B. blueprints)")
    sp.add_argument("id")
    sp.add_argument("file")
    sp.set_defaults(fn=cmd_update)
    sp = sub.add_parser("evaluate", help="offene Kandidaten mit API-Daten bewerten")
    sp.add_argument("--limit", type=int, default=0, help="max. Kandidaten in diesem Lauf")
    sp.set_defaults(fn=cmd_evaluate)
    sub.add_parser("status", help="Fortschritt + Stopp-Kriterien").set_defaults(fn=cmd_status)
    sp = sub.add_parser("top", help="Top-Scorer anzeigen")
    sp.add_argument("--n", type=int, default=10)
    sp.set_defaults(fn=cmd_top)
    sub.add_parser("report", help="report.md schreiben").set_defaults(fn=cmd_report)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
