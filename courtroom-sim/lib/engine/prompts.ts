// Prompt construction. The case file is the source of truth for every character.
import type { CaseFile } from "./caseTypes";
import { GROUNDS } from "./objections";
import { JURY_ABSENT, phaseInfo } from "./phases";
import type { TrialState } from "./state";
import { bareJudge, witnessById } from "./witness";

export type PlayerInput =
  | { kind: "proceed" } // let the court / prosecution speak
  | { kind: "speech"; text: string } // the player speaking at the lectern
  | { kind: "objection"; groundId: string | null; text: string }
  | { kind: "motion"; motionId: string; text: string }
  | { kind: "challenge"; jurorId: number; text: string }; // for-cause challenge in voir dire

const TEMPERAMENT: Record<CaseFile["judge"]["temperament"], string> = {
  fair: "Even-handed and patient, but insists on proper procedure.",
  strict: "Terse and impatient. Cuts off rambling, issues contempt warnings for disrespect or repeated violations.",
  "pro-prosecution": "Former prosecutor. Gives the State the benefit of the doubt on close calls, but follows clear law.",
  "defense-friendly": "Former public defender. Protective of constitutional rights, skeptical of police shortcuts.",
};

export function systemPrompt(c: CaseFile): string {
  const { basedOn: _omit, defenseAngles: _hints, ...playable } = c;
  return `You are the engine of a realistic American criminal trial simulator. The human player is DEFENSE COUNSEL for ${c.defendant.name}. You voice everyone else: Judge ${bareJudge(c)}, prosecutor ${c.prosecutor.name}, witnesses, the clerk, prospective jurors, and silent juror reactions.

Hard rules:
- NEVER write dialogue for defense counsel. Only react to what the player said.
- Follow real procedure and the Federal Rules of Evidence / the jurisdiction's equivalents. Rulings must be legally correct for the situation and cite the rule briefly.
- Judge temperament: ${TEMPERAMENT[c.judge.temperament]}
- Prosecutor style: ${c.prosecutor.style}
- Witnesses stay in character per their demeanor. On cross they answer only what is asked. They reveal a hiddenFact or concede a priorStatement contradiction ONLY when the defense's question specifically and competently targets it — then report it in factsRevealed. Vague questions get evasive answers.
- If the defense asks a leading question on direct, asks something improper, argues with a witness, or mentions excluded evidence, the prosecutor objects (prosecutorObjected=true) and the judge rules.
- If the defense is disrespectful to the court or repeatedly defies rulings, set contemptWarning.
- Juror reactions: seated jurors react to persuasiveness through their personal biases. Strong impeachment, a sustained defense objection, or exposing a lie move jurors +3..+8 toward not guilty; damaging testimony or a sloppy defense moves them toward guilty. Most turns affect 2-6 jurors, not all 12.
- scoreEvents grade the defense's advocacy technique honestly (good and bad).
- Keep each spoken line to 1-3 sentences — this is read aloud. Sound like a real courtroom, not a TV show.
- Output ONLY a JSON object matching the schema.

CASE FILE (confidential to the engine):
${JSON.stringify(playable)}`;
}

const clip = (t: string, n: number) => (t.length > n ? t.slice(0, n - 1) + "…" : t);

/**
 * The sworn record of the last trial, condensed for the model. Witnesses are bound by it: a witness who
 * strays from prior testimony hands the defense an impeachment, and the engine should play it that way.
 */
