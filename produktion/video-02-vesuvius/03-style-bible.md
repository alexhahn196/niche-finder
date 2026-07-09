# Style-Bible: Video 02 — Vesuv 79 n. Chr. (baut auf Kanal-Standard V01 auf)

Regel Nr. 1 unverändert: **Ein Look, null Ausreißer.** Jeder Prompt =
BASE + MOOD + SZENE + NEG. Kanal-Regeln aus V01 §3-§5 (Shot-Grammatik,
Time-Slip-Format, Insert-Ritual) gelten weiter — hier nur V02-Spezifika.

## 1. Prompt-Architektur

**BASE (jede Einstellung):**
`cinematic still, photorealistic historical reconstruction, 79 AD Roman
Campania, Pompeii and Herculaneum, Roman architecture with painted facades,
shot on 35mm anamorphic, volumetric light, ultra-detailed, film grain, muted
realistic color grade, no text, no watermark`

**MOOD-Tokens (Farbklima = Dramaturgie):**
- `MOOD_RIVIERA` (Act 1 Morgen): warm Mediterranean morning light, golden
  haze over blue bay, lush green mountain slopes
- `MOOD_UNEASE` (Act 2 Vorzeichen): hard noon light turning sallow, still
  air, long shadows, dogs alert
- `MOOD_ERUPTION` (Act 2 Ausbruch): towering dark eruption column, bruised
  purple-grey sky, day turning to dusk at noon
- `MOOD_ASHFALL` (Act 2/3 Bimsregen): grey pumice rain, torchlight in
  daytime darkness, dust haze, ghostly streets
- `MOOD_SURGE` (Act 3 Glutwolke): night, incandescent orange avalanche
  against black, harsh rim light, embers
- `MOOD_TOMB` (Act 3/4 danach): pale colorless dawn, monochrome grey ash
  moonscape, washed-out palette
- `MOOD_MODERN` (Time-Slip/Museum/Grabung): clean daylight, contemporary
  photo look

**NEG (Negativ-Prompt, immer):**
`modern twin-peaked Vesuvius silhouette, red lava rivers, flowing lava,
tomatoes, corn, potatoes, oranges, lemon market stalls, coffee, paper books,
horseshoes, stirrups, medieval or renaissance architecture, modern buildings,
cars, powerlines, tourists, cartoon, painting style, text, watermark,
deformed hands, extra fingers`
(Ausnahmen: der eine Fehler-Shot §6; MOOD_MODERN-Shots dürfen heutige
Silhouette/Touristen zeigen — NUR dort.)

