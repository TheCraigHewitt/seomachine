"use client";
import { GROUNDS } from "@/lib/engine/objections";

export default function ObjectionBar({ onObject, disabled }: { onObject: (groundId: string) => void; disabled: boolean }) {
  return (
    <div className="panel p-3">
      <div className="mb-2 flex items-center justify-between">
        <h3 className="font-serif text-lg text-guilty">Objection!</h3>
        <span className="text-xs text-ink">or say “Objection, hearsay”</span>
      </div>
      <div className="flex flex-wrap gap-1.5">
        {GROUNDS.map((g) => (
          <button
            key={g.id}
            disabled={disabled}
            title={`${g.rule}: ${g.tip}`}
            onClick={() => onObject(g.id)}
            className="rounded border border-guilty/40 bg-guilty/10 px-2 py-1 text-xs hover:bg-guilty/25 disabled:opacity-40"
          >
            {g.label}
          </button>
        ))}
      </div>
    </div>
  );
}
