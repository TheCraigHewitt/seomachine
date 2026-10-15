"use client";
// Text-to-speech per courtroom role, with distinct pitch/rate and voice where available.

type Role = "judge" | "prosecutor" | "witness" | "clerk" | "bailiff" | "juror" | "defendant" | "defense" | "system";

const PROFILE: Record<Role, { pitch: number; rate: number; voiceIndex: number }> = {
  judge: { pitch: 0.8, rate: 0.95, voiceIndex: 0 },
  prosecutor: { pitch: 1.05, rate: 1.08, voiceIndex: 1 },
  witness: { pitch: 1.15, rate: 1.0, voiceIndex: 2 },
  clerk: { pitch: 1.2, rate: 1.1, voiceIndex: 3 },
  bailiff: { pitch: 0.9, rate: 1.0, voiceIndex: 0 },
  juror: { pitch: 1.1, rate: 1.0, voiceIndex: 4 },
  defendant: { pitch: 1.0, rate: 0.95, voiceIndex: 2 },
  defense: { pitch: 1, rate: 1, voiceIndex: 0 },
  system: { pitch: 1, rate: 1, voiceIndex: 0 },
};

let cached: SpeechSynthesisVoice[] = [];
function voices(): SpeechSynthesisVoice[] {
  if (typeof window === "undefined" || !window.speechSynthesis) return [];
  if (!cached.length) cached = window.speechSynthesis.getVoices().filter((v) => v.lang.startsWith("en"));
  return cached;
}
if (typeof window !== "undefined" && window.speechSynthesis) {
  window.speechSynthesis.onvoiceschanged = () => { cached = []; voices(); };
}

/** Speaks lines sequentially; resolves when finished or cancelled. */
export function speakLines(lines: Array<{ speaker: string; text: string }>, enabled: boolean): Promise<void> {
  if (!enabled || typeof window === "undefined" || !window.speechSynthesis) return Promise.resolve();
  const synth = window.speechSynthesis;
  const vs = voices();
  return new Promise((resolve) => {
    let remaining = lines.length;
    if (!remaining) return resolve();
    lines.forEach((l) => {
      const p = PROFILE[(l.speaker as Role) in PROFILE ? (l.speaker as Role) : "witness"];
      const u = new SpeechSynthesisUtterance(l.text);
      u.pitch = p.pitch;
      u.rate = p.rate;
      if (vs.length) u.voice = vs[p.voiceIndex % vs.length];
      u.onend = u.onerror = () => { if (--remaining === 0) resolve(); };
      synth.speak(u);
    });
  });
}

let generation = 0;

/**
 * Plays lines one at a time and reports which line is live, so the courtroom scene can animate the
 * speaker. With voices on, timing follows speech synthesis. With voices off, each line stays up
 * long enough to read. Cancelled by silence().
 */
export function playLines(
  lines: Array<{ speaker: string; text: string }>,
  enabled: boolean,
  onLine: (index: number | null) => void,
): Promise<void> {
  const gen = ++generation;
  const alive = () => gen === generation;
  const synth = typeof window !== "undefined" ? window.speechSynthesis : undefined;
  if (!lines.length) { onLine(null); return Promise.resolve(); }
  if (!enabled || !synth) {
    return new Promise((resolve) => {
      let i = 0;
      const step = () => {
        if (!alive()) return resolve();
        if (i >= lines.length) { onLine(null); return resolve(); }
        onLine(i);
        const ms = Math.min(5200, 900 + lines[i].text.length * 34);
        i++;
        window.setTimeout(step, ms);
      };
      step();
    });
  }
  const vs = voices();
  return new Promise((resolve) => {
    let remaining = lines.length;
    lines.forEach((l, i) => {
      const p = PROFILE[(l.speaker as Role) in PROFILE ? (l.speaker as Role) : "witness"];
      const u = new SpeechSynthesisUtterance(l.text);
      u.pitch = p.pitch;
      u.rate = p.rate;
      if (vs.length) u.voice = vs[p.voiceIndex % vs.length];
      u.onstart = () => { if (alive()) onLine(i); };
      u.onend = u.onerror = () => { if (--remaining === 0) { if (alive()) onLine(null); resolve(); } };
      synth.speak(u);
    });
  });
}

export function silence() {
  generation++;
  if (typeof window !== "undefined") window.speechSynthesis?.cancel();
}
