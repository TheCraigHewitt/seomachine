"use client";
import type { Juror } from "@/lib/engine/jurors";

interface Props {
  jurors: Juror[];
  peremptoriesLeft: number;
  challengeTarget: number | null;
  onStrike: (id: number) => void;
  onChallenge: (id: number | null) => void;
  disabled: boolean;
}

export default function VoirDire({ jurors, peremptoriesLeft, challengeTarget, onStrike, onChallenge, disabled }: Props) {
  const panel = jurors.filter((j) => j.status === "venire");
  const gone = jurors.filter((j) => j.status === "struck-defense" || j.status === "excused-cause");
  return (
    <div className="panel p-3">
      <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
        <h3 className="font-serif text-lg">The venire: {panel.length} prospective jurors</h3>
        <span className="text-xs text-ink">Peremptory strikes left: <b className="text-brass">{peremptoriesLeft}</b> · the State strikes 3 at seating</span>
      </div>
      <p className="mb-2 text-xs text-ink">
        Ask the panel questions at the lectern to surface bias (“Does anyone believe police officers are more truthful than other witnesses?”).
        The first 12 left in the box when you seat the jury will serve.
      </p>
      <div className="scrollbar-thin grid max-h-72 gap-1.5 overflow-y-auto sm:grid-cols-2">
        {panel.map((j) => (
          <div key={j.id} className={`rounded border p-2 text-xs ${challengeTarget === j.id ? "border-caution" : "border-wood-600"}`}>
            <div className="flex items-center justify-between">
              <span className="font-semibold">#{j.id} {j.name}</span>
              <span className="text-ink">{j.age}</span>
            </div>
            <p className="text-ink">{j.occupation}</p>
            {j.revealed ? <p className="mt-1 text-caution">“{j.bias}”</p> : <p className="mt-1 italic text-ink/60">Views unknown</p>}
            <div className="mt-1.5 flex gap-1.5">
              <button disabled={disabled || peremptoriesLeft <= 0} onClick={() => onStrike(j.id)} className="ghost-btn px-2 py-0.5 text-xs">Strike</button>
              <button disabled={disabled} onClick={() => onChallenge(challengeTarget === j.id ? null : j.id)} className="ghost-btn px-2 py-0.5 text-xs">
                {challengeTarget === j.id ? "Cancel challenge" : "Challenge for cause"}
              </button>
            </div>
          </div>
        ))}
      </div>
      {gone.length > 0 && <p className="mt-2 text-xs text-ink">Removed: {gone.map((j) => `#${j.id}`).join(", ")}</p>}
    </div>
  );
}
