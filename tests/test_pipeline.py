"""End-to-End-Tests der Pipeline mit Fake-API (2 Test-Nischen, ohne API-Key)."""
import tempfile
import unittest
from pathlib import Path

from niche_finder import config, report, state
from niche_finder.evaluate import evaluate_candidate
from niche_finder.youtube_client import YouTubeClient

from tests.fake_api import FakeService, build_fixture


def candidate(cid, q_en, q_de, **over):
    cand = {
        "id": cid, "name": cid, "topic": "T", "audience": "A", "format": "F",
        "queries_en": [q_en], "queries_de": [q_de],
        "rpm_category_usd": 18, "affiliate_potential": True,
        "needs_us_context": False, "feasibility_10_15h": 8,
        "de_transferability": 9, "energiepilot_synergy": False,
    }
    cand.update(over)
    return cand


class PipelineTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self._orig = {k: getattr(config, k) for k in
                      ("STATE_DIR", "CACHE_DIR", "NICHES_FILE", "QUOTA_FILE",
                       "CHECKPOINT_FILE", "REPORT_FILE")}
        config.STATE_DIR = base / "state"
        config.CACHE_DIR = base / "state" / "api_cache"
        config.NICHES_FILE = base / "state" / "niches.json"
        config.QUOTA_FILE = base / "state" / "quota.json"
        config.CHECKPOINT_FILE = base / "state" / "checkpoint.json"
        config.REPORT_FILE = base / "report.md"
        self.yt = YouTubeClient(service=FakeService(build_fixture()))

    def tearDown(self):
        for k, v in self._orig.items():
            setattr(config, k, v)
        self.tmp.cleanup()

    # --- die zwei Test-Nischen (Briefing: "erst mit 2 Nischen testen") -----

    def test_winner_scores_at_least_80(self):
        cand = evaluate_candidate(self.yt, candidate("w", "winner en", "winner de"))
        self.assertEqual(cand["status"], "evaluated")
        self.assertEqual(cand["kill_reasons"], [])
        self.assertGreaterEqual(cand["score"], 80)
        en = cand["evidence"]["en"]
        self.assertEqual(len(en["young_100k_channels"]), 2)
        best = en["young_100k_channels"][0]
        self.assertEqual(best["views"], 500_000)
        self.assertAlmostEqual(best["outlier_score"], 25.0, delta=1.0)
        self.assertIn(en["trend"], ("rising", "rising_strong"))

    def test_loser_killed_by_k1(self):
        cand = evaluate_candidate(self.yt, candidate("l", "loser en", "loser de"))
        self.assertEqual(cand["status"], "killed")
        self.assertIn("K1", cand["kill_reasons"])
        self.assertEqual(cand["score"], 0)

    # --- übrige Kill-Kriterien ---------------------------------------------

    def test_falling_trend_killed_by_k2(self):
        cand = evaluate_candidate(self.yt, candidate("f", "falling en", "falling de"))
        self.assertIn("K2", cand["kill_reasons"])

    def test_no_affiliate_low_rpm_killed_by_k3_without_quota(self):
        cand = evaluate_candidate(self.yt, candidate(
            "k3", "winner en", "winner de",
            affiliate_potential=False, rpm_category_usd=5))
        self.assertIn("K3", cand["kill_reasons"])
        self.assertEqual(state.used_today(), 0)  # K3/K4-Kill kostet keine Quota

    def test_us_context_killed_by_k4(self):
        cand = evaluate_candidate(self.yt, candidate(
            "k4", "winner en", "winner de", needs_us_context=True))
        self.assertIn("K4", cand["kill_reasons"])

    def test_dead_german_market_killed_by_k5(self):
        cand = evaluate_candidate(self.yt, candidate("k5", "winner en", "deadde de"))
        self.assertIn("K5", cand["kill_reasons"])

    # --- Persistenz, Cache, Quota ------------------------------------------

    def test_duplicates_rejected(self):
        store = state.load_store()
        added, rejected = state.add_candidates(
            store, [candidate("a", "q", "q"), candidate("a", "q", "q")])
        self.assertEqual(added, ["a"])
        self.assertEqual(rejected, ["a"])
        _, rejected2 = state.add_candidates(store, [candidate("a", "q", "q")])
        self.assertEqual(rejected2, ["a"])

    def test_quota_charged_and_cache_makes_rerun_free(self):
        evaluate_candidate(self.yt, candidate("w", "winner en", "winner de"))
        used_first = state.used_today()
        self.assertGreaterEqual(used_first, 200)  # 2 Suchen à 100 + Listen
        evaluate_candidate(self.yt, candidate("w2", "winner en", "winner de"))
        self.assertEqual(state.used_today(), used_first)  # alles aus dem Cache

    def test_quota_stop_raises_before_reserve(self):
        state.charge(8_900)  # 1_100 übrig
        with self.assertRaises(state.QuotaExceeded):
            state.charge(config.SEARCH_COST * 2)  # würde Reserve reißen

    def test_iterations_counted_per_batch(self):
        store = state.load_store()
        state.add_candidates(store, [candidate("a", "q", "q")])
        state.add_candidates(store, [candidate("b", "q", "q")])
        self.assertEqual(store["iterations"], 2)

    # --- API-Robustheit -------------------------------------------------------

    def test_video_without_statistics_does_not_crash(self):
        data = build_fixture()
        # Premiere/Livestream: videos.list-Item ganz ohne "statistics"
        data.videos["premiere"] = {
            "id": "premiere",
            "snippet": {"channelId": "young1",
                        "publishedAt": data.videos["young1-hit"]["snippet"]["publishedAt"],
                        "title": "Premiere ohne Stats"},
        }
        data.searches[("winner en", "en")].append("premiere")
        yt = YouTubeClient(service=FakeService(data))
        cand = evaluate_candidate(yt, candidate("w", "winner en", "winner de"))
        self.assertEqual(cand["status"], "evaluated")
        self.assertGreaterEqual(cand["score"], 80)

    # --- Report --------------------------------------------------------------

    def test_report_fills_top5_with_non_winners(self):
        store = state.load_store()
        for cid, score in (("a", 85), ("b", 70)):
            store["niches"][cid] = {
                "id": cid, "name": f"Nische-{cid}", "status": "evaluated",
                "score": score, "evidence": {"en": {}, "de": {}},
            }
        text = report.generate(store)
        self.assertIn("Nische-a", text)
        self.assertIn("Nische-b", text)  # auch Nicht-Gewinner füllen die Top 5

    def test_report_contains_winner_and_evidence(self):
        store = state.load_store()
        cand = evaluate_candidate(self.yt, candidate("w", "winner en", "winner de"))
        cand["name"] = "Gewinner-Nische"
        store["niches"]["w"] = cand
        state.save_store(store)
        text = report.generate(store)
        self.assertIn("Gewinner-Nische", text)
        self.assertIn("youtube.com/watch", text)
        self.assertIn("Outlier", text)


if __name__ == "__main__":
    unittest.main()
