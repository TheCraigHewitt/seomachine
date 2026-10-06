import type { CaseFile } from "@/lib/engine/caseTypes";

export const fixture: CaseFile = {
  id: "state-v-test",
  title: "State v. Test",
  tier: 1,
  category: "gang",
  tagline: "A test case.",
  jurisdiction: "Test County",
  courtName: "Test Superior Court",
  basedOn: { name: "Real v. Case", year: "2000", summary: "s", realOutcome: "o", keyLessons: ["l"], sources: ["https://example.com"] },
  defendant: { name: "Dee Fendant", age: 20, background: "b", privateAccount: "I was at my aunt's house.", priors: "none", testifyRisk: "Admits gang membership on cross." },
  judge: { name: "Harlan", temperament: "fair", bio: "b" },
  prosecutor: { name: "Pross", style: "aggressive" },
  caseSummary: "c",
  prosecutionTheory: "The defendant shot the victim.",
  charges: [
    { id: "murder", name: "Murder", statute: "§ 187", elements: ["killed", "malice"], maxSentence: "life" },
    { id: "gang-enh", name: "Gang Enhancement", statute: "§ 186.22", elements: ["for benefit of gang"], maxSentence: "+10y" },
  ],
  evidence: [
    { id: "lyrics", name: "Rap lyrics", type: "digital", offeredBy: "prosecution", description: "d", weakness: "w", admissibilityIssue: "403", suppressible: true },
    { id: "gun", name: "Gun", type: "physical", offeredBy: "prosecution", description: "d", weakness: "w" },
  ],
  witnesses: [
    {
      id: "eyewitness", name: "Ida Witness", role: "Eyewitness", side: "prosecution", demeanor: "nervous",
      publicTestimony: "I saw him shoot.",
      hiddenFacts: ["She was wearing no glasses and it was dark under a broken streetlight"],
      priorStatements: ["Told police she only saw the shooter from behind"],
      credibilityIssues: ["Paid informant"],
    },
    { id: "det", name: "Det. Ruiz", role: "Lead Detective", side: "prosecution", demeanor: "calm", publicTestimony: "p", hiddenFacts: ["h"], priorStatements: [], credibilityIssues: [] },
    { id: "alibi", name: "Aunt May", role: "Alibi", side: "defense", demeanor: "warm", publicTestimony: "He was with me.", hiddenFacts: [], priorStatements: [], credibilityIssues: [] },
  ],
  pretrialMotions: [{ id: "lyrics-motion", name: "Motion in Limine to Exclude Lyrics", basis: "403", targets: ["lyrics"], merit: 60 }],
  defenseAngles: ["a"],
  startingLean: 45,
};
