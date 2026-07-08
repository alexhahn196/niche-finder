# Style-Bible: Video 01 (und Kanal-Standard)

Regel Nr. 1: **Ein Look, null Ausreißer.** Jeder Prompt = BASE + MOOD + SZENE + NEG.
Hollywood-Anspruch heißt: Konsistenz schlägt Einzelbild-Brillanz.

## 1. Prompt-Architektur (Bausteine)

**BASE (jede Einstellung):**
`cinematic still, photorealistic historical reconstruction, 1453 Constantinople,
Byzantine architecture, shot on 35mm anamorphic, volumetric light, ultra-detailed,
film grain, muted realistic color grade, no text, no watermark`

**MOOD-Tokens (Farbklima = Dramaturgie, Playbook §8):**
- `MOOD_GLORY` (Act 1/2 Stadt): golden hour light, warm amber haze, soft god rays
- `MOOD_TENSION` (Act 2 Belagerung): overcast steel-grey sky, cold desaturated
  palette, smoke on horizon
- `MOOD_OMEN` (Act 3 Omen): twilight, deep blue hour, eerie green-white glow,
  heavy atmosphere, fog
- `MOOD_STORM` (Act 3 Sturm): night, firelight against darkness, orange embers,
  smoke, harsh chiaroscuro
- `MOOD_AFTERMATH` (Act 4): pale dawn light, ash in air, washed-out cool palette
- `MOOD_MODERN` (Time-Slip/Intro): clean daylight, contemporary photo look

**NEG (Negativ-Prompt, immer):**
`minarets on Hagia Sophia, Blue Mosque, Ottoman 16th century architecture,
modern buildings, cars, cables, glass windows, coffee, tomatoes*, clocks,
cartoon, painting style, text, watermark, deformed hands, extra fingers`
(*Ausnahme: der eine geplante Fehler-Shot, siehe §6)

## 2. Charakter-Tokens (Konsistenz über Referenzbild!)

Vorgehen: Pro Figur EIN Referenz-Porträt generieren, freigeben, dann via
Image-Referenz/Character-Feature in jeder Szene wiederverwenden.

- `CHAR_BARBARO`: "Venetian man in his late 30s, olive skin, dark short hair,
  trimmed beard, red Venetian cap, dark blue doublet with white collar, worn
  leather physician's satchel, intelligent tired eyes"
- `CHAR_CONSTANTINE`: "Byzantine emperor, late 40s, grey-streaked beard, purple
  cloak with golden double-headed eagles, gilded lamellar armor, weary dignity"
- `CHAR_MEHMED`: "Ottoman sultan, 21 years old, aquiline nose, sparse young
  beard, red kaftan, large white turban with heron feather aigrette, falcon-
  intense gaze"
- `CHAR_GIUSTINIANI`: "Genoese condottiere, 40s, full plate armor, white
  surcoat with red cross, commanding posture"

## 3. Shot-Grammatik (aus dem Playbook abgeleitet)

- **Wide/Aerial** = Skala + Staunen (Stadt, Mauern, Flotten) - dominiert Act 1/2
- **Medium** = Menschen im Raum (Markt, Liturgie, Mauerreparatur)
- **Close** = emotionale Anker (Hände, Kettenglied, Ikone, Tagebuchfeder)
- Bewegung: 80 % Stills mit Ken-Burns (langsamer Push-in = Spannung, Pull-out =
  Skala, Lateral = Tour); 15-20 Video-Clips NUR für: Time-Slip, Kanonenschuss,
  Schiffe-über-Land, Elmsfeuer, Sturmwellen, Fahnen-Moment, Flucht
- Schnittrhythmus: Hook 4-5 s/Shot, Mittelteil 7-9 s, emotionale Beats 10-12 s

## 4. Der Time-Slip (Marken-Shot, ~1:30)

Modernes Foto der Hagia Sophia (mit Minaretten, MOOD_MODERN) -> Morph auf
identische Komposition 1453: Minarette lösen sich auf, Werbetafeln/Menschenmenge
weichen byzantinischen Prozessionsfahnen. Umsetzung: 2 Keyframes (image-to-image,
gleiche Kamera) + Video-Morph. Wiederverwendbar als 15-s-Short.

## 5. Diary-Inserts (4 Stück)

Eigenes visuelles Format: Nahaufnahme Manuskript/Feder im Kerzenlicht,
Datums-Karte ("FROM THE DIARY OF NICOLÒ BARBARO — APRIL 22, 1453"),
VO wechselt in leicht intimeren Ton. Selber Look bei allen 4 -> Ritual.

## 6. DAS EINE FALSCHE DETAIL (Video 01)

**Platzierung:** Act 2, Markt-Szene auf der Mese (S43). In einem Marktstand
liegt gut sichtbar (aber nicht zentral) ein **Korb mit Tomaten** - unmöglich
1453: Tomaten kommen erst nach 1492 aus der Neuen Welt nach Europa.
- Schwierigkeit: mittel (Historiker sofort, aufmerksame Laien nach Nachdenken)
- Auflösung in Video 02, mit 3-Sekunden-Zoom auf den Korb + Erklärkarte
- NIE: Fakten, Zahlen, Karten oder Pietäts-Details verfälschen

## 7. Musik- & Grading-Bogen (Referenz für Assembly)

| Act | Grading | Musik |
|---|---|---|
| 1 | warm/golden | Streicher + entfernter orthodoxer Chor, Staunen |
| 2 | Entsättigung wächst | tiefe Drones, ferne Mehter-Trommeln nähern sich |
| 3 | blau/Nacht/Feuer | Perkussion, Stille-Drops vor jedem Omen, Chor-Cluster |
| 4 | fahle Dämmerung | Duduk-Solo + Chor-Elegie, am Ende einzelnes Cello |
