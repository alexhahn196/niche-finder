# Produktions-Checkliste: Video 01 (Ablauf mit QC-Gates)

Voraussetzung: Higgsfield **Ultra** aktiv + Stimmen-Bake-off entschieden.
Geschätzte Credits: **550-650 (Premium-Kern)** · Durchlaufzeit: ~1 Arbeitstag · Deine Zeit: ~2 h QC.

**AUFLÖSUNGS-REGELN (Audit, verbindlich):**
- Stills mit Push-in/Pull-out: Seedream 4.5 quality=high (~6K) — Default "basic" reicht NICHT für Zoom-Reserve
- NB Pro nur mit resolution=4k und nur für STAT-Shots + Charakter-Referenzen (kein Zoom-Headroom)
- Effizienz-Modell-Shots (1-2K nativ): vor Assembly Batch-Upscale auf 4K (~40-60 Credits, eingepreist)
- Signature-Clips: Seedance 2.0 mit resolution=4k EXPLIZIT setzen (Default ist 720p!); übrige Clips 1080p
- Sparmodus-Fallback: 1080p-Master -> 2K-Stills reichen für alle Zooms, Upscale-Batch entfällt

## Schritt 1 — Referenz-Assets (zuerst! ~30 Credits)
- [ ] 4 Charakter-Porträts generieren (CHAR_-Tokens) -> **QC-GATE 1: Du gibst
      Gesichter frei** (sie tauchen in ~20 Szenen auf)
- [ ] 1 Master-Stadtpanorama 1453 (wird Referenz für alle Weitwinkel + Thumbnail 1)
- [ ] Style-Proof: 3 Testbilder (GLORY/OMEN/STORM) -> Look-Freigabe

## Schritt 2 — Voiceover (parallel, ~0 Credits / ElevenLabs)
- [ ] **ZUERST: Skript-Ausbau auf ~2.150 Wörter** (Per-Act-Ziele in 02-skript.md Kopfzeile)
      ODER Entscheidung für 12:30-Schnitt — vor jedem Credit-Einsatz für die Shotlist!
- [ ] Skript in 4 Akt-Blöcken + 5 Diary-Inserts rendern (Aussprache-Führer anwenden)
- [ ] Kontingent-Hinweis: ~2.150 Wörter ≈ 12k Zeichen/Video; ElevenLabs Creator (100k/Mon.)
      trägt 1 Video/Woche komfortabel, wird bei 8 Videos/Monat + Retries knapp -> dann Pro-Tier
- [ ] **QC-GATE 2: Du hörst 2 Min. Probe** (Stimme = Marke, einmal richtig entscheiden)
- [ ] Finale Audiolänge messen -> Shotlist-Timings feinjustieren (Skript ist auf
      ~16 Min. gebaut, ±40 s Toleranz)

## Schritt 3 — Stills-Batches (88 Bilder, ~150-250 Credits)
- [ ] Batch je Akt generieren (BASE+MOOD+NEG aus Style-Bible), 8 parallel
- [ ] Ich prüfe jedes Bild per Vision auf: Anachronismen (Sperrliste!), Hand-/
      Gesichtsfehler, Look-Konsistenz -> Ausschuss neu prompten
- [ ] Shot #45 Fehler-Shot: Tomatenkorb MUSS klar erkennbar sein (das Spiel ist fair)
- [ ] **QC-GATE 3: Du siehst Kontaktbogen aller 88** (30 Min.)

## Schritt 4 — Video-Clips (13 Stück, ~100-150 Credits)
- [ ] Priorität: Time-Slip (#16) > Kanonenschuss (#43) > Schiffe-über-Land (#57) >
      Mondfinsternis/Elmsfeuer (#66/#68) > Rest (14 Clips gesamt)
- [ ] Image-to-Video von freigegebenen Stills (Konsistenz!), 5-10 s, je 2 Versuche max.
- [ ] Fallback-Regel: Clip nach 2 Fehlversuchen -> Ken-Burns-Still statt Credit-Grab

## Schritt 5 — Assembly (ffmpeg, 0 Credits)
- [ ] Assembly-Skript baut Timeline aus Shotlist-JSON: Ken-Burns-Pfade, Crossfades,
      Diary-Rahmen, Karten-Grafiken (S9/S64/S108), Untertitel (EN), Kapitelmarken
- [ ] Audio-Mix nach 05-audio-spec (VO -14 LUFS, Ducking, Ambience-Layer)
- [ ] Render 4K -> **QC-GATE 4: Du schaust das ganze Video** (Fakten-Stichprobe:
      5 Szenen gegen Dossier prüfen)

## Schritt 6 — Verpackung & Launch
- [ ] 3 Thumbnails generieren -> Test & Compare einrichten
- [ ] Metadaten aus 06 einsetzen, Altered-Content-Flag setzen
- [ ] Pinned Comment vorbereiten (Quellen + Spielregeln)
- [ ] Premiere Sa 15:00 UTC planen; Shorts für Tag +1/+3 schneiden (aus S16/S55-58)
- [ ] Virality-Check: fertiges Video durch Higgsfield `virality_predictor` (Hook-
      Stärke/Retention-Risiko) -> bei rotem Hook: erste 30 s nachschneiden

## Nach dem Launch (Feedback-Schleife, Masterplan §4)
- [ ] 48h: CTR der Thumbnail-Varianten -> Verlierer töten
- [ ] Tag 7: Retention-Screenshot an mich -> Hook-Analyse für Video 02
- [ ] Kommentare: Fehler-Rater zählen, Stadtwahl auszählen, Top-Kommentar für
      Video-02-Shoutout markieren
