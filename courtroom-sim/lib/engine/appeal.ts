// Appeals: after a conviction the player files a brief and an appellate panel rules on the trial record.
import { z } from "zod";
import type { CaseFile } from "./caseTypes";
import type { Deliberation } from "./schema";
import type { TrialState } from "./state";

export const DISPOSITIONS = ["affirmed", "reversed-insufficient", "reversed-error", "vacated"] as const;
export type Disposition = (typeof DISPOSITIONS)[number];

export const AppealOpinion = z.object({
  court: z.string().describe("Name of the reviewing court, e.g. 'Court of Appeals of Georgia'"),
  summary: z.string().describe("2-4 sentence statement of the judgment"),
  enumerations: z.array(
    z.object({
      title: z.string(),
      ruling: z.enum(["sustained", "overruled", "moot"]),
      reasoning: z.string().describe("3-8 sentences applying the standard of review to the record"),
    }),
  ),
  counts: z.array(
    z.object({
      chargeId: z.string(),
      disposition: z.enum(DISPOSITIONS),
      reason: z.string().describe("One sentence"),
    }),
  ),
  plainError: z.string().nullable().describe("A defect the court noticed on its own, or null"),
  critique: z.array(z.string()).describe("3-6 chambers notes on the brief's craft: citations, record cites, structure, argument quality"),
  briefGrade: z.enum(["A+", "A", "B", "C", "D", "F"]),
});
export type AppealOpinion = z.infer<typeof AppealOpinion>;

export interface AppealRecord {
  brief: string;
  opinion: AppealOpinion;
  points: number;
  model: string;
  date: string;
}

/** Lenient coercion in the spirit of coerceTurn: small models capitalise enums and drop fields. */
export function coerceAppeal(raw: unknown): unknown {
  const isObj = (v: unknown): v is Record<string, unknown> => typeof v === "object" && v !== null && !Array.isArray(v);
  const r = (isObj(raw) && !("counts" in raw) && Object.keys(raw).length === 1 && isObj(Object.values(raw)[0]) ? Object.values(raw)[0] : raw) as Record<string, unknown>;
  const arr = (v: unknown): unknown[] => (Array.isArray(v) ? v : v == null ? [] : [v]);
  const str = (v: unknown) => (v == null ? "" : String(v));
  const norm = (v: unknown) => str(v).toLowerCase().trim().replace(/[\s_]+/g, "-");
  const disp = (v: unknown): Disposition => {
    const k = norm(v);
    if ((DISPOSITIONS as readonly string[]).includes(k)) return k as Disposition;
    if (k.startsWith("reversed") && /insuff/.test(k)) return "reversed-insufficient";
    if (k.startsWith("reversed") || k.includes("remand") || k.includes("new-trial")) return "reversed-error";
    if (k.includes("vacat")) return "vacated";
    return "affirmed";
  };
  const grade = (v: unknown) => { const g = str(v).toUpperCase().trim(); return ["A+", "A", "B", "C", "D", "F"].includes(g) ? g : g.startsWith("A") ? "A" : g.startsWith("B") ? "B" : g.startsWith("C") ? "C" : g.startsWith("D") ? "D" : "C"; };
  if (!isObj(r)) return r;
  return {
    court: str(r.court) || "Court of Appeals",
    summary: str(r.summary),
    enumerations: arr(r.enumerations).filter(isObj).map((e) => ({
      title: str(e.title) || "Enumeration of error",
      ruling: (["sustained", "overruled", "moot"].includes(norm(e.ruling)) ? norm(e.ruling) : /sustain|grant|agree/.test(norm(e.ruling)) ? "sustained" : /moot/.test(norm(e.ruling)) ? "moot" : "overruled"),
      reasoning: str(e.reasoning),
    })),
    counts: arr(r.counts).filter(isObj).map((x) => ({ chargeId: str(x.chargeId), disposition: disp(x.disposition), reason: str(x.reason) })),
    plainError: r.plainError == null || str(r.plainError).trim() === "" || /^(none|null|n\/a)$/i.test(str(r.plainError).trim()) ? null : str(r.plainError),
    critique: arr(r.critique).map(str).filter(Boolean),
    briefGrade: grade(r.briefGrade),
  };
}

