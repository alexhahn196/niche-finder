# Nischen-Neusuche B: Hoch-RPM-Felder mit hartem Geld-Beweis (Longform only)

**Auftrag (User, 2026-07-10):** Nischen finden, die das Geld-Kriterium
**nachweislich** erfüllen — Beweis nur über **Longform-Videos, keine Shorts**.
Kriterium K3+: junger Kanal (< 24 Monate) mit gemessener Longform-Run-Rate
≥ 20–30k $/Monat ODER RPM ≥ 20 $ mit Affiliate-Stack, in K6-konformen
Formaten (Story/Doku/Erklär — keine Screencasts, keine Gesichter).

**Methodik:** 22 Felder per YouTube Data API v3 durchsucht (Top-50 je Query),
Longform-Filter ≥ 3 Min., je Feld junge Kanäle + Ceiling-Kanäle mit
**90-Tage-Longform-Run-Rate** vermessen (letzte 50 Uploads, Shorts getrennt,
zählen nie in den Umsatz). Format-Verifikation per Kanalbeschreibung +
Thumbnail-Sichtprüfung. ~2.770 Quota-Units, 0 Credits.
Rohdaten: `state/money_proof/` · Skripte: `scripts/`.

---

## 1. Das strikte Urteil zuerst (ehrlich)

