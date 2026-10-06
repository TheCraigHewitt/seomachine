// Offline court used when OPENROUTER_API_KEY is not set. Rule-based but playable:
// keyword overlap with a witness's hidden facts reveals them, motion merit decides rulings.
import type { AppealOpinion } from "@/lib/engine/appeal";
import type { CaseFile } from "../engine/caseTypes";
import { GROUNDS } from "../engine/objections";
import { JURY_ABSENT, phaseInfo } from "../engine/phases";
import type { PlayerInput } from "../engine/prompts";
import type { CourtTurn, Deliberation } from "../engine/schema";
import { seated, type Juror } from "../engine/jurors";
import type { TrialState } from "../engine/state";
import { bareJudge, witnessById } from "../engine/witness";
import { hashString } from "../engine/jurors";

const STOP = new Set("the a an and or but of to in on at for with was were is are that this his her their they he she it you your did not have had from by as be been what when where who why how".split(" "));
const words = (s: string) => new Set(s.toLowerCase().match(/[a-z0-9']{3,}/g)?.filter((w) => !STOP.has(w)) ?? []);
const overlap = (a: string, b: string) => { const A = words(a); let n = 0; words(b).forEach((w) => A.has(w) && n++); return n; };

const empty = (): CourtTurn => ({
  lines: [], ruling: null, prosecutorObjected: false, evidenceAdmitted: [], evidenceExcluded: [], factsRevealed: [],
  jurorReactions: [], scoreEvents: [], jurorsRevealed: [], contemptWarning: false, witnessExcused: false, countsDismissed: [],
});

const PERSUASIVE = /reasonable doubt|inconsistent|prior statement|you told|isn't it true|never|no evidence|didn't see|deal|immunity|lied|contaminat|chain of custody|burden|presum/i;

function react(s: TrialState, text: string, strength: number): CourtTurn["jurorReactions"] {
  if (JURY_ABSENT.includes(s.phase)) return [];
  const hits = (text.match(new RegExp(PERSUASIVE, "gi")) ?? []).length;
  const base = Math.min(8, strength + hits * 2);
  return seated(s.jurors).slice(0, 12).map((j: Juror, i) => ({
    seat: i + 1,
    delta: Math.round(base * (j.biasShift >= 0 ? 1 : 0.5) * ((i * 7) % 3 === 0 ? 1 : 0.5)),
    reason: hits ? "Found the point persuasive" : "Listening carefully",
  })).filter((r) => r.delta !== 0);
}

export function mockTurn(c: CaseFile, s: TrialState, input: PlayerInput): CourtTurn {
  const t = empty();
  const J = { speaker: "judge" as const, name: `Judge ${bareJudge(c)}` };
  const P = { speaker: "prosecutor" as const, name: c.prosecutor.name };
  const w = witnessById(c, s.currentWitness);
  const W = w ? { speaker: "witness" as const, name: w.name } : null;

  if (input.kind === "objection") {
    const g = GROUNDS.find((x) => x.id === input.groundId);
    const lastProsecution = [...s.transcript].reverse().find((l) => l.speaker === "prosecutor")?.text ?? "";
    const sustained = !!g && (g.id === "leading" ? /\?$/.test(lastProsecution) && /^(isn't|didn't|wasn't|you|so)/i.test(lastProsecution) : ["hearsay", "speculation", "character", "prejudice", "vouching", "misstates"].includes(g.id) ? lastProsecution.length % 2 === 0 : false);
    t.lines.push({ ...J, text: g ? (sustained ? `Sustained. The jury will disregard that.` : `Overruled. You may continue.`) : "On what grounds, counsel?" });
    if (g) t.ruling = { on: g.label, result: sustained ? "sustained" : "overruled", reason: `${g.rule}: ${g.tip}`, favorsDefense: sustained };
    t.jurorReactions = sustained ? react(s, "reasonable doubt", 1) : [];
    return t;
  }

  if (input.kind === "motion") {
    const m = c.pretrialMotions.find((x) => x.id === input.motionId);
    const granted = !!m && m.merit + Math.min(30, input.text.length / 8) >= 70;
    t.lines.push({ ...P, text: "The State opposes. The evidence was lawfully obtained and is highly probative." });
    t.lines.push({ ...J, text: granted ? `Having considered the arguments, the motion is granted.` : `The motion is denied. The defense may renew the objection at trial.` });
    t.ruling = { on: m?.name ?? input.motionId, result: granted ? "granted" : "denied", reason: m?.basis ?? "", favorsDefense: granted };
    if (granted && m?.targets) t.evidenceExcluded = m.targets;
    return t;
  }

  if (input.kind === "challenge") {
    const j = s.jurors.find((x) => x.id === input.jurorId);
    const ok = !!j && j.revealed && Math.abs(j.biasShift) >= 10;
    t.lines.push({ ...J, text: ok ? `Challenge for cause is sustained. Juror ${j!.id}, you are excused with the court's thanks.` : "Overruled. The juror stated they can be fair." });
    t.ruling = { on: `Challenge for cause — juror #${input.jurorId}`, result: ok ? "sustained" : "overruled", reason: "Actual bias must appear on the record.", favorsDefense: ok };
    return t;
  }

  if (input.kind === "proceed") {
    switch (s.phase) {
      case "arraignment":
        t.lines.push({ speaker: "clerk", name: "Clerk", text: `Calling ${c.title}, case number CR-${(hashString(c.id) % 90000) + 10000}.` });
        t.lines.push({ ...J, text: `${c.defendant.name}, you are charged with ${c.charges.map((x) => x.name).join(", ")}. Counsel, how does your client plead?` });
        return t;
      case "voir_dire":
        t.lines.push({ ...J, text: "Ladies and gentlemen of the panel, the attorneys will now ask you some questions. Please answer honestly. Defense, you may inquire." });
        return t;
      case "prosecution_opening":
        t.lines.push({ ...P, text: c.prosecutionTheory });
        t.lines.push({ ...P, text: "At the end of this trial, the evidence will leave you with only one verdict: guilty." });
        t.jurorReactions = seated(s.jurors).map((_, i) => ({ seat: i + 1, delta: -3, reason: "The State's story sounds coherent" }));
        return t;
      case "prosecution_case":
        if (w && W) {
          const said = s.transcript.filter((l) => l.name === w.name).length;
          if (said === 0) {
            t.lines.push({ ...P, text: `Please state your name and tell the jury what you do.` });
            t.lines.push({ ...W, text: `${w.name}. I'm the ${w.role.toLowerCase()} in this case.` });
            t.lines.push({ ...P, text: "Tell the jury what you know." });
            t.lines.push({ ...W, text: w.publicTestimony });
            t.jurorReactions = seated(s.jurors).map((_, i) => ({ seat: i + 1, delta: i % 2 ? -2 : -1, reason: "Damaging testimony" }));
          } else {
            t.lines.push({ ...P, text: "Nothing further, Your Honor. Pass the witness." });
          }
          return t;
        }
        t.lines.push({ ...J, text: s.witnessQueue.length ? "The State may call its next witness." : "Does the State rest?" });
        if (!s.witnessQueue.length) t.lines.push({ ...P, text: "The State rests, Your Honor." });
        return t;
      case "defense_case":
        if (w && W && s.examMode === "cross") {
          t.lines.push({ ...P, text: `You'd say anything to help the defendant, wouldn't you?` });
          t.lines.push({ ...W, text: "No. I'm telling the truth." });
          t.lines.push({ ...P, text: "Nothing further." });
          t.witnessExcused = true;
          return t;
        }
        t.lines.push({ ...J, text: "Defense, call your next witness, or rest." });
        return t;
      case "prosecution_closing":
        t.lines.push({ ...P, text: `You've heard the evidence. ${c.prosecutionTheory} The defendant is guilty on every count.` });
        t.jurorReactions = seated(s.jurors).map((_, i) => ({ seat: i + 1, delta: -3, reason: "Closing tied it together" }));
        return t;
      case "instructions":
        t.lines.push({ ...J, text: "Members of the jury, the defendant is presumed innocent. The State must prove every element beyond a reasonable doubt. The defendant need not prove anything." });
        c.charges.forEach((ch) => t.lines.push({ ...J, text: `As to ${ch.name}, the State must prove: ${ch.elements.join("; ")}.` }));
        return t;
      default:
        t.lines.push({ ...J, text: "Counsel, you may proceed." });
        return t;
    }
  }

  // Player speech.
  const text = input.text;
  if (s.phase === "arraignment") {
    const bail = /bail|release|recogni|ties|family|job|flight/i.test(text);
    t.lines.push({ ...P, text: "The State asks that the defendant be held without bail given the seriousness of the charges." });
    t.lines.push({ ...J, text: bail ? "Bail is set with conditions of electronic monitoring." : "The defendant is remanded pending trial." });
    t.ruling = { on: "Bail", result: bail ? "granted" : "denied", reason: "Weighing flight risk and danger to the community.", favorsDefense: bail };
    return t;
  }
  if (s.phase === "voir_dire") {
    const target = s.jurors.filter((j) => j.status === "venire").sort((a, b) => overlap(text, b.bias) - overlap(text, a.bias))[0];
    if (target) {
      t.lines.push({ speaker: "juror", name: `Juror #${target.id} ${target.name}`, text: `I'll be honest, since you asked. (${target.bias})` });
      t.jurorsRevealed = [target.id];
    }
    return t;
  }
  if (w && W) {
    const cross = s.examMode === "cross";
    const facts = [...w.hiddenFacts, ...w.priorStatements].filter((f) => !s.revealed.some((r) => r.fact === f));
    const best = facts.map((f) => ({ f, n: overlap(text, f) })).sort((a, b) => b.n - a.n)[0];
    if (!cross && /^(isn't|didn't|wasn't|weren't|you|so you)/i.test(text.trim())) {
      t.lines.push({ ...P, text: "Objection, leading." });
      t.lines.push({ ...J, text: "Sustained. Rephrase, counsel." });
      t.prosecutorObjected = true;
      t.ruling = { on: "Leading", result: "sustained", reason: "FRE 611(c): leading questions on direct.", favorsDefense: false };
      return t;
    }
    if (best && best.n >= 2) {
      t.lines.push({ ...W, text: `...Yes. ${best.f}` });
      t.factsRevealed = [{ witnessId: w.id, fact: best.f }];
      t.jurorReactions = react(s, text + " inconsistent", 4);
      t.scoreEvents = [{ label: cross ? "Effective impeachment" : "Strong direct", points: 4 }];
    } else {
      t.lines.push({ ...W, text: cross ? "I don't recall exactly. I told the police what I saw." : "Yes, that's right." });
      t.jurorReactions = react(s, text, 0);
    }
    return t;
  }
  t.jurorReactions = react(s, text, s.phase.includes("closing") ? 3 : 1);
  t.scoreEvents = text.length > 250 ? [{ label: "Thorough argument", points: 3 }] : [];
  if (s.phase === "rule29") {
    t.lines.push({ ...J, text: "Viewing the evidence in the light most favorable to the State, the motion is denied." });
    t.ruling = { on: "Motion for judgment of acquittal", result: "denied", reason: "A rational juror could find each element.", favorsDefense: false };
  } else {
    t.lines.push({ ...J, text: "Thank you, counsel." });
  }
  return t;
}

/** Offline appellate panel: affirms unless the brief plausibly attacks an element with nothing behind it in the record. */
export function mockAppeal(c: CaseFile, s: TrialState, brief: string): AppealOpinion {
  const d = s.deliberation!;
  const convicted = d.verdicts.filter((v) => v.result === "guilty" || v.result === "guilty-lesser");
  const text = brief.toLowerCase();
  const sufficiency = /insufficien|jackson v\. virginia|no rational|constructive possession|equal access/.test(text);
  const heads = brief.split(/\n/).filter((l) => /^enumeration|^argument|^issue|^point\s+[ivx\d]/i.test(l.trim())).slice(0, 6);
  return {
    court: `Court of Appeals (${c.jurisdiction})`,
    summary: sufficiency && s.revealed.length >= 2
      ? "The convictions are reversed for insufficient evidence on this record, and retrial is barred."
      : "The convictions are affirmed. The evidence, viewed in the light most favorable to the verdict, permitted a rational juror to find each element.",
    enumerations: (heads.length ? heads : ["Enumeration of Error I"]).map((h) => ({
      title: h.trim(),
      ruling: sufficiency && s.revealed.length >= 2 ? "sustained" as const : "overruled" as const,
      reasoning: sufficiency && s.revealed.length >= 2
        ? `The defense exposed ${s.revealed.length} facts on cross that the State never answered, leaving the contested element without rational support.`
        : "Appellant asks this court to reweigh the evidence. That is the jury's province, not ours.",
    })),
    counts: convicted.map((v) => ({ chargeId: v.chargeId, disposition: sufficiency && s.revealed.length >= 2 ? "reversed-insufficient" as const : "affirmed" as const, reason: "Offline panel." })),
    plainError: null,
    critique: ["Offline mock panel — add an OpenRouter key for a real appellate opinion.", `The brief raised ${heads.length || 1} enumeration(s).`],
    briefGrade: brief.length > 1500 ? "B" : "C",
  };
}

export function mockDeliberation(c: CaseFile, s: TrialState): Deliberation {
  const jury = seated(s.jurors);
  const ng = jury.filter((j) => j.lean >= 50).length;
  const result = ng >= 10 ? "not-guilty" : ng <= 2 ? "guilty" : "hung";
  return {
    transcript: jury.slice(0, 8).map((j, i) => ({
      seat: i + 1,
      name: j.name,
      text: j.lean >= 50 ? "I just don't think they proved it. There's too much doubt." : "The evidence points one way. I'm voting guilty.",
    })),
    verdicts: c.charges.map((ch) => ({
      chargeId: ch.id,
      result: s.dismissedCounts.includes(ch.id) ? "not-guilty" : result,
      lesser: null,
      votesNotGuilty: s.dismissedCounts.includes(ch.id) ? 12 : result === "not-guilty" ? 12 : result === "guilty" ? 0 : ng,
    })),
    foreperson: jury[0]?.name ?? "Foreperson",
    keyFactor: s.revealed.length ? `The defense exposed: ${s.revealed[0].fact}` : "The State's witnesses went largely unchallenged.",
    critique: [
      `You exposed ${s.revealed.length} hidden fact(s) on cross.`,
      `${s.objections.sustained} of ${s.objections.made} objections sustained.`,
      "Offline mock mode — add an OpenRouter key for full AI deliberation.",
    ],
  };
}

export function mockPhaseNote(s: TrialState) { return phaseInfo(s.phase).label; }
