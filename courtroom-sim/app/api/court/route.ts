import { NextResponse } from "next/server";
import { getCase } from "@/lib/cases";
import { callModel, hasKey } from "@/lib/ai/openrouter";
import { mockTurn } from "@/lib/ai/mock";
import { systemPrompt, turnPrompt, type PlayerInput } from "@/lib/engine/prompts";
import { coerceTurn, CourtTurn, sanitizeTurn } from "@/lib/engine/schema";
import { JURY_ABSENT } from "@/lib/engine/phases";
import { activeCase, type TrialState } from "@/lib/engine/state";

export const runtime = "nodejs";

interface Body { caseId: string; state: TrialState; input: PlayerInput }

export async function POST(req: Request) {
  const body = (await req.json()) as Body;
  const full = getCase(body.caseId);
  if (!full || !body.state || !body.input) return NextResponse.json({ error: "Bad request" }, { status: 400 });
  const s = body.state;
  const c = activeCase(full, s); // on a retrial, acquitted counts are gone
  const opts = {
    juryPresent: !JURY_ABSENT.includes(s.phase),
    validEvidence: new Set(c.evidence.map((e) => e.id)),
    validCharges: new Set(c.charges.map((x) => x.id)),
  };

  if (!hasKey()) {
    return NextResponse.json({ turn: sanitizeTurn(mockTurn(c, s, body.input), opts), model: "offline-mock", fellBack: false });
  }
  try {
    // Voir dire panel chatter is low-stakes: send it to the lightweight model first.
    const prefer = s.phase === "voir_dire" && body.input.kind === "speech" ? "light" : "fast";
    const r = await callModel({
      schema: CourtTurn,
      schemaName: "court_turn",
      prepare: coerceTurn,
      system: systemPrompt(c),
      user: turnPrompt(c, s, body.input),
      prefer,
    });
    return NextResponse.json({ turn: sanitizeTurn(r.data, opts), model: r.model, fellBack: r.fellBack });
  } catch (e) {
    const reason = e instanceof Error ? e.message : String(e);
    console.error("[court] AI turn failed:", reason);
    // Keep the trial moving rather than dead-ending the player.
    return NextResponse.json({
      turn: sanitizeTurn(mockTurn(c, s, body.input), opts),
      model: "offline-mock",
      fellBack: true,
      warning: `AI court unavailable, so the offline court answered. Reason: ${reason}`,
    });
  }
}
