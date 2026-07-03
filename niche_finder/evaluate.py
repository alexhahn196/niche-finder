"""Bewertungs-Pipeline: echte API-Daten -> Kill-Kriterien K1-K5 -> Scorecard 0-100.

Datengetrieben: K1 (Newcomer-Beweis), K2 (Trend), K5 (DE tot).
Aus Agent-Einschätzung im Kandidaten-JSON: K3 (Monetarisierung), K4 (US-Kontext).
"""
from . import config, metrics, state


def _is_quota_error(exc) -> bool:
    return "quota" in str(exc).lower()


# ------------------------------------------------------------ Datensammlung

def analyze_language(yt, query: str, lang: str) -> dict:
    """Top-50-Suche + Kanal-Tiefenanalyse für eine Sprache ('en'/'de')."""
    items = yt.search_top50(query, lang)
    video_ids = [i["id"]["videoId"] for i in items if i["id"].get("videoId")]
    vids = yt.videos(video_ids)
    result_videos = [vids[v] for v in video_ids if v in vids]

    channel_ids = sorted({v["snippet"]["channelId"] for v in result_videos})
    chans = yt.channels(channel_ids)

    max_views = {}
    for v in result_videos:
        cid = v["snippet"]["channelId"]
        views = int(v["statistics"].get("viewCount", 0))
        max_views[cid] = max(max_views.get(cid, 0), views)

    # Tiefenanalyse: junge Kanäle zuerst, dann die mit den größten Videos
    def priority(cid):
        young = metrics.age_months(chans[cid]["snippet"]["publishedAt"]) < 24
        return (0 if young else 1, -max_views.get(cid, 0))

    deep_ids = sorted([c for c in channel_ids if c in chans], key=priority)
    deep_ids = deep_ids[:config.DEEP_DIVE_CHANNELS]

    # Uploads aller Deep-Dive-Kanäle holen (gebatcht -> wenig Units)
    upload_ids: list[str] = []
    for cid in deep_ids:
        playlist = (chans[cid].get("contentDetails", {})
                    .get("relatedPlaylists", {}).get("uploads"))
        if playlist:
            try:
                upload_ids += yt.recent_upload_ids(playlist)
            except state.QuotaExceeded:
                raise
            except Exception as exc:
                if _is_quota_error(exc):
                    raise
                continue  # z. B. gelöschte/leere Playlist (404)
    upload_vids = yt.videos(upload_ids)
    uploads_by_channel: dict[str, list[dict]] = {cid: [] for cid in deep_ids}
    for v in upload_vids.values():
        cid = v["snippet"]["channelId"]
        if cid in uploads_by_channel:
            uploads_by_channel[cid].append(v)

    profiles = {cid: metrics.channel_profile(chans[cid], uploads_by_channel[cid])
                for cid in deep_ids}

    # Outlier-Scores: Suchergebnis-Videos + Uploads der Deep-Dive-Kanäle
    outliers = []
    seen = set()
    for v in result_videos + [u for vs in uploads_by_channel.values() for u in vs]:
        if v["id"] in seen:
            continue
        seen.add(v["id"])
        prof = profiles.get(v["snippet"]["channelId"])
        if not prof or prof["median_views"] <= 0:
            continue
        views = int(v["statistics"].get("viewCount", 0))
        outliers.append({
            "video_id": v["id"],
            "title": v["snippet"]["title"],
            "url": f"https://www.youtube.com/watch?v={v['id']}",
            "views": views,
            "published_at": v["snippet"]["publishedAt"],
            "age_days": round(metrics.age_days(v["snippet"]["publishedAt"])),
            "outlier_score": metrics.outlier_score(views, prof["median_views"]),
            "channel_title": prof["title"],
            "channel_url": prof["url"],
            "channel_age_months": prof["age_months"],
            "channel_median_views": prof["median_views"],
            "channel_subscribers": prof["subscribers"],
        })
    outliers.sort(key=lambda o: o["outlier_score"], reverse=True)

    # K1-Beweis: Kanal < 12 Monate mit einem Video >= 100k Views
    young_100k = []
    best_by_channel: dict[str, dict] = {}
    for v in result_videos + [u for vs in uploads_by_channel.values() for u in vs]:
        cid = v["snippet"]["channelId"]
        ch = chans.get(cid)
        if not ch or metrics.age_months(ch["snippet"]["publishedAt"]) >= config.YOUNG_CHANNEL_MONTHS:
            continue
        views = int(v["statistics"].get("viewCount", 0))
        if views >= config.OUTLIER_VIEWS_K1:
            best = best_by_channel.get(cid)
            if not best or views > best["views"]:
                prof = profiles.get(cid) or {}
                best_by_channel[cid] = {
                    "channel_title": ch["snippet"]["title"],
                    "channel_url": f"https://www.youtube.com/channel/{cid}",
                    "channel_age_months": round(metrics.age_months(ch["snippet"]["publishedAt"]), 1),
                    "subscribers": int(ch.get("statistics", {}).get("subscriberCount", 0)),
                    "best_video_title": v["snippet"]["title"],
                    "best_video_url": f"https://www.youtube.com/watch?v={v['id']}",
                    "views": views,
                    "outlier_score": metrics.outlier_score(views, prof.get("median_views", 0)),
                }
    young_100k = sorted(best_by_channel.values(), key=lambda h: h["views"], reverse=True)

    trend, trend_detail = metrics.trend_label(result_videos)

    # Sättigung
    n = max(len(result_videos), 1)
    mega = sum(1 for v in result_videos
               if int(chans.get(v["snippet"]["channelId"], {}).get("statistics", {})
                      .get("subscriberCount", 0)) > 1_000_000)
    young24 = sum(1 for v in result_videos
                  if v["snippet"]["channelId"] in chans
                  and metrics.age_months(chans[v["snippet"]["channelId"]]["snippet"]["publishedAt"]) < 24)
    saturation = {
        "results": len(result_videos),
        "unique_channels": len(channel_ids),
        "unique_ratio": round(len(channel_ids) / n, 2),
        "mega_channel_share": round(mega / n, 2),
        "young_channel_share": round(young24 / n, 2),
    }

    # Lebenszeichen (für K5 auf der DE-Seite)
    alive_recent = {v["snippet"]["channelId"] for v in result_videos
                    if metrics.age_days(v["snippet"]["publishedAt"]) <= 120}
    alive_deep = {cid for cid, p in profiles.items()
                  if p["last_upload_days_ago"] is not None and p["last_upload_days_ago"] <= 120}
    living_outliers = [o for o in outliers
                       if o["age_days"] <= 365
                       and ((o["outlier_score"] >= 3 and o["views"] >= 20_000)
                            or o["views"] >= 100_000)]

    return {
        "query": query,
        "lang": lang,
        "result_count": len(result_videos),
        "trend": trend,
        "trend_detail": trend_detail,
        "saturation": saturation,
        "young_100k_channels": young_100k,
        "top_outliers": outliers[:8],
        "channel_profiles": sorted(profiles.values(),
                                   key=lambda p: p["subscribers"], reverse=True),
        "living_channel_count": len(alive_recent | alive_deep),
        "living_outliers": living_outliers[:5],
    }


