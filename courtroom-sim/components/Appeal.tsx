"use client";
import { useState } from "react";
import type { CaseFile } from "@/lib/engine/caseTypes";
import { briefTemplate, type AppealOpinion, type AppealRecord } from "@/lib/engine/appeal";
import type { TrialState } from "@/lib/engine/state";

const DISP = {
  affirmed: { label: "AFFIRMED", cls: "text-guilty" },
  "reversed-insufficient": { label: "REVERSED · retrial barred", cls: "text-acquit" },
  "reversed-error": { label: "REVERSED · remanded for new trial", cls: "text-caution" },
  vacated: { label: "VACATED", cls: "text-caution" },
} as const;

/** The appellate stage: write the brief, the panel confers, the opinion comes down. */
export default function Appeal({ c, s, onDecided, onBack }: { c: CaseFile; s: TrialState; onDecided: (r: AppealRecord) => void; onBack: () => void }) {
  const [brief, setBrief] = useState(() => briefTemplate(c, s));
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const d = s.deliberation!;
  const chName = (id: string) => c.charges.find((x) => x.id === id)?.name ?? id;
  const convicted = d.verdicts.filter((v) => v.result === "guilty" || v.result === "guilty-lesser");
  const evName = (id: string) => c.evidence.find((e) => e.id === id)?.name ?? id;

  const file = async () => {
    setBusy(true);
    setError(null);
    try {
      const res = await fetch("/api/appeal", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ caseId: c.id, state: { ...s, appeal: null }, brief }),
      });
      const data = (await res.json()) as { opinion?: AppealOpinion; points?: number; model?: string; warning?: string; error?: string };
      if (!data.opinion) throw new Error(data.error || "The panel did not return an opinion.");
      onDecided({ brief, opinion: data.opinion, points: data.points ?? 0, model: data.model ?? "", date: new Date().toISOString() });
    } catch (e) {
      setError(e instanceof Error ? e.message : "The clerk's office is closed. Try again.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mx-auto max-w-5xl space-y-5 py-6">
      <div className="panel p-6">
        <p className="text-sm uppercase tracking-[0.3em] text-brass">Notice of appeal · {c.jurisdiction}</p>
        <h1 className="mt-1 font-serif text-3xl font-bold">{c.title}</h1>
        <p className="mt-2 text-sm text-ink">
          Your client stands convicted of {convicted.map((v) => chName(v.chargeId)).join(" and ")}. Write the brief. A three-judge panel will rule on the trial record, count by count.
        </p>
      </div>

      <div className="grid gap-5 lg:grid-cols-[1fr_320px]">
        <div className="panel p-4">
          <label className="mb-2 block font-serif text-lg">Brief of appellant</label>
          <textarea value={brief} onChange={(e) => setBrief(e.target.value)} rows={26} disabled={busy}
            className="w-full rounded border border-wood-600 bg-black/30 p-3 font-serif text-[15px] leading-relaxed" />
          {error && <p className="mt-2 text-sm text-guilty">{error}</p>}
          <div className="mt-3 flex flex-wrap items-center gap-3">
            <button onClick={file} disabled={busy || brief.trim().length < 200} className="brass-btn">{busy ? "The panel is conferring…" : "File the brief"}</button>
            <button onClick={onBack} disabled={busy} className="ghost-btn">Back to verdict</button>
            <span className="text-xs text-ink">{brief.length.toLocaleString()} characters</span>
          </div>
        </div>

        <aside className="space-y-4 text-xs">
          <div className="panel p-4">
            <h3 className="font-serif text-lg">How the panel reads it</h3>
            <ul className="mt-2 list-disc space-y-1 pl-4 text-ink">
              <li><b className="text-parchment">Sufficiency</b>: reverse only if no rational juror could find an element on this record. Wins here bar retrial.</li>
              <li><b className="text-parchment">Trial error</b>: a wrong ruling that was preserved and not harmless. Wins here get a new trial.</li>
              <li>Inconsistent verdicts are not a ground. Acquittals on other counts don't undo this one.</li>
              <li>Cite the record: what a witness said, what was excluded, what the judge ruled. Assertions the transcript contradicts get overruled.</li>
              <li>Placeholder citations and hypothetical framing ("if the record shows…") cost you in chambers.</li>
            </ul>
          </div>
          <div className="panel p-4">
            <h3 className="font-serif text-lg">Your record</h3>
            <p className="mt-1 text-ink">Convicted counts and their elements:</p>
            <ul className="mt-1 space-y-2">
              {convicted.map((v) => {
                const ch = c.charges.find((x) => x.id === v.chargeId);
                return <li key={v.chargeId}><b>{ch?.name ?? v.chargeId}</b><ol className="list-decimal pl-4 text-ink">{ch?.elements.map((e) => <li key={e}>{e}</li>)}</ol></li>;
              })}
            </ul>
            <p className="mt-3 text-ink">Rulings against you: {s.rulings.filter((r) => !r.favorsDefense).map((r) => `${r.on} (${r.result})`).join("; ") || "none"}</p>
            <p className="mt-1 text-ink">Excluded: {s.excluded.map(evName).join("; ") || "nothing"}</p>
            <p className="mt-1 text-ink">Facts you exposed: {s.revealed.map((r) => r.fact).join("; ") || "none"}</p>
            <p className="mt-1 text-ink">Jury's deciding factor: {d.keyFactor}</p>
          </div>
        </aside>
      </div>
    </div>
  );
}

