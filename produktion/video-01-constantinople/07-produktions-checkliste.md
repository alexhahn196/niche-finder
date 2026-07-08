# Produktions-Checkliste: Video 01 (Ablauf mit QC-Gates)

Voraussetzung: Higgsfield-Zugang aktiv (Trial/Plus) + ElevenLabs-Stimme gewählt.
Geschätzte Credits: 300-450 · Durchlaufzeit: ~1 Arbeitstag · Deine Zeit: ~2 h QC.

## Schritt 1 — Referenz-Assets (zuerst! ~30 Credits)
- [ ] 4 Charakter-Porträts generieren (CHAR_-Tokens) -> **QC-GATE 1: Du gibst
      Gesichter frei** (sie tauchen in ~20 Szenen auf)
- [ ] 1 Master-Stadtpanorama 1453 (wird Referenz für alle Weitwinkel + Thumbnail 1)
- [ ] Style-Proof: 3 Testbilder (GLORY/OMEN/STORM) -> Look-Freigabe

## Schritt 2 — Voiceover (parallel, ~0 Credits / ElevenLabs)
- [ ] Skript in 4 Akt-Blöcken + 4 Diary-Inserts rendern (Aussprache-Führer anwenden)
- [ ] **QC-GATE 2: Du hörst 2 Min. Probe** (Stimme = Marke, einmal richtig entscheiden)
- [ ] Finale Audiolänge messen -> Shotlist-Timings feinjustieren (Skript ist auf
      ~16 Min. gebaut, ±40 s Toleranz)

## Schritt 3 — Stills-Batches (88 Bilder, ~150-250 Credits)
- [ ] Batch je Akt generieren (BASE+MOOD+NEG aus Style-Bible), 8 parallel
- [ ] Ich prüfe jedes Bild per Vision auf: Anachronismen (Sperrliste!), Hand-/
      Gesichtsfehler, Look-Konsistenz -> Ausschuss neu prompten
- [ ] S45 Fehler-Shot: Tomatenkorb MUSS klar erkennbar sein (das Spiel ist fair)
- [ ] **QC-GATE 3: Du siehst Kontaktbogen aller 88** (30 Min.)

## Schritt 4 — Video-Clips (13 Stück, ~100-150 Credits)
- [ ] Priorität: Time-Slip (S16) > Kanonenschuss (S43) > Schiffe-über-Land (S57) >
      Mondfinsternis/Elmsfeuer (S66/68) > Rest
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
