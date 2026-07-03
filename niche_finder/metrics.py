"""Metriken: Kanalalter, Median-Views, Upload-Frequenz, Outlier-Score, Trend."""
import statistics
from datetime import datetime, timezone


def parse_ts(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def age_months(published_at: str, now: datetime | None = None) -> float:
    now = now or datetime.now(timezone.utc)
    return (now - parse_ts(published_at)).days / 30.44


def age_days(published_at: str, now: datetime | None = None) -> float:
    now = now or datetime.now(timezone.utc)
    return (now - parse_ts(published_at)).days


def median(values: list[float]) -> float:
    return float(statistics.median(values)) if values else 0.0


def outlier_score(video_views: int, channel_median_views: float) -> float:
    """Outlier-Score = Video-Views ÷ Median-Views des Kanals."""
    if channel_median_views <= 0:
        return 0.0
    return round(video_views / channel_median_views, 1)


def channel_profile(channel: dict, upload_videos: list[dict]) -> dict:
    """Profil eines Kanals aus channels.list-Item + Stats seiner letzten Uploads."""
    stats = channel.get("statistics", {})
    views = [int(v["statistics"].get("viewCount", 0)) for v in upload_videos]
    dates = sorted(parse_ts(v["snippet"]["publishedAt"]) for v in upload_videos)
    uploads_per_week = 0.0
    if len(dates) >= 2:
        span_days = max((dates[-1] - dates[0]).days, 1)
        uploads_per_week = round((len(dates) - 1) / span_days * 7, 2)
    return {
        "channel_id": channel["id"],
        "title": channel["snippet"]["title"],
        "url": f"https://www.youtube.com/channel/{channel['id']}",
        "age_months": round(age_months(channel["snippet"]["publishedAt"]), 1),
        "subscribers": int(stats.get("subscriberCount", 0)),
        "median_views": median(views),
        "uploads_per_week": uploads_per_week,
        "last_upload_days_ago": age_days(dates[-1].isoformat()) if dates else None,
    }


def trend_label(result_videos: list[dict]) -> tuple[str, dict]:
    """12-Monats-Trend-Näherung aus den Top-50-Ergebnissen (K2).

    Vergleicht Videos der letzten 6 Monate mit Videos, die 6–18 Monate alt
    sind: Publikationsrate pro Monat und Median-Views. Beides klar fallend
    -> "falling" (Kill K2).
    """
    recent, mid = [], []
    for v in result_videos:
        days = age_days(v["snippet"]["publishedAt"])
        views = int(v["statistics"].get("viewCount", 0))
        if days <= 183:
            recent.append(views)
        elif days <= 548:
            mid.append(views)
    detail = {
        "videos_0_6m": len(recent), "videos_6_18m": len(mid),
        "median_views_0_6m": median(recent), "median_views_6_18m": median(mid),
    }
    if len(recent) + len(mid) < 8:
        return "unclear", detail
    rate_recent = len(recent) / 6            # Videos pro Monat, letzte 6 Monate
    rate_mid = len(mid) / 12                 # Videos pro Monat, 6–18 Monate
    view_ratio = (median(recent) / median(mid)) if median(mid) > 0 else 1.0
    detail["rate_ratio"] = round(rate_recent / rate_mid, 2) if rate_mid else None
    detail["view_ratio"] = round(view_ratio, 2)
    if rate_mid > 0 and rate_recent < 0.6 * rate_mid and view_ratio < 0.7:
        return "falling", detail
    if rate_mid == 0 or rate_recent > 1.3 * rate_mid:
        if view_ratio > 1.3:
            return "rising_strong", detail
        return "rising", detail
    if view_ratio > 1.3:
        return "rising", detail
    return "flat", detail
