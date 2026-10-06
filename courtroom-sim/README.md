# Defense Counsel: Courtroom Simulator

A voice-driven criminal defense game. You are defense counsel. You speak into your mic at the lectern and object in real time, and you cross-examine witnesses who hide facts until you ask the right question. Twelve jurors react live to everything that happens, and an AI plays the judge, the prosecutor, the witnesses and the jury.

The cases are **fictionalized** versions of real prosecutions: gang and RICO cases, murders, and self-defense shootings. The names are invented. After your verdict, a debrief compares your result with what happened in the real case and links the sources.

## Run it

```bash
cd courtroom-sim
npm install
cp .env.example .env.local   # add your OpenRouter key
npm run dev                  # http://localhost:3000
```

Without an `OPENROUTER_API_KEY` the game runs on an **offline court**: a rule-based engine that still reveals hidden facts, rules on motions and objections, and moves the jury. You can use it to try the game or to develop without a key.

The live mic uses the Web Speech API, so use **Chrome, Edge or Safari** and allow microphone access. Firefox falls back to typing. To object, say "Objection, hearsay" (or any other ground) or tap a button. The judge rules immediately.

## AI models (OpenRouter)

| Env var | Role |
|---|---|
| `COURT_MODEL_FAST` | Primary model. Handles every courtroom turn and the jury deliberation. Pick a fast model that supports structured JSON output. |
| `COURT_MODEL_LIGHT` | Lightweight model. It is the fallback when the primary errors, times out (`COURT_MODEL_TIMEOUT_MS`) or returns invalid JSON. It also answers voir dire panel questions first. |

**Is the AI working?** Open http://localhost:3000/api/health. It shows whether your key was loaded (masked), which env files it found, and a live test of each model with the exact error if one fails (bad key, no credits, unknown model ID, network). If a courtroom turn falls back to the offline court, the warning on screen gives the reason too.

The output is type-safe end to end. Each request sends a JSON Schema generated from zod (`lib/engine/schema.ts`), and each response is validated against the same zod schema. Out-of-range values are then clamped (`sanitizeTurn`), so a misbehaving model can't break the game. If both models fail, the offline court handles that turn so the trial keeps going.

## How a trial works

Arraignment & bail → pretrial motions (suppression, 403/404(b), Daubert) → voir dire (question the panel, 3 peremptories, for-cause challenges) → openings → the State's case (you object and cross) → Rule 29 motion → defense case (including whether your client testifies) → closings → jury instructions → deliberation → verdict → real-case debrief.

- **Jury meter:** each seated juror has a lean from 0 (guilty) to 100 (not guilty) that is shaped by a hidden bias. Hover a juror to see their last reaction. The reasonable-doubt gauge and the "if they voted now" tally update live.
- **Hidden facts:** witnesses carry facts the case file doesn't show you. Only a pointed question brings them out, and each one you expose moves the jury.
- **Scoring & career:** your grade comes from the verdict plus your advocacy (objection accuracy, impeachments, motions won, contempt warnings). Ranks run from Public Defender to Legend of the Bar. Tier II unlocks after 1 acquittal and Tier III after 3; practice mode unlocks everything.

## Layout

```
app/                 pages + API routes (/api/court, /api/deliberate)
components/          courtroom UI (Trial orchestrator, JuryBox, Lectern, ObjectionBar…)
lib/engine/          phases, reducer, jurors, objections, prompts, zod schema, scoring
lib/ai/              OpenRouter client (fast → light fallback) and offline mock court
lib/speech/          mic (SpeechRecognition) and per-role court voices (speechSynthesis)
data/cases/*.json    case files (schema: lib/engine/caseTypes.ts)
tests/               vitest: engine, case-file validation, model fallback
```

To add a case, drop a JSON file matching `CaseFile` into `data/cases/`. `npm test` checks its references and that real names stay inside `basedOn`.

## Checks

```bash
npm run lint   # tsc --noEmit
npm test       # vitest
npm run build
```

Deploy to Netlify (see the repo-root `netlify.toml`) or Vercel, and set the env vars there.

Educational game, not legal advice.