export function priorTrialNotes(c: CaseFile, s: TrialState, budget = 9000): string {
  const prior = s.retrial?.prior?.at(-1);
  if (!prior) return "";
  const evName = (id: string) => c.evidence.find((e) => e.id === id)?.name ?? id;
  const chName = (id: string) => c.charges.find((x) => x.id === id)?.name ?? id;
  const out: string[] = [];
  out.push(`Verdicts: ${prior.verdicts.map((v) => `${chName(v.chargeId)} ${v.result} (${v.votesNotGuilty}-${12 - v.votesNotGuilty} NG)`).join("; ")}. Jury's deciding factor: ${prior.keyFactor}`);
  if (prior.bail) out.push(`Bail last time: client ${prior.bail}.`);
  const motions = Object.entries(prior.motionsHeard).map(([m, r]) => `${m}: ${r}`);
  if (motions.length) out.push(`Pretrial motions last time (law of the case; the judge will normally adhere unless new grounds are shown): ${motions.join("; ")}`);
  if (prior.excluded.length) out.push(`Evidence excluded last time: ${prior.excluded.map(evName).join("; ")}`);
  if (prior.revealed.length) out.push(`Facts the defense exposed last time (now on the record; witnesses cannot credibly deny them): ${prior.revealed.map((r) => r.fact).join("; ")}`);
  const rulings = prior.rulings.filter((r) => r.result === "sustained" || r.result === "overruled").slice(-12);
  if (rulings.length) out.push(`Notable objection rulings last time: ${rulings.map((r) => `${r.on} ${r.result}`).join("; ")}`);

  // Sworn testimony, grouped by witness: each answer with the question that drew it.
  const witnesses = [...c.witnesses.map((w) => ({ name: w.name })), { name: c.defendant.name }];
  const perWitness = Math.max(600, Math.floor((budget - out.join("\n").length) / Math.max(1, witnesses.length)));
  const t = prior.transcript;
  for (const w of witnesses) {
    const pairs: string[] = [];
    t.forEach((l, i) => {
      if (l.name !== w.name || !["witness", "defendant"].includes(l.speaker)) return;
      const q = t[i - 1];
      const qs = q && q.name !== w.name ? `Q (${q.name}): ${clip(q.text, 160)} ` : "";
      pairs.push(`${qs}A: ${clip(l.text, 220)}`);
    });
    if (!pairs.length) continue;
    let block = "";
    for (const p of pairs) {
      if (block.length + p.length > perWitness) { block += "\n  [… further testimony omitted]"; break; }
      block += "\n  " + p;
    }
    out.push(`SWORN TESTIMONY OF ${w.name.toUpperCase()} (trial ${prior.round}):${block}`);
  }
  return out.join("\n");
}

function retrialNote(c: CaseFile, s: TrialState): string {
  if (!s.retrial) return "";
  return `RETRIAL (round ${s.retrial.round}): the last jury hung on the remaining count(s) and a mistrial was declared. The defendant was ACQUITTED of: ${(s.retrial.acquittedNames ?? s.retrial.acquitted).join(", ") || "none"}. Those counts are final (double jeopardy) and must not be charged, argued, or mentioned as pending. Only the charges in the case file are before this court. This is a new jury with no memory of the first trial, but both lawyers have the full record. Witnesses testified under oath last time and are bound by it: they should testify consistently with their prior sworn testimony, and if they deviate or the defense confronts them with it, treat that as impeachment with a prior statement (report it in factsRevealed). The prosecutor has adjusted to the defense's first-trial strategy and will try to shore up the weaknesses the defense exposed.
PRIOR TRIAL RECORD:
${priorTrialNotes(c, s)}
`;
}

function jurySummary(s: TrialState): string {
  if (s.phase === "voir_dire") {
    return s.jurors
      .filter((j) => j.status === "venire")
      .map((j) => `#${j.id} ${j.name}, ${j.age}, ${j.occupation}. Hidden bias: ${j.bias}${j.revealed ? " (already revealed)" : ""}`)
      .join("\n");
  }
  return s.jurors
    .filter((j) => j.status === "seated")
    .map((j, i) => `Seat ${i + 1}: ${j.occupation}, ${j.age}. Bias: ${j.bias} Lean(0 guilty-100 not guilty)=${j.lean}`)
    .join("\n");
}