**HÄRTESTE REGEL (Dossier):** Vesuv VOR dem Ausbruch = **EIN grüner Kegel
mit Weinbergen** — niemals die heutige Doppel-Silhouette (Somma + Kegel),
die entsteht ERST durch diesen Ausbruch (Shot #92 zeigt den Morph!).
Und: **KEINE Lavaströme** — Bims, Asche, Glutwolken. Das sind die zwei
häufigsten Genre-Fehler; unsere Präzision hier IST die Marke.

## 2. Charakter-Tokens (Konsistenz über Referenzbild)

- `CHAR_CELER`: "Roman slave baker, late 20s, sturdy build, short dark hair,
  simple grey work tunic, flour dust on forearms, bronze bread stamp in hand,
  calm focused expression"
- `CHAR_PLINY_YOUNG`: "Roman youth, 17, slim, white tunic with narrow purple
  stripe, wax tablet and stylus, alert intelligent eyes"
- `CHAR_PLINY_ELDER`: "Roman fleet commander and scholar, mid 50s, heavyset,
  commander's cloak over tunic, scroll in hand, calm authority"
- `CHAR_RECTINA` (optional, 1 Shot): "Roman noblewoman in stola on villa
  terrace at the foot of the mountain, urgent expression"

Vorgehen wie V01: pro Figur EIN Referenz-Porträt generieren, freigeben,
dann via Image-Referenz in jeder Szene wiederverwenden. KEINE Gesichter
in Todesszenen (Pietät + Policy): Surge-Opfer nur als Silhouetten,
Rückansichten, Totalen oder Cut-to-Black.

## 3. Signature-Sequenzen (V02)

1. **Time-Slip (#13, ~12 s):** Forum Pompeji heute (Ruinen, Absperrungen,
   Touristen, heutige Vesuv-Silhouette im Hintergrund!) -> Morph auf 79:
   Säulen wachsen, Dächer schließen sich, Farbe flutet, EIN-Kegel-Vesuv.
   Doppelt lehrreich: der Berg im Hintergrund wechselt die Form mit.
2. **Säulen-Kollaps -> Surge (#62-64):** der visuelle Höhepunkt. Physik
   korrekt: Säule sackt, Glutlawine rollt hangabwärts, KEIN Lava-Look.
3. **Berg-Morph (#92):** EIN-Kegel-Silhouette -> heutige Doppel-Silhouette
   in einem Shot. Marken-tauglich als 15-s-Short ("the mountain in every
   photo of Naples is a scar").
4. **Brot-Bookend (#5 / #97-99):** Museums-Vitrine in Act 1 = exakt dieselbe
   Kadrage wie das Finale. Der Kreis ist die Dramaturgie.

## 4. Letter-Inserts (5 Stück, Ritual analog V01-Diary)

Nahaufnahme Wachstafel/Schriftrolle im Lampenlicht, Karte:
"FROM THE LETTERS OF PLINY THE YOUNGER — TO THE HISTORIAN TACITUS".
VO intimer (Audio-Spec §1). Selber Look bei allen 5.

## 5. Pietäts-Regeln (Katastrophe mit echten Toten)

- Bootshäuser: Menschen wartend, bang, menschlich — NIE der Moment des
  Todes im Bild. Surge-Ankunft = Außen-Totale + harter Schwarzschnitt.
- Skelette/Abgüsse: dokumentarisch-respektvoll (MOOD_MODERN, Museums-/
  Grabungskontext), keine Sensationalisierung, keine Nahaufnahmen von
  Kinder-Casts.
- Keine Schmerzens-/Panik-Gesichter in Nahaufnahme.

## 6. DAS EINE FALSCHE DETAIL (Video 02)

**Platzierung: Shot #31** (Ambience-Fenster B, Marktstände Pompeji).
Auf einem Obststand liegt gut sichtbar (nicht zentral) **eine Ananas** —
unmöglich 79 n. Chr.: Neue-Welt-Frucht, erreicht Europa erst nach 1493.
- Schwierigkeit: mittel; fair findbar (deutlich im Bild, ~4 s Standzeit)
- Auflösung in Video 03 + Bonus-Fakt für die Auflösungskarte: das berühmte
  „Ananas"-Mosaik von Pompeji zeigt in Wahrheit einen **Pinienzapfen**
- NIE: Fakten, Zahlen, Karten oder Pietäts-Details verfälschen
- Saisonneutralität (Datums-Debatte!): Marktstände ohne forcierte Sommer-/
  Herbst-Marker — Feigen/Trauben/Oliven ok, KEINE Granatapfel-Pyramiden

## 7. Musik- & Grading-Bogen (Referenz für Assembly)

| Act | Grading | Musik |
|---|---|---|
| 1 | warm, mediterran | Lyra + leichte Streicher, Alltagswärme, Vogelklang |
| 2 | Licht kippt ins Fahle | Drones schwellen, Herzschlag-Puls unter Ausbruch |
| 3 | Nacht/Glut/Grau | Perkussion + Chor-Cluster; TOTALER Abriss bei #65 (Schwarz) |
| 4 | fahles Grau -> Museumslicht | Elegie Solo-Cello; beim Brot: einzelne warme Note + Ofenknistern |
