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
   - **K6 (hart, Produktions-Constraint)**: Nische muss zu **100 %** mit
     dieser Pipeline produzierbar sein: Recherche/Skript (Claude) →
     KI-Voiceover → KI-Bilder/Clips (Higgsfield) → Auto-Assembly.
     Erfordert die Nische Screenrecording, Kamera, Gameplay-Capture oder
     ein Gesicht → **Kill**. (Agent-Feld `pipeline_producible`.)
4. **Scorecard (0–100):**
   - Newcomer-Beweis: **25**
   - Monetarisierung: **25**
   - Trend: **15**
   - Sättigung (invers): **15**
   - Machbarkeit: **10** — definiert als **Produzierbarkeit in 10–15 h/Woche
     MIT der KI-Pipeline** (nicht allgemeiner Aufwand)
   - DE-Übertragbarkeit: **10**
   - **BONUS +10** bei Synergie mit Projekt **EnergiePilot** (Solar /
     Energie-Autarkie DE).
   - **SLOP-CHECK (Pflicht für jeden Kandidaten)**: Anteil erkennbar
     massenproduzierter KI-Videos unter den Top-Newcomern sichten und als
     `slop_share` (0–1) loggen. **> 50 % = „Policy-Minenfeld" = −15 auf
     Machbarkeit.** Ohne gesetzten `slop_share` bleibt der Kandidat im
     Status `needs_slop_check` und zählt nie als Gewinner.
5. **Ergebnisse in `state/niches.json` loggen** (macht die CLI automatisch).

