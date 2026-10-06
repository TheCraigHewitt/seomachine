// Trial state machine. Each phase says who speaks first and what the player can do.

export type PhaseId =
  | "arraignment"
  | "pretrial"
  | "voir_dire"
  | "prosecution_opening"
  | "defense_opening"
  | "prosecution_case"
  | "rule29"
  | "defense_case"
  | "prosecution_closing"
  | "defense_closing"
  | "instructions"
  | "deliberation"
  | "verdict";

export interface PhaseInfo {
  id: PhaseId;
  label: string;
  short: string;
  /** The AI speaks when the phase opens (player presses "Proceed"). */
  aiOpens: boolean;
  /** The player is expected to speak in this phase. */
  playerSpeaks: boolean;
  /** Guidance shown to the player. */
  hint: string;
  /** What the model is told is happening. */
  direction: string;
}

export const PHASES: PhaseInfo[] = [
  {
    id: "arraignment",
    label: "Arraignment & Bail",
    short: "Arraign",
    aiOpens: true,
    playerSpeaks: true,
    hint: "Enter your client's plea and argue bail: ties to the community, flight risk, dangerousness.",
    direction:
      "Arraignment. The clerk calls the case, the judge reads the charges and asks for a plea. After the plea the prosecutor argues for remand or high bail; the defense argues for release. The judge rules on bail.",
  },
  {
    id: "pretrial",
    label: "Pretrial Motions",
    short: "Motions",
    aiOpens: false,
    playerSpeaks: true,
    hint: "Pick a motion and argue it. Cite the doctrine (Miranda, Fourth Amendment, 404(b), 403, Daubert, Crawford). Granted motions keep evidence away from the jury.",
    direction:
      "Pretrial motion hearing, outside the jury's presence. The defense argues a motion; the prosecutor responds; the judge rules GRANTED or DENIED with a legal reason. Base the ruling on the motion's merit and the quality of the defense argument. If granted, list the excluded evidence ids in evidenceExcluded.",
  },
  {
    id: "voir_dire",
    label: "Jury Selection",
    short: "Voir Dire",
    aiOpens: true,
    playerSpeaks: true,
    hint: "Question the panel to expose bias. Strike jurors with peremptories, or argue a for-cause challenge.",
    direction:
      "Voir dire. The defense questions prospective jurors (panel seats listed). Prospective jurors answer in character, honestly revealing their biases when asked well. If the defense argues a for-cause challenge, the judge rules SUSTAINED or OVERRULED.",
  },
  {
    id: "prosecution_opening",
    label: "Prosecution Opening",
    short: "Opening (P)",
    aiOpens: true,
    playerSpeaks: false,
    hint: "Listen. Object if the prosecutor argues instead of previewing evidence, or mentions excluded evidence.",
    direction:
      "The prosecutor delivers an opening statement (4-7 sentences) previewing the evidence. It must not mention evidence excluded pretrial. Jurors shift toward guilt modestly.",
  },
  {
    id: "defense_opening",
    label: "Defense Opening",
    short: "Opening (D)",
    aiOpens: false,
    playerSpeaks: true,
    hint: "Give your opening. Tell the jury your theory of the case and what the evidence will NOT show. Don't argue yet.",
    direction:
      "The defense gives an opening statement. The prosecutor may object if it becomes argument. React with juror deltas reflecting how persuasive it was.",
  },
  {
    id: "prosecution_case",
    label: "State's Case-in-Chief",
    short: "State's Case",
    aiOpens: true,
    playerSpeaks: true,
    hint: "The prosecutor examines each witness. Object to improper questions, then cross-examine. Short leading questions, one fact at a time. Impeach with prior statements.",
    direction:
      "Prosecution case-in-chief. The prosecutor conducts direct examination of the current witness (a few Q&A exchanges per turn). When the defense cross-examines, the witness answers the defense's question in character. Witnesses reveal hiddenFacts ONLY when the defense asks a question that actually targets them; they are confronted with priorStatements only when the defense uses them.",
  },
  {
    id: "rule29",
    label: "Motion for Acquittal",
    short: "Rule 29",
    aiOpens: false,
    playerSpeaks: true,
    hint: "The State rests. Argue that no rational juror could find each element proven, count by count. Rarely granted, but it preserves the issue.",
    direction:
      "Motion for judgment of acquittal outside the jury's presence. The judge views the evidence in the light most favorable to the State and rules GRANTED (per count) or DENIED. Granting is rare and requires a genuinely missing element.",
  },
  {
    id: "defense_case",
    label: "Defense Case",
    short: "Defense Case",
    aiOpens: false,
    playerSpeaks: true,
    hint: "Call your witnesses and do direct (open-ended questions, not leading). The prosecutor will cross. Decide whether your client testifies. Or rest.",
    direction:
      "Defense case. The defense conducts direct examination of the current defense witness, who answers helpfully but truthfully per their facts. The prosecutor objects to leading questions. When the defense passes the witness, the prosecutor cross-examines aggressively.",
  },
  {
    id: "prosecution_closing",
    label: "Prosecution Closing",
    short: "Closing (P)",
    aiOpens: true,
    playerSpeaks: false,
    hint: "Listen. Object to burden-shifting, vouching, or appeals to passion.",
    direction:
      "The prosecutor delivers closing argument (5-8 sentences) tying the admitted evidence to each element. Only admitted evidence and testimony from the transcript may be referenced.",
  },
  {
    id: "defense_closing",
    label: "Defense Closing",
    short: "Closing (D)",
    aiOpens: false,
    playerSpeaks: true,
    hint: "Your closing. Hammer reasonable doubt, the element they can't prove, and every impeachment you landed.",
    direction:
      "The defense gives closing argument. Jurors react strongly (deltas up to ±10) based on how well it uses the actual trial record. The prosecutor may object to arguing facts not in evidence.",
  },
  {
    id: "instructions",
    label: "Jury Instructions",
    short: "Charge",
    aiOpens: true,
    playerSpeaks: false,
    hint: "The judge charges the jury: presumption of innocence, reasonable doubt, and the elements of each count.",
    direction:
      "The judge instructs the jury: presumption of innocence, burden of proof beyond a reasonable doubt, the elements of each charge and any lesser-included offenses. No juror deltas.",
  },
  {
    id: "deliberation",
    label: "Deliberation",
    short: "Deliberation",
    aiOpens: true,
    playerSpeaks: false,
    hint: "The jury is out.",
    direction: "",
  },
  {
    id: "verdict",
    label: "Verdict",
    short: "Verdict",
    aiOpens: false,
    playerSpeaks: false,
    hint: "",
    direction: "",
  },
];

export const phaseIndex = (id: PhaseId) => PHASES.findIndex((p) => p.id === id);
export const phaseInfo = (id: PhaseId): PhaseInfo => PHASES[phaseIndex(id)];

export function nextPhase(id: PhaseId): PhaseId {
  const i = phaseIndex(id);
  return PHASES[Math.min(i + 1, PHASES.length - 1)].id;
}

/** Phases heard outside the jury's presence — juror deltas are ignored there. */
export const JURY_ABSENT: PhaseId[] = ["arraignment", "pretrial", "voir_dire", "rule29", "instructions"];
