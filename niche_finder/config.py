"""Zentrale Konfiguration: Pfade, Quota-Budget, Stopp-Kriterien."""
import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = PROJECT_ROOT / "state"
CACHE_DIR = STATE_DIR / "api_cache"
NICHES_FILE = STATE_DIR / "niches.json"
QUOTA_FILE = STATE_DIR / "quota.json"
CHECKPOINT_FILE = STATE_DIR / "checkpoint.json"
REPORT_FILE = PROJECT_ROOT / "report.md"

# Stopp-Kriterien (siehe CLAUDE.md)
TARGET_SCORE = 80
TARGET_COUNT = 5
MAX_ITERATIONS = 30

# YouTube Data API v3 Quota
DAILY_QUOTA = 10_000
QUOTA_STOP_THRESHOLD = 1_000  # Stopp, sobald weniger als 10 % übrig
SEARCH_COST = 100             # search.list
LIST_COST = 1                 # videos.list / channels.list / playlistItems.list

# Analyse-Parameter
SEARCH_RESULTS = 50           # Top-50-Suche laut Briefing
DEEP_DIVE_CHANNELS = 15       # pro Sprache: so viele Kanäle im Detail (Median-Views etc.)
UPLOADS_PER_CHANNEL = 30      # letzte N Uploads für Median/Frequenz
YOUNG_CHANNEL_MONTHS = 12     # "Newcomer": Kanal jünger als 12 Monate
OUTLIER_VIEWS_K1 = 100_000    # K1: junger Kanal braucht ein Video mit >= 100k Views


def api_key() -> str:
    load_dotenv(PROJECT_ROOT / ".env")
    key = os.getenv("YOUTUBE_API_KEY")
    if not key:
        raise SystemExit(
            "YOUTUBE_API_KEY fehlt. `cp .env.example .env` und Key eintragen "
            "(Google Cloud Console -> YouTube Data API v3 -> API-Schlüssel)."
        )
    return key
