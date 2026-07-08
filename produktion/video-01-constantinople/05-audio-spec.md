# Audio-Spezifikation: Video 01

## 1. Voiceover

- **Stimmprofil:** männlich, tief-warm, ruhig, britisch-neutraler Doku-Ton
  (Referenzklasse: BBC-Historiendoku). KEINE Hype-Stimme — die Bilder hypen,
  die Stimme erdet. ElevenLabs-Kandidaten testen: "Daniel", "George" o. ä.,
  Stability hoch, Style niedrig.
- **Tempo:** 148-152 wpm Grundtempo. Diary-Inserts: -10 % Tempo, intimer.
  Act 3 Sturm: +5 %, härtere Konsonanten. Nach S77 ("the world ends"): 1,5 s Pause.
- **Beat-Pausen:** nach jeder Zahlen-Salve (z. B. "Eight thousand defenders.
  [Pause] Five point seven kilometers.") 0,6-0,8 s.
- **Diary-Stimme:** gleiche Stimme, aber näher am Mikro (ElevenLabs: separates
  Rendering mit mehr "Similarity", leiser Raumhall in der Mischung).

## 2. Aussprache-Führer (in TTS phonetisch erzwingen)

| Wort | Aussprache |
|---|---|
| Nicolò Barbaro | nee-ko-LO BAR-ba-ro |
| Giustiniani | joo-stee-nee-AH-nee |
| Theodosian | thee-o-DOH-shan |
| Mehmed | MEH-met |
| bashi-bazouks | BAH-shee-ba-ZOOKS |
| Kerkoporta | ker-ko-POR-ta |
| Palaiologos | pa-lay-OH-lo-gos |
| Mese | MEH-see |
| Hagia Sophia | HAH-ya so-FEE-a |

## 3. Sound-Design (der Layer, den die Konkurrenz nicht hat)

Drei Spuren unter JEDER Szene: (a) Raum-Ambience, (b) Detail-Foley, (c) Musik.
Quellen: freesound.org (CC0) + lizenzfreie Packs; Liste in Assembly-Skript.

Schlüssel-Momente (aus Shotlist):
- S43 Kanonenschuss: voller Impact, danach 2 s Tinnitus-Piep + gedämpfte Welt
  (der "Saving-Private-Ryan-Moment" — stärkster Audio-Beat des Videos)
- S56/77 Glocken-Fadeout in Totenstille vor dem Sturm — Stille ist der Jumpscare
- S85 Janitscharen: KEINE Musik, nur synchroner Marschtritt (Disziplin = Grusel)
- S95 Panorama nach dem Fall: nur Wind. 15 Sekunden kein einziger Musikton.
- Mehter-Trommeln als Spannungs-Thermometer: Act 1 fern -> Act 3 überall -> Act 4 weg

## 4. Musik-Bogen (lizenzfrei/KI, Stems getrennt)

| Abschnitt | Charakter | Instrumente |
|---|---|---|
| Act 1 | Staunen mit Riss | Streicher, orthodoxer Chor fern, tiefer Puls |
| Act 2 | Schlinge zieht sich | Drones, Cello-Ostinato, Mehter perkussiv |
| Act 3 Omen | sakrale Angst | Chor-Cluster, Glas-Harmonics, Stille-Löcher |
| Act 3 Sturm | Entfesselung | Taiko/Davul, Blech-Stöße, dann ABRISS bei S95 |
| Act 4 | Elegie -> Neuanfang | Duduk, Solo-Cello, zuletzt heller Streicher-Aufgang |

## 5. Mix-Regeln (Assembly)

- VO immer -14 LUFS Anker; Musik duckt -8 dB unter VO (Sidechain)
- Ambience nie ganz weg (Immersions-Grundrauschen 24/7)
- Shorts-Ableger: separater lauterer Mix (Mobile)
