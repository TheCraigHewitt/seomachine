import type { CaseFile, Witness } from "./caseTypes";

export const DEFENDANT_ID = "defendant";

/** The defendant can take the stand like any defense witness. */
export function defendantAsWitness(c: CaseFile): Witness {
  return {
    id: DEFENDANT_ID,
    name: c.defendant.name,
    role: "Defendant",
    side: "defense",
    demeanor: "Nervous; answers in their own words. Vulnerable to a sharp cross.",
    publicTestimony: c.defendant.privateAccount,
    hiddenFacts: [c.defendant.testifyRisk],
    priorStatements: [],
    credibilityIssues: [c.defendant.priors],
  };
}

export function witnessById(c: CaseFile, id: string | null): Witness | undefined {
  if (!id) return undefined;
  return id === DEFENDANT_ID ? defendantAsWitness(c) : c.witnesses.find((w) => w.id === id);
}

/** What the player's browser receives: hidden facts stay on the server. */
export function publicCase(c: CaseFile): CaseFile {
  return { ...c, witnesses: c.witnesses.map((w) => ({ ...w, hiddenFacts: [] })) };
}

/** "Hon. Deborah L. Nance" / "Judge Nance" → "Deborah L. Nance" so the UI can add its own title. */
export const bareJudge = (c: CaseFile) => c.judge.name.replace(/^((the\s+)?(hon(orable)?\.?|judge)\s+)+/i, "");
