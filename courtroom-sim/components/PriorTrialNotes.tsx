"use client";
import type { CaseFile } from "@/lib/engine/caseTypes";
import type { PriorTrial, TrialState } from "@/lib/engine/state";

const RESULT = { "not-guilty": "Not guilty", guilty: "Guilty", hung: "Hung", "guilty-lesser": "Guilty (lesser)" } as const;

/** Sworn testimony from the last trial, grouped by witness, with the question that drew each answer. */
function testimonyByWitness(c: CaseFile, p: PriorTrial) {
  const names = [...c.witnesses.map((w) => w.name), c.defendant.name];
  return names
    .map((name) => {
      const pairs: Array<{ q: string | null; a: string; phase: string }> = [];
      p.transcript.forEach((l, i) => {
        if (l.name !== name || (l.speaker !== "witness" && l.speaker !== "defendant")) return;
        const prev = p.transcript[i - 1];
        pairs.push({ q: prev && prev.name !== name ? `${prev.name}: ${prev.text}` : null, a: l.text, phase: l.phase.replace(/_/g, " ") });
      });
      return { name, pairs };
    })
    .filter((w) => w.pairs.length);
}

/** What the defense carries into a retrial: the record of the trial that ended in a mistrial. */
export default function PriorTrialNotes({ c, s }: { c: CaseFile; s: TrialState }) {
  const p = s.retrial?.prior?.at(-1);
  if (!s.retrial || !p) return null;
  const chName = (id: string) => c.charges.find((x) => x.id === id)?.name ?? id;
  const evName = (id: string) => c.evidence.find((x) => x.id === id)?.name ?? id;
  const motions = Object.entries(p.motionsHeard);
  const witnesses = testimonyByWitness(c, p);

  return (
    <details className="panel p-3 text-xs">
      <summary className="cursor-pointer font-serif text-lg">Notes from trial {p.round}</summary>
      <div className="scrollbar-thin mt-2 max-h-[48vh] space-y-3 overflow-y-auto pr-1">
        <section>
          <h4 className="font-semibold text-brass">Where it ended</h4>
          <ul className="mt-1 space-y-0.5">
            {p.verdicts.map((v) => (
              <li key={v.chargeId}>
                {chName(v.chargeId)}: <b className={v.result === "hung" ? "text-caution" : v.result === "not-guilty" ? "text-acquit" : "text-guilty"}>{RESULT[v.result]}</b> ({v.votesNotGuilty}–{12 - v.votesNotGuilty} NG)
              </li>
            ))}
          </ul>
          {p.keyFactor && <p className="mt-1 text-ink">Jury&apos;s deciding factor: {p.keyFactor}</p>}
          <p className="mt-1 text-ink">
            Acquitted counts are final. Only {c.charges.filter((x) => !s.retrial!.acquitted.includes(x.id)).map((x) => x.name).join(", ")} {c.charges.length - s.retrial.acquitted.length === 1 ? "is" : "are"} before this jury.
          </p>
        </section>

        <section>
          <h4 className="font-semibold text-brass">What changed</h4>
          <ul className="mt-1 list-disc space-y-0.5 pl-4">
            <li>New venire. Nothing said to the first jury carries over. Voir dire starts fresh.</li>
            <li>Every witness testified under oath. Their answers below are prior sworn testimony: any change is impeachment material.</li>
            <li>The State has read the same record and knows where its case broke. Expect it to shore up the weak points you found.</li>
            {p.bail && <li>Client was {p.bail} pending the first trial. Bail is argued again at arraignment.</li>}
            {motions.length > 0 && <li>Pretrial rulings are the law of the case. The judge will usually adhere unless you show new grounds.</li>}
          </ul>
        </section>

        {motions.length > 0 && (
          <section>
            <h4 className="font-semibold text-brass">Pretrial rulings last time</h4>
            <ul className="mt-1 space-y-0.5">
              {motions.map(([m, r]) => (
                <li key={m}>{m}: <b className={r === "denied" ? "text-guilty" : "text-acquit"}>{r}</b></li>
              ))}
            </ul>
            {p.excluded.length > 0 && <p className="mt-1">Excluded: {p.excluded.map(evName).join("; ")}</p>}
          </section>
        )}

        {p.revealed.length > 0 && (
          <section>
            <h4 className="font-semibold text-brass">Facts you exposed</h4>
            <ul className="mt-1 list-disc space-y-0.5 pl-4">{p.revealed.map((r, i) => <li key={i}>{r.fact}</li>)}</ul>
          </section>
        )}

        {p.critique.length > 0 && (
          <section>
            <h4 className="font-semibold text-brass">Senior partner&apos;s critique</h4>
            <ul className="mt-1 list-disc space-y-0.5 pl-4">{p.critique.map((x, i) => <li key={i}>{x}</li>)}</ul>
          </section>
        )}

        <section>
          <h4 className="font-semibold text-brass">Plan for round {s.retrial.round}</h4>
          <ul className="mt-1 list-disc space-y-0.5 pl-4">
            {p.revealed.map((r, i) => <li key={i}>Lead with it, don&apos;t rediscover it: {r.fact}</li>)}
            {witnesses.map((w) => <li key={w.name}>{w.name} gave {w.pairs.length} sworn answers. Read them before cross; lock the witness to each one before you spring the contradiction.</li>)}
            {p.motionsHeard && Object.entries(p.motionsHeard).some(([, r]) => r === "denied") && <li>Re-argue the denied motion only with new grounds or new facts from the record. The judge already ruled once.</li>}
            <li>Voir dire is a clean slate. The biases that hung the last jury will be in this panel too.</li>
          </ul>
        </section>

        {witnesses.length > 0 && (
          <section>
            <h4 className="font-semibold text-brass">Sworn testimony, by witness</h4>
            {witnesses.map((w) => (
              <details key={w.name} className="mt-1">
                <summary className="cursor-pointer font-semibold text-sky-200">{w.name} <span className="font-normal text-ink">({w.pairs.length} answers)</span></summary>
                <ol className="mt-1 space-y-1 border-l border-wood-600 pl-2">
                  {w.pairs.map((x, i) => (
                    <li key={i}>
                      {x.q && <p className="text-ink">{x.q}</p>}
                      <p>{x.a}</p>
                    </li>
                  ))}
                </ol>
              </details>
            ))}
          </section>
        )}
      </div>
    </details>
  );
}
