# Masterplan: Marktführer „AI History Reconstruction" (EN)

Ziel: Bessere Qualität als jeder Top-Kanal der Nische -> Leader werden -> Umsatz maximieren.
Grundlage: report.md (5 validierte Nischen), en-deep-dive.md (Demand-Map), nische-playbook.md
(Gewinner-Formel, quantifiziert). Stand: 2026-07-07.

---

## 0. Die Sieg-These (warum wir gewinnen können)

Die Konkurrenz-Analyse zeigt: **Jeder Top-Kanal hat genau EINE Stärke.**

| Kanal | Stärke | Schwäche |
|---|---|---|
| Lem | Beste Visuals (Median 306k) | 0,08 Videos/Woche - praktisch inaktiv |
| Arthur Revives the Past | Katastrophen-Dramaturgie | keine Serien-Systematik, Host-abhängig |
| ancient editions | Serien-Prinzip "What X Looked Like" | Median nur 2k - Qualität schwankt stark |
| timewarp cities | Immersions-Format | Median 17k - inkonsistent |
| itsaihistory | Shorts-Discovery (8,7M) | Longform-Tiefe fehlt |

**Unser Stack schlägt das strukturell:** Claude-Recherche (Präzision) + Higgsfield-Visuals
(Lem-Niveau) + gemessene Hook-Formel + Serien-Systematik + 2 Videos/Woche konstant.
Kein Mensch schafft alle fünf gleichzeitig - eine Pipeline schon.

## 1. Die 8 Qualitäts-Hebel (konkret besser als die Top-Kanäle)

1. **Lem-Qualität bei 2/Woche:** fotorealistische Renders, einheitliches Farbklima-System
   (Glanz = goldenes Licht, Krise = entsättigt, Katastrophe = Nacht/Feuer). Konsistenz
   schlägt Einzel-Brillanz.
2. **Historische Präzision als Marke:** jede Szene quellenbasiert (ich recherchiere pro
   Video 15+ Quellen); Pinned Comment mit Quellenliste. Kein Top-Kanal macht das ->
   Trust-Differenzierung UND Anti-Slop-Schutz.
3. **Sound-Design-Layer:** Ambience unter jeder Szene (Marktlärm, Glocken, Regen, Schritte).
   Die Konkurrenz nutzt fast nur Musik. Kostet ~0, bringt massive Immersion.
4. **Die gemessene Hook-Formel** (Playbook §8): 6-Schritt-Aufbau in 95 Sek., Ø 5,7 Sek./Szene,
   Zahlen-Dichte, Katastrophen-Tease mit Todeszahl, Split-Screen-Methodenreveal.
5. **Serien-Architektur mit Cliffhangern:** 3 Format-Säulen (s. §3), jedes Video endet mit
   Teaser auf das nächste -> Session-Time, die der Algorithmus belohnt.
6. **Thumbnail-A/B-Tests** (YouTube "Test & Compare", 3 Varianten je Video) nach dem
   Gewinner-Code - kein Konkurrent testet erkennbar.
7. **Outlier-Radar:** wöchentlicher Scan (unsere Cache-Infrastruktur, ~200 Units) - wir
   produzieren in nachgewiesene Nachfrage statt zu raten. Alleinstellungsmerkmal.
8. **Retention-Feedback-Schleife:** nach jedem Video Retention-Kurve aus YouTube Studio
   analysieren (User liefert Screenshot) -> Hook/Pacing der nächsten Videos justieren.

**Anti-Slop-/Policy-Versicherung:** offene "AI Reconstruction"-Kennzeichnung (ist ohnehin
das CTR-Asset), sichtbare Eigenleistung (Quellen, Karten, konsistenter Erzähler), YouTube-
AI-Disclosure-Flag bei realistischen Szenen setzen, kein Massenausstoß (max. 4/Woche).

## 2. Phase 0 - Fundament (Woche 1)

- [ ] Higgsfield aktivieren (Trial 0 EUR -> Proof, dann Plus 49 EUR; Ultra ab 6 Videos/Monat)
- [ ] ElevenLabs-Konto (~22 EUR): 3 Erzählstimmen testen -> EINE festlegen (Stimme = Marke;
      tief, ruhig, BBC-Doku-Ton)
- [ ] Kanal-Identität: Name (Arbeitstitel-Shortlist unten), Logo/Banner via generate_image,
      Kanal-Trailer-Beschreibung, einheitliche Titel-Typo (Serifen, Gelb/Weiß)
- [ ] **Produktions-Pipeline als Code in diesem Repo:** Shotlist-JSON-Schema ->
      Batch-Bildgenerierung -> Ken-Burns/ffmpeg-Assembly -> Untertitel + Kapitel ->
      Render. Einmal bauen, für immer nutzen.
- [ ] Proof of Concept: 95-Sek.-Hook von Video 1 komplett rendern -> Qualitäts-Freigabe
- Kanalname-Shortlist: "Vanished Worlds", "The Reconstructed Past", "Echoes Rebuilt",
  "Chronovisor". Kriterien: merkbar, seriös, serienfähig, .com frei.

## 3. Phase 1 - Beweis (Woche 2-5: Videos 1-4)

Drei Format-Säulen von Anfang an (aus der Demand-Map):

| Säule | Format | Erste Videos |
|---|---|---|
| A "The Final Days" | Event-Katastrophen-Rekonstruktion | 1. Constantinople 1453 - Hour by Hour · 2. Pompeii's Final 24 Hours |
| B "What X Really Looked Like" | Stadt × Epoche | 3. London 1348 - The Plague Year |
| C "Could You Survive?" | Szenario/Immersion | 4. You Wouldn't Survive 24 Hours in Ancient Rome |