export function turnPrompt(c: CaseFile, s: TrialState, input: PlayerInput): string {
  const p = phaseInfo(s.phase);
  const witness = witnessById(c, s.currentWitness);
  const recent = s.transcript
    .slice(-30)
    .map((l) => `${l.name}: ${l.text}`)
    .join("\n");
  const ev = (ids: string[]) => ids.map((id) => c.evidence.find((e) => e.id === id)?.name ?? id).join("; ") || "none";

  let action = "";
  switch (input.kind) {
    case "proceed":
      action = witness
        ? `The defense yields the floor. Continue the ${s.examMode} examination of ${witness.name} (prosecution side) with 2-3 question/answer exchanges, then stop for possible defense objection. Set witnessExcused when the prosecutor says "no further questions" and the defense has already crossed, or when appropriate.`
        : `The court proceeds with this phase. ${p.aiOpens ? "Open the phase." : "Prompt defense counsel to proceed."}`;
      break;
    case "speech":
      action = `DEFENSE COUNSEL says: "${input.text}"`;
      break;
    case "objection": {
      const g = GROUNDS.find((x) => x.id === input.groundId);
      action = `DEFENSE COUNSEL OBJECTS${g ? ` — ${g.label} (${g.rule})` : " (no ground stated)"}: "${input.text}". The judge rules on the objection to the most recent question or statement. A ground-less objection should be overruled or the judge asks for the ground.`;
      break;
    }
    case "motion": {
      const m = c.pretrialMotions.find((x) => x.id === input.motionId);
      action = `DEFENSE COUNSEL argues ${m?.name ?? "a motion"} (id ${input.motionId}, baseline merit ${m?.merit ?? 30}/100, targets evidence: ${m?.targets?.join(", ") || "n/a"}): "${input.text}". Prosecutor responds, then the judge rules (ruling.on must be "${m?.name ?? input.motionId}").`;
      break;
    }
    case "challenge":
      action = `DEFENSE COUNSEL challenges prospective juror #${input.jurorId} for cause: "${input.text}". The judge rules SUSTAINED only if the record shows the juror cannot be impartial.`;
      break;
  }

  return `${retrialNote(c, s)}PHASE: ${p.label}. ${p.direction}
${witness ? `CURRENT WITNESS: ${witness.name} (${witness.role}, ${witness.side} witness, id ${witness.id}). Examination: ${s.examMode}.` : ""}
JURY ${JURY_ABSENT.includes(s.phase) ? "IS NOT PRESENT (jurorReactions must be empty)" : "IS PRESENT"}.
${s.phase === "voir_dire" ? "PANEL:" : "SEATED JURY:"}
${jurySummary(s)}
ADMITTED EVIDENCE: ${ev(s.admitted)}
EXCLUDED (must never be mentioned in front of the jury): ${ev(s.excluded)}
FACTS ALREADY EXPOSED: ${s.revealed.map((r) => r.fact).join("; ") || "none"}
COUNTS DISMISSED: ${s.dismissedCounts.join(", ") || "none"}

RECENT TRANSCRIPT:
${recent || "(start of proceedings)"}

NOW: ${action}`;
}

