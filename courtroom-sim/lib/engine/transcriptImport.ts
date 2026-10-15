// Rebuild a prior-trial record from a pasted transcript (the trial screen's copy of the record,
// optionally with the verdict screen pasted above it). Used when a retrial was started before
// the record was being snapshotted, or when a player wants to attach a transcript by hand.
import type { CaseFile } from "./caseTypes";
import type { PhaseId } from "./phases";
import type { PriorTrial, TrialState } from "./state";

const PHASE_MARK = /^— (.+) —$/;
const VERDICT_LINE = /^(.+?):\s*(NOT GUILTY|GUILTY(?: \(lesser\))?|HUNG JURY)\s*(?:—\s*(.+?))?\s*\((\d+)\s*[–-]\s*(\d+)\s*NG\)\s*$/i;
const FOREPERSON = /^Foreperson (.+?) · Deciding factor: (.+)$/;
const RULING_LINE = /^(Motion .+?):\s*(granted-in-part|granted|denied)\s*$/i;

export function speakerFor(c: CaseFile, name: string): TrialState["transcript"][number]["speaker"] {
  if (/^defense/i.test(name)) return "defense";
  if (/^judge/i.test(name) || name === c.judge.name) return "judge";
  if (/^clerk/i.test(name)) return "clerk";
  if (/^bailiff/i.test(name)) return "bailiff";
  if (name === c.prosecutor.name || /^(ADA|ASA|DA|AUSA|Prosecutor)\b/i.test(name)) return "prosecutor";
  if (name === c.defendant.name) return "defendant";
  if (c.witnesses.some((w) => w.name === name)) return "witness";
  // The prosecutor's display name varies ("ASA Urquhart" vs the full title); match on surname.
  const surname = c.prosecutor.name.split(" ").pop();
  if (surname && name.endsWith(surname)) return "prosecutor";
  return "juror";
}

/** Parse pasted text into a PriorTrial. Lines are "Name: text"; "— PHASE —" markers set the phase. */
export function parsePriorTrial(
  c: CaseFile,
  text: string,
  opts: { round?: number; acquitted?: string[]; motionsHeard?: PriorTrial["motionsHeard"] } = {},
): PriorTrial {
  const acquitted = new Set(opts.acquitted ?? []);
  const motionsHeard: PriorTrial["motionsHeard"] = { ...(opts.motionsHeard ?? {}) };
  const transcript: PriorTrial["transcript"] = [];
  const verdicts = new Map<string, PriorTrial["verdicts"][number]>();
  let phase: PhaseId = "arraignment";
  let foreperson = "";
  let keyFactor = "";

  for (const raw of text.split(/\r?\n/)) {
    const l = raw.trim();
    if (!l) continue;
    const mark = PHASE_MARK.exec(l);
    if (mark) { phase = mark[1].toLowerCase().replace(/\s+/g, "_") as PhaseId; continue; }
    const fp = FOREPERSON.exec(l);
    if (fp) { foreperson = fp[1]; keyFactor = fp[2]; continue; }
    const rl = RULING_LINE.exec(l);
    if (rl) {
      const m = c.pretrialMotions.find((x) => x.name.toLowerCase() === rl[1].trim().toLowerCase());
      if (m) motionsHeard[m.name] = rl[2].toLowerCase() as PriorTrial["motionsHeard"][string];
      continue;
    }
    const v = VERDICT_LINE.exec(l);
    if (v) {
      const ch = c.charges.find((x) => x.name.toLowerCase() === v[1].trim().toLowerCase());
      if (ch) {
        const label = v[2].toUpperCase();
        const result = label === "HUNG JURY" ? "hung" : label === "NOT GUILTY" ? "not-guilty" : label.includes("LESSER") ? "guilty-lesser" : "guilty";
        verdicts.set(ch.id, { chargeId: ch.id, result, lesser: v[3] ?? null, votesNotGuilty: Number(v[4]) });
      }
      continue;
    }
    const m = /^([^:]{2,60}?):\s+(.+)$/.exec(l);
    if (!m) continue;
    transcript.push({ speaker: speakerFor(c, m[1]), name: m[1], text: m[2], phase });
  }

  // Fill in any verdicts the paste didn't include from what we know: acquitted counts are not-guilty, the rest hung.
  for (const ch of c.charges) {
    if (!verdicts.has(ch.id)) verdicts.set(ch.id, { chargeId: ch.id, result: acquitted.has(ch.id) ? "not-guilty" : "hung", lesser: null, votesNotGuilty: acquitted.has(ch.id) ? 12 : 6 });
  }

  return {
    round: opts.round ?? 1,
    verdicts: c.charges.map((ch) => verdicts.get(ch.id)!),
    keyFactor: keyFactor || (foreperson ? `Foreperson ${foreperson}` : ""),
    critique: [],
    bail: null,
    motionsHeard,
    rulings: [],
    admitted: [],
    excluded: c.pretrialMotions.filter((m) => motionsHeard[m.name] === "granted").flatMap((m) => m.targets ?? []),
    revealed: [],
    transcript,
  };
}
