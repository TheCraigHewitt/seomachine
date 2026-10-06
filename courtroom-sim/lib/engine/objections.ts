// Objection grounds and live-mic detection.

export interface ObjectionGround {
  id: string;
  label: string;
  rule: string;
  /** Spoken forms recognised after the word "objection". */
  patterns: RegExp[];
  tip: string;
}

export const GROUNDS: ObjectionGround[] = [
  { id: "hearsay", label: "Hearsay", rule: "FRE 801-802", patterns: [/hear ?say/], tip: "Out-of-court statement offered for its truth." },
  { id: "leading", label: "Leading", rule: "FRE 611(c)", patterns: [/leading/], tip: "Suggests the answer on direct examination." },
  { id: "relevance", label: "Relevance", rule: "FRE 401-402", patterns: [/relevan/, /irrelevant/], tip: "No tendency to make a fact of consequence more or less probable." },
  { id: "speculation", label: "Speculation", rule: "FRE 602", patterns: [/speculat/, /personal knowledge/], tip: "Witness lacks personal knowledge." },
  { id: "foundation", label: "Foundation", rule: "FRE 901", patterns: [/foundation/, /authenticat/], tip: "Exhibit or opinion not properly laid." },
  { id: "asked_answered", label: "Asked & Answered", rule: "FRE 611(a)", patterns: [/asked and answered/, /already answered/], tip: "Repetitive questioning." },
  { id: "argumentative", label: "Argumentative", rule: "FRE 611(a)", patterns: [/argumentative/, /badgering/], tip: "Arguing with the witness instead of asking." },
  { id: "compound", label: "Compound", rule: "FRE 611(a)", patterns: [/compound/], tip: "Two questions in one." },
  { id: "narrative", label: "Narrative", rule: "FRE 611(a)", patterns: [/narrative/], tip: "Calls for a long uninterrupted story." },
  { id: "scope", label: "Beyond Scope", rule: "FRE 611(b)", patterns: [/scope/], tip: "Cross exceeds the subject of direct." },
  { id: "prejudice", label: "Unfair Prejudice", rule: "FRE 403", patterns: [/prejudic/, /403/], tip: "Probative value substantially outweighed by unfair prejudice — gang imagery, lyrics, gruesome photos." },
  { id: "character", label: "Improper Character", rule: "FRE 404(b)", patterns: [/character/, /404/, /prior bad act/, /propensity/], tip: "Other acts offered to show propensity — gang affiliation, priors." },
  { id: "confrontation", label: "Confrontation", rule: "6th Amend. / Crawford", patterns: [/confrontation/, /crawford/], tip: "Testimonial statement of an absent witness." },
  { id: "misstates", label: "Misstates Evidence", rule: "FRE 611(a)", patterns: [/misstat/, /mischaracteriz/, /facts not in evidence/], tip: "Question or argument misstates the record." },
  { id: "vouching", label: "Improper Vouching", rule: "Due Process", patterns: [/vouch/, /burden shift/, /shifting the burden/], tip: "Prosecutor vouches for a witness or shifts the burden to the defense." },
];

const OBJECTION_RE = /\bobjection\b[\s,.:;!-]*(?:your honor[\s,.:;!-]*)?(.*)$/i;

/** Detects "Objection, hearsay" style utterances. Returns null when the speech isn't an objection. */
export function detectObjection(transcript: string): { ground: ObjectionGround | null; raw: string } | null {
  const m = transcript.toLowerCase().match(OBJECTION_RE);
  if (!m) return null;
  const rest = m[1] ?? "";
  const ground = GROUNDS.find((g) => g.patterns.some((p) => p.test(rest))) ?? null;
  return { ground, raw: transcript.trim() };
}