/** The appellate panel: rules on the brief against the trial record, count by count. */
export function appealPrompt(c: CaseFile, s: TrialState, brief: string): string {
  const d = s.deliberation!;
  const chName = (id: string) => c.charges.find((x) => x.id === id)?.name ?? id;
  const evName = (id: string) => c.evidence.find((e) => e.id === id)?.name ?? id;
  const verdicts = d.verdicts.map((v) => `${v.chargeId} (${chName(v.chargeId)}): ${v.result}${v.lesser ? ` — ${v.lesser}` : ""}, poll ${v.votesNotGuilty}-${12 - v.votesNotGuilty} NG`).join("\n");
  const convicted = d.verdicts.filter((v) => v.result === "guilty" || v.result === "guilty-lesser").map((v) => v.chargeId);
  const rulings = s.rulings.map((r) => `[${r.phase}] ${r.on}: ${r.result} (${r.reason})`).join("\n") || "none recorded";
  const transcript = s.transcript.filter((l) => l.speaker !== "system" || /—/.test(l.text)).map((l) => `${l.name}: ${l.text}`).join("\n").slice(-30000);
  return `You are a three-judge panel of the intermediate appellate court for ${c.jurisdiction}. Defense counsel has filed a brief appealing the convictions in ${c.title}. Decide it like a real court: on the trial record below and the law of the jurisdiction, applying the correct standard of review to each claim.

STANDARDS:
- Sufficiency of the evidence: view the record in the light most favorable to the verdict; ask whether ANY rational juror could find each element beyond a reasonable doubt (Jackson v. Virginia). This is deferential. Reverse only if an element has no evidentiary support in the record. Disposition "reversed-insufficient" bars retrial (double jeopardy).
- Trial error (evidence wrongly admitted or excluded, wrong jury instruction, Brady/Giglio violation, prosecutorial misconduct, ex parte contact, denial of a meritorious motion): reverse only if the error was preserved (or is plain error) AND not harmless beyond a reasonable doubt. Disposition "reversed-error" remands for a new trial on that count.
- "vacated": the conviction cannot stand for a structural reason (e.g. non-unanimous verdict, count legally impossible on the acquitted counts). Say whether retrial is possible.
- Inconsistent verdicts are not a ground for reversal. Acquittal on one count does not undo another.
- Do not reverse because you would have weighed the evidence differently. Do not reverse on arguments that the record contradicts. If the brief asserts facts the transcript does not support, say so and overrule.
- Rule on every enumeration the brief raises (sustained / overruled / moot). Then give a disposition for EVERY convicted count id: ${convicted.join(", ")}.
- If you notice a defect the brief missed (plain error), you may act on it and say so in plainError; otherwise null.
- Write like a court: precise, unsentimental, 3-8 sentences per enumeration. Then, separately, chambers notes critiquing the brief's craft (record citations, placeholder or fabricated citations, hypothetical framing, structure, hedging) and a grade for the brief itself, independent of who won.

CASE FILE (charges, elements, evidence, witnesses):
${JSON.stringify({ charges: c.charges, evidence: c.evidence.map((e) => ({ id: e.id, name: e.name, description: e.description, weakness: e.weakness, admissibilityIssue: e.admissibilityIssue })), witnesses: c.witnesses.map((w) => ({ id: w.id, name: w.name, role: w.role, side: w.side, priorStatements: w.priorStatements, credibilityIssues: w.credibilityIssues })) })}

VERDICTS:
${verdicts}
Counts dismissed by the trial judge: ${s.dismissedCounts.join(", ") || "none"}
Evidence admitted: ${s.admitted.map(evName).join("; ") || "none recorded"}
Evidence excluded: ${s.excluded.map(evName).join("; ") || "none"}
Rulings on motions and objections:
${rulings}
Facts exposed on cross: ${s.revealed.map((r) => r.fact).join("; ") || "none"}
Jury's stated deciding factor: ${d.keyFactor}

TRIAL TRANSCRIPT (the record):
${transcript || "(no transcript preserved)"}

BRIEF OF APPELLANT:
${brief.slice(0, 20000)}

Return ONLY JSON matching the schema.`;
}

export function deliberationPrompt(c: CaseFile, s: TrialState): string {
  const jury = s.jurors
    .filter((j) => j.status === "seated")
    .map((j, i) => `Seat ${i + 1} ${j.name} (${j.occupation}; bias: ${j.bias}) lean=${j.lean}`)
    .join("\n");
  const transcript = s.transcript.map((l) => `${l.name}: ${l.text}`).join("\n").slice(-24000);
  return `${retrialNote(c, s)}The jury retires to deliberate in ${c.title}. Charges: ${c.charges
    .map((ch) => `${ch.id}: ${ch.name} — elements: ${ch.elements.join("; ")}${ch.lesserIncluded?.length ? ` — lesser included: ${ch.lesserIncluded.join(", ")}` : ""}`)
    .join(" | ")}.
Counts already dismissed by the judge (verdict must be not-guilty): ${s.dismissedCounts.join(", ") || "none"}.
The verdict must be unanimous; if jurors cannot agree on a count the result is "hung". votesNotGuilty is the FINAL poll: 12 for a not-guilty verdict, 0 for a guilty verdict; only a hung count has a split (e.g. 7). If your deliberation ends with holdouts on a count, that count is "hung", not a verdict.
Jurors and their current lean (0 certain guilty — 100 certain not guilty). Treat leans as strong priors: jurors at >=60 argue for acquittal, <=40 for conviction; persuadable ones in between follow the strongest arguments grounded in the actual record and reasonable-doubt instruction.
${jury}

Defense performance notes: ${s.revealed.length} hidden facts exposed (${s.revealed.map((r) => r.fact).join("; ") || "none"}); objections sustained ${s.objections.sustained}/${s.objections.made}; evidence excluded: ${s.excluded.join(", ") || "none"}.

FULL TRIAL TRANSCRIPT:
${transcript}

Write the deliberation and return verdicts for every charge id. Return ONLY JSON.`;
}
