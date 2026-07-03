"""YouTube Data API v3 – dünner Wrapper mit Cache + Quota-Buchhaltung.

Für Tests kann ein Fake-Service injiziert werden (gleiche Methodenkette wie
googleapiclient: service.search().list(**p).execute() usw.).
"""
from . import config
from .cache import cached_call


def _chunks(seq, size=50):
    for i in range(0, len(seq), size):
        yield seq[i:i + size]


class YouTubeClient:
    def __init__(self, service=None):
        if service is None:
            from googleapiclient.discovery import build
            service = build("youtube", "v3", developerKey=config.api_key())
        self.service = service

    # ------------------------------------------------------------- Endpunkte

    def search_top50(self, query: str, lang: str) -> list[dict]:
        """Top-50-Videosuche. lang: 'en' (US) oder 'de' (DE). Kostet 100 Units."""
        region = {"en": "US", "de": "DE"}[lang]
        params = {
            "part": "snippet", "q": query, "type": "video",
            "maxResults": config.SEARCH_RESULTS,
            "relevanceLanguage": lang, "regionCode": region,
        }
        resp = cached_call(
            "search", params, config.SEARCH_COST,
            lambda: self.service.search().list(**params).execute(),
        )
        return resp.get("items", [])

    def videos(self, video_ids: list[str]) -> dict[str, dict]:
        """statistics+snippet für bis zu N Videos. 1 Unit pro 50er-Batch."""
        out = {}
        for batch in _chunks(sorted(set(video_ids))):
            params = {"part": "snippet,statistics", "id": ",".join(batch)}
            resp = cached_call(
                "videos", params, config.LIST_COST,
                lambda p=params: self.service.videos().list(**p).execute(),
            )
            for item in resp.get("items", []):
                out[item["id"]] = item
        return out

    def channels(self, channel_ids: list[str]) -> dict[str, dict]:
        """snippet+statistics+contentDetails für Kanäle. 1 Unit pro 50er-Batch."""
        out = {}
        for batch in _chunks(sorted(set(channel_ids))):
            params = {"part": "snippet,statistics,contentDetails", "id": ",".join(batch)}
            resp = cached_call(
                "channels", params, config.LIST_COST,
                lambda p=params: self.service.channels().list(**p).execute(),
            )
            for item in resp.get("items", []):
                out[item["id"]] = item
        return out

    def recent_upload_ids(self, uploads_playlist_id: str) -> list[str]:
        """Video-IDs der letzten Uploads eines Kanals (1 Unit)."""
        params = {
            "part": "contentDetails", "playlistId": uploads_playlist_id,
            "maxResults": config.UPLOADS_PER_CHANNEL,
        }
        resp = cached_call(
            "playlistItems", params, config.LIST_COST,
            lambda: self.service.playlistItems().list(**params).execute(),
        )
        return [i["contentDetails"]["videoId"] for i in resp.get("items", [])]
