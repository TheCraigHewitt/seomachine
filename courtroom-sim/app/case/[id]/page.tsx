import Link from "next/link";
import { notFound } from "next/navigation";
import { getCase } from "@/lib/cases";
import { publicCase } from "@/lib/engine/witness";
import { ChargeStatus, EvidenceStatus, MotionStatus, RetrialBanner } from "@/components/CaseFileStatus";

export const dynamic = "force-dynamic";

export default async function CasePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const c = getCase(id);
  if (!c) notFound();
  const pub = publicCase(c); // safe to ship to the browser: no hidden facts

  return (
    <main className="mx-auto max-w-5xl px-4 py-8">
      <Link href="/" className="text-sm text-brass hover:underline">← Docket</Link>
      <header className="mt-3 mb-6">
        <p className="text-sm uppercase tracking-[0.25em] text-brass">Case File · {c.courtName}</p>
        <h1 className="font-serif text-4xl font-bold sm:text-5xl">{c.title}</h1>
        <p className="mt-2 text-ink">{c.tagline}</p>
        <p className="mt-1 text-xs italic text-brass-dim">
          Fictionalized. Inspired by {c.basedOn.name} ({c.basedOn.year}). The real outcome is revealed after your verdict.
        </p>
      </header>

      <div className="grid gap-5 lg:grid-cols-3">
        <RetrialBanner c={pub} />
        <section className="panel p-5 lg:col-span-2">
          <h2 className="mb-2 font-serif text-2xl">Charging narrative</h2>
          <p className="whitespace-pre-line text-sm leading-relaxed">{c.caseSummary}</p>
          <h3 className="mt-4 font-serif text-xl">The State&apos;s theory</h3>
          <p className="text-sm leading-relaxed">{c.prosecutionTheory}</p>
        </section>

        <section className="panel p-5">
          <h2 className="mb-2 font-serif text-2xl">Your client</h2>
          <p className="font-semibold">{c.defendant.name}, {c.defendant.age}</p>
          <p className="text-sm text-ink">{c.defendant.background}</p>
          <p className="mt-2 text-sm"><span className="text-brass">Priors:</span> {c.defendant.priors}</p>
          <h3 className="mt-3 font-serif text-lg">In confidence, they tell you:</h3>
          <blockquote className="border-l-2 border-brass pl-3 text-sm italic">{c.defendant.privateAccount}</blockquote>
          <p className="mt-3 text-sm"><span className="text-guilty">If they testify:</span> {c.defendant.testifyRisk}</p>
        </section>

        <section className="panel p-5 lg:col-span-3">
          <h2 className="mb-3 font-serif text-2xl">Charges</h2>
          <div className="grid gap-3 sm:grid-cols-2">
            {c.charges.map((ch) => (
              <div key={ch.id} className="rounded-lg border border-wood-600 p-3">
                <p className="font-semibold">{ch.name}</p>
                <p className="text-xs text-ink">{ch.statute} · Max: {ch.maxSentence}</p>
                <ol className="mt-2 list-decimal pl-5 text-sm">{ch.elements.map((e) => <li key={e}>{e}</li>)}</ol>
                {ch.lesserIncluded?.length ? <p className="mt-1 text-xs text-ink">Lesser included: {ch.lesserIncluded.join(", ")}</p> : null}
                <ChargeStatus c={pub} chargeId={ch.id} />
              </div>
            ))}
          </div>
        </section>

        <section className="panel p-5 lg:col-span-2">
          <h2 className="mb-3 font-serif text-2xl">Discovery: evidence</h2>
          <ul className="space-y-3">
            {c.evidence.map((e) => (
              <li key={e.id} className="rounded-lg border border-wood-600 p-3 text-sm">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="font-semibold">{e.name}</span>
                  <span className="rounded bg-wood-700 px-1.5 text-xs uppercase">{e.type}</span>
                  <span className="text-xs text-ink">offered by {e.offeredBy}</span>
                  {e.suppressible && <span className="rounded bg-caution/20 px-1.5 text-xs text-caution">suppressible</span>}
                </div>
                <p className="mt-1">{e.description}</p>
                {e.admissibilityIssue && <p className="mt-1 text-xs text-caution">Admissibility: {e.admissibilityIssue}</p>}
                <EvidenceStatus c={pub} evidenceId={e.id} />
              </li>
            ))}
          </ul>
        </section>

        <section className="panel p-5">
          <h2 className="mb-3 font-serif text-2xl">Pretrial motions</h2>
          <ul className="space-y-3 text-sm">
            {c.pretrialMotions.map((m) => (
              <li key={m.id}><p className="font-semibold">{m.name}</p><p className="text-ink">{m.basis}</p><MotionStatus c={pub} motionName={m.name} /></li>
            ))}
          </ul>
          <h3 className="mt-5 font-serif text-xl">Bench</h3>
          <p className="text-sm"><span className="text-brass">Judge {c.judge.name}</span>: {c.judge.bio}</p>
          <p className="mt-2 text-sm"><span className="text-brass">ADA {c.prosecutor.name}</span>: {c.prosecutor.style}</p>
        </section>

        <section className="panel p-5 lg:col-span-3">
          <h2 className="mb-3 font-serif text-2xl">Witness list & prior statements (Jencks / Brady disclosure)</h2>
          <div className="grid gap-3 sm:grid-cols-2">
            {c.witnesses.map((w) => (
              <div key={w.id} className="rounded-lg border border-wood-600 p-3 text-sm">
                <p className="font-semibold">{w.name} <span className="text-xs font-normal text-ink">— {w.role} ({w.side})</span></p>
                <p className="mt-1">{w.publicTestimony}</p>
                {w.priorStatements.length > 0 && (
                  <>
                    <p className="mt-2 text-xs uppercase tracking-wide text-brass">Prior statements</p>
                    <ul className="list-disc pl-5 text-ink">{w.priorStatements.map((p) => <li key={p}>{p}</li>)}</ul>
                  </>
                )}
                {w.credibilityIssues.length > 0 && (
                  <>
                    <p className="mt-2 text-xs uppercase tracking-wide text-caution">Known credibility issues</p>
                    <ul className="list-disc pl-5 text-ink">{w.credibilityIssues.map((p) => <li key={p}>{p}</li>)}</ul>
                  </>
                )}
              </div>
            ))}
          </div>
          <p className="mt-3 text-xs text-ink">Each witness is hiding more than this. Only well-aimed questions on cross will bring it out.</p>
        </section>

        <details className="panel p-5 lg:col-span-3">
          <summary className="cursor-pointer font-serif text-xl text-brass">Senior partner&apos;s notes (hints)</summary>
          <ul className="mt-3 list-disc pl-5 text-sm">{c.defenseAngles.map((a) => <li key={a}>{a}</li>)}</ul>
        </details>
      </div>

      <div className="sticky bottom-4 mt-8 flex justify-center">
        <Link href={`/trial/${c.id}`} className="brass-btn px-8 py-3 text-lg shadow-2xl">⚖ Enter the courtroom</Link>
      </div>
    </main>
  );
}
