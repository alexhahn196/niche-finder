"""Money-Proof-Messmodul: 90-Tage-LONGFORM-Run-Rate je Kanal -> $/Monat.

Nutzt die niche_finder-Infrastruktur (cached_call = Cache + Quota-Buchhaltung).
Shorts (< 180 s) werden getrennt erfasst und NIE in den Umsatz gerechnet
(User-Vorgabe: Beweis nur über Longform).
"""
import datetime as dt
import re
import sys

sys.path.insert(0, "/home/user/niche-finder")
from niche_finder import config
from niche_finder.cache import cached_call

LONGFORM_SEC = 180          # >= 3 Min = Longform
MIDROLL_SEC = 480           # >= 8 Min = Mid-Roll-fähig (voller RPM)
RUNRATE_DAYS = 90

_service = None


def service():
    global _service
    if _service is None:
        from googleapiclient.discovery import build
        _service = build("youtube", "v3", developerKey=config.api_key())
    return _service


def _now():
    return dt.datetime.now(dt.timezone.utc)


def _parse_ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def iso_dur_sec(d):
    # Robust gegen P#DT#H#M#S (Videos > 24 h) und P0D (Livestreams)
    m = re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "PT0S")
    if not m:
        return 0
    days, h, mi, s = (int(x) if x else 0 for x in m.groups())
    return days * 86400 + h * 3600 + mi * 60 + s


def channels_info(channel_ids):
    """snippet+statistics+contentDetails, gebatcht, 1 Unit je 50."""
    out = {}
    ids = sorted(set(channel_ids))
    for i in range(0, len(ids), 50):
        batch = ids[i:i + 50]
        params = {"part": "snippet,statistics,contentDetails", "id": ",".join(batch)}
        resp = cached_call("channels", params, config.LIST_COST,
                           lambda p=params: service().channels().list(**p).execute())
        for it in resp.get("items", []):
            it.setdefault("statistics", {})
            out[it["id"]] = it
    return out


def videos_full(video_ids):
    """snippet+statistics+contentDetails (mit Dauer!), gebatcht."""
    out = {}
    ids = sorted(set(video_ids))
    for i in range(0, len(ids), 50):
        batch = ids[i:i + 50]
        params = {"part": "snippet,statistics,contentDetails", "id": ",".join(batch)}
        resp = cached_call("videos", params, config.LIST_COST,
                           lambda p=params: service().videos().list(**p).execute())
        for it in resp.get("items", []):
            it.setdefault("statistics", {})
            out[it["id"]] = it
    return out


def recent_upload_ids_50(uploads_playlist_id):
    params = {"part": "contentDetails", "playlistId": uploads_playlist_id,
              "maxResults": 50}
    resp = cached_call("playlistItems", params, config.LIST_COST,
                       lambda: service().playlistItems().list(**params).execute())
    return [i["contentDetails"]["videoId"] for i in resp.get("items", [])]


def measure_channel(channel_id, ch=None):
    """90d-Run-Rate eines Kanals, Longform/Shorts getrennt. ~2 Units (ungecacht)."""
    now = _now()
    if ch is None:
        ch = channels_info([channel_id]).get(channel_id)
    if not ch:
        return {"channel_id": channel_id, "fehler": "Kanal nicht gefunden"}
    st = ch.get("statistics", {})
    res = {
        "channel_id": channel_id,
        "name": ch["snippet"]["title"],
        "url": f"https://www.youtube.com/channel/{channel_id}",
        "alter_monate": round((now - _parse_ts(ch["snippet"]["publishedAt"])).days / 30.4, 1),
        "subs": int(st.get("subscriberCount", 0)),
        "total_views": int(st.get("viewCount", 0)),
        "videos_gesamt": int(st.get("videoCount", 0)),
    }
    pl = (ch.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")
          or "UU" + channel_id[2:])
    try:
        vids = videos_full(recent_upload_ids_50(pl))
    except Exception as e:
        if "quota" in str(e).lower():
            raise
        res["fehler"] = str(e)[:120]
        return res
    lf, sh, n_lf, n_mid = 0, 0, 0, 0
    oldest_in_window = None
    best = None
    for v in vids.values():
        pub = _parse_ts(v["snippet"]["publishedAt"])
        age = (now - pub).days
        views = int(v["statistics"].get("viewCount", 0))
        dur = iso_dur_sec(v.get("contentDetails", {}).get("duration"))
        if dur >= LONGFORM_SEC and (best is None or views > best["views"]):
            best = {"titel": v["snippet"]["title"][:70], "views": views,
                    "age_days": age, "dauer_min": round(dur / 60, 1),
                    "url": f"https://www.youtube.com/watch?v={v['id']}"}
        if age <= RUNRATE_DAYS:
            oldest_in_window = max(oldest_in_window or 0, age)
            if dur >= LONGFORM_SEC:
                lf += views; n_lf += 1
                if dur >= MIDROLL_SEC:
                    n_mid += 1
            else:
                sh += views
    # Falls die letzten 50 Uploads das 90d-Fenster nicht abdecken (Vielposter),
    # Fenster auf das tatsächlich abgedeckte kürzen — sonst unterschätzen wir.
    window = RUNRATE_DAYS
    if len(vids) == 50:
        ages = sorted((now - _parse_ts(v["snippet"]["publishedAt"])).days
                      for v in vids.values())
        if ages and ages[-1] < RUNRATE_DAYS:
            window = max(ages[-1], 30)
    res.update({
        "lf_views_90d": lf, "lf_n_90d": n_lf, "lf_n_midroll": n_mid,
        "shorts_views_90d": sh, "runrate_fenster_tage": window,
        "lf_monat": round(lf / (window / 30.4)),
        "bestes_lf_video": best,
    })
    return res


def usd_monat(lf_monat, rpm_lo, rpm_hi):
    return (round(lf_monat / 1000 * rpm_lo), round(lf_monat / 1000 * rpm_hi))


def fmt_row(m, rpm_lo, rpm_hi):
    if m.get("fehler"):
        return f"  !! {m.get('name', m['channel_id'])}: {m['fehler']}"
    lo, hi = usd_monat(m["lf_monat"], rpm_lo, rpm_hi)
    best = m.get("bestes_lf_video") or {}
    return (f"  {m['name'][:32]:<32} {m['alter_monate']:>5.1f}Mo {m['subs']:>8,} Abos "
            f"LF/Mo {m['lf_monat']:>9,} -> {lo:>6,}-{hi:<6,}$ "
            f"(best: {best.get('views', 0):,} v, {best.get('dauer_min', 0)}min)")
