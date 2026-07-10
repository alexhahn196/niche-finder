"""B-Sweep Runde 2: Fokus-Cluster Finanz/Econ-Erklärstücke (bewiesenes Muster)."""
import datetime as dt
import json
import sys

sys.path.insert(0, ".")
import b_sweep
import moneyproof as mp

NICHES2 = [
    {"id": "rise-fall-companies-v2", "name": "Rise & Fall von Firmen v2 (Rerun)",
     "query": "the rise and fall of company", "rpm": (12, 20)},
    {"id": "finanzkrisen-erklaert", "name": "Finanzkrisen erklärt (Crayon-Feld)",
     "query": "financial crisis explained", "rpm": (12, 20)},
    {"id": "warum-alles-teuer", "name": "Warum alles so teuer ist (Cost-of-Living)",
     "query": "why everything is so expensive", "rpm": (12, 20)},
    {"id": "kreditkarten-wahrheit", "name": "Kreditkarten/Kredit-System erklärt",
     "query": "the truth about credit cards", "rpm": (20, 35)},
    {"id": "versicherung-erklaert", "name": "Wie Versicherungen wirklich funktionieren",
     "query": "how insurance actually works", "rpm": (20, 35)},
    {"id": "boerse-erklaert", "name": "Börse/Investieren erklärt (Story-Format)",
     "query": "how the stock market actually works", "rpm": (15, 25)},
    {"id": "wealth-inequality", "name": "Vermögensungleichheit & Geldsystem",
     "query": "wealth inequality explained", "rpm": (12, 20)},
]

results = []
for n in NICHES2:
    try:
        r = b_sweep.sweep_niche(n)
    except Exception as e:
        if "quota" in str(e).lower():
            print(f"QUOTA-STOPP bei {n['id']}: {e}")
            break
        r = {"id": n["id"], "name": n["name"], "fehler": str(e)[:200]}
    results.append(r)
    rpm = n.get("rpm", (0, 0))
    print(f"\n=== {r['name']} [{r.get('verdict', 'FEHLER')}] "
          f"maxYoung={r.get('max_young_usd_monat_mid_rpm', 0):,}$/Mo ===")
    if r.get("fehler"):
        print("  FEHLER:", r["fehler"])
    for m in r.get("young_channels", []):
        print("  JUNG " + mp.fmt_row(m, *rpm))
    for m in r.get("ceiling_channels", []):
        print("  CEIL " + mp.fmt_row(m, *rpm))
    json.dump(results, open("b_sweep_r2_results.json", "w"),
              ensure_ascii=False, indent=1)
q = json.load(open("/home/user/niche-finder/state/quota.json"))
print("\nQuota heute:", q.get(dt.datetime.now(dt.timezone.utc).date().isoformat()))
