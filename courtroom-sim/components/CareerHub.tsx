"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { EMPTY, loadCareer, saveCareer, type Career } from "@/lib/career";
import { rankFor, tierUnlocked } from "@/lib/engine/scoring";

export interface DocketCase {
  id: string; title: string; tier: number; category: string; tagline: string;
  jurisdiction: string; basedOn: string; charges: string[];
}

const TIER_NAMES = ["", "Tier I — Misdemeanor Court Veteran", "Tier II — Homicide Docket", "Tier III — Gang & RICO Task Force"];
const CAT_COLORS: Record<string, string> = {
  gang: "bg-red-900/60 text-red-200", rico: "bg-purple-900/60 text-purple-200", murder: "bg-stone-700 text-stone-200",
  "self-defense": "bg-sky-900/60 text-sky-200", "wrongful-conviction": "bg-amber-900/60 text-amber-200",
};

export default function CareerHub({ cases, ai }: { cases: DocketCase[]; ai: string | null }) {
  const [career, setCareer] = useState<Career>(EMPTY);
  useEffect(() => { setCareer(loadCareer()); }, []);
  const rank = rankFor(career.points);
  const togglePractice = () => { const c = { ...career, practice: !career.practice }; saveCareer(c); setCareer(c); };
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState({ wins: 0, hung: 0, losses: 0, points: 0 });
  const openEditor = () => { setDraft({ wins: career.wins, hung: career.hung, losses: career.losses, points: career.points }); setEditing(true); };
  const num = (v: string) => Math.max(0, Math.floor(Number(v) || 0));
  const restore = () => {
    const c: Career = { ...career, wins: num(String(draft.wins)), hung: num(String(draft.hung)), losses: num(String(draft.losses)), points: num(String(draft.points)) };
    saveCareer(c); setCareer(c); setEditing(false);
  };

  return (
    <main className="mx-auto max-w-6xl px-4 py-8 sm:py-12">
      <header className="mb-8 flex flex-col gap-6 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-brass">Superior Court Simulator</p>
          <h1 className="font-serif text-5xl font-bold sm:text-6xl">Defense Counsel</h1>
          <p className="mt-3 max-w-xl text-ink">
            Take the lectern and speak your case live. Object in real time, break witnesses on cross, and watch
            twelve jurors decide your client&apos;s fate. The cases are inspired by real gang, RICO and murder trials.
          </p>
        </div>
        <div className="panel min-w-64 p-4">
          <p className="text-xs uppercase tracking-widest text-ink">Rank</p>
          <p className="font-serif text-2xl text-brass">{rank.name}</p>
          <div className="mt-2 h-1.5 overflow-hidden rounded bg-wood-700">
            <div className="h-full bg-brass" style={{ width: `${rank.next ? Math.min(100, ((career.points - rank.min) / (rank.next.min - rank.min)) * 100) : 100}%` }} />
          </div>
          <p className="mt-1 text-xs text-ink">{career.points} pts{rank.next ? ` · ${rank.next.min - career.points} to ${rank.next.name}` : ""}</p>
          <div className="mt-3 grid grid-cols-3 text-center text-sm">
            <div><p className="text-xl font-semibold text-acquit">{career.wins}</p><p className="text-ink">Acquittals</p></div>
            <div><p className="text-xl font-semibold text-caution">{career.hung}</p><p className="text-ink">Hung/Split</p></div>
            <div><p className="text-xl font-semibold text-guilty">{career.losses}</p><p className="text-ink">Convicted</p></div>
          </div>
          {editing ? (
            <div className="mt-3 border-t border-wood-600 pt-3 text-xs">
              <p className="text-ink">Restore a record this browser lost. Points drive rank; acquittals unlock tiers.</p>
              <div className="mt-2 grid grid-cols-2 gap-2">
                {([["wins", "Acquittals"], ["hung", "Hung/Split"], ["losses", "Convicted"], ["points", "Points"]] as const).map(([k, label]) => (
                  <label key={k} className="flex items-center justify-between gap-2">
                    <span className="text-ink">{label}</span>
                    <input type="number" min={0} value={draft[k]} onChange={(e) => setDraft({ ...draft, [k]: num(e.target.value) })} className="w-20 rounded border border-wood-600 bg-black/30 px-1 py-0.5 text-right" />
                  </label>
                ))}
              </div>
              <div className="mt-2 flex gap-2">
                <button onClick={restore} className="brass-btn px-3 py-1 text-xs">Save record</button>
                <button onClick={() => setEditing(false)} className="ghost-btn px-3 py-1 text-xs">Cancel</button>
              </div>
            </div>
          ) : (
            <button onClick={openEditor} className="mt-3 text-xs text-ink underline hover:text-brass">Restore record…</button>
          )}
        </div>
      </header>

      <div className="mb-6 flex flex-wrap items-center gap-3 text-sm">
        <span className={`rounded-full px-3 py-1 ${ai ? "bg-acquit/20 text-acquit" : "bg-caution/20 text-caution"}`}>
          {ai ? `AI key loaded · ${ai}` : "Offline court (set OPENROUTER_API_KEY for full AI)"}
        </span>
        <a href="/api/health" target="_blank" rel="noreferrer" className="text-xs text-brass underline">Test AI connection</a>
        <label className="flex cursor-pointer items-center gap-2 text-ink">
          <input type="checkbox" checked={career.practice} onChange={togglePractice} className="accent-[#c9a45c]" />
          Practice mode (unlock every case)
        </label>
      </div>

      {[1, 2, 3].map((tier) => {
        const open = tierUnlocked(tier, career.wins, career.practice);
        const list = cases.filter((c) => c.tier === tier);
        if (!list.length) return null;
        return (
          <section key={tier} className="mb-10">
            <h2 className="mb-3 font-serif text-2xl">
              {TIER_NAMES[tier]} {!open && <span className="ml-2 text-base text-ink">🔒 {tier === 2 ? "Win 1 acquittal" : "Win 3 acquittals"} to unlock</span>}
            </h2>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {list.map((c) => {
                const rec = career.cases[c.id];
                return (
                  <div key={c.id} className={`panel flex flex-col p-5 ${open ? "" : "opacity-50"}`}>
                    <div className="mb-2 flex items-center justify-between">
                      <span className={`rounded px-2 py-0.5 text-xs uppercase tracking-wide ${CAT_COLORS[c.category] ?? "bg-wood-700"}`}>{c.category}</span>
                      {rec && <span className="font-serif text-lg text-brass">Grade {rec.grade}</span>}
                    </div>
                    <h3 className="font-serif text-xl font-semibold">{c.title}</h3>
                    <p className="text-xs text-ink">{c.jurisdiction}</p>
                    <p className="mt-2 flex-1 text-sm">{c.tagline}</p>
                    <p className="mt-2 text-xs text-ink">Charges: {c.charges.join(" · ")}</p>
                    <p className="mt-1 text-xs italic text-brass-dim">Inspired by {c.basedOn}</p>
                    {open ? (
                      <Link href={`/case/${c.id}`} className="brass-btn mt-4 text-center">{rec ? "Retry case" : "Open case file"}</Link>
                    ) : (
                      <button disabled className="brass-btn mt-4">Locked</button>
                    )}
                  </div>
                );
              })}
            </div>
          </section>
        );
      })}
      {!cases.length && <p className="text-ink">No case files found in data/cases.</p>}
      <footer className="mt-12 border-t border-wood-700 pt-4 text-xs text-ink">
        Every case is fictionalized: names, places and details are invented and adapted from public records of the real case
        credited on each file. This is an educational game, not legal advice.
      </footer>
    </main>
  );
}
