# Produktions-Checkliste: Video 02 (Ablauf mit QC-Gates, Muster V01)

Voraussetzung: Higgsfield **Ultra** aktiv + Kanalstimme aus V01-Bake-off.
Geschätzte Credits: **550-650 (Premium-Kern)** · Durchlaufzeit: ~1 Arbeitstag ·
Deine Zeit: ~2 h QC.

**AUFLÖSUNGS-REGELN (verbindlich, aus V01-Audit):**
- Stills mit Push-in/Pull-out: Seedream 4.5 quality=high (~6K Zoom-Reserve)
- NB Pro nur resolution=4k, nur STAT-Shots + Charakter-Referenzen
- Effizienz-Modell-Shots: vor Assembly Batch-Upscale auf 4K (~40-60 Credits)
- Signature-Clips (#13, #34, #45, #62/63, #92): Seedance 2.0 resolution=4k
  EXPLIZIT (Default 720p!); übrige Clips 1080p
- Sparmodus-Fallback: 1080p-Master -> 2K-Stills, Upscale-Batch entfällt

## Schritt 0 — Abhängigkeiten von V1 (VOR VO-Rendering!)
- [ ] **QA-Pipeline abgeschlossen?** Fakten-Audit + Kreativ-Review +
      Final-Rewrite auf ~2.400 Wörter (v1 liegt bewusst ~15 % drüber)
- [ ] **Stadtwahl V1 auszählen** -> [STADTWAHL-SIEGER]-Platzhalter ersetzen
      (Skript S78/S79 + End-Card-Variante + Beschreibung + Shot #105-107)
      · Governance: < 50 Stimmen -> wir entscheiden (Daten-Favorit Baghdad),
      Voter werden trotzdem gecredited
- [ ] **Fehler-Spiel V1**: ersten richtigen Tomaten-Kommentar identifizieren
      -> [PIN-NAME] in Skript S43 + Shot #55 einsetzen
- [ ] V1-Retention-Daten (falls schon vorhanden) gegen Hook prüfen —
      Playbook-Feedback-Schleife

## Schritt 1 — Referenz-Assets (zuerst! ~30 Credits)
- [ ] 3-4 Charakter-Porträts (CHAR_CELER, CHAR_PLINY_YOUNG, CHAR_PLINY_ELDER,
      optional CHAR_RECTINA) -> **QC-GATE 1: Gesichter-Freigabe**
- [ ] 1 Master-Panorama Bucht 79 (EIN-Kegel-Vesuv! wird Referenz für alle
      Weitwinkel + Thumbnail 1) + 1 Master Forum Pompeji + 1 Master
      Herculaneum-Seefront
- [ ] Style-Proof: 3 Testbilder (RIVIERA/ASHFALL/SURGE) -> Look-Freigabe
- [ ] **Konsistenz-Warnung:** JEDER Berg-Shot gegen Sperrliste prüfen —
      Bildmodelle kennen nur den heutigen Doppel-Vesuv und driften dahin

## Schritt 2 — Voiceover (parallel, ~0 Credits / ElevenLabs)
- [ ] Final-Skript (nach Rewrite) in 4 Akt-Blöcken + 5 Letter-Inserts
      rendern (Aussprache-Führer §2 anwenden; Letter-Inserts separat,
      intimer)
- [ ] **QC-GATE 2: 2-Min.-Probe hören** (nur wenn Stimme neu; sonst
      Stichprobe Letter-Insert-Ton)
- [ ] Finale Audiolänge messen -> Shotlist-Timings skalieren (Assembly)

## Schritt 3 — Stills-Batches (~85 Bilder, ~150-250 Credits)
- [ ] Batch je Akt (BASE+MOOD+NEG), 8 parallel; Vision-Check jedes Bild:
      Anachronismen (Sperrliste! v. a. Doppel-Vesuv/Lava), Hände/Gesichter,
      Look-Konsistenz
- [ ] Shot #31: ANANAS muss klar erkennbar sein (faires Spiel), Stand
      saisonneutral
- [ ] Pietäts-Check Act 3 (Style-Bible §5): keine Todes-Nahaufnahmen
- [ ] **QC-GATE 3: Kontaktbogen aller Stills** (30 Min.)

## Schritt 4 — Video-Clips (12 Stück, ~100-150 Credits)
- [ ] Priorität: Säulen-Kollaps/Surge (#62-64) > Time-Slip (#13) >
      Berg-Morph (#92) > Ausbruch (#34) > Quadriremen (#45) > Rest
- [ ] Image-to-Video von freigegebenen Stills, 5-10 s, max. 2 Versuche,
      Fallback Ken-Burns (V01-Regel)

## Schritt 5 — Assembly (ffmpeg, 0 Credits)
- [ ] Timeline aus Shotlist-JSON; Schwarzbild #65 mit exakt 3 s Stille
- [ ] Audio-Mix nach 05-audio-spec (Bimsregen-Teppich! Stille-Abriss #65)
- [ ] Render 4K -> **QC-GATE 4: ganzes Video schauen** (Fakten-Stichprobe:
      5 Szenen gegen Dossier, speziell Berg-Silhouette + keine Lava)

## Schritt 6 — Verpackung & Launch
- [ ] 3-4 Thumbnails generieren -> Test & Compare
- [ ] Metadaten aus 06 einsetzen (Platzhalter-Check! Altered-Content-Flag)
- [ ] Pinned Comment (Quellen + Spielregeln + V1-Vote-Dank)
- [ ] Premiere Sa 15:00 UTC; Shorts Tag +1/+3/+5 (Brot / Berg-Morph /
      Bootshäuser)
- [ ] `virality_predictor` auf das fertige Video (Hook/Retention) ->
      bei rotem Hook erste 30 s nachschneiden

## Nach dem Launch (Feedback-Schleife)
- [ ] 48h: Thumbnail-CTR -> Verlierer töten
- [ ] Tag 7: Retention-Kurve -> Hook-Analyse für Video 03
- [ ] Kommentare: Ananas-Rater zählen (Auflösung in V03), YES/NOT-YET-Quote
      als Audience-Signal, Top-Kommentar für V03-Shoutout markieren
- [ ] Nach V02+V03: Daten-Checkpoint V4 (Säule-A-Überperformance? ->
      Krakatoa-Swap, erste-10-videos.md)
