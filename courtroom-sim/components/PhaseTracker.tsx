import { PHASES, phaseIndex, type PhaseId } from "@/lib/engine/phases";

export default function PhaseTracker({ phase }: { phase: PhaseId }) {
  const cur = phaseIndex(phase);
  return (
    <ol className="scrollbar-thin flex gap-1 overflow-x-auto pb-1 text-[11px]">
      {PHASES.map((p, i) => (
        <li
          key={p.id}
          className={`shrink-0 rounded px-2 py-1 ${i === cur ? "bg-brass font-semibold text-wood-950" : i < cur ? "bg-wood-700 text-ink" : "border border-wood-700 text-ink/60"}`}
        >
          {p.short}
        </li>
      ))}
    </ol>
  );
}
