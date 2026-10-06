// Type-safe contract between the model and the game. The model must return JSON matching
// these schemas; the server validates with zod and clamps anything out of range.
import { z } from "zod";

export const SPEAKERS = ["judge", "prosecutor", "witness", "clerk", "bailiff", "juror", "defendant"] as const;

export const CourtLine = z.object({
  speaker: z.enum(SPEAKERS),
  name: z.string().describe("Display name, e.g. 'Judge Harlan' or 'Det. Ruiz'"),
  text: z.string(),
});

export const Ruling = z.object({
  on: z.string().describe("What was ruled on: objection ground, motion name, bail, challenge"),
  result: z.enum(["sustained", "overruled", "granted", "denied", "granted-in-part"]),
  reason: z.string().describe("One sentence legal basis, citing the rule"),
  favorsDefense: z.boolean(),
});

export const CourtTurn = z.object({
  lines: z.array(CourtLine).describe("Dialogue in order. 1-6 lines."),
  ruling: Ruling.nullable(),
  prosecutorObjected: z.boolean().describe("True if the prosecutor objected to the defense this turn"),
  evidenceAdmitted: z.array(z.string()).describe("Evidence ids admitted this turn"),
  evidenceExcluded: z.array(z.string()).describe("Evidence ids excluded/suppressed this turn"),
  factsRevealed: z
    .array(z.object({ witnessId: z.string(), fact: z.string() }))
    .describe("Hidden facts or prior-statement contradictions the defense exposed this turn"),
  jurorReactions: z
    .array(z.object({ seat: z.number().int(), delta: z.number().int(), reason: z.string() }))
    .describe("Seated juror lean changes, -10..10; positive = toward NOT GUILTY. Empty when the jury is absent."),
  scoreEvents: z
    .array(z.object({ label: z.string(), points: z.number().int() }))
    .describe("Advocacy feedback, -10..10 each, e.g. 'Effective impeachment' +6, 'Leading on direct' -2"),
  jurorsRevealed: z.array(z.number().int()).describe("Venire numbers whose hidden bias came out in voir dire"),
  contemptWarning: z.boolean(),
  witnessExcused: z.boolean().describe("True when the examination of the current witness is finished"),
  countsDismissed: z.array(z.string()).describe("Charge ids dismissed or acquitted by the judge (Rule 29)"),
});
export type CourtTurn = z.infer<typeof CourtTurn>;
export type CourtLineT = z.infer<typeof CourtLine>;
export type RulingT = z.infer<typeof Ruling>;

export const Deliberation = z.object({
  transcript: z
    .array(z.object({ seat: z.number().int(), name: z.string(), text: z.string() }))
    .describe("8-14 lines of jury-room debate"),
  verdicts: z.array(
    z.object({
      chargeId: z.string(),
      result: z.enum(["guilty", "not-guilty", "hung", "guilty-lesser"]),
      lesser: z.string().nullable(),
      votesNotGuilty: z.number().int(),
    }),
  ),
  foreperson: z.string(),
  keyFactor: z.string().describe("The single thing that most decided the verdict"),
  critique: z.array(z.string()).describe("3-5 coaching notes on the defense's performance"),
});
export type Deliberation = z.infer<typeof Deliberation>;

// ---- Lenient coercion ------------------------------------------------------------------
// Models (especially small fallback ones) often drop empty fields, capitalise enum values,
// or send numbers as strings. Coerce toward the schema before validating so a nearly-right
// reply is accepted instead of discarded.

type Obj = Record<string, unknown>;
const isObj = (v: unknown): v is Obj => typeof v === "object" && v !== null && !Array.isArray(v);
const arr = (v: unknown): unknown[] => (Array.isArray(v) ? v : v == null ? [] : [v]);
const str = (v: unknown) => (v == null ? "" : String(v));
const num = (v: unknown) => { const n = Number(v); return Number.isFinite(n) ? Math.round(n) : 0; };
const bool = (v: unknown) => v === true || v === "true" || v === 1;
const pick = <T extends string>(v: unknown, allowed: readonly T[], alias: Record<string, T>, fallback: T): T => {
  const k = str(v).toLowerCase().trim().replace(/[\s_]+/g, "-");
  return (allowed as readonly string[]).includes(k) ? (k as T) : alias[k] ?? fallback;
};

const SPEAKER_ALIAS: Record<string, (typeof SPEAKERS)[number]> = {
  court: "judge", "the-court": "judge", prosecution: "prosecutor", state: "prosecutor", ada: "prosecutor",
  da: "prosecutor", government: "prosecutor", "prospective-juror": "juror", panelist: "juror", accused: "defendant",
};
const RESULTS = ["sustained", "overruled", "granted", "denied", "granted-in-part"] as const;

