// Trial state + reducer. All model output flows through `applyTurn`.
import type { CaseFile } from "./caseTypes";
import { JURY_ABSENT, nextPhase, type PhaseId } from "./phases";
import { clampLean, generateVenire, hashString, prosecutionStrikes, seatJury, type Juror } from "./jurors";
import type { CourtLineT, CourtTurn, Deliberation, RulingT } from "./schema";
import { appliedVerdicts, type AppealRecord } from "./appeal";

export type ExamMode = "direct" | "cross" | "redirect";

export interface TranscriptLine extends Omit<CourtLineT, "speaker"> {
  id: number;
  speaker: CourtLineT["speaker"] | "defense" | "system";
}

export interface ScoreEvent { label: string; points: number; phase: PhaseId }

/** What survives a mistrial: the sworn record. Everything the lawyers can hold witnesses to next time. */
export interface PriorTrial {
  round: number;
  verdicts: Deliberation["verdicts"];
  keyFactor: string;
  critique: string[];
  bail: TrialState["bail"];
  motionsHeard: TrialState["motionsHeard"];
  rulings: Array<RulingT & { phase: PhaseId }>;
  admitted: string[];
  excluded: string[];
  revealed: Array<{ witnessId: string; fact: string }>;
  /** Non-system transcript lines, in order: the prior sworn testimony and argument. */
  transcript: Array<{ speaker: TranscriptLine["speaker"]; name: string; text: string; phase: PhaseId }>;
}

export interface RetrialInfo {
  round: number; // 2 for the first retrial
  acquitted: string[]; // charge ids resolved not-guilty in earlier rounds (jeopardy attached; cannot be retried)
  acquittedNames: string[]; // display names for the ids above (the model only sees a case file with those charges removed)
  prior: PriorTrial[]; // one record per earlier round, oldest first
}

export interface TrialState {
  caseId: string;
  phase: PhaseId;
  transcript: TranscriptLine[];
  jurors: Juror[];
  peremptoriesLeft: number;
  admitted: string[];
  excluded: string[];
  motionsHeard: Record<string, "granted" | "denied" | "granted-in-part">;
  witnessQueue: string[]; // prosecution witness ids remaining
  defenseCalled: string[];
  currentWitness: string | null;
  examMode: ExamMode | null;
  revealed: Array<{ witnessId: string; fact: string }>;
  rulings: Array<RulingT & { phase: PhaseId }>;
  score: ScoreEvent[];
  objections: { made: number; sustained: number; againstYou: number; againstYouSustained: number };
  contempt: number;
  dismissedCounts: string[];
  deliberation: Deliberation | null;
  /** Set when this trial is a retrial of counts the last jury hung on. Acquitted counts never come back. */
  retrial: RetrialInfo | null;
  /** The appeal taken from this trial's verdict, once decided. */
  appeal: AppealRecord | null;
  bail: "remanded" | "released" | null;
  nextId: number;
}

export function initTrial(c: CaseFile, seed = hashString(c.id + Date.now())): TrialState {
  return {
    caseId: c.id,
    phase: "arraignment",
    transcript: [],
    jurors: generateVenire(seed, c.startingLean),
    peremptoriesLeft: 3,
    admitted: [],
    excluded: [],
    motionsHeard: {},
    witnessQueue: c.witnesses.filter((w) => w.side === "prosecution").map((w) => w.id),
    defenseCalled: [],
    currentWitness: null,
    examMode: null,
    revealed: [],
    rulings: [],
    score: [],
    objections: { made: 0, sustained: 0, againstYou: 0, againstYouSustained: 0 },
    contempt: 0,
    dismissedCounts: [],
    deliberation: null,
    retrial: null,
    appeal: null,
    bail: null,
    nextId: 1,
  };
}

/** Charge ids the defendant can no longer be tried on in this trial. */
export function acquittedCounts(s: TrialState): string[] {
  return s.retrial?.acquitted ?? [];
}

/** Charges still live in this trial: earlier-round acquittals are gone for good. */
export function activeCase(c: CaseFile, s: TrialState): CaseFile {
  const gone = new Set(acquittedCounts(s));
  return gone.size ? { ...c, charges: c.charges.filter((ch) => !gone.has(ch.id)) } : c;
}

/**
 * A hung jury ends in a mistrial, and the State may retry the counts the jury could not decide.
 * Counts the jury acquitted on (or the judge dismissed) are final under the Double Jeopardy Clause.
 * Returns null unless at least one count hung and none ended in a conviction.
 */
export function retriableCounts(s: TrialState): string[] | null {
  const d = s.deliberation;
  if (!d) return null;
  // After an appeal, reversed-for-error counts read as "hung" (the State may retry) and
  // reversed-for-insufficiency counts read as acquittals.
  const verdicts = appliedVerdicts(s);
  const hung = verdicts.filter((v) => v.result === "hung" && !s.dismissedCounts.includes(v.chargeId)).map((v) => v.chargeId);
  const convicted = verdicts.some((v) => (v.result === "guilty" || v.result === "guilty-lesser") && !s.dismissedCounts.includes(v.chargeId));
  return hung.length && !convicted ? hung : null;
}

