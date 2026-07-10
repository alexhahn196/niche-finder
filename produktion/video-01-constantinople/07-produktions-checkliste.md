# Produktions-Checkliste: Video 01 (Ablauf mit QC-Gates)

Voraussetzung: Higgsfield **Ultra** aktiv + Stimmen-Bake-off entschieden.
Geschätzte Credits: **570-680 (Premium-Kern, inkl. Retries)** + Thumbnails
~20-30 · Durchlaufzeit: ~1 Arbeitstag · Deine Zeit: ~2 h QC.
Schritt-Summen (Audit-Lauf 2): ~40 + ~280-330 + ~200-300 + ~20-30 ≈ 540-700.

**AUFLÖSUNGS-REGELN (Audit-Lauf 2, verbindlich):**
- **HERO-Stills (18 Stück, in der Shotlist markiert):** Seedream 4.5
  quality=high (~6K) — Default "basic" reicht NICHT für Zoom-Reserve
- **Alle übrigen PI/PO-Stills:** Effizienz-Modell + Batch-Upscale auf 4K;
  Ken-Burns-Zoom auf max. 5 % begrenzt (Assembly-Skript erzwingt das Limit);
  stärkere Bewegung nur LAT/STAT oder Umstufung zu HERO
- NB Pro nur mit resolution=4k und nur für STAT-Shots + Charakter-Referenzen (kein Zoom-Headroom)
- Effizienz-Modell-Shots (1-2K nativ): vor Assembly Batch-Upscale auf 4K (~40-60 Credits, in Schritt 3 enthalten)
- Signature-Clips: Seedance 2.0 mit resolution=4k EXPLIZIT setzen (Default ist 720p!); übrige Clips 1080p
- Sparmodus-Fallback (dokumentierte Alternative, NICHT Default): 1080p-Master -> 2K-Stills reichen für alle Zooms, Upscale-Batch entfällt

## Schritt 1 — Referenz-Assets (zuerst! ~40 Credits)
- [ ] 4 Charakter-Porträts generieren (CHAR_-Tokens) -> **QC-GATE 1: Du gibst
      Gesichter frei** (sie tauchen in ~20 Szenen auf)
- [ ] 1 Master-Stadtpanorama 1453 (wird Referenz für alle Weitwinkel + Thumbnail 1)
- [ ] Style-Proof: 3 Testbilder (GLORY/OMEN/STORM) -> Look-Freigabe

## Schritt 2 — Voiceover (parallel, ~0 Credits / ElevenLabs)
- [ ] Wortzahl-Check: Skript ist FINAL (~2.250 Wörter Sprechtext + 68 s Stille
      ≈ 16:10, s. Kopfzeile 02-skript.md) — vor VO-Render nur kurz gegenprüfen
- [ ] Skript in 4 Akt-Blöcken + 3 Diary-Zitat-Inserts rendern (Aussprache-Führer
      anwenden; Diary-Karten kommen als Text-Overlay im Assembly)
- [ ] Kontingent-Hinweis: ~2.250 Wörter ≈ 13k Zeichen/Video; ElevenLabs Creator
      (100k/Mon.) trägt 1 Video/Woche komfortabel, wird bei 8 Videos/Monat +
      Retries knapp -> dann Pro-Tier
- [ ] **QC-GATE 2: Du hörst 2 Min. Probe** (Stimme = Marke, einmal richtig entscheiden)
- [ ] Finale Audiolänge messen -> Shotlist-Timings feinjustieren (Skript ist auf
      ~16 Min. gebaut, ±40 s Toleranz)

## Schritt 3 — Stills-Batches (~98 Bilder: 94 I + 4 D, ~280-330 Credits inkl. Upscale-Batch)
- [ ] Batch je Akt generieren (BASE+MOOD+NEG aus Style-Bible), 8 parallel
- [ ] Ich prüfe jedes Bild per Vision auf: Anachronismen (Sperrliste!), Hand-/
      Gesichtsfehler, Look-Konsistenz -> Ausschuss neu prompten
- [ ] Shot #45 Fehler-Shot: Tomatenkorb MUSS klar erkennbar sein (das Spiel ist fair)
- [ ] **QC-GATE 3: Du siehst Kontaktbogen aller ~98** (30 Min.)

## Schritt 4 — Video-Clips (14 Stück, ~200-300 Credits inkl. Retries)
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
- [ ] 4 Thumbnail-Varianten generieren (~20-30 Credits, s. 06-metadata) ->
      Test & Compare einrichten
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