/** Unwraps `{ "court_turn": {...} }`-style envelopes some models add. */
function unwrap(raw: unknown, key: string): Obj {
  if (!isObj(raw)) return {};
  if (key in raw || Object.keys(raw).length !== 1) return raw;
  const only = Object.values(raw)[0];
  return isObj(only) ? only : raw;
}

export function coerceTurn(raw: unknown): unknown {
  const r = unwrap(raw, "lines");
  const ruling = isObj(r.ruling) && r.ruling.result
    ? {
        on: str(r.ruling.on) || "Ruling",
        result: pick(r.ruling.result, RESULTS, { sustain: "sustained", overrule: "overruled", grant: "granted", deny: "denied" }, "overruled"),
        reason: str(r.ruling.reason),
        favorsDefense: bool(r.ruling.favorsDefense),
      }
    : null;
  return {
    lines: arr(r.lines).filter(isObj).map((l) => ({
      speaker: pick(l.speaker, SPEAKERS, SPEAKER_ALIAS, "witness"),
      name: str(l.name) || str(l.speaker),
      text: str(l.text ?? l.dialogue ?? l.content),
    })),
    ruling,
    prosecutorObjected: bool(r.prosecutorObjected),
    evidenceAdmitted: arr(r.evidenceAdmitted).map(str),
    evidenceExcluded: arr(r.evidenceExcluded).map(str),
    factsRevealed: arr(r.factsRevealed).filter(isObj).map((f) => ({ witnessId: str(f.witnessId), fact: str(f.fact) })).filter((f) => f.fact),
    jurorReactions: arr(r.jurorReactions).filter(isObj).map((j) => ({ seat: num(j.seat), delta: num(j.delta), reason: str(j.reason) })),
    scoreEvents: arr(r.scoreEvents).filter(isObj).map((e) => ({ label: str(e.label), points: num(e.points) })).filter((e) => e.label),
    jurorsRevealed: arr(r.jurorsRevealed).map(num).filter((n) => n > 0),
    contemptWarning: bool(r.contemptWarning),
    witnessExcused: bool(r.witnessExcused),
    countsDismissed: arr(r.countsDismissed).map(str),
  };
}

const VERDICTS = ["guilty", "not-guilty", "hung", "guilty-lesser"] as const;

export function coerceDeliberation(raw: unknown): unknown {
  const r = unwrap(raw, "verdicts");
  return {
    transcript: arr(r.transcript).filter(isObj).map((l) => ({ seat: num(l.seat), name: str(l.name), text: str(l.text) })),
    verdicts: arr(r.verdicts).filter(isObj).map((v) => {
      const result = pick(v.result, VERDICTS, { "not guilty": "not-guilty", notguilty: "not-guilty", acquitted: "not-guilty", "hung-jury": "hung", mistrial: "hung", lesser: "guilty-lesser" }, "hung");
      const polled = Math.max(0, Math.min(12, num(v.votesNotGuilty)));
      // A verdict is unanimous by definition; only a hung count has a split poll. Models sometimes
      // report the first ballot next to the final verdict, which would put an 8-4 "guilty" on the record.
      const votesNotGuilty = result === "hung" ? polled : result === "not-guilty" ? 12 : 0;
      return { chargeId: str(v.chargeId), result, lesser: v.lesser == null || v.lesser === "" ? null : str(v.lesser), votesNotGuilty };
    }),
    foreperson: str(r.foreperson) || "Foreperson",
    keyFactor: str(r.keyFactor),
    critique: arr(r.critique).map(str).filter(Boolean),
  };
}

const clampInt = (n: number, lo: number, hi: number) => Math.max(lo, Math.min(hi, Math.round(n)));

/** Normalises model output so a misbehaving model can't break game balance. */
export function sanitizeTurn(t: CourtTurn, opts: { juryPresent: boolean; validEvidence: Set<string>; validCharges: Set<string> }): CourtTurn {
  return {
    ...t,
    lines: t.lines.slice(0, 8).filter((l) => l.text.trim()),
    evidenceAdmitted: t.evidenceAdmitted.filter((id) => opts.validEvidence.has(id)),
    evidenceExcluded: t.evidenceExcluded.filter((id) => opts.validEvidence.has(id)),
    jurorReactions: opts.juryPresent
      ? t.jurorReactions
          .filter((r) => r.seat >= 1 && r.seat <= 12)
          .map((r) => ({ ...r, delta: clampInt(r.delta, -10, 10) }))
      : [],
    scoreEvents: t.scoreEvents.slice(0, 4).map((e) => ({ ...e, points: clampInt(e.points, -10, 10) })),
    factsRevealed: t.factsRevealed.slice(0, 3),
    countsDismissed: t.countsDismissed.filter((id) => opts.validCharges.has(id)),
  };
}