# ------------------------------------------------------------ Kill-Kriterien

def kill_criteria(cand: dict, en: dict, de: dict) -> list[str]:
    kills = []
    if not en["young_100k_channels"]:
        kills.append("K1")  # kein Kanal <12 Monate mit >=100k-Video
    if en["trend"] == "falling":
        kills.append("K2")  # 12-Monats-Trend fallend
    if not cand.get("affiliate_potential") and cand.get("rpm_category_usd", 0) < 8:
        kills.append("K3")  # kein Affiliate UND RPM < 8$
    if cand.get("needs_us_context"):
        kills.append("K4")  # braucht US-Kontext
    de_tried_and_dead = (de["result_count"] >= 10
                         and de["living_channel_count"] == 0
                         and not de["living_outliers"])
    if de_tried_and_dead:
        kills.append("K5")  # in DE nur tote Kanäle, keine lebenden Outlier
    overrides = set(cand.get("kill_overrides", []))
    return [k for k in kills if k not in overrides]


# ----------------------------------------------------------------- Scorecard

def _clamp(x, lo, hi):
    return max(lo, min(hi, x))


def scorecard(cand: dict, en: dict, de: dict) -> tuple[int, dict]:
    # Newcomer-Beweis (25)
    yc = en["young_100k_channels"]
    base = {0: 0, 1: 12, 2: 16}.get(len(yc), 20)
    best_outlier = max((h["outlier_score"] for h in yc), default=0)
    outlier_bonus = 5 if best_outlier >= 10 else 3 if best_outlier >= 5 else 1 if best_outlier >= 2 else 0
    newcomer = min(25, base + outlier_bonus) if yc else 0

    # Monetarisierung (25)
    rpm = cand.get("rpm_category_usd", 0)
    rpm_pts = 15 if rpm >= 20 else 12 if rpm >= 12 else 9 if rpm >= 8 else 5 if rpm >= 4 else 2
    monetization = rpm_pts + (10 if cand.get("affiliate_potential") else 0)

    # Trend (15)
    trend_pts = {"rising_strong": 15, "rising": 12, "flat": 8,
                 "unclear": 6, "falling": 0}[en["trend"]]

    # Sättigung invers (15)
    sat = en["saturation"]
    saturation_pts = round(15 * (0.4 * sat["unique_ratio"]
                                 + 0.4 * (1 - sat["mega_channel_share"])
                                 + 0.2 * min(1.0, sat["young_channel_share"] * 3)))

    # Machbarkeit bei 10-15h/Woche (10) – Agent-Einschätzung
    feasibility = _clamp(int(cand.get("feasibility_10_15h", 0)), 0, 10)

    # DE-Übertragbarkeit (10) – Agent-Einschätzung, +1 wenn DE-Beweis existiert
    de_pts = _clamp(int(cand.get("de_transferability", 0)), 0, 10)
    if de["living_outliers"]:
        de_pts = min(10, de_pts + 1)

    # BONUS: EnergiePilot-Synergie (+10)
    synergy = 10 if cand.get("energiepilot_synergy") else 0

    breakdown = {
        "newcomer_25": newcomer,
        "monetization_25": monetization,
        "trend_15": trend_pts,
        "saturation_inverse_15": saturation_pts,
        "feasibility_10": feasibility,
        "de_transferability_10": de_pts,
        "energiepilot_bonus_10": synergy,
    }
    total = min(100, sum(breakdown.values()))
    return total, breakdown


