// Deterministic venire generation so a case always seats a reproducible panel for a given seed.

export interface Juror {
  id: number; // venire number 1..18
  name: string;
  age: number;
  occupation: string;
  background: string;
  /** Hidden until revealed in voir dire. */
  bias: string;
  /** How the bias moves them: negative = pro-prosecution. */
  biasShift: number;
  revealed: boolean;
  /** 0 = certain guilty, 100 = certain not guilty. */
  lean: number;
  lastReason: string;
  lastDelta: number;
  status: "venire" | "seated" | "struck-defense" | "struck-prosecution" | "excused-cause" | "alternate";
}

const FIRST = ["Maria", "James", "Denise", "Tyrone", "Linda", "Carlos", "Karen", "DeShawn", "Patricia", "Hector", "Nancy", "Andre", "Susan", "Wei", "Robert", "Aisha", "Michael", "Rosa", "Gary", "Imani", "Frank", "Priya", "Dale", "Latoya", "Steven", "Ngozi", "Brian", "Elena"];
const LAST = ["Alvarez", "Brooks", "Chen", "Dawson", "Ellis", "Foster", "Gutierrez", "Hayes", "Ibrahim", "Jensen", "Kowalski", "Lopez", "Morales", "Nguyen", "Okafor", "Park", "Quinn", "Reyes", "Sullivan", "Thompson", "Underwood", "Vasquez", "Washington", "Young"];
const JOBS = ["retired police sergeant", "ER nurse", "public school teacher", "truck driver", "software engineer", "pastor", "bus mechanic", "small-business owner", "social worker", "retired Marine", "accountant", "barista and grad student", "construction foreman", "insurance claims adjuster", "hospital janitor", "real-estate agent", "corrections officer's spouse", "community organizer", "bank teller", "UPS driver"];
const BIASES: Array<[string, number]> = [
  ["Believes police officers rarely lie under oath.", -12],
  ["Had a car broken into last year and wants neighborhoods 'cleaned up'.", -8],
  ["Brother served time on a wrongful conviction that was later overturned.", 14],
  ["Thinks rap music glorifies violence and says so openly.", -10],
  ["Watches forensic crime shows and expects DNA in every case.", 6],
  ["Was stopped and frisked multiple times as a teenager.", 12],
  ["Cousin was killed in a gang shooting.", -14],
  ["Distrusts informants who get deals: 'everyone's lying to save themselves'.", 10],
  ["Believes 'if you're arrested, you probably did something'.", -15],
  ["Served on a jury that acquitted; felt proud of it.", 8],
  ["Strong gun-rights views; believes in self-defense.", 6],
  ["Works with at-risk youth and has seen kids pressured into gangs.", 7],
  ["No strong views; wants to 'just follow the evidence'.", 0],
  ["Neighbor is a prosecutor; they talk about cases at barbecues.", -9],
  ["Skeptical of expert witnesses who are 'paid to say things'.", 5],
  ["Very religious; believes in forgiveness but also accountability.", -2],
];

function rng(seed: number) {
  let s = seed >>> 0 || 1;
  return () => {
    s ^= s << 13; s ^= s >>> 17; s ^= s << 5;
    return ((s >>> 0) % 100000) / 100000;
  };
}

export function hashString(str: string): number {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>> 0;
}

export function generateVenire(seed: number, startingLean: number, size = 18): Juror[] {
  const r = rng(seed);
  const pick = <T,>(arr: T[]) => arr[Math.floor(r() * arr.length)];
  const used = new Set<string>();
  const jurors: Juror[] = [];
  for (let i = 1; i <= size; i++) {
    let name = "";
    do name = `${pick(FIRST)} ${pick(LAST)}`; while (used.has(name));
    used.add(name);
    const [bias, biasShift] = pick(BIASES);
    const age = 22 + Math.floor(r() * 50);
    const noise = Math.round((r() - 0.5) * 10);
    jurors.push({
      id: i,
      name,
      age,
      occupation: pick(JOBS),
      background: `${age}-year-old ${pick(["lifelong resident", "moved here ten years ago", "grew up across town", "recently relocated"])}, ${pick(["married with kids", "single", "divorced", "widowed", "caring for a parent"])}.`,
      bias,
      biasShift,
      revealed: false,
      lean: clampLean(startingLean + biasShift + noise),
      lastReason: "",
      lastDelta: 0,
      status: "venire",
    });
  }
  return jurors;
}

export const clampLean = (n: number) => Math.max(2, Math.min(98, Math.round(n)));

export const seated = (jurors: Juror[]) => jurors.filter((j) => j.status === "seated");

/** Average lean of the seated jury (the "reasonable doubt" gauge). */
export function doubtLevel(jurors: Juror[]): number {
  const s = seated(jurors);
  if (!s.length) return 50;
  return Math.round(s.reduce((a, j) => a + j.lean, 0) / s.length);
}

export function straw(jurors: Juror[]) {
  const s = seated(jurors);
  return {
    notGuilty: s.filter((j) => j.lean >= 60).length,
    guilty: s.filter((j) => j.lean <= 40).length,
    undecided: s.filter((j) => j.lean > 40 && j.lean < 60).length,
  };
}

/** Prosecutor exercises strikes on the most defense-leaning panelists. */
export function prosecutionStrikes(jurors: Juror[], count: number): number[] {
  return jurors
    .filter((j) => j.status === "venire")
    .sort((a, b) => b.lean - a.lean)
    .slice(0, count)
    .map((j) => j.id);
}

/** Seat the first 12 remaining panelists in venire order; next 2 become alternates. */
export function seatJury(jurors: Juror[]): Juror[] {
  let seatedCount = 0;
  let alternates = 0;
  return jurors.map((j) => {
    if (j.status !== "venire") return j;
    if (seatedCount < 12) { seatedCount++; return { ...j, status: "seated" }; }
    if (alternates < 2) { alternates++; return { ...j, status: "alternate" }; }
    return j;
  });
}
