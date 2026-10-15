"use client";
// The live courtroom: an SVG scene where whoever is speaking lights up, the jury's mood shows on
// each seat, objections stamp the screen and rulings bang the gavel. Purely presentational.
import type { CaseFile, Witness } from "@/lib/engine/caseTypes";
import { seated, type Juror } from "@/lib/engine/jurors";
import type { TrialState } from "@/lib/engine/state";
import { bareJudge } from "@/lib/engine/witness";

export interface LiveLine { speaker: string; name: string; text: string }
export interface Flash { kind: "objection" | "sustained" | "overruled" | "granted" | "denied" | "verdict"; text: string; key: number }

const W = 960, H = 420;

/** Juror mood colour: red at certain-guilty, amber in the middle, green at certain-not-guilty. */
function moodColor(lean: number) {
  const t = Math.max(0, Math.min(1, lean / 100));
  const r = t < 0.5 ? 208 : Math.round(208 + (95 - 208) * ((t - 0.5) / 0.5));
  const g = t < 0.5 ? Math.round(87 + (182 - 87) * (t / 0.5)) : Math.round(182 + (174 - 182) * ((t - 0.5) / 0.5));
  const b = t < 0.5 ? Math.round(75 + (78 - 75) * (t / 0.5)) : Math.round(78 + (132 - 78) * ((t - 0.5) / 0.5));
  return `rgb(${r},${g},${b})`;
}

function Figure({ x, y, scale = 1, skin = "#c9a27a", suit = "#2b2b33", hair = "#2a1d14", speaking, label, sub, robe, delta }: {
  x: number; y: number; scale?: number; skin?: string; suit?: string; hair?: string; speaking?: boolean; label?: string; sub?: string; robe?: boolean; delta?: number;
}) {
  return (
    <g transform={`translate(${x} ${y}) scale(${scale})`} className={speaking ? "ct-speaking" : undefined}>
      {speaking && <ellipse cx={0} cy={22} rx={34} ry={40} fill="none" stroke="#c9a45c" strokeWidth={2.5} className="ct-ring" />}
      {/* shoulders / body */}
      <path d={robe ? "M-30 58 C-30 30 -14 22 0 22 C14 22 30 30 30 58 Z" : "M-24 58 C-24 34 -12 26 0 26 C12 26 24 34 24 58 Z"} fill={suit} />
      {!robe && <path d="M-6 27 L0 40 L6 27 Z" fill="#e8e0d0" />}
      {/* head */}
      <circle cx={0} cy={6} r={14} fill={skin} />
      <path d="M-14 4 C-14 -10 14 -10 14 4 C10 -2 -10 -2 -14 4 Z" fill={hair} />
      {label && <text x={0} y={74} textAnchor="middle" fontSize={11} fill="#efe6d6" fontFamily="Inter, sans-serif">{label}</text>}
      {sub && <text x={0} y={87} textAnchor="middle" fontSize={9.5} fill="#b9ac98" fontFamily="Inter, sans-serif">{sub}</text>}
      {delta !== undefined && delta !== 0 && (
        <g className="ct-delta">
          <rect x={10} y={-22} width={28} height={16} rx={4} fill={delta > 0 ? "#5fae84" : "#d0574b"} />
          <text x={24} y={-10} textAnchor="middle" fontSize={11} fontWeight={700} fill={delta > 0 ? "#0f0a07" : "#fff"} fontFamily="Inter, sans-serif">{delta > 0 ? "+" : ""}{delta}</text>
        </g>
      )}
    </g>
  );
}

function Bubble({ x, y, text, name, side = "center" }: { x: number; y: number; text: string; name: string; side?: "left" | "right" | "center" }) {
  const w = 300, h = 84;
  const bx = side === "left" ? x : side === "right" ? x - w : x - w / 2;
  return (
    <g className="ct-bubble">
      <rect x={bx} y={y - h} width={w} height={h} rx={10} fill="#efe6d6" stroke="#c9a45c" />
      <path d={`M${x - 8} ${y} L${x + 8} ${y} L${x} ${y + 10} Z`} fill="#efe6d6" stroke="#c9a45c" />
      <foreignObject x={bx + 10} y={y - h + 8} width={w - 20} height={h - 14}>
        <div style={{ fontFamily: "'EB Garamond', Georgia, serif", fontSize: 13, lineHeight: 1.25, color: "#1b130d", overflow: "hidden", maxHeight: h - 14 }}>
          <span style={{ fontFamily: "Inter, sans-serif", fontSize: 10, fontWeight: 700, textTransform: "uppercase", letterSpacing: ".06em", color: "#8c7442" }}>{name} </span>
          {text.length > 230 ? text.slice(0, 227) + "…" : text}
        </div>
      </foreignObject>
    </g>
  );
}