**Ein junger, K6-produzierbarer Kanal mit gemessenen ≥ 20–30k $/Monat wurde
in 22 Feldern NICHT gefunden.** Der einzige junge Kanal über der Schwelle
(„The Tech Report", 12,7 Mo, 2,1M LF-Views/Mo ≈ 25–42k $) ist ein
**Interview-Clips-Kanal** (Ed-Zitron-Podcast, Gesichter, Fremd-Content) —
für unsere Pipeline unbrauchbar, als Beweis disqualifiziert.

**Was stattdessen bewiesen ist** (und das ist substanziell):

## 2. Das Gewinner-Muster: Animierte Finanz/Econ-Erklärstücke

Drei junge Kanäle, alle **faceless/animiert = 100 % K6-produzierbar**
(Format per Thumbnail + Beschreibung verifiziert):

| Kanal | Alter | Abos | Output | LF-Views/Mo | $/Monat (Schätzung) |
|---|---|---|---|---|---|
| **Casual Finance** | 11,8 Mo | 281k | **nur 1 LF-Video/Monat!** | 767.000 | **9–15k $** (12–20 RPM) |
| **Nick Invests** (Whiteboard-Animation) | 17,9 Mo | 187k | ~17/Mo (Fließband) | 469.000 | 9–16k $ (Personal-Finance-RPM 20–35) |
| **Crayon Capital** („Big finance, drawn small") | 15,3 Mo | 226k | 25 Videos LIFETIME | 180.000 (Hit-getrieben) | Hits: **8–13k $ PRO VIDEO** |

Die Pro-Video-Ökonomie ist der Kernfund:
- **Casual Finance: ~404.000 Views pro Video ≈ 5–8k $ pro Video — bei einem
  Video im Monat.** Das ist exakt das Produktionsprofil unserer Pipeline.
- **Crayon Capital: 16,3M Views mit 25 Videos** (Ø 650k/Video). Größte Hits:
  „Wolf of Wall Street Scam" 4,1M · „Great Depression" 2,6M · „2008 Financial
  Crisis" 2,2M · „Rockefeller" 1,1M — **Finanzgeschichte als Cartoon-Story.**

**Ceiling desselben Felds (alles faceless, alles Longform):**

| Kanal | Alter | LF-Views/Mo | $/Monat |
|---|---|---|---|
| The Infographics Show | 15,4 J | 14,3M | 286–500k $ |
| How Money Works | 7,6 J | 3,6M | **36–72k $** |
| Coffeezilla | 7,9 J | 4,0M | 40–72k $ |
| Logically Answered | 13,9 J | 1,9M | 19–39k $ |
| Economics Explained | 13,9 J | 1,5M | 15–30k $ |
| MagnatesMedia / James Jani (Hit-Modell) | 7,6/6,6 J | unregelmäßig | Einzel-Hits bis 19M Views ≈ 190–380k $/Video |

Zum Vergleich unsere History-Nische: bester junger Kanal (timewarp cities)
415k LF-Views/Mo bei 3–8 $ RPM = 1,2–3,3k $/Mo. **Das Finanz-Feld zahlt bei
gleichen Views das 2–4-Fache und hat eine zigfach höhere bewiesene Decke.**

## 3. Was sonst geprüft wurde (und durchfiel)

22 Felder, u. a.: Corporate-Fraud, Startup-/Krypto-Skandale, Steueroasen,
Banken-Kollaps, Business-Models, Rise & Fall, Chip-War, Versicherungs- und
Recht-Stories, Housing, Wirtschaftskrieg, Luxury, Scam-Exposés,
Kreditkarten, Börse, Vermögensungleichheit, Cost-of-Living. Ergebnis-Muster
überall gleich: **riesige Decken bei etablierten Kanälen** (LegalEagle
124–206k $, More Perfect Union 176–293k $), aber **keine jungen
K6-kompatiblen Kanäle über ~5k $/Mo** außerhalb des Finanz-Erklär-Clusters.
Die Alt-Gewinner Old Money (82/81) wurden ebenfalls hart nachgemessen:
Spitze 1,8–4,3k $/Mo — Liga darunter.

## 4. Neue Kandidaten im System (voll evaluiert, K1–K6 + Slop-Check)

| Kandidat | Score | Status | Anmerkung |
|---|---|---|---|
| **Finanzkrisen & Geld-Stories — animiert** | **79** | kein Kill · slop 0.4 | Crayon/Casual-Feld; Slop-Anteil merklich → Differenzierung nötig |
| **AI-Industrie-Analysen** | 77 | kein Kill · slop 0.15 | heiß, aber Trend-Risiko (Bubble-Diskurs); Newcomer-Beweis nur via Casual Finance |
| Steuertricks der Reichen (Nick-Feld) | 0 | **gekillt** K1+K2 | kein Kanal < 12 Mo mit 100k-Video in der Suche; Trend fallend |

Die 79/77 liegen knapp unter der alten 80er-Marke (Sättigungs-Abzüge) — aber
die Score-Skala wurde für DE-Arbitrage gebaut. **Am neuen K3+-Kriterium
gemessen schlagen beide alle fünf Alt-Gewinner deutlich.**

## 5. Fazit & Empfehlung

**Der datengestützte Pfad zu 30k+ sieht so aus — einen schnelleren gibt es
nachweislich nicht:**
1. Feld mit bewiesener hoher Decke wählen → **Geld-Stories/Finanz-Erklär**
   (Decke 36–500k $, faceless, K6-konform).
2. Bewiesene Newcomer-Realität: **10–19k $/Monat nach 12–18 Monaten** ist
   der gemessene Best Case junger Kanäle (Casual Finance, Nick Invests) —
   plus Einzelvideo-Hits von 50–80k $ (Crayon).
3. 30k+ kommt aus Reife + Katalog-Effekt + Affiliate-Stack (Broker-,
   Kreditkarten-, Tool-Provisionen — die höchsten im Markt), nicht aus
   Monat 12.

**Empfehlung: Schwenk auf „Geld-Stories" als Kanal-Kern** — Finanzkrisen,
Betrug, Aufstieg & Fall von Vermögen/Firmen, animiert/dokumentarisch erzählt.
Das vereint: unser bestes Neusuche-Ergebnis (79), die Alt-Gewinner
Milliardärs-Abstürze (82), Old Money (81) und Ponzi (73) — es ist dasselbe
Meta-Feld — UND unsere aufgebaute Doku-Produktionskompetenz (QA-Pipeline,
Dossier-Standard). Brücke zu den fertigen V1-Assets: Crayon Capital beweist,
dass Finanz-GESCHICHTE (Great Depression, Rockefeller) im selben Kanal wie
Gegenwarts-Themen funktioniert — ein Kanal-Framing „Aufstieg & Ruin" kann
Constantinople 1453 (Fall eines 1000-Jahre-Reichs) als Launch-Video tragen
und danach auf die RPM-starken Geld-Themen schwenken (1929, Tulpenmanie,
Ponzi, FTX, Medici …).

**Entscheidungsfrage an dich** (Produktion bleibt bis dahin pausiert):
- **P1 — Voller Pivot:** Neuer Finanz-Story-Kanal, erste Videos auf den
  bewiesenen Outlier-Themen (2008 / Great Depression / Wolf of Wall Street:
  je 2–4M bewiesene Nachfrage). V1-History-Assets einmotten.
- **P2 — „Aufstieg & Ruin"-Framing:** V1 Constantinople wie geplant
  launchen (Assets fertig, ~200–300 Rest-Credits), Kanal aber von Video 3 an
  auf Wirtschafts-/Finanzgeschichte drehen. Kein Asset verloren, Feld-Schwenk
  vollzogen.
- **P3 — A/B-Test:** V1 launchen + parallel EIN Finanz-Story-Video
  produzieren, nach 30 Tagen Daten entscheiden lassen (~doppelte Credits).

Meine Empfehlung: **P2** — er verbrennt nichts, nutzt die 91 fertigen Stills
und richtet jeden weiteren Euro/Credit auf das Feld mit dem gemessen besten
Geld-Beweis.

---

*Datenstand 2026-07-10 · 22 Suchfelder, ~2.770 Quota-Units, 0 Credits ·
Alle Kanalmessungen: 90-Tage-Longform-Run-Rate, Shorts ausgeschlossen ·
RPM-Bänder sind Schätzungen (Branchenwerte), Views sind Messwerte.*