const PHASE_MARK = /^— (.+) —$/;

/** Snapshot the record of a finished trial so a retrial can use it. */
export function priorTrialRecord(prev: TrialState): PriorTrial {
  // Transcript lines carry no phase; the system markers ("— VOIR DIRE —") tell us where we are.
  let phase: PhaseId = "arraignment";
  const transcript: PriorTrial["transcript"] = [];
  for (const l of prev.transcript) {
    if (l.speaker === "system") {
      const m = PHASE_MARK.exec(l.text);
      if (m) phase = m[1].toLowerCase().replace(/\s+/g, "_") as PhaseId;
      continue;
    }
    transcript.push({ speaker: l.speaker, name: l.name, text: l.text, phase });
  }
  const d = prev.deliberation;
  return {
    round: prev.retrial?.round ?? 1,
    verdicts: appliedVerdicts(prev),
    keyFactor: d?.keyFactor ?? "",
    critique: d?.critique ?? [],
    bail: prev.bail,
    motionsHeard: prev.motionsHeard,
    rulings: prev.rulings,
    admitted: prev.admitted,
    excluded: prev.excluded,
    revealed: prev.revealed,
    transcript,
  };
}

/**
 * Law of the case: pretrial rulings from the last trial bind the retrial. Motions the judge granted stay
 * granted (and their evidence stays out); denied motions may be re-argued on new grounds, so they are left open.
 */
export function applyPriorRulings(c: CaseFile, s: TrialState, prior: PriorTrial): TrialState {
  const motionsHeard = { ...s.motionsHeard };
  const excluded = new Set(s.excluded);
  for (const [name, r] of Object.entries(prior.motionsHeard)) {
    if (r === "denied") continue;
    motionsHeard[name] = r;
    const m = c.pretrialMotions.find((x) => x.name === name);
    if (r === "granted") for (const id of m?.targets ?? []) excluded.add(id);
  }
  for (const id of prior.excluded) excluded.add(id);
  return { ...s, motionsHeard, excluded: [...excluded] };
}

/** Fresh trial (new venire, clean record) on only the counts the last jury hung on. The first trial's record comes along. */
export function initRetrial(c: CaseFile, prev: TrialState, seed?: number): TrialState {
  const hung = new Set(retriableCounts(prev) ?? []);
  const acquitted = [...new Set([...acquittedCounts(prev), ...c.charges.map((ch) => ch.id).filter((id) => !hung.has(id))])];
  const fresh = seed === undefined ? initTrial(c) : initTrial(c, seed);
  const acquittedNames = acquitted.map((id) => c.charges.find((ch) => ch.id === id)?.name ?? id);
  const record = priorTrialRecord(prev);
  const next = { ...fresh, retrial: { round: (prev.retrial?.round ?? 1) + 1, acquitted, acquittedNames, prior: [...(prev.retrial?.prior ?? []), record] } };
  return applyPriorRulings(c, next, record);
}

export type Action =
  | { type: "say"; speaker: TranscriptLine["speaker"]; name: string; text: string }
  | { type: "turn"; turn: CourtTurn; objectionByDefense?: boolean }
  | { type: "advance" }
  | { type: "callWitness"; witnessId: string; mode: ExamMode }
  | { type: "setExam"; mode: ExamMode }
  | { type: "excuseWitness" }
  | { type: "strike"; jurorId: number }
  | { type: "excuseForCause"; jurorId: number }
  | { type: "seatJury" }
  | { type: "deliberated"; result: Deliberation }
  | { type: "appealed"; appeal: AppealRecord }
  | { type: "load"; state: TrialState };

function push(s: TrialState, lines: Array<Omit<TranscriptLine, "id">>): TrialState {
  let id = s.nextId;
  return { ...s, transcript: [...s.transcript, ...lines.map((l) => ({ ...l, id: id++ }))], nextId: id };
}

