export const meta = {
  name: 'kreativ-review',
  description: 'Pflicht-Kreativ-Review eines Video-Skripts (Hook, Retention, VO-Sprache, Engagement, CTR) mit Synthese-Richter',
  whenToUse: 'NACH dem Fakten-Audit + Einarbeitung der Fixes, VOR dem finalen Rewrite. Aufruf: Workflow({name:"kreativ-review", args:{videoDir:"produktion/video-XX-...", zielWorte: 2150}})',
  phases: [
    { title: 'Review', detail: '5 Kreativ-Linsen parallel' },
    { title: 'Synthese', detail: 'Richter filtert gegen Playbook-Daten' },
  ],
}

const FINDINGS_SCHEMA = {
  type: 'object',
  properties: {
    findings: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          beat: { type: 'string' },
          problem: { type: 'string' },
          vorschlag: { type: 'string' },
          severity: { type: 'string', enum: ['muss', 'stark', 'nice'] },
        },
        required: ['beat', 'problem', 'vorschlag', 'severity'],
      },
    },
  },
  required: ['findings'],
}

const SYNTH_SCHEMA = {
  type: 'object',
  properties: {
    regieanweisungen: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          prio: { type: 'integer' },
          beat: { type: 'string' },
          anweisung: { type: 'string' },
          begruendung_daten: { type: 'string' },
        },
        required: ['prio', 'beat', 'anweisung', 'begruendung_daten'],
      },
    },
    verworfen: { type: 'array', items: { type: 'string' } },
    act_schreibnotizen: {
      type: 'object',
      properties: {
        act1: { type: 'string' }, act2: { type: 'string' },
        act3: { type: 'string' }, act4: { type: 'string' },
      },
      required: ['act1', 'act2', 'act3', 'act4'],
    },
  },
  required: ['regieanweisungen', 'verworfen', 'act_schreibnotizen'],
}

const dir = (args && args.videoDir) || 'produktion/video-01-constantinople'
const zielWorte = (args && args.zielWorte) || 2150

const CONTEXT = `Repo: /home/user/niche-finder. Zu pruefen: ${dir}/02-skript.md (Ziel ~${zielWorte} Woerter).
PFLICHT-KONTEXT vorher lesen: nische-playbook.md (§8 Hook-Formel, §9 drei Hook-Archetypen,
§10 Gewinner-Sprache, §11 Thumbnail-Code v2), masterplan.md §1b (Witness Protocol),
${dir}/01-recherche-dossier.md (FAKTEN SIND BINDEND - kreative Vorschlaege duerfen sie nie
verletzen; neue Fakten-Ideen nur mit "vor Rendering verifizieren + Dossier-Nachtrag"-Flag),
${dir}/03-style-bible.md + 06-metadata-thumbnails.md.
Massstab: die analysierten Nischen-Gewinner in ihrer Disziplin schlagen. Kritik NUR mit
konkretem, ausformuliertem Vorschlag (EN); Geschmack ohne Retention-/CTR-Bezug weglassen.
Witness-Protocol-Slots pruefen: Opening-Zeile, Cold Open, Tease mit Zahlen, Trikolon,
Time-Slip ~1:40, Fehler-Spiel (999/Objekt/Pin), frueher Null-Aufwand-CTA ~2:00, Zeuge
emotional + Ueberlebens-Loop, Mid-Video-Frage (ab Video 2: Fehler-Aufloesung des
Vorgaengers), Stadtwahl One-Letter mit Macht-Ansage, konditionale Abo-Formel, End-Card
Mensch+Termin.`

const LENSES = [
  { key: 'hook-doktor', prompt: `${CONTEXT}

Du bist Hook-Spezialist. Seziere die ersten ~100 Sekunden Beat fuer Beat gegen Playbook §8/§9
(passenden Archetyp waehlen: Glory-first / Banality-first / Myth-Busting+Avatar). Wortbudget
bis Trikolon pruefen (<=245 W.), Jahr bis Sek. ~12, Tease mit Todeszahl/Stakes, Time-Slip-Slot.
Sekundengenaue Verbesserungen mit ausformulierten Alternativ-Zeilen.` },
  { key: 'retention-dramaturg', prompt: `${CONTEXT}

Du bist Retention-Dramaturg. Markiere jede Absprungstelle: Spannungs-Luecken >30 s, Curiosity
Loops (wo geoeffnet/geschlossen?), Re-Hooks alle 2-3 Min., Act-Uebergaenge, Stille-Bloecke
(max 25-35 s am Stueck). Top-5-Drop-off-Risiken mit Fix.` },
  { key: 'vo-sprachqualitaet', prompt: `${CONTEXT}

Du bist Skript-Doktor fuer gesprochene Doku-Narration. Satzrhythmus, Zungenbrecher,
Zahlen-Dosierung + Koerper-Anker, Sensorik-Zeilen (Geruch/Klang), Relatability-Zeilen,
eine zitierfaehige Signature-Line. Umformulierungen fuer die schwaechsten 8-10 Zeilen.` },
  { key: 'engagement-mechanik', prompt: `${CONTEXT}

Du bist Engagement-Stratege. Pruefe ALLE Witness-Protocol-Slots (Liste im Kontext) auf
Praesenz, Timing und Wortlaut gegen die Gewinner-Beweise. Konkrete Wortlaute (EN) fuer
jede Verbesserung.` },
  { key: 'titel-thumbnail-ctr', prompt: `${CONTEXT}

Du bist CTR-Spezialist. Pruefe 06-metadata-thumbnails.md: Titel-Formel (Ort vorn, Jahr,
AI-Label sichtbar <=70 Zeichen, KEIN Overclaim - Titel verspricht nur, was das Skript
liefert!), Thumbnail-Konzepte gegen §11 (Selektiv-Farb-Pop als Witness-Signatur dabei?
Superlativ-Subline? textlose Variante?), Beschreibungs-Snippet (erste 2 Zeilen), Kapitel.` },
]

phase('Review')
const reviews = await parallel(LENSES.map(l => () =>
  agent(l.prompt, { label: `review:${l.key}`, phase: 'Review', schema: FINDINGS_SCHEMA, effort: 'high' })
))

phase('Synthese')
const all = reviews.filter(Boolean).flatMap((r, i) => (r.findings || []).map(f => ({ lens: LENSES[i].key, ...f })))
log(`${all.length} Kreativ-Funde -> Synthese-Richter`)
const synth = await agent(`${CONTEXT}

Du bist der Synthese-Richter. Unten alle Funde von 5 Kreativ-Reviewern:
(1) Dedupliziere, loese Widersprueche. (2) VERWIRF alles ohne Playbook-Daten- oder klare
Retention-/CTR-Begruendung sowie alles, was auditierte Fakten verletzt (Dossier bindend) -
Liste unter 'verworfen' mit 1-Satz-Grund. (3) Priorisiere den Rest als Regieanweisungen.
(4) Schreibe pro Akt eine Schreibnotiz fuer den finalen Rewrite auf ~${zielWorte} Woerter.

FUNDE:
${JSON.stringify(all, null, 1)}`,
  { label: 'synthese-richter', phase: 'Synthese', schema: SYNTH_SCHEMA, effort: 'xhigh' })

return { anweisungen: synth.regieanweisungen, verworfen: synth.verworfen, schreibnotizen: synth.act_schreibnotizen, rohfunde: all.length }
