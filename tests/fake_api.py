"""Fake für die googleapiclient-Kette: service.search().list(**p).execute() usw."""
from datetime import datetime, timedelta, timezone


def iso(days_ago: float) -> str:
    dt = datetime.now(timezone.utc) - timedelta(days=days_ago)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


class FakeData:
    def __init__(self):
        self.searches = {}   # (query, lang) -> [video_id, ...]
        self.videos = {}     # video_id -> videos.list-Item
        self.channels = {}   # channel_id -> channels.list-Item
        self.playlists = {}  # playlist_id -> [video_id, ...]

    def add_channel(self, cid, *, age_days, subs, uploads, title=None):
        """uploads: Liste (days_ago, views). Legt Kanal + Upload-Videos an."""
        self.channels[cid] = {
            "id": cid,
            "snippet": {"title": title or cid, "publishedAt": iso(age_days)},
            "statistics": {"subscriberCount": str(subs)},
            "contentDetails": {"relatedPlaylists": {"uploads": f"UU{cid}"}},
        }
        vids = []
        for i, (days_ago, views) in enumerate(uploads):
            vid = f"{cid}-u{i}"
            self._add_video(vid, cid, days_ago, views)
            vids.append(vid)
        self.playlists[f"UU{cid}"] = vids
        return vids

    def _add_video(self, vid, cid, days_ago, views):
        self.videos[vid] = {
            "id": vid,
            "snippet": {"channelId": cid, "publishedAt": iso(days_ago),
                        "title": f"Video {vid}"},
            "statistics": {"viewCount": str(views)},
        }

    def add_search_result(self, query, lang, cid, days_ago=None, views=None, vid=None):
        """Hängt ein Video an die Suchergebnisse (vid=None -> neues Video anlegen)."""
        if vid is None:
            vid = f"{cid}-s{len(self.videos)}"
            self._add_video(vid, cid, days_ago, views)
        self.searches.setdefault((query, lang), []).append(vid)


class _Call:
    def __init__(self, result):
        self._result = result

    def execute(self):
        return self._result


class _Resource:
    def __init__(self, list_fn):
        self.list = list_fn


class FakeService:
    def __init__(self, data: FakeData):
        self.data = data

    def search(self):
        def _list(**p):
            ids = self.data.searches.get((p["q"], p["relevanceLanguage"]), [])
            items = [{"id": {"videoId": v}, "snippet": self.data.videos[v]["snippet"]}
                     for v in ids[:p["maxResults"]]]
            return _Call({"items": items})
        return _Resource(_list)

    def videos(self):
        def _list(**p):
            ids = p["id"].split(",")
            return _Call({"items": [self.data.videos[i] for i in ids
                                    if i in self.data.videos]})
        return _Resource(_list)

    def channels(self):
        def _list(**p):
            ids = p["id"].split(",")
            return _Call({"items": [self.data.channels[i] for i in ids
                                    if i in self.data.channels]})
        return _Resource(_list)

    def playlistItems(self):
        def _list(**p):
            vids = self.data.playlists.get(p["playlistId"], [])[:p["maxResults"]]
            return _Call({"items": [{"contentDetails": {"videoId": v}} for v in vids]})
        return _Resource(_list)


def build_fixture() -> FakeData:
    """Zwei Test-Nischen: 'winner' (junge Outlier-Kanäle, EN boomt, DE leer)
    und 'loser' (nur alte Mega-Kanäle -> K1). Dazu 'falling' (K2) und
    'deadde' (DE tot -> K5)."""
    d = FakeData()

    # --- WINNER (EN): 2 junge Kanäle mit 100k+-Outliern -------------------
    d.add_channel("young1", age_days=180, subs=40_000,
                  uploads=[(150 - i * 10, 20_000) for i in range(12)])
    d._add_video("young1-hit", "young1", 60, 500_000)   # Outlier 25x
    d.playlists["UUyoung1"].insert(0, "young1-hit")
    d.add_channel("young2", age_days=300, subs=25_000,
                  uploads=[(250 - i * 20, 15_000) for i in range(8)])
    d._add_video("young2-hit", "young2", 100, 150_000)  # Outlier 10x
    d.playlists["UUyoung2"].insert(0, "young2-hit")

    d.add_search_result("winner en", "en", "young1", vid="young1-hit")
    d.add_search_result("winner en", "en", "young1", 30, 25_000)
    d.add_search_result("winner en", "en", "young1", 90, 18_000)
    d.add_search_result("winner en", "en", "young2", vid="young2-hit")
    # 16 etablierte, aber nicht-Mega-Kanäle + 1 Mega-Kanal
    for i in range(16):
        cid = f"est{i}"
        d.add_channel(cid, age_days=1200 + i * 100, subs=60_000 + i * 50_000,
                      uploads=[(200 - j * 15, 25_000 + i * 1000) for j in range(6)])
        if i % 2 == 0:
            d.add_search_result("winner en", "en", cid, 20 + i * 18, 30_000 + i * 2000)
        else:
            d.add_search_result("winner en", "en", cid, 200 + i * 40, 15_000 + i * 700)
    d.add_channel("mega", age_days=3000, subs=2_000_000,
                  uploads=[(100 - j * 10, 900_000) for j in range(6)])
    d.add_search_result("winner en", "en", "mega", 300, 800_000)
    # WINNER (DE): fast leer -> Arbitrage-Lücke, kein K5 (< 10 Treffer)
    d.add_channel("de-small", age_days=800, subs=3_000,
                  uploads=[(400 - j * 30, 1_500) for j in range(5)])
    for days in (400, 500, 600):
        d.add_search_result("winner de", "de", "de-small", days, 2_000)

    # --- LOSER (EN): nur alte Mega-Kanäle -> K1 ----------------------------
    for i in range(8):
        cid = f"big{i}"
        d.add_channel(cid, age_days=2500 + i * 200, subs=1_500_000 + i * 100_000,
                      uploads=[(90 - j * 10, 400_000) for j in range(6)])
        d.add_search_result("loser en", "en", cid, 50 + i * 30, 500_000 + i * 10_000)
        d.add_search_result("loser en", "en", cid, 250 + i * 30, 450_000)
    d.add_search_result("loser de", "de", "de-small", 450, 1_000)

    # --- FALLING (EN): Trend klar fallend -> K2 ----------------------------
    d.add_channel("fyoung", age_days=360, subs=30_000,
                  uploads=[(300 - j * 20, 12_000) for j in range(6)])
    d._add_video("fyoung-hit", "fyoung", 200, 150_000)
    d.playlists["UUfyoung"].insert(0, "fyoung-hit")
    d.add_search_result("falling en", "en", "fyoung", vid="fyoung-hit")
    for i in range(14):
        cid = f"fest{i}"
        d.add_channel(cid, age_days=1500 + i * 50, subs=80_000,
                      uploads=[(400 - j * 20, 100_000) for j in range(5)])
        d.add_search_result("falling en", "en", cid, 200 + i * 24, 120_000)
    d.add_search_result("falling en", "en", "fest0", 30, 4_000)
    d.add_search_result("falling en", "en", "fest1", 90, 5_000)
    d.add_search_result("falling de", "de", "de-small", 420, 800)

    # --- DEADDE (DE): >= 10 Treffer, alles tot -> K5 -----------------------
    for i in range(4):
        cid = f"dead{i}"
        d.add_channel(cid, age_days=2000, subs=8_000,
                      uploads=[(500 - j * 40, 3_000) for j in range(5)])
        for k in range(3):
            d.add_search_result("deadde de", "de", cid, 400 + k * 60 + i * 10, 2_500)

    return d
