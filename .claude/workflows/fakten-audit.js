export const meta = {
  name: 'fakten-audit',
  description: 'Pflicht-Fakten-Audit eines Video-Produktionspakets (Historik + Produktions-Mathematik, adversarial verifiziert)',
  whenToUse: 'Nach dem Schreiben von Dossier+Skript eines neuen Videos, VOR dem Kreativ-Review. Aufruf: Workflow({name:"fakten-audit", args:{videoDir:"produktion/video-XX-...", epoche:"z.B. Byzanz 1453"}})',
  phases: [
    { title: 'Audit', detail: '2 Experten-Linsen parallel' },
    { title: 'Verify', detail: 'jeden Fund adversarial gegenpruefen (WebSearch)' },
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
          file: { type: 'string' },
          title: { type: 'string' },
          detail: { type: 'string' },
          fix: { type: 'string' },
          severity: { type: 'string', enum: ['kritisch', 'wichtig', 'klein'] },
        },
        required: ['file', 'title', 'detail', 'fix', 'severity'],
      },
    },
  },
  required: ['findings'],
}

const VERDICT_SCHEMA = {
  type: 'object',
  properties: {
    isReal: { type: 'boolean' },
    reasoning: { type: 'string' },
    improvedFix: { type: 'string' },
  },
  required: ['isReal', 'reasoning'],
}

// args kann je nach Aufrufer als JSON-String statt Objekt ankommen -> beides tolerieren
const _a = (typeof args === 'string') ? (() => { try { return JSON.parse(args) } catch (e) { return {} } })() : (args || {})
const dir = _a.videoDir || 'produktion/video-01-constantinople'
const epoche = _a.epoche || 'siehe Dossier'

const CONTEXT = `Repo: /home/user/niche-finder. Zu pruefen: ${dir}/ (alle Dateien, v. a.
01-recherche-dossier.md und 02-skript.md). Der Kanal verkauft QUELLEN-PRAEZISION als Marke -
jeder Fehler ist Markenschaden. Du darfst WebSearch/WebFetch zur Verifikation und Python
(.venv/bin/python) zum Nachrechnen nutzen. Melde NUR echte Defekte mit konkretem Fix.
Bindende Kanal-Regeln (CLAUDE.md QA-Kapitel): (1) KEIN woertliches Zitat ohne notierte
Fundstelle - erfundene/paraphrasierte Zitate mit Quellen-Datums-Karte sind toedlich.
(2) Jede Superlativ-Behauptung ("nie", "erste", "groesste") auf historische Angriffsflaechen
pruefen, die Kommentatoren sofort finden. (3) Legenden/duenne Quellenlage muessen im Skript
attribuiert sein ("if X is to be believed" / "tradition records"). (4) Anachronismus-
Sperrliste des Dossiers auf Vollstaendigkeit pruefen.`

const LENSES = [
  { key: 'historik', prompt: `${CONTEXT}

Du bist Fachhistoriker (${epoche}). Pruefe Dossier + Skript Zeile fuer Zeile: alle Zahlen,
Daten, Chronologie, Namen, Zitat-Authentizitaet (jedes Zitat per WebSearch gegen
Standard-Uebersetzungen pruefen!), Superlative, Legenden-vs-Fakten-Trennung,
Anachronismus-Sperrliste, Zeugen-Details (Beruf, Quellenlage, Schicksal).` },
  { key: 'produktion', prompt: `${CONTEXT}

Du bist Technical Producer. Pruefe Shotlist/Skript/Checkliste auf Machbarkeit: Timing-Summen
nachrechnen (Python!), Wortzahl vs. Ziel-Laenge (150 wpm + Stille-Budget), Beat-Mapping
Skript<->Shotlist konsistent, Aufloesungs-Regeln eingehalten (Zoom-Shots = Seedream
quality=high ~6K; Seedance resolution=4k explizit; Upscale-Batch eingepreist),
Clip-/Still-Zaehlungen, Credit-Schaetzung Premium-Kern (550-650), ElevenLabs-Zeichenbudget.` },
]

phase('Audit')
const results = await pipeline(
  LENSES,
  l => agent(l.prompt, { label: `audit:${l.key}`, phase: 'Audit', schema: FINDINGS_SCHEMA, effort: 'high' }),
  (review, lens) => {
    const findings = (review && review.findings) ? review.findings : []
    log(`${lens.key}: ${findings.length} Funde`)
    return parallel(findings.map(f => () =>
      agent(`${CONTEXT}

Ein Auditor (${lens.key}) meldet folgenden Befund. WIDERLEGE ihn, wenn er falsch, irrelevant
oder uebertrieben ist - lies selbst, rechne selbst, recherchiere selbst (WebSearch).
isReal=true NUR wenn sachlich korrekt UND handlungsrelevant; verbessere dann ggf. den Fix.

Datei: ${f.file}
Befund [${f.severity}]: ${f.title}
Detail: ${f.detail}
Fix-Vorschlag: ${f.fix}`,
        { label: `verify:${f.title.slice(0, 38)}`, phase: 'Verify', schema: VERDICT_SCHEMA, effort: 'high' })
        .then(v => ({ ...f, lens: lens.key, verdict: v }))
    ))
  }
)

const confirmed = results.filter(Boolean).flat().filter(Boolean).filter(f => f.verdict && f.verdict.isReal)
const order = { kritisch: 0, wichtig: 1, klein: 2 }
confirmed.sort((a, b) => (order[a.severity] ?? 3) - (order[b.severity] ?? 3))
log(`Bestaetigte Funde: ${confirmed.length}`)
return { confirmed }
