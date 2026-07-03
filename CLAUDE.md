# YouTube-Nischen-Finder — Projekt-Briefing (dauerhaft)

Dieses Dokument ist die permanente Arbeitsanweisung für dieses Projekt.
Jede Session liest es zuerst und arbeitet danach.

## ZIEL

**5 YouTube-Nischen mit Score ≥ 80/100 finden (EN→DE-Arbitrage-Fokus). Dann Stopp + Report.**

EN→DE-Arbitrage = Nischen, die im englischsprachigen YouTube nachweislich
funktionieren (junge Kanäle mit Outlier-Videos), aber im deutschsprachigen
Raum noch unbesetzt oder schwach besetzt sind.

## SETUP

1. `CLAUDE.md` (diese Datei) speichert das gesamte Briefing dauerhaft.
2. Python-Projekt: `venv` (lokal `.venv/`), `requirements.txt` mit
   `google-api-python-client`, `youtube-transcript-api`, `python-dotenv`.
3. `.env` enthält `YOUTUBE_API_KEY` (steht in `.gitignore`, niemals committen).
   Vorlage: `.env.example`.
4. `state/niches.json` ist der persistente Speicher aller geprüften Nischen:
   **nichts doppelt prüfen, jede API-Antwort cachen** (Cache: `state/api_cache/`).

## LOOP (pro Iteration)

1. **10 neue Sub-Nischen generieren** (Thema × Zielgruppe × Format).
   Muster der bisherigen Top-Scorer als Seeds verwenden
   (`python -m niche_finder top` zeigt sie an).
2. **Pro Kandidat echte Daten via YouTube Data API v3:**
   Top-50-Suche (EN und DE), Kanalalter, Abos, Median-Views, Upload-Frequenz.
   **Outlier-Score = Video-Views ÷ Median-Views des Kanals.**
3. **Kill-Kriterien** (jedes einzelne killt den Kandidaten):
   - **K1**: kein Kanal < 12 Monate alt mit einem Video ≥ 100k Views
   - **K2**: 12-Monats-Trend fallend
   - **K3**: kein Affiliate-Potenzial UND RPM-Kategorie < 8 $
   - **K4**: Nische braucht US-Kontext (nicht nach DE übertragbar)
   - **K5**: in DE nur tote Kanäle, keine lebenden Outlier
4. **Scorecard (0–100):**
   - Newcomer-Beweis: **25**
   - Monetarisierung: **25**
   - Trend: **15**
   - Sättigung (invers): **15**
   - Machbarkeit bei 10–15 h/Woche: **10**
   - DE-Übertragbarkeit: **10**
   - **BONUS +10** bei Synergie mit Projekt **EnergiePilot** (Solar /
     Energie-Autarkie DE).
5. **Ergebnisse in `state/niches.json` loggen** (macht die CLI automatisch).

## STOPP-KRITERIEN

- **5 Kandidaten ≥ 80** ODER
- **30 Iterationen** ODER
- **Tages-Quota unter 10 %** (eine Suche kostet 100 Units, Budget 10.000/Tag).
  Bei Quota-Stopp: Checkpoint schreiben (`state/checkpoint.json`),
  am nächsten Tag nahtlos fortsetzen.

## START-SEEDS (zuerst prüfen)

1. KI-Automatisierung für KMU
2. KI-Workflows pro Berufsgruppe
3. Scam-/Betrugs-Dokus
4. Solopreneur mit KI
5. Longevity-Protokolle
6. Geoökonomie-Erklärstücke
7. Second Brain / Produktivität
8. Energie-Autarkie DE

## OUTPUT

`report.md` mit den Top 5, Belegen (Kanal-Links, Outlier-Videos, Zahlen)
und je **10 Video-Blueprints** pro Nische.

## ARBEITSWEISE

Kleine Schritte, nach jedem Baustein committen,
erst mit 2 Nischen testen, dann der volle Loop.

---

## Architektur & Bedienung (für die nächste Session)

Aufgabenteilung Mensch/Agent ↔ Skript:

- **Der Agent (Claude) generiert Kandidaten** und beurteilt die
  qualitativen Felder (RPM-Kategorie, Affiliate-Potenzial, US-Kontext,
  Machbarkeit, EnergiePilot-Synergie) — als JSON-Datei.
- **Das Skript holt die harten Daten** (YouTube Data API v3), rechnet
  Metriken, prüft datengetriebene Kill-Kriterien (K1, K2, K5, teils K4/K3
  über die Agent-Felder), berechnet den Score und persistiert alles.

### CLI-Befehle

```bash
source .venv/bin/activate
python -m niche_finder seed                      # Start-Seeds als Kandidaten anlegen (einmalig)
python -m niche_finder add candidates.json        # neue Kandidaten aus JSON-Datei anlegen
python -m niche_finder evaluate [--limit N]       # offene Kandidaten mit echten API-Daten bewerten
python -m niche_finder status                     # Fortschritt, Quota, Stopp-Kriterien
python -m niche_finder top [--n 10]               # Top-Scorer (Seeds für die nächste Generation)
python -m niche_finder report                     # report.md schreiben
```

### Kandidaten-JSON-Format (für `add`)

```json
[
  {
    "id": "ki-automatisierung-kmu",
    "name": "KI-Automatisierung für KMU",
    "topic": "KI-Automatisierung",
    "audience": "KMU-Inhaber",
    "format": "Tutorial/Case-Study",
    "queries_en": ["AI automation small business", "automate business with AI"],
    "queries_de": ["KI Automatisierung Unternehmen", "Geschäftsprozesse mit KI automatisieren"],
    "rpm_category_usd": 15,
    "affiliate_potential": true,
    "needs_us_context": false,
    "feasibility_10_15h": 8,
    "de_transferability": 9,
    "energiepilot_synergy": false,
    "notes": "B2B-RPM hoch, Tool-Affiliates (Make, Zapier, n8n)"
  }
]
```

`feasibility_10_15h` und `de_transferability` sind Agent-Einschätzungen 0–10.

### Iterations-Protokoll pro Session

1. `python -m niche_finder status` — Stopp-Kriterien erreicht? Dann `report` und fertig.
2. `python -m niche_finder top` — Muster der Top-Scorer lesen.
3. 10 neue Sub-Nischen (Thema × Zielgruppe × Format) als JSON generieren,
   dabei Duplikate zu `state/niches.json` vermeiden (das Skript lehnt
   doppelte IDs/Namen ohnehin ab).
4. `add` → `evaluate` → Ergebnisse prüfen → committen
   (`state/` wird mitcommittet, damit der Fortschritt persistent ist).
5. Bei Quota-Stopp: Checkpoint ist automatisch geschrieben; Session beenden,
   morgen mit Schritt 1 fortsetzen.

### Quota-Buchhaltung

`state/quota.json` hält `{datum, verbrauchte_units}` pro Tag.
Kosten: search.list = 100 Units, videos.list = 1, channels.list = 1.
Das Skript stoppt selbstständig, sobald < 1.000 Units (10 %) übrig sind.
Gecachte Antworten kosten 0 Units — deshalb wird **jede** API-Antwort unter
`state/api_cache/` abgelegt und bei Wiederholung von dort gelesen.