Pro Video: 12-20 Min. Longform + 2 Shorts-Ableger (bester Moment; Tag +1 und +3)
+ 3 Thumbnail-Varianten im A/B-Test + Kommentar-CTA bei Min. 3-4 ("Which city next?")
+ Kapitelmarken + Quellen-Pinned-Comment.
Upload-Rhythmus: fix 2/Woche (z. B. Di/Sa 15:00 UTC - US-Prime + EU-Abend).

**Gate 1 (Ende Woche 5):** >= 1 Video > 25k Views ODER Kanal > 50k Gesamt-Views.
Sonst: Formatsäulen-Rotation (Daten sagen, welche Säule zieht) - NICHT die Nische wechseln.

## 4. Phase 2 - Rhythmus & YPP (Monat 2-3: Videos 5-12)

- Reihenfolge 5-10 aus en-deep-dive.md, ab Video 8 nach eigener Kanal-Statistik justiert
- YPP-Antrag sofort bei 1.000 Abos + 4.000 Watch-Stunden (Shorts beschleunigen Abos)
- Wöchentlicher Outlier-Radar-Lauf -> Themen-Backlog aktuell halten
- Retention-Reviews: Hook-Drop > 40 % in den ersten 30 Sek. = Hook-Rebuild beim nächsten Video
- **Gate 2 (Ende Monat 4): 100.000+ Views/Monat, YPP aktiv.** Das ist der ehrliche
  Meilenstein, an dem das 10k-Ziel realistisch bleibt (Referenz: timewarp cities war
  bei Monat 8 auf ~460k/Monat).

## 5. Phase 3 - Monetarisierungs-Stack (Monat 4-6)

Vier Einnahme-Schichten übereinander:

1. **AdSense:** 12-20 Min. = Midrolls; History-EN-RPM ~5-9 USD
2. **Affiliate ab Video 1:** Audible/Buch-Links passend zum Thema (History-Publikum
   konvertiert stark auf Hörbücher) - kostet nichts, läuft passiv
3. **Sponsoring ab ~250k Views/Monat:** Audible, Brilliant, Incogni & Co. zahlen in
   History 15-25+ USD CPM; 2 gesponserte Videos/Monat = oft mehr als AdSense
4. **DE-Zwilling als Batch-Port:** gleiche Visuals, deutsches ElevenLabs-VO - jetzt
   sinnvoll, weil Templates stehen; +20-30 % Umsatz für ~15 % Aufwand

Ziel Monat 6: 300k-1M Views/Monat = 2.000-6.000 EUR/Monat (AdSense + Affiliate + erste Sponsor-Deals).

## 6. Phase 4 - Leader & Skalierung (Monat 6-12+)

- Output 3-4/Woche (Ultra-Plan, Batch-Produktion: 1 Recherche-Tag = 2 Skripte)
- **Kanal 2** aus dem validierten Portfolio: Old-Money-Dynastien / Milliardärs-Abstürze
  (Score 81/82, teilt sich das Finanz-Story-Publikum, gleiche Pipeline)
- Ab 3.000 EUR/Monat: 1 Freelancer für QC/Upload/Community (deine Zeit zurück auf Strategie)
- Sprach-Ports ES/FR prüfen (AI-VO macht Mehrsprachigkeit fast gratis)
- Leader-Definition: #1 der Nische nach Median-Views UND Format-Referenz, die kopiert wird
- Pfad: 10k EUR/Monat realistisch Monat 9-18 · 100k EUR/Monat = Netzwerk aus 5-10 Kanälen
  bzw. 1 Mega-Kanal + Satelliten, Horizont 24-36 Monate, mit Reinvestition

## 7. Budget & Werkzeuge

| Posten | Monat 1-3 | ab Skalierung |
|---|---|---|
| Higgsfield | 49 EUR (Plus) | 99-129 EUR (Ultra) |
| ElevenLabs | 22 EUR | 22-99 EUR |
| Musik-Lizenz | 0-15 EUR | 15 EUR |
| **Summe** | **~70-90 EUR/Monat** | ~150-250 EUR/Monat |

Materialkosten je Video: ~15-30 EUR. Klassische Produktion zum Vergleich: 300-1.500 EUR.

## 8. Wochen-Loop (dein 10-15-h-Budget)

| Wer | Aufgabe | Zeit |
|---|---|---|
| Claude | Outlier-Radar, 2 Skripte + Shotlists, Generierung, Assembly, Thumbnails, Metadaten | (Session-Zeit) |
| Du | 2× QC + Fakten-Stichprobe + Upload (je 1-1,5 h) | 2-3 h |
| Du | Retention-Screenshots liefern, Community-Antworten, Sponsor-Mails (ab Phase 3) | 2-4 h |
| Puffer | Hook-Rebuilds, Thumbnail-Iterationen | 2-3 h |

## 9. Risiko-Register

| Risiko | Gegenmaßnahme |
|---|---|
| YouTube-Policy gegen KI-Massencontent | Qualität + Quellen + Disclosure + max. 4/Woche (siehe §1) |
| Hit-Varianz (Plateau 2-3 Monate) | 3 Format-Säulen parallel; Gates entscheiden datenbasiert |
| Nische kühlt ab | Outlier-Radar erkennt es früh; Portfolio (5 validierte Nischen) als Ausweichpfad |
| Konkurrenz kopiert uns | Geschwindigkeit + Serien-Bindung + Qualitäts-Moat (Pipeline reproduziert das nicht jeder) |
| Higgsfield-/Modell-Ausfall | Pipeline modular: Bild-/VO-Anbieter austauschbar |

---

**Nächster konkreter Schritt:** Phase 0 starten - Higgsfield-Trial aktivieren, dann baue
ich Pipeline + Hook-Proof von "The Fall of Constantinople 1453" in einer Session.