/** The opinion, rendered on the verdict screen once the appeal is decided. */
export function OpinionPanel({ c, r }: { c: CaseFile; r: AppealRecord }) {
  const o = r.opinion;
  const chName = (id: string) => c.charges.find((x) => x.id === id)?.name ?? id;
  return (
    <div className="panel p-5">
      <p className="text-sm uppercase tracking-[0.25em] text-brass">{o.court} · opinion</p>
      <p className="mt-2 font-serif text-lg">{o.summary}</p>
      <div className="mt-3 space-y-1">
        {o.counts.map((x) => (
          <p key={x.chargeId} className="text-sm">
            {chName(x.chargeId)}: <b className={DISP[x.disposition].cls}>{DISP[x.disposition].label}</b> <span className="text-ink">— {x.reason}</span>
          </p>
        ))}
      </div>
      {o.plainError && <p className="mt-3 rounded border border-caution/40 bg-caution/10 p-2 text-sm text-caution"><b>Noticed by the court:</b> {o.plainError}</p>}
      <div className="mt-4 grid gap-4 md:grid-cols-2">
        <div>
          <h3 className="font-serif text-lg">Enumerations of error</h3>
          <ul className="mt-1 space-y-2 text-sm">
            {o.enumerations.map((e, i) => (
              <li key={i}>
                <p><b>{e.title}</b> <span className={e.ruling === "sustained" ? "text-acquit" : e.ruling === "moot" ? "text-ink" : "text-guilty"}>· {e.ruling}</span></p>
                <p className="text-ink">{e.reasoning}</p>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <h3 className="font-serif text-lg">Chambers notes on the brief</h3>
          <ul className="mt-1 list-disc space-y-1 pl-5 text-sm">{o.critique.map((x, i) => <li key={i}>{x}</li>)}</ul>
          <p className="mt-3 text-sm">Brief grade: <b className="font-serif text-2xl text-brass">{o.briefGrade}</b> · Appeal points: <b className={r.points >= 0 ? "text-acquit" : "text-guilty"}>{r.points > 0 ? "+" : ""}{r.points}</b></p>
          <details className="mt-3 text-xs"><summary className="cursor-pointer text-ink">Your brief</summary><pre className="mt-1 max-h-64 overflow-y-auto whitespace-pre-wrap font-serif text-[13px]">{r.brief}</pre></details>
        </div>
      </div>
    </div>
  );
}
