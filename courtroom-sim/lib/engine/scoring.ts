// Per-trial grade and career progression.
import type { Deliberation } from "./schema";
import type { TrialState } from "./state";

export type Outcome = "acquittal" | "partial" | "hung" | "conviction";

export function outcomeOf(d: Deliberation, dismissed: string[]): Outcome {
  const results = d.verdicts.map((v) => (dismissed.includes(v.chargeId) ? "not-guilty" : v.result));
  if (results.every((r) => r === "not-guilty")) return "acquittal";
  if (results.every((r) => r === "guilty")) return "conviction";
  if (results.some((r) => r === "hung") && !results.includes("guilty")) return "hung";
  return "partial";
}

const OUTCOME_POINTS: Record<Outcome, number> = { acquittal: 40, hung: 20, partial: 12, conviction: 0 };

export function trialPoints(s: TrialState, outcome: Outcome): number {
  const advocacy = s.score.reduce((a, e) => a + e.points, 0);
  return Math.max(0, advocacy + OUTCOME_POINTS[outcome]);
}

export function grade(points: number, outcome: Outcome): string {
  const bonus = outcome === "acquittal" ? 10 : outcome === "conviction" ? -10 : 0;
  const p = points + bonus;
  if (p >= 90) return "A+";
  if (p >= 75) return "A";
  if (p >= 60) return "B";
  if (p >= 45) return "C";
  if (p >= 30) return "D";
  return "F";
}

export const RANKS = [
  { name: "Public Defender", min: 0 },
  { name: "Trial Associate", min: 100 },
  { name: "Senior Trial Counsel", min: 250 },
  { name: "Partner", min: 450 },
  { name: "Legend of the Bar", min: 750 },
];

export function rankFor(points: number) {
  let r = RANKS[0];
  for (const x of RANKS) if (points >= x.min) r = x;
  const next = RANKS[RANKS.indexOf(r) + 1];
  return { ...r, next };
}

/** Tier 2 opens after 1 acquittal, tier 3 after 3. Practice mode unlocks everything. */
export function tierUnlocked(tier: number, wins: number, practice: boolean): boolean {
  if (practice || tier === 1) return true;
  return tier === 2 ? wins >= 1 : wins >= 3;
}