export default function Courtroom({ c, s, witness, live, flash, juryPresent }: {
  c: CaseFile; s: TrialState; witness?: Witness; live: LiveLine | null; flash: Flash | null; juryPresent: boolean;
}) {
  const jurors = seated(s.jurors);
  const speaking = live?.speaker ?? null;
  const isDefense = speaking === "defense";
  const isJudge = speaking === "judge";
  const isProsecutor = speaking === "prosecutor";
  const isWitness = speaking === "witness";
  const isDefendant = speaking === "defendant";
  const isClerk = speaking === "clerk" || speaking === "bailiff";
  const isJuror = speaking === "juror";
  const witnessOnStand = witness && witness.id !== "defendant" ? witness : undefined;
  const defendantOnStand = witness?.id === "defendant";

  // Where the bubble goes: near the speaker.
  const anchor = isJudge ? { x: 480, y: 62, side: "center" as const }
    : isWitness || (isDefendant && defendantOnStand) ? { x: 322, y: 140, side: "left" as const }
    : isProsecutor ? { x: 205, y: 250, side: "left" as const }
    : isDefense ? { x: 520, y: 250, side: "center" as const }
    : isDefendant ? { x: 590, y: 250, side: "right" as const }
    : isClerk ? { x: 632, y: 140, side: "right" as const }
    : isJuror ? { x: 700, y: 120, side: "right" as const }
    : null;

  return (
    <div className="relative overflow-hidden rounded-lg border border-wood-600 bg-[#120c08]">
      <svg viewBox={`0 0 ${W} ${H}`} className="block h-auto w-full" role="img" aria-label="Courtroom">
        <defs>
          <linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#2a1c14" /><stop offset="1" stopColor="#1a110c" /></linearGradient>
          <linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#5a3d2b" /><stop offset="1" stopColor="#3a271b" /></linearGradient>
          <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#241810" /><stop offset="1" stopColor="#140d09" /></linearGradient>
          <radialGradient id="spot" cx="0.5" cy="0.2" r="0.7"><stop offset="0" stopColor="#c9a45c" stopOpacity="0.18" /><stop offset="1" stopColor="#000" stopOpacity="0" /></radialGradient>
        </defs>

        {/* room */}
        <rect width={W} height={H} fill="url(#wall)" />
        <rect y={200} width={W} height={H - 200} fill="url(#floor)" />
        <rect width={W} height={H} fill="url(#spot)" />
        {[...Array(12)].map((_, i) => <rect key={i} x={i * 80} y={0} width={2} height={200} fill="#000" opacity={0.25} />)}
        {/* seal */}
        <circle cx={480} cy={40} r={22} fill="none" stroke="#c9a45c" strokeWidth={2} opacity={0.7} />
        <text x={480} y={44} textAnchor="middle" fontSize={11} fill="#c9a45c" fontFamily="EB Garamond, serif" opacity={0.9}>⚖</text>
        <text x={480} y={14} textAnchor="middle" fontSize={9} letterSpacing={2} fill="#8c7442" fontFamily="Inter, sans-serif">{c.courtName.toUpperCase().slice(0, 48)}</text>

        {/* bench */}
        <rect x={370} y={112} width={220} height={58} rx={4} fill="url(#wood)" stroke="#6b4a33" />
        <rect x={360} y={106} width={240} height={10} rx={2} fill="#7a5539" />
        <Figure x={480} y={56} robe suit="#141416" hair="#5b5049" speaking={isJudge} label={`Judge ${bareJudge(c).split(" ").pop()}`} />
        {flash && (flash.kind === "sustained" || flash.kind === "overruled" || flash.kind === "granted" || flash.kind === "denied") && (
          <g className="ct-gavel"><text x={560} y={104} fontSize={22}>🔨</text></g>
        )}

        {/* witness stand */}
        <rect x={286} y={150} width={74} height={44} rx={3} fill="url(#wood)" stroke="#6b4a33" />
        <rect x={280} y={146} width={86} height={8} rx={2} fill="#7a5539" />
        {(witnessOnStand || defendantOnStand) && (
          <Figure x={323} y={98} scale={0.9} suit={witness?.side === "prosecution" ? "#3a4a6b" : "#4a3a5e"} speaking={isWitness || (isDefendant && defendantOnStand)}
            label={(witnessOnStand?.name ?? c.defendant.name).split(" ").slice(-1)[0]} sub={s.examMode ?? undefined} />
        )}
        {!witnessOnStand && !defendantOnStand && <text x={323} y={176} textAnchor="middle" fontSize={9} fill="#8c7442" fontFamily="Inter, sans-serif">WITNESS</text>}

        {/* clerk */}
        <rect x={600} y={150} width={70} height={44} rx={3} fill="url(#wood)" stroke="#6b4a33" />
        <Figure x={635} y={102} scale={0.85} suit="#3b3b44" speaking={isClerk} label="Clerk" />

        {/* jury box */}
        <rect x={700} y={110} width={250} height={200} rx={6} fill="#1e140e" stroke="#6b4a33" />
        <rect x={700} y={300} width={250} height={10} fill="#7a5539" />
        <text x={825} y={126} textAnchor="middle" fontSize={9} letterSpacing={2} fill="#8c7442" fontFamily="Inter, sans-serif">{juryPresent ? "JURY" : jurors.length ? "JURY (not present)" : "JURY BOX (empty)"}</text>
        {jurors.slice(0, 12).map((j: Juror, i) => {
          const col = i % 6, row = Math.floor(i / 6);
          const x = 722 + col * 41, y = 140 + row * 78;
          return (
            <g key={j.id} opacity={juryPresent ? 1 : 0.35}>
              <Figure x={x} y={y} scale={0.55} skin={moodColor(j.lean)} suit={row === 0 ? "#3a3a44" : "#2f2f38"} speaking={isJuror && i === 0} delta={j.lastDelta} />
              <title>{`Seat ${i + 1}: ${j.name}, ${j.occupation}. Lean ${j.lean}`}</title>
            </g>
          );
        })}

        {/* prosecution table */}
        <rect x={120} y={262} width={190} height={14} rx={3} fill="url(#wood)" stroke="#6b4a33" />
        <rect x={128} y={276} width={8} height={40} fill="#3a271b" /><rect x={294} y={276} width={8} height={40} fill="#3a271b" />
        <Figure x={205} y={214} scale={0.95} suit="#243a5e" speaking={isProsecutor} label={c.prosecutor.name.split(" ").slice(-1)[0]} sub="for the State" />

        {/* defense table */}
        <rect x={430} y={262} width={210} height={14} rx={3} fill="url(#wood)" stroke="#6b4a33" />
        <rect x={438} y={276} width={8} height={40} fill="#3a271b" /><rect x={624} y={276} width={8} height={40} fill="#3a271b" />
        <Figure x={500} y={214} scale={0.95} suit="#2a2a2e" speaking={isDefense} label="You" sub="defense counsel" />
        {!defendantOnStand && <Figure x={590} y={214} scale={0.95} suit="#4a3a3a" skin="#b48a62" speaking={isDefendant} label={c.defendant.name.split(" ").slice(-1)[0]} sub="your client" />}

        {/* bar + gallery */}
        <rect x={0} y={334} width={W} height={4} fill="#7a5539" />
        {[...Array(9)].map((_, i) => <rect key={i} x={40 + i * 100} y={356} width={80} height={12} rx={2} fill="#2a1c14" stroke="#3f2c21" />)}
        {[...Array(9)].map((_, i) => <rect key={i} x={40 + i * 100} y={388} width={80} height={12} rx={2} fill="#2a1c14" stroke="#3f2c21" />)}

        {/* speech bubble */}
        {live && anchor && <Bubble x={anchor.x} y={anchor.y} side={anchor.side} name={live.name} text={live.text} />}

        {/* stamps */}
        {flash && (
          <g key={flash.key} className="ct-stamp">
            <text x={480} y={230} textAnchor="middle" fontFamily="Inter, sans-serif" fontWeight={900} fontSize={flash.kind === "objection" ? 56 : 44}
              fill={flash.kind === "objection" ? "#d0574b" : flash.kind === "sustained" || flash.kind === "granted" ? "#5fae84" : flash.kind === "verdict" ? "#c9a45c" : "#e0b64e"}
              stroke="#0f0a07" strokeWidth={2} transform="rotate(-8 480 230)" letterSpacing={2}>{flash.text}</text>
          </g>
        )}
      </svg>
    </div>
  );
}
