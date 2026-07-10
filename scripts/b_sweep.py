"""B-Sweep: Hoch-RPM-Nischen-Suche mit hartem Geld-Beweis (K3+).

Pro Nische: EN-Top-50-Suche -> Longform-Filter (Shorts zählen NIE) ->
junge Kanäle (<24 Mo) mit LF-Video >= 100k -> 90d-LF-Run-Rate -> $/Monat.
Zusätzlich 2 Ceiling-Kanäle (beliebiges Alter) pro Nische.
"""
import datetime as dt
import json
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "/home/user/niche-finder")
import moneyproof as mp
from niche_finder import config
from niche_finder.cache import cached_call

YOUNG_MONTHS = 24
PROOF_USD = 20_000      # K3+: junger Kanal >= 20k $/Mo (Mittel-RPM) = PROOF
PROMISING_USD = 8_000   # >= 8k = PROMISING

NICHES = [
    {"id": "corporate-fraud-dokus", "name": "Corporate-Fraud-Dokus",
     "query": "biggest corporate frauds documentary", "rpm": (12, 20)},
    {"id": "startup-betrug-v2", "name": "Startup-Betrug & Tech-Skandale v2",
     "query": "tech startup scandal story", "rpm": (12, 20)},
    {"id": "krypto-skandale-v2", "name": "Krypto-Skandale v2",
     "query": "biggest crypto collapses explained", "rpm": (10, 18)},
    {"id": "steueroasen-v2", "name": "Steueroasen & Reichen-Steuertricks v2",
     "query": "how billionaires avoid taxes", "rpm": (15, 25)},
    {"id": "banken-kollaps", "name": "Banken-Kollaps & Finanzkrisen",
     "query": "why banks collapse explained", "rpm": (15, 25)},
    {"id": "business-model-erklaert", "name": "Business-Model-Erklärstücke",
     "query": "genius business model explained", "rpm": (12, 20)},
    {"id": "rise-fall-companies-v2", "name": "Rise & Fall von Firmen v2",
     "query": "the rise and fall of company", "rpm": (12, 20)},
    {"id": "ai-industry-analysen", "name": "AI-Industrie-Analysen",
     "query": "AI bubble explained", "rpm": (12, 20)},
    {"id": "chip-war", "name": "Chip-War & Halbleiter-Geopolitik",
     "query": "semiconductor war explained", "rpm": (12, 20)},
    {"id": "insurance-stories", "name": "Versicherungs-Horror-Stories",
     "query": "insurance company denied claim story", "rpm": (15, 25)},
    {"id": "legal-stories", "name": "Recht/Prozess-Stories",
     "query": "the lawsuit that destroyed a company", "rpm": (15, 25)},
    {"id": "housing-erklaert", "name": "Immobilien/Housing-Erklärstücke",
     "query": "why housing is so expensive", "rpm": (15, 25)},
    {"id": "economic-warfare", "name": "Wirtschaftskrieg & Sanktionen",
     "query": "economic warfare explained", "rpm": (12, 20)},
    {"id": "luxury-dark-side", "name": "Dark Side of Luxury",
     "query": "dark side of luxury brands", "rpm": (10, 15)},
    {"id": "scam-exposes", "name": "Scam/Guru-Exposés (James-Jani-Feld)",
     "query": "get rich quick scams exposed", "rpm": (12, 18)},
]


def search_top50_en(query):
    params = {"part": "snippet", "q": query, "type": "video", "maxResults": 50,
              "relevanceLanguage": "en", "regionCode": "US"}
    resp = cached_call("search", params, config.SEARCH_COST,
                       lambda: mp.service().search().list(**params).execute())
    return resp.get("items", [])


def sweep_niche(n):
    items = search_top50_en(n["query"])
    vid_ids = [i["id"]["videoId"] for i in items if i["id"].get("videoId")]
    vids = mp.videos_full(vid_ids)
    lf_vids = [v for v in vids.values()
               if mp.iso_dur_sec(v.get("contentDetails", {}).get("duration")) >= mp.LONGFORM_SEC]
    ch_ids = sorted({v["snippet"]["channelId"] for v in lf_vids})
    chans = mp.channels_info(ch_ids)
    now = dt.datetime.now(dt.timezone.utc)

    def age_months(ch):
        pub = dt.datetime.fromisoformat(ch["snippet"]["publishedAt"].replace("Z", "+00:00"))
        return (now - pub).days / 30.4

    best_lf = {}
    for v in lf_vids:
        cid = v["snippet"]["channelId"]
        views = int(v["statistics"].get("viewCount", 0))
        if views > best_lf.get(cid, (0, None))[0]:
            best_lf[cid] = (views, v["snippet"]["title"])

    young_ids = [cid for cid in ch_ids if cid in chans
                 and age_months(chans[cid]) < YOUNG_MONTHS
                 and best_lf.get(cid, (0,))[0] >= 100_000]
    young_ids.sort(key=lambda c: -best_lf[c][0])
    ceiling_ids = [cid for cid in ch_ids if cid in chans and cid not in young_ids]
    ceiling_ids.sort(key=lambda c: -best_lf.get(c, (0,))[0])

    young = [mp.measure_channel(cid, ch=chans[cid]) for cid in young_ids[:6]]
    ceiling = [mp.measure_channel(cid, ch=chans[cid]) for cid in ceiling_ids[:2]]
    for group in (young, ceiling):
        for m in group:
            m["bestes_video_in_suche"] = best_lf.get(m["channel_id"], (0, ""))[1]
    rpm_lo, rpm_hi = n["rpm"]
    rpm_mid = (rpm_lo + rpm_hi) / 2

    def usd_mid(m):
        return round((m.get("lf_monat") or 0) / 1000 * rpm_mid)

    young.sort(key=lambda m: -usd_mid(m))
    max_young = usd_mid(young[0]) if young else 0
    verdict = ("PROOF" if max_young >= PROOF_USD
               else "PROMISING" if max_young >= PROMISING_USD
               else "FAIL")
    return {
        "id": n["id"], "name": n["name"], "query": n["query"], "rpm": n["rpm"],
        "lf_results": len(lf_vids), "shorts_results": len(vids) - len(lf_vids),
        "young_channels": young, "ceiling_channels": ceiling,
        "max_young_usd_monat_mid_rpm": max_young, "verdict": verdict,
    }


def main():
    results = []
    for n in NICHES:
        try:
            r = sweep_niche(n)
        except Exception as e:
            if "quota" in str(e).lower():
                print(f"QUOTA-STOPP bei {n['id']}: {e}")
                break
            r = {"id": n["id"], "name": n["name"], "fehler": str(e)[:200]}
        results.append(r)
        rpm = n.get("rpm", (0, 0))
        print(f"\n=== {r['name']} [{r.get('verdict', 'FEHLER')}] "
              f"query={n['query']!r} maxYoung={r.get('max_young_usd_monat_mid_rpm', 0):,}$/Mo ===")
        for m in r.get("young_channels", []):
            print("  JUNG " + mp.fmt_row(m, *rpm))
        for m in r.get("ceiling_channels", []):
            print("  CEIL " + mp.fmt_row(m, *rpm))
        json.dump(results, open("b_sweep_results.json", "w"),
                  ensure_ascii=False, indent=1)
    q = json.load(open("/home/user/niche-finder/state/quota.json"))
    print("\nQuota heute:", q.get(dt.datetime.now(dt.timezone.utc).date().isoformat()) or q)


if __name__ == "__main__":
    main()
