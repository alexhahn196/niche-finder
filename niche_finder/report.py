"""Erzeugt report.md: Top 5 mit Belegen und je 10 Video-Blueprints."""
from . import config, state


def _fmt_int(n) -> str:
    return f"{int(n):,}".replace(",", ".")


def _niche_section(rank: int, n: dict) -> list[str]:
    en = n.get("evidence", {}).get("en", {})
    de = n.get("evidence", {}).get("de", {})
    b = n.get("score_breakdown", {})
    lines = [
        f"## {rank}. {n['name']} — Score {n['score']}/100",
        "",
        f"*{n.get('topic', '')} × {n.get('audience', '')} × {n.get('format', '')}*",
        "",
        f"| Newcomer | Monetarisierung | Trend | Sättigung⁻¹ | Machbarkeit | DE | Bonus |",
        f"|---|---|---|---|---|---|---|",
        f"| {b.get('newcomer_25', '?')}/25 | {b.get('monetization_25', '?')}/25 "
        f"| {b.get('trend_15', '?')}/15 | {b.get('saturation_inverse_15', '?')}/15 "
        f"| {b.get('feasibility_10', '?')}/10 | {b.get('de_transferability_10', '?')}/10 "
        f"| +{b.get('energiepilot_bonus_10', 0)} |",
        "",
        f"**EN-Beweis** (Query: `{en.get('query', '?')}`, Trend: {en.get('trend', '?')}):",
        "",
    ]
    for h in en.get("young_100k_channels", [])[:5]:
        lines.append(
            f"- Newcomer-Kanal [{h['channel_title']}]({h['channel_url']}) "
            f"({h['channel_age_months']} Monate alt, {_fmt_int(h['subscribers'])} Abos): "
            f"[{h['best_video_title']}]({h['best_video_url']}) — "
            f"{_fmt_int(h['views'])} Views, Outlier-Score {h['outlier_score']}"
        )
    lines.append("")
    top_outliers = en.get("top_outliers", [])[:3]
    if top_outliers:
        lines.append("**Top-Outlier-Videos (EN):**")
        lines.append("")
        for o in top_outliers:
            lines.append(
                f"- [{o['title']}]({o['url']}) — {_fmt_int(o['views'])} Views, "
                f"Outlier {o['outlier_score']}× (Kanal-Median {_fmt_int(o['channel_median_views'])}, "
                f"[{o['channel_title']}]({o['channel_url']}))"
            )
        lines.append("")
    sat = en.get("saturation", {})
    lines += [
        f"**Sättigung (EN):** {sat.get('unique_channels', '?')} Kanäle in "
        f"{sat.get('results', '?')} Top-Treffern, Mega-Kanal-Anteil "
        f"{round(100 * sat.get('mega_channel_share', 0))} %, "
        f"junge Kanäle {round(100 * sat.get('young_channel_share', 0))} %.",
        "",
        f"**DE-Lage** (Query: `{de.get('query', '?')}`): {de.get('result_count', '?')} Treffer, "
        f"{de.get('living_channel_count', '?')} lebende Kanäle, "
        f"{len(de.get('living_outliers', []))} lebende Outlier "
        f"-> {'DE-Markt aktiv (Beweis, dass es funktioniert)' if de.get('living_outliers') else 'DE-Lücke offen (Arbitrage-Chance)'}.",
        "",
    ]
    for o in de.get("living_outliers", [])[:3]:
        lines.append(
            f"- DE-Outlier: [{o['title']}]({o['url']}) — {_fmt_int(o['views'])} Views, "
            f"Outlier {o['outlier_score']}× ([{o['channel_title']}]({o['channel_url']}))"
        )
    if de.get("living_outliers"):
        lines.append("")
    lines.append("**10 Video-Blueprints:**")
    lines.append("")
    blueprints = n.get("blueprints", [])
    if blueprints:
        for i, bp in enumerate(blueprints[:10], 1):
            if isinstance(bp, dict):
                lines.append(f"{i}. **{bp.get('title', '?')}** — {bp.get('concept', '')}")
            else:
                lines.append(f"{i}. {bp}")
    else:
        lines.append("_Blueprints noch nicht erstellt — via "
                     f"`python -m niche_finder update {n['id']} blueprints.json` anhängen._")
    lines.append("")
    return lines


def generate(store: dict) -> str:
    ranked = state.scored(store)
    win = [n for n in ranked if n.get("score", 0) >= config.TARGET_SCORE]
    top5 = ranked[:5]  # ranked ist nach Score sortiert -> Gewinner stehen vorn
    killed = [n for n in store["niches"].values() if n.get("status") == "killed"]
    lines = [
        "# YouTube-Nischen-Finder — Report",
        "",
        f"Stand: {state.now_iso()} · Iterationen: {store.get('iterations', 0)} · "
        f"geprüft: {sum(1 for n in store['niches'].values() if n.get('status') != 'pending')} · "
        f"gekillt: {len(killed)} · Gewinner (≥{config.TARGET_SCORE}): {len(win)}",
        "",
        "## Top 5",
        "",
        "| # | Nische | Score | Kern-Beleg |",
        "|---|---|---|---|",
    ]
    for i, n in enumerate(top5, 1):
        yc = n.get("evidence", {}).get("en", {}).get("young_100k_channels", [])
        proof = (f"{len(yc)} Newcomer-Kanäle mit 100k+-Video, "
                 f"bester Outlier {max((h['outlier_score'] for h in yc), default=0)}×"
                 if yc else "—")
        lines.append(f"| {i} | {n['name']} | **{n['score']}** | {proof} |")
    lines.append("")
    for i, n in enumerate(top5, 1):
        lines += _niche_section(i, n)
    if killed:
        lines += ["## Gekillte Kandidaten", ""]
        for n in sorted(killed, key=lambda x: x["name"]):
            lines.append(f"- **{n['name']}**: {', '.join(n.get('kill_reasons', []))}")
        lines.append("")
    return "\n".join(lines)


def write(store: dict) -> None:
    config.REPORT_FILE.write_text(generate(store), encoding="utf-8")
