"use client";
import { doubtLevel, seated, straw, type Juror } from "@/lib/engine/jurors";

const face = (lean: number) => (lean >= 70 ? "🙂" : lean >= 55 ? "🤔" : lean > 45 ? "😐" : lean > 30 ? "🤨" : "😠");
const barColor = (lean: number) => (lean >= 60 ? "bg-acquit" : lean <= 40 ? "bg-guilty" : "bg-caution");

export function JurorCard({ j, seat }: { j: Juror; seat: number }) {
  const flash = j.lastDelta > 0 ? "flash-up" : j.lastDelta < 0 ? "flash-down" : "";
  return (
    <div key={`${j.id}-${j.lean}`} className={`group relative rounded-md border border-wood-600 bg-wood-900 p-1.5 text-center ${flash}`}>
      <div className="text-[10px] text-ink">Seat {seat}</div>
      <div className="text-2xl leading-none">{face(j.lean)}</div>
      <div className="mt-1 h-1.5 overflow-hidden rounded bg-wood-700">
        <div className={`h-full ${barColor(j.lean)} transition-all duration-700`} style={{ width: `${j.lean}%` }} />
      </div>
      {j.lastDelta !== 0 && (
        <div className={`absolute -top-2 -right-1 rounded px-1 text-[10px] font-bold ${j.lastDelta > 0 ? "bg-acquit text-wood-950" : "bg-guilty text-white"}`}>
          {j.lastDelta > 0 ? "+" : ""}{j.lastDelta}
        </div>
      )}
      <div className="pointer-events-none absolute left-1/2 top-full z-20 mt-1 hidden w-52 -translate-x-1/2 rounded-md border border-wood-600 bg-wood-950 p-2 text-left text-xs shadow-xl group-hover:block">
        <p className="font-semibold">{j.name}</p>
        <p className="text-ink">{j.age}, {j.occupation}</p>
        {j.revealed && <p className="mt-1 text-caution">{j.bias}</p>}
        <p className="mt-1">Leaning {j.lean >= 50 ? "NOT GUILTY" : "GUILTY"} ({j.lean})</p>
        {j.lastReason && <p className="mt-1 italic text-ink">“{j.lastReason}”</p>}
      </div>
    </div>
  );
}

export function DoubtGauge({ jurors }: { jurors: Juror[] }) {
  const level = doubtLevel(jurors);
  const s = straw(jurors);
  return (
    <div>
      <div className="flex items-baseline justify-between text-xs">
        <span className="text-guilty">GUILTY</span>
        <span className="font-serif text-sm text-brass">Reasonable doubt: {level}%</span>
        <span className="text-acquit">NOT GUILTY</span>
      </div>
      <div className="relative mt-1 h-3 rounded-full bg-gradient-to-r from-guilty via-caution to-acquit">
        <div className="absolute -top-1 h-5 w-1.5 rounded bg-parchment shadow transition-all duration-700" style={{ left: `calc(${level}% - 3px)` }} />
      </div>
      <p className="mt-1 text-center text-xs text-ink">
        If they voted now: <span className="text-acquit">{s.notGuilty} NG</span> · <span className="text-caution">{s.undecided} undecided</span> · <span className="text-guilty">{s.guilty} G</span>
      </p>
    </div>
  );
}

export default function JuryBox({ jurors }: { jurors: Juror[] }) {
  const s = seated(jurors);
  return (
    <div className="panel p-3">
      <div className="mb-2 flex items-center justify-between">
        <h3 className="font-serif text-lg">Jury Box</h3>
        <span className="text-xs text-ink">hover a juror</span>
      </div>
      {s.length ? (
        <>
          <div className="grid grid-cols-6 gap-1.5">{s.map((j, i) => <JurorCard key={j.id} j={j} seat={i + 1} />)}</div>
          <div className="mt-3"><DoubtGauge jurors={jurors} /></div>
        </>
      ) : (
        <p className="text-sm text-ink">The jury has not been selected yet.</p>
      )}
    </div>
  );
}