/** Every convicted count gets a disposition; counts the jury acquitted or hung on are untouched by the appeal. */
export function finalizeAppeal(c: CaseFile, d: Deliberation, o: AppealOpinion): AppealOpinion {
  const convicted = d.verdicts.filter((v) => v.result === "guilty" || v.result === "guilty-lesser").map((v) => v.chargeId);
  const counts = convicted.map((id) => o.counts.find((x) => x.chargeId === id) ?? { chargeId: id, disposition: "affirmed" as const, reason: "The court did not disturb this count." });
  // Reversal of a predicate felony takes a derivative firearm/enhancement count with it when the court said so; otherwise trust the opinion.
  return { ...o, counts, enumerations: o.enumerations.slice(0, 8), critique: o.critique.slice(0, 6) };
}

/** Points for the appeal: reversals are worth a lot; the brief's craft matters too. Server-side so the model can't inflate it. */
export function appealPoints(o: AppealOpinion): number {
  const perCount = o.counts.reduce((a, x) => a + (x.disposition === "reversed-insufficient" ? 18 : x.disposition === "reversed-error" ? 10 : x.disposition === "vacated" ? 8 : 0), 0);
  const craft = { "A+": 12, A: 9, B: 5, C: 2, D: 0, F: -4 }[o.briefGrade] ?? 0;
  return perCount + craft;
}

/**
 * The verdicts as they stand after the appeal. Reversed-for-insufficiency and vacated-with-no-retrial counts
 * become acquittals (jeopardy bars retrial). Reversed-for-error counts go back to "hung" so the retrial machinery
 * can pick them up: the State may try them again.
 */
export function appliedVerdicts(s: TrialState): Deliberation["verdicts"] {
  const d = s.deliberation;
  if (!d) return [];
  const o = s.appeal?.opinion;
  if (!o) return d.verdicts;
  return d.verdicts.map((v) => {
    const x = o.counts.find((k) => k.chargeId === v.chargeId);
    if (!x || x.disposition === "affirmed") return v;
    if (x.disposition === "reversed-insufficient") return { ...v, result: "not-guilty" as const, lesser: null, votesNotGuilty: 12 };
    return { ...v, result: "hung" as const, lesser: null, votesNotGuilty: 6 };
  });
}

/** Where the appeal can be filed: a decided trial with at least one conviction and no appeal yet. */
export function canAppeal(s: TrialState): boolean {
  return s.phase === "verdict" && !!s.deliberation && !s.appeal && s.deliberation.verdicts.some((v) => v.result === "guilty" || v.result === "guilty-lesser");
}

/** A skeleton the player can fill in. Real briefs have this shape. */
export function briefTemplate(c: CaseFile, s: TrialState): string {
  const convicted = (s.deliberation?.verdicts ?? []).filter((v) => v.result === "guilty" || v.result === "guilty-lesser").map((v) => c.charges.find((x) => x.id === v.chargeId)?.name ?? v.chargeId);
  return `BRIEF OF APPELLANT ${c.defendant.name.toUpperCase()}

Introduction
[Which convictions you appeal and why, in one paragraph. Convicted counts: ${convicted.join("; ")}.]

Enumeration of Error I
[State the error. Sufficiency: no rational juror could find element X on this record (Jackson v. Virginia). Trial error: the court erred in admitting/excluding Y, and it was not harmless. Cite what the transcript shows.]

Enumeration of Error II
[...]

Conclusion
[The relief you want for each count: reverse for insufficiency (retrial barred), or reverse and remand for a new trial.]`;
}
