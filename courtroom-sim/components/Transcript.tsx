"use client";
import { useEffect, useRef } from "react";
import type { TranscriptLine } from "@/lib/engine/state";

const STYLE: Record<string, string> = {
  judge: "text-brass",
  prosecutor: "text-guilty",
  defense: "text-acquit",
  witness: "text-sky-300",
  juror: "text-violet-300",
  clerk: "text-ink",
  bailiff: "text-ink",
  defendant: "text-amber-200",
  system: "text-ink",
};

export default function Transcript({ lines, pending }: { lines: TranscriptLine[]; pending: boolean }) {
  const end = useRef<HTMLDivElement>(null);
  useEffect(() => {
    // Block body: newer browsers return a Promise from smooth scrollIntoView,
    // which React would otherwise treat as an effect cleanup function.
    end.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [lines.length, pending]);
  return (
    <div className="scrollbar-thin h-full overflow-y-auto pr-2 font-serif text-[17px] leading-relaxed">
      {lines.length === 0 && <p className="text-ink">The courtroom is silent. Press the gold button below to begin.</p>}
      {lines.map((l) =>
        l.speaker === "system" ? (
          <p key={l.id} className="my-3 text-center font-sans text-xs tracking-[0.3em] text-brass-dim">{l.text}</p>
        ) : (
          <p key={l.id} className="mb-2">
            <span className={`font-sans text-xs font-semibold uppercase tracking-wide ${STYLE[l.speaker] ?? ""}`}>{l.name}: </span>
            {l.text}
          </p>
        ),
      )}
      {pending && <p className="animate-pulse text-ink">…</p>}
      <div ref={end} />
    </div>
  );
}
