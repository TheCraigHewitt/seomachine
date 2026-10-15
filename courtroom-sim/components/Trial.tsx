"use client";
import Link from "next/link";
import { useCallback, useEffect, useRef, useState } from "react";
import type { CaseFile } from "@/lib/engine/caseTypes";
import { detectObjection, GROUNDS } from "@/lib/engine/objections";
import { JURY_ABSENT, phaseInfo } from "@/lib/engine/phases";
import type { PlayerInput } from "@/lib/engine/prompts";
import type { CourtTurn, Deliberation } from "@/lib/engine/schema";
import { grade, outcomeOf, trialPoints } from "@/lib/engine/scoring";
import { acquittedCounts, initRetrial, initTrial, reducer, type Action, type TrialState } from "@/lib/engine/state";
import { bareJudge, DEFENDANT_ID, witnessById } from "@/lib/engine/witness";
import { clearTrial, loadTrial, recordAppeal, recordTrial, saveTrial } from "@/lib/career";
import { appliedVerdicts, type AppealRecord } from "@/lib/engine/appeal";
import Appeal from "./Appeal";
import { playLines, silence } from "@/lib/speech/voices";
import Courtroom, { type Flash, type LiveLine } from "./Courtroom";
import EvidencePanel from "./EvidencePanel";
import JuryBox from "./JuryBox";
import Lectern from "./Lectern";
import ObjectionBar from "./ObjectionBar";
import PhaseTracker from "./PhaseTracker";
import PriorTrialNotes from "./PriorTrialNotes";
import Transcript from "./Transcript";
import Verdict from "./Verdict";
import VoirDire from "./VoirDire";

const YOU = "Defense (You)";

/** Only what the server needs; keeps request bodies small. */
function wire(s: TrialState): TrialState {
  return { ...s, transcript: s.transcript.slice(-40), deliberation: null };
}

