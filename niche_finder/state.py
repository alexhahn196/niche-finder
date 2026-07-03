"""Persistenter Speicher: state/niches.json, Quota-Buchhaltung, Checkpoint."""
import json
from datetime import datetime, timezone

from . import config


def _quota_day() -> str:
    """YouTube-Quota resettet um Mitternacht Pacific Time."""
    try:
        from zoneinfo import ZoneInfo
        tz = ZoneInfo("America/Los_Angeles")
    except Exception:
        tz = timezone.utc
    return datetime.now(tz).date().isoformat()


def _load_json(path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def _save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------- niches.json

def load_store() -> dict:
    return _load_json(config.NICHES_FILE, {"iterations": 0, "niches": {}})


def save_store(store: dict) -> None:
    _save_json(config.NICHES_FILE, store)


def add_candidates(store: dict, candidates: list[dict]) -> tuple[list[str], list[str]]:
    """Fügt Kandidaten hinzu. Doppelte IDs/Namen werden abgelehnt (nichts doppelt prüfen).

    Liefert (hinzugefügte IDs, abgelehnte IDs).
    """
    existing_names = {n["name"].strip().lower() for n in store["niches"].values()}
    added, rejected = [], []
    for cand in candidates:
        cid = cand["id"]
        if cid in store["niches"] or cand["name"].strip().lower() in existing_names:
            rejected.append(cid)
            continue
        cand.setdefault("status", "pending")
        cand["added_at"] = now_iso()
        store["niches"][cid] = cand
        existing_names.add(cand["name"].strip().lower())
        added.append(cid)
    if added:
        store["iterations"] += 1
    return added, rejected


def pending(store: dict) -> list[dict]:
    return [n for n in store["niches"].values() if n.get("status") == "pending"]


def scored(store: dict) -> list[dict]:
    done = [n for n in store["niches"].values() if n.get("status") == "evaluated"]
    return sorted(done, key=lambda n: n.get("score", 0), reverse=True)


def winners(store: dict) -> list[dict]:
    return [n for n in scored(store) if n.get("score", 0) >= config.TARGET_SCORE]


# ----------------------------------------------------------------- quota.json

class QuotaExceeded(Exception):
    """Tages-Quota unter 10 % – Stopp laut Briefing."""


def _quota() -> dict:
    return _load_json(config.QUOTA_FILE, {})


def used_today() -> int:
    return int(_quota().get(_quota_day(), 0))


def remaining_today() -> int:
    return config.DAILY_QUOTA - used_today()


def charge(units: int) -> None:
    """Bucht Units. Wirft QuotaExceeded, BEVOR das Budget unter 10 % fallen würde."""
    if remaining_today() - units < config.QUOTA_STOP_THRESHOLD:
        raise QuotaExceeded(
            f"Quota-Stopp: {remaining_today()} Units übrig, "
            f"Anfrage kostet {units}, Reserve ist {config.QUOTA_STOP_THRESHOLD}."
        )
    data = _quota()
    key = _quota_day()
    data[key] = int(data.get(key, 0)) + units
    _save_json(config.QUOTA_FILE, data)


# ------------------------------------------------------------- checkpoint.json

def write_checkpoint(reason: str, pending_ids: list[str]) -> None:
    _save_json(config.CHECKPOINT_FILE, {
        "written_at": now_iso(),
        "reason": reason,
        "pending_ids": pending_ids,
        "resume": "Morgen einfach wieder `python -m niche_finder evaluate` ausführen – "
                  "der Cache macht bereits geholte Antworten kostenlos.",
    })


def clear_checkpoint() -> None:
    if config.CHECKPOINT_FILE.exists():
        config.CHECKPOINT_FILE.unlink()