**Explorations-Constraint:** Neue Kandidaten nur noch in K6-kompatiblen
Feldern generieren: **Story, Doku, Erklär, Listen, Szenarien** — keine
Tutorials/Screencasts, keine Praxis-Tests, keine Vlogs/Talking-Heads.

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
python -m niche_finder rescore                    # Kills/Scores aus gespeicherter Evidence neu berechnen (0 Units)
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
    "pipeline_producible": true,
    "feasibility_10_15h": 8,
    "de_transferability": 9,
    "energiepilot_synergy": false,
    "slop_share": null,
    "notes": "B2B-RPM hoch, Tool-Affiliates (Make, Zapier, n8n)"
  }
]
```

`feasibility_10_15h` (= Produzierbarkeit mit der KI-Pipeline) und
`de_transferability` sind Agent-Einschätzungen 0–10.
`pipeline_producible` (Pflicht, bool) steuert K6.
`slop_share` (0–1) wird **nach** `evaluate` anhand der Top-Newcomer-Evidence
gesetzt (`update` + `rescore`); bis dahin Status `needs_slop_check`.

### Iterations-Protokoll pro Session

1. `python -m niche_finder status` — Stopp-Kriterien erreicht? Dann `report` und fertig.
2. `python -m niche_finder top` — Muster der Top-Scorer lesen.
3. 10 neue Sub-Nischen (Thema × Zielgruppe × Format) als JSON generieren,
   dabei Duplikate zu `state/niches.json` vermeiden (das Skript lehnt
   doppelte IDs/Namen ohnehin ab).
4. `add` → `evaluate` → **Slop-Check** für jeden nicht gekillten Kandidaten
   (Top-Newcomer-Titel/Kanäle in der Evidence sichten, `slop_share` per
   `update` setzen, dann `rescore`) → Ergebnisse prüfen → committen
   (`state/` wird mitcommittet, damit der Fortschritt persistent ist).
5. Bei Quota-Stopp: Checkpoint ist automatisch geschrieben; Session beenden,
   morgen mit Schritt 1 fortsetzen.

### QA-PIPELINE PRO VIDEO (PFLICHT — kein Upload ohne alle 6 Schritte)

Etabliert nach Video 1 (Fakten-Audit fand 32 echte Fehler, Kreativ-Review
lieferte 22 Verbesserungen). Für JEDES Video in dieser Reihenfolge:

1. **Dossier + Skript v1 schreiben** (`produktion/video-XX-<name>/`, 7-Datei-
   Struktur wie Video 01). Eiserne Regeln dabei:
   - **Zitat-Regel:** KEIN wörtliches Zitat ohne notierte Fundstelle im Dossier
     (Standard-Übersetzung/Edition angeben). Paraphrasen niemals als Zitat framen.
   - **Superlativ-Regel:** jede „nie/erste/größte"-Behauptung präzise scopen und
     auf die vorhersehbarste Besserwisser-Korrektur abklopfen (Beispiel 1204).
   - **Legenden-Regel:** dünne Quellenlage im Skript attribuieren („if Doukas is
     to be believed", „tradition records") statt als Fakt zu erzählen.
   - **Overclaim-Regel:** Titel/Thumbnail versprechen nur, was das Video liefert.
2. **Fakten-Audit:** `Workflow({name:"fakten-audit", args:{videoDir:"...", epoche:"..."}})`
   — Historik + Produktions-Mathe, jeder Fund adversarial verifiziert (WebSearch).
3. **Alle bestätigten Funde einarbeiten** (Befunde als `audit-befunde.json` in
   den Videoordner committen).
4. **Kreativ-Review:** `Workflow({name:"kreativ-review", args:{videoDir:"...", zielWorte:2150}})`
   — 5 Linsen (Hook/Retention/VO-Sprache/Engagement/CTR) + Synthese-Richter, der
   Geschmacks-Rauschen und Fakten-Verstöße verwirft.
5. **Final-Rewrite in einem Rutsch** (Regieanweisungen + Wortzahl-Ziel); neue
   Fakten aus dem Review IMMER verifizieren und als Dossier-Nachtrag festhalten;
   Wortzahl-Check per Skript (~150 wpm + Stille-Budget = Ziel-Länge).
6. **QC-Gates mit dem User** (Checkliste des Videoordners) + `virality_predictor`
   auf das fertige Video vor dem Upload.

Erkenntnisse fließen zurück: Nach jedem Launch Retention-Daten gegen Playbook
prüfen (Gewinner-Code-Review alle 3 Videos, nische-playbook.md fortschreiben).

### Quota-Buchhaltung

`state/quota.json` hält `{datum, verbrauchte_units}` pro Tag
(**Tagesgrenze = Mitternacht Pacific Time**, wie der echte YouTube-Reset).
Kosten: search.list = 100 Units, videos.list = 1, channels.list = 1.
Das Skript stoppt selbstständig, sobald < 1.000 Units (10 %) übrig sind.
Gecachte Antworten kosten 0 Units — deshalb wird **jede** API-Antwort unter
`state/api_cache/` abgelegt und bei Wiederholung von dort gelesen.
**`state/api_cache/` wird mitcommittet**: Sessions laufen in frischen
Containern; ohne committeten Cache würde jede Session die volle Quota
erneut verbrauchen.

### Design-Entscheidungen & Grenzen (bewusst so gebaut)

- **Pro Sprache wird nur `queries_en[0]` bzw. `queries_de[0]` gesucht**
  (Quota: 1 Suche = 100 Units). Weitere Queries in der Liste sind Reserve
  für manuelle Zweitläufe.
- **K3/K4 werden vor jedem API-Call geprüft** (nur Agent-Felder nötig) —
  tote Kandidaten kosten 0 Units.
- **K2 ist eine Näherung**: Vergleich der Top-50-Ergebnisse 0–6 Monate vs.
  6–18 Monate (Publikationsrate UND Median-Views müssen klar fallen).
  Konservativ, um Fehl-Kills zu vermeiden.
- **K5 greift erst ab ≥ 10 DE-Treffern**: ein fast leerer DE-Markt ist
  keine tote Nische, sondern die Arbitrage-Chance.
- **`kill_overrides`** (optionales Kandidaten-Feld, z. B. `["K5"]`):
  übersteuert einzelne Kill-Kriterien bewusst — Begründung gehört in `notes`.
- **`evaluate --retry-errors`** setzt Kandidaten mit Status `error`
  (transiente API-Fehler) zurück auf `pending`.
- **Das 30-Iterationen-Limit stoppt nur `add`** (neue Kandidaten);
  bereits angelegte Kandidaten dürfen weiterhin bewertet werden.
- **Score-Deckel bei 100**: der EnergiePilot-Bonus steht separat im
  Breakdown (`energiepilot_bonus_10`).