export function applyTurn(s: TrialState, t: CourtTurn, objectionByDefense = false): TrialState {
  let next = push(s, t.lines);
  const juryPresent = !JURY_ABSENT.includes(s.phase);

  // Jurors: map seat numbers (1-12 in seating order) to venire ids.
  if (juryPresent && t.jurorReactions.length) {
    const seats = next.jurors.filter((j) => j.status === "seated").map((j) => j.id);
    const bySeat = new Map(t.jurorReactions.map((r) => [seats[r.seat - 1], r]));
    next.jurors = next.jurors.map((j) => {
      const r = bySeat.get(j.id);
      return r ? { ...j, lean: clampLean(j.lean + r.delta), lastDelta: r.delta, lastReason: r.reason } : { ...j, lastDelta: 0 };
    });
  }
  if (t.jurorsRevealed.length) {
    next.jurors = next.jurors.map((j) => (t.jurorsRevealed.includes(j.id) ? { ...j, revealed: true } : j));
  }

  const excluded = [...new Set([...next.excluded, ...t.evidenceExcluded])];
  next.excluded = excluded;
  next.admitted = [...new Set([...next.admitted, ...t.evidenceAdmitted])].filter((id) => !excluded.includes(id));

  const newFacts = t.factsRevealed.filter((f) => !next.revealed.some((r) => r.fact === f.fact));
  next.revealed = [...next.revealed, ...newFacts];

  const score: ScoreEvent[] = t.scoreEvents.map((e) => ({ ...e, phase: s.phase }));
  newFacts.forEach((f) => score.push({ label: `Exposed: ${f.fact.slice(0, 60)}`, points: 5, phase: s.phase }));

  const objections = { ...next.objections };
  if (t.ruling) {
    next.rulings = [...next.rulings, { ...t.ruling, phase: s.phase }];
    const r = t.ruling.result;
    if (objectionByDefense) {
      objections.made++;
      if (r === "sustained") objections.sustained++;
      score.push({ label: `Objection ${r}: ${t.ruling.on}`, points: r === "sustained" ? 3 : -1, phase: s.phase });
    } else if (t.prosecutorObjected) {
      objections.againstYou++;
      if (r === "sustained") { objections.againstYouSustained++; score.push({ label: `Prosecution objection sustained: ${t.ruling.on}`, points: -2, phase: s.phase }); }
    } else if (s.phase === "pretrial") {
      const motion = t.ruling.on;
      if (r !== "sustained" && r !== "overruled") next.motionsHeard = { ...next.motionsHeard, [motion]: r };
      if (t.ruling.favorsDefense) score.push({ label: `Motion won: ${motion}`, points: 8, phase: s.phase });
    } else if (s.phase === "arraignment" && (r === "granted" || r === "denied")) {
      next.bail = t.ruling.favorsDefense ? "released" : "remanded";
    }
  }
  next.objections = objections;
  next.score = [...next.score, ...score];

  if (t.contemptWarning) {
    next.contempt++;
    next.score = [...next.score, { label: "Contempt warning from the bench", points: -8, phase: s.phase }];
  }
  if (t.countsDismissed.length) next.dismissedCounts = [...new Set([...next.dismissedCounts, ...t.countsDismissed])];
  if (t.witnessExcused && next.currentWitness) next = excuse(next);
  return next;
}

function excuse(s: TrialState): TrialState {
  return {
    ...s,
    witnessQueue: s.witnessQueue.filter((w) => w !== s.currentWitness),
    currentWitness: null,
    examMode: null,
  };
}

export function reducer(s: TrialState, a: Action): TrialState {
  switch (a.type) {
    case "load":
      return a.state;
    case "say":
      return push(s, [{ speaker: a.speaker, name: a.name, text: a.text }]);
    case "turn":
      return applyTurn(s, a.turn, a.objectionByDefense);
    case "advance": {
      const phase = nextPhase(s.phase);
      let next: TrialState = { ...s, phase, currentWitness: null, examMode: null };
      if (s.phase === "voir_dire") next = { ...next, jurors: finalizeJury(next.jurors) };
      return push(next, [{ speaker: "system", name: "Court", text: `— ${phase.replace(/_/g, " ").toUpperCase()} —` }]);
    }
    case "callWitness":
      return {
        ...s,
        currentWitness: a.witnessId,
        examMode: a.mode,
        defenseCalled: a.mode === "direct" && s.phase === "defense_case" ? [...new Set([...s.defenseCalled, a.witnessId])] : s.defenseCalled,
      };
    case "setExam":
      return { ...s, examMode: a.mode };
    case "excuseWitness":
      return excuse(s);
    case "strike":
      if (s.peremptoriesLeft <= 0) return s;
      return {
        ...s,
        peremptoriesLeft: s.peremptoriesLeft - 1,
        jurors: s.jurors.map((j) => (j.id === a.jurorId ? { ...j, status: "struck-defense" } : j)),
      };
    case "excuseForCause":
      return { ...s, jurors: s.jurors.map((j) => (j.id === a.jurorId ? { ...j, status: "excused-cause" } : j)) };
    case "seatJury":
      return { ...s, jurors: finalizeJury(s.jurors) };
    case "deliberated":
      return { ...s, deliberation: a.result, phase: "verdict" };
    case "appealed":
      return { ...s, appeal: a.appeal };
  }
}

function finalizeJury(jurors: Juror[]): Juror[] {
  if (jurors.some((j) => j.status === "seated")) return jurors;
  const strikes = prosecutionStrikes(jurors, 3);
  return seatJury(jurors.map((j) => (strikes.includes(j.id) ? { ...j, status: "struck-prosecution" } : j)));
}
