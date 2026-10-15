// Schema for a case file in data/cases/*.json.
// Every case is fictionalized: names are invented, facts are adapted from a real prosecution
// referenced in `basedOn` for the post-trial debrief.

export type Tier = 1 | 2 | 3;
export type Side = "prosecution" | "defense";
export type JudgeTemperament = "fair" | "strict" | "pro-prosecution" | "defense-friendly";

export interface Charge {
  id: string;
  name: string; // e.g. "Murder in the First Degree"
  statute: string; // e.g. "Cal. Penal Code § 187(a)"
  elements: string[]; // what the state must prove beyond a reasonable doubt
  maxSentence: string;
  lesserIncluded?: string[];
}

export interface Evidence {
  id: string;
  name: string;
  type: "physical" | "forensic" | "digital" | "documentary" | "testimonial" | "video" | "statement";
  offeredBy: Side;
  description: string;
  weakness: string; // what a sharp defense lawyer can attack
  admissibilityIssue?: string; // e.g. "404(b) character evidence", "Miranda", "chain of custody"
  suppressible?: boolean; // can a pretrial motion exclude it
}

export interface Witness {
  id: string;
  name: string;
  role: string; // "Lead Detective", "Eyewitness", "Cooperating co-defendant", ...
  side: Side;
  demeanor: string; // how the AI should play them
  publicTestimony: string; // what they say on direct
  hiddenFacts: string[]; // only revealed if the defense asks the right questions
  priorStatements: string[]; // earlier statements usable for impeachment
  credibilityIssues: string[]; // bias, deals, record, vision, intoxication...
}

export interface PretrialMotion {
  id: string;
  name: string; // "Motion to Suppress Custodial Statement"
  basis: string;
  targets?: string[]; // evidence ids excluded if granted
  merit: number; // 0-100 baseline likelihood the judge grants it with a good argument
}

export interface CaseFile {
  id: string; // kebab-case, matches filename
  title: string; // "State v. Marcus Doe"
  tier: Tier;
  category: "gang" | "rico" | "murder" | "self-defense" | "wrongful-conviction";
  tagline: string; // one sentence for the docket card
  jurisdiction: string;
  courtName: string;
  basedOn: {
    name: string; // real case name
    year: string;
    summary: string; // 2-4 sentences on the real case
    realOutcome: string;
    keyLessons: string[];
    sources: string[]; // URLs
  };
  defendant: {
    name: string;
    age: number;
    background: string;
    privateAccount: string; // what the client tells you in confidence
    priors: string;
    testifyRisk: string; // what happens if they take the stand
  };
  judge: { name: string; temperament: JudgeTemperament; bio: string };
  prosecutor: { name: string; style: string };
  caseSummary: string; // police report / charging narrative, 1-3 paragraphs
  prosecutionTheory: string;
  charges: Charge[];
  evidence: Evidence[];
  witnesses: Witness[];
  pretrialMotions: PretrialMotion[];
  defenseAngles: string[]; // hints unlocked on the case file screen
  startingLean: number; // 0-100 baseline jury lean toward NOT GUILTY (e.g. 35 = hard case)
}