export default function Trial({ c }: { c: CaseFile }) {
  const [s, setS] = useState<TrialState | null>(null);
  const ref = useRef<TrialState | null>(null);
  const [pending, setPending] = useState(false);
  const [voices, setVoices] = useState(true);
  const [notice, setNotice] = useState<string | null>(null);
  const [model, setModel] = useState<string>("");
  const [motionId, setMotionId] = useState<string | null>(null);
  const [challenge, setChallenge] = useState<number | null>(null);
  const [gavel, setGavel] = useState(0);
  const [appealing, setAppealing] = useState(false);
  const [live, setLive] = useState<LiveLine | null>(null);
  const [flash, setFlash] = useState<Flash | null>(null);
  const [scene, setScene] = useState(true);
  const stamp = (kind: Flash["kind"], text: string) => setFlash({ kind, text, key: Date.now() });

  useEffect(() => {
    const saved = loadTrial(c.id);
    const init = saved ?? initTrial(c);
    ref.current = init;
    setS(init);
  }, [c]);

  const act = useCallback((a: Action) => {
    if (!ref.current) return;
    const n = reducer(ref.current, a);
    ref.current = n;
    setS(n);
    saveTrial(n);
  }, []);

  const send = useCallback(async (input: PlayerInput) => {
    const cur = ref.current;
    if (!cur) return;
    setPending(true);
    setNotice(null);
    try {
      const res = await fetch("/api/court", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ caseId: c.id, state: wire(cur), input }),
      });
      const data = (await res.json()) as { turn?: CourtTurn; model?: string; warning?: string; error?: string };
      if (!data.turn) throw new Error(data.error || "No response from the court");
      setModel(data.model ?? "");
      if (data.warning) setNotice(data.warning);
      if (data.turn.ruling) setGavel((g) => g + 1);
      act({ type: "turn", turn: data.turn, objectionByDefense: input.kind === "objection" });
      if (data.turn.prosecutorObjected) stamp("objection", "OBJECTION!");
      const lines = data.turn.lines;
      await playLines(lines, voices, (i) => setLive(i === null ? null : { speaker: lines[i].speaker, name: lines[i].name, text: lines[i].text }));
      const r = data.turn.ruling;
      if (r) {
        const k = r.result === "sustained" || r.result === "overruled" ? r.result : r.result === "denied" ? "denied" : "granted";
        stamp(k, r.result.toUpperCase().replace("-", " "));
      }
    } catch (e) {
      setNotice(e instanceof Error ? e.message : "The court is in recess (network error). Try again.");
    } finally {
      setPending(false);
    }
  }, [act, c.id, voices]);

  // Deliberation kicks off automatically once the jury is charged and sent out.
  const deliberating = useRef(false);
  useEffect(() => {
    if (!s || s.phase !== "deliberation" || deliberating.current) return;
    deliberating.current = true;
    (async () => {
      try {
        const res = await fetch("/api/deliberate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ caseId: c.id, state: { ...ref.current, deliberation: null } }),
        });
        const data = (await res.json()) as { result: Deliberation; warning?: string };
        if (data.warning) setNotice(data.warning);
        act({ type: "deliberated", result: data.result });
        const done = ref.current!;
        const outcome = outcomeOf(data.result, done.dismissedCounts);
        const pts = trialPoints(done, outcome);
        recordTrial(c.id, outcome, pts, grade(pts, outcome));
        setGavel((g) => g + 1);
      } catch {
        setNotice("Deliberation failed. Reload the page to try again.");
      } finally {
        deliberating.current = false;
      }
    })();
  }, [s, act, c.id]);

  if (!s) return <main className="p-8 text-ink">Opening the courtroom…</main>;

  const restart = () => {
    clearTrial(c.id);
    silence();
    const fresh = initTrial(c);
    ref.current = fresh;
    setS(fresh);
    setNotice(null);
  };

  // Mistrial on some counts: a new jury hears only those. Acquittals are final.
  const retrial = () => {
    const cur = ref.current;
    if (!cur) return;
    silence();
    const fresh = initRetrial(c, cur);
    ref.current = fresh;
    setS(fresh);
    saveTrial(fresh);
    setNotice(null);
  };

  const decided = (r: AppealRecord) => {
    const cur = ref.current!;
    const before = outcomeOf(cur.deliberation!, cur.dismissedCounts);
    act({ type: "appealed", appeal: r });
    const after = outcomeOf({ ...cur.deliberation!, verdicts: appliedVerdicts({ ...cur, appeal: r }) }, cur.dismissedCounts);
    const pts = trialPoints(cur, after) + r.points;
    recordAppeal(c.id, before, after, pts, grade(pts, after));
    setAppealing(false);
    setGavel((g) => g + 1);
  };

  if (s.phase === "verdict" && s.deliberation && appealing) {
    return <main className="px-4"><Appeal c={c} s={s} onDecided={decided} onBack={() => setAppealing(false)} /></main>;
  }
  if (s.phase === "verdict" && s.deliberation) {
    return <main className="px-4"><Verdict c={c} s={s} onRestart={restart} onRetrial={retrial} onAppeal={() => setAppealing(true)} /></main>;
  }

  const info = phaseInfo(s.phase);
  const witness = witnessById(c, s.currentWitness);
  const juryPresent = !JURY_ABSENT.includes(s.phase);
  const busy = pending || s.phase === "deliberation";

  const onSpeak = (text: string) => {
    silence();
    act({ type: "say", speaker: "defense", name: YOU, text });
    setLive({ speaker: "defense", name: YOU, text });
    const obj = detectObjection(text);
    if (obj) stamp("objection", "OBJECTION!");
    if (obj) return send({ kind: "objection", groundId: obj.ground?.id ?? null, text });
    if (s.phase === "pretrial" && motionId) { const m = motionId; setMotionId(null); return send({ kind: "motion", motionId: m, text }); }
    if (s.phase === "voir_dire" && challenge) {
      const id = challenge;
      setChallenge(null);
      return send({ kind: "challenge", jurorId: id, text }).then(() => {
        const r = ref.current?.rulings.at(-1);
        if (r?.result === "sustained" && r.on.includes(`#${id}`)) act({ type: "excuseForCause", jurorId: id });
      });
    }
    return send({ kind: "speech", text });
  };

  const object = (groundId: string) => {
    silence();
    const g = GROUNDS.find((x) => x.id === groundId)!;
    const text = `Objection, Your Honor — ${g.label.toLowerCase()}.`;
    act({ type: "say", speaker: "defense", name: YOU, text });
    setLive({ speaker: "defense", name: YOU, text });
    stamp("objection", "OBJECTION!");
    send({ kind: "objection", groundId, text });
  };

  const advance = () => { silence(); setMotionId(null); setChallenge(null); act({ type: "advance" }); };

  // ---- Phase controls -------------------------------------------------------
  const controls: React.ReactNode[] = [];
  const proceedBtn = (label = "Proceed") => (
    <button key="proceed" disabled={busy} onClick={() => send({ kind: "proceed" })} className="brass-btn">{label}</button>
  );
  const nextBtn = (label: string) => (
    <button key="next" disabled={busy} onClick={advance} className="ghost-btn">{label} →</button>
  );

  switch (s.phase) {
    case "arraignment":
      controls.push(proceedBtn("Call the case"), nextBtn("To pretrial motions"));
      break;
    case "pretrial":
      controls.push(nextBtn("To jury selection"));
      break;
    case "voir_dire":
      controls.push(proceedBtn("Judge addresses panel"), nextBtn("Seat the jury"));
      break;
    case "prosecution_opening":
      controls.push(proceedBtn("Prosecution opens"), nextBtn("Your opening"));
      break;
    case "defense_opening":
      controls.push(nextBtn("State calls first witness"));
      break;
    case "prosecution_case":
      if (!witness && s.witnessQueue.length) {
        const nextW = witnessById(c, s.witnessQueue[0])!;
        controls.push(
          <button key="call" disabled={busy} className="brass-btn" onClick={() => {
            act({ type: "callWitness", witnessId: nextW.id, mode: "direct" });
            act({ type: "say", speaker: "prosecutor", name: c.prosecutor.name, text: `The State calls ${nextW.name}.` });
            send({ kind: "proceed" });
          }}>State calls {nextW.name}</button>,
        );
      } else if (witness && s.examMode === "direct") {
        controls.push(
          proceedBtn("Let direct continue"),
          <button key="cross" disabled={busy} className="brass-btn" onClick={() => {
            act({ type: "setExam", mode: "cross" });
            act({ type: "say", speaker: "judge", name: `Judge ${bareJudge(c)}`, text: "Cross-examination, counsel?" });
          }}>Begin cross-examination</button>,
        );
      } else if (witness) {
        controls.push(
          <button key="nfq" disabled={busy} className="ghost-btn" onClick={() => {
            act({ type: "say", speaker: "defense", name: YOU, text: "No further questions, Your Honor." });
            act({ type: "excuseWitness" });
          }}>No further questions</button>,
        );
      } else {
        controls.push(nextBtn("The State rests: move for acquittal"));
      }
      break;
    case "rule29":
      controls.push(nextBtn("Open the defense case"));
      break;
    case "defense_case": {
      if (!witness) {
        const available = [...c.witnesses.filter((w) => w.side === "defense"), witnessById(c, DEFENDANT_ID)!].filter((w) => !s.defenseCalled.includes(w.id));
        available.forEach((w) =>
          controls.push(
            <button key={w.id} disabled={busy} className={w.id === DEFENDANT_ID ? "ghost-btn border-caution text-caution" : "ghost-btn"} onClick={() => {
              act({ type: "callWitness", witnessId: w.id, mode: "direct" });
              act({ type: "say", speaker: "defense", name: YOU, text: w.id === DEFENDANT_ID ? `The defense calls the defendant, ${w.name}.` : `The defense calls ${w.name}.` });
            }}>{w.id === DEFENDANT_ID ? `⚠ Put your client on the stand` : `Call ${w.name}`}</button>,
          ),
        );
        controls.push(nextBtn("The defense rests"));
      } else if (s.examMode === "direct" || s.examMode === "redirect") {
        controls.push(
          <button key="pass" disabled={busy} className="brass-btn" onClick={() => {
            act({ type: "say", speaker: "defense", name: YOU, text: "Pass the witness." });
            act({ type: "setExam", mode: "cross" });
            send({ kind: "proceed" });
          }}>Pass the witness</button>,
        );
      } else {
        controls.push(
          proceedBtn("Prosecutor continues cross"),
          <button key="redirect" disabled={busy} className="ghost-btn" onClick={() => act({ type: "setExam", mode: "redirect" })}>Redirect</button>,
          <button key="excuse" disabled={busy} className="ghost-btn" onClick={() => act({ type: "excuseWitness" })}>Excuse witness</button>,
        );
      }
      break;
    }
    case "prosecution_closing":
      controls.push(proceedBtn("Prosecution closes"), nextBtn("Your closing"));
      break;
    case "defense_closing":
      controls.push(nextBtn("Jury instructions"));
      break;
    case "instructions":
      controls.push(proceedBtn("Judge charges the jury"), nextBtn("Send the jury out"));
      break;
  }

  const lecternOpen =
    info.playerSpeaks &&
    !(s.phase === "prosecution_case" && (!witness || s.examMode === "direct")) &&
    !(s.phase === "defense_case" && (!witness || s.examMode === "cross"));
  const objectionsOpen = juryPresent && s.phase !== "deliberation";

  const placeholder =
    s.phase === "pretrial" ? (motionId ? "Argue the motion… cite the rule and the facts." : "Select a motion to argue first.")
    : s.phase === "voir_dire" ? (challenge ? `Argue why juror #${challenge} cannot be impartial…` : "Ask the panel a question…")
    : witness ? `Question ${witness.name}…`
    : "Address the court… (Enter to speak)";

  return (
    <main className="mx-auto flex min-h-screen max-w-7xl flex-col gap-3 px-4 py-4">
      <header className="flex flex-wrap items-center justify-between gap-2">
        <div>
          <Link href={`/case/${c.id}`} className="text-xs text-brass hover:underline">← Case file</Link>
          <h1 className="font-serif text-2xl font-bold leading-tight sm:text-3xl">{c.title}</h1>
          <p className="text-xs text-ink">{c.courtName} · Hon. {bareJudge(c)} presiding · For the State: {c.prosecutor.name}{s.bail ? ` · Client ${s.bail}` : ""}</p>
          {s.retrial && (
            <p className="mt-1 text-xs text-caution">
              Retrial · round {s.retrial.round} · Acquitted last time: {acquittedCounts(s).map((id) => c.charges.find((x) => x.id === id)?.name ?? id).join(", ")} · Still on trial: {c.charges.filter((x) => !acquittedCounts(s).includes(x.id)).map((x) => x.name).join(", ")}
            </p>
          )}
        </div>
        <div className="flex items-center gap-2 text-xs">
          <span key={gavel} className={gavel ? "gavel-strike text-2xl" : "text-2xl"}>🔨</span>
          <label className="flex items-center gap-1 text-ink">
            <input type="checkbox" checked={voices} onChange={(e) => { setVoices(e.target.checked); if (!e.target.checked) silence(); }} className="accent-[#c9a45c]" />
            Court voices
          </label>
          <label className="flex items-center gap-1 text-ink">
            <input type="checkbox" checked={scene} onChange={(e) => setScene(e.target.checked)} className="accent-[#c9a45c]" />
            Live scene
          </label>
          <button onClick={() => { if (confirm("Restart this trial from arraignment?")) restart(); }} className="ghost-btn px-2 py-1 text-xs">Restart</button>
        </div>
      </header>

      <PhaseTracker phase={s.phase} />

      <div className="grid flex-1 gap-3 lg:grid-cols-[1fr_360px]">
        <div className="flex min-h-0 flex-col gap-3">
          <div className="panel flex items-start gap-3 p-3">
            <div className="flex-1">
              <p className="font-serif text-lg text-brass">{info.label}</p>
              <p className="text-sm text-ink">{info.hint}</p>
            </div>
            {witness && (
              <div className="rounded-md border border-sky-800 bg-sky-950/40 px-3 py-1.5 text-right text-xs">
                <p className="text-ink">On the stand · {s.examMode}</p>
                <p className="font-semibold text-sky-200">{witness.name}</p>
                <p className="text-ink">{witness.role}</p>
              </div>
            )}
          </div>

          {scene && <Courtroom c={c} s={s} witness={witness} live={live} flash={flash} juryPresent={juryPresent} />}
          <div className={`panel p-4 ${scene ? "h-[30vh] min-h-56" : "h-[46vh] min-h-72 lg:h-[56vh]"}`}>
            <Transcript lines={s.transcript} pending={busy} />
          </div>

          {s.phase === "pretrial" && (
            <div className="panel p-3">
              <h3 className="mb-2 font-serif text-lg">Motions calendar</h3>
              <div className="flex flex-wrap gap-2">
                {c.pretrialMotions.map((m) => {
                  const heard = s.motionsHeard[m.name];
                  const lastTime = s.retrial?.prior?.at(-1)?.motionsHeard[m.name];
                  const carried = !!lastTime && lastTime !== "denied"; // law of the case: granted rulings stand
                  return (
                    <button key={m.id} disabled={busy || !!heard} onClick={() => setMotionId(motionId === m.id ? null : m.id)}
                      title={carried ? `${lastTime} in trial ${s.retrial!.prior.at(-1)!.round}. The ruling stands.` : lastTime === "denied" ? `Denied in trial ${s.retrial!.prior.at(-1)!.round}. Re-argue only with new grounds.` : m.basis}
                      className={`rounded-md border px-3 py-1.5 text-left text-xs ${motionId === m.id ? "border-brass bg-brass/15" : "border-wood-600"} disabled:opacity-60`}>
                      {m.name}
                      {heard && <span className={`ml-1 font-semibold ${heard === "denied" ? "text-guilty" : "text-acquit"}`}>· {heard}{carried ? " (trial " + s.retrial!.prior.at(-1)!.round + ")" : ""}</span>}
                      {!heard && lastTime === "denied" && <span className="ml-1 text-caution">· denied last time</span>}
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {s.phase === "voir_dire" && (
            <VoirDire jurors={s.jurors} peremptoriesLeft={s.peremptoriesLeft} challengeTarget={challenge}
              onStrike={(id) => act({ type: "strike", jurorId: id })} onChallenge={setChallenge} disabled={busy} />
          )}

          {s.phase === "deliberation" && (
            <div className="panel p-6 text-center">
              <p className="animate-pulse font-serif text-2xl text-brass">The jury is deliberating…</p>
              <p className="text-sm text-ink">Twelve people are deciding your client&apos;s future.</p>
            </div>
          )}

          {notice && (
            <p className="rounded-md border border-caution/40 bg-caution/10 px-3 py-2 text-xs text-caution">
              {notice}
              {/unavailable/i.test(notice) && <> · <a href="/api/health" target="_blank" rel="noreferrer" className="underline">Run AI diagnostics</a></>}
            </p>
          )}

          <div className="flex flex-wrap items-center gap-2">
            {controls}
            {model && <span className="ml-auto text-[10px] text-ink/60">court engine: {model}</span>}
          </div>

          {lecternOpen && (
            <Lectern onSubmit={onSpeak} onObjectionHeard={silence} disabled={busy || (s.phase === "pretrial" && !motionId)} placeholder={placeholder} />
          )}
        </div>

        <aside className="flex flex-col gap-3">
          <JuryBox jurors={s.jurors} />
          {objectionsOpen && <ObjectionBar onObject={object} disabled={busy} />}
          {!lecternOpen && objectionsOpen && (
            <Lectern onSubmit={onSpeak} onObjectionHeard={silence} disabled={busy} placeholder="Say “Objection, …” or address the court" />
          )}
          <PriorTrialNotes c={c} s={s} />
          <EvidencePanel c={c} admitted={s.admitted} excluded={s.excluded} />
          <div className="panel p-3 text-xs">
            <h3 className="mb-1 font-serif text-lg">Running score</h3>
            <p>Points: <b className="text-brass">{s.score.reduce((a, e) => a + e.points, 0)}</b> · Objections {s.objections.sustained}/{s.objections.made} · Exposed {s.revealed.length} · Contempt {s.contempt}</p>
            <ul className="scrollbar-thin mt-1 max-h-28 space-y-0.5 overflow-y-auto">
              {[...s.score].reverse().slice(0, 12).map((e, i) => (
                <li key={i} className="flex justify-between gap-2"><span className="truncate">{e.label}</span><span className={e.points >= 0 ? "text-acquit" : "text-guilty"}>{e.points > 0 ? "+" : ""}{e.points}</span></li>
              ))}
            </ul>
          </div>
        </aside>
      </div>
    </main>
  );
}
