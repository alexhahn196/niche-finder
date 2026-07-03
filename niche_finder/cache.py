"""API-Response-Cache: jede Antwort wird gespeichert, Wiederholungen kosten 0 Units."""
import hashlib
import json

from . import config, state


def _cache_path(endpoint: str, params: dict):
    key = json.dumps({"endpoint": endpoint, "params": params}, sort_keys=True)
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:24]
    return config.CACHE_DIR / endpoint / f"{digest}.json"


def cached_call(endpoint: str, params: dict, cost: int, fetch):
    """Liefert die gecachte Antwort oder ruft `fetch()` auf (bucht dann `cost` Units)."""
    path = _cache_path(endpoint, params)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    state.charge(cost)  # wirft QuotaExceeded vor dem echten API-Call
    response = fetch()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(response, ensure_ascii=False), encoding="utf-8")
    return response