# ------------------------------------------------------------------ Pipeline

def evaluate_candidate(yt, cand: dict) -> dict:
    """Bewertet einen Kandidaten mit echten API-Daten. Mutiert und liefert `cand`."""
    # K3/K4 hängen nur von Agent-Feldern ab -> vor jedem API-Call prüfen,
    # damit tote Kandidaten keine Quota kosten.
    overrides = set(cand.get("kill_overrides", []))
    pre_kills = []
    if not cand.get("affiliate_potential") and cand.get("rpm_category_usd", 0) < 8:
        pre_kills.append("K3")
    if cand.get("needs_us_context"):
        pre_kills.append("K4")
    pre_kills = [k for k in pre_kills if k not in overrides]
    if pre_kills:
        cand["status"] = "killed"
        cand["kill_reasons"] = pre_kills
        cand["score"] = 0
        cand["evaluated_at"] = state.now_iso()
        cand["evidence"] = {"note": "K3/K4 aus Agent-Feldern - ohne API-Quota gekillt"}
        return cand

    en = analyze_language(yt, cand["queries_en"][0], "en")
    de = analyze_language(yt, cand["queries_de"][0], "de")
    kills = kill_criteria(cand, en, de)
    cand["evidence"] = {"en": en, "de": de}
    cand["evaluated_at"] = state.now_iso()
    if kills:
        cand["status"] = "killed"
        cand["kill_reasons"] = kills
        cand["score"] = 0
    else:
        score, breakdown = scorecard(cand, en, de)
        cand["status"] = "evaluated"
        cand["kill_reasons"] = []
        cand["score"] = score
        cand["score_breakdown"] = breakdown
    return cand
