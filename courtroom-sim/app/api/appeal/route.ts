import { NextResponse } from "next/server";
import { getCase } from "@/lib/cases";
import { callModel, hasKey } from "@/lib/ai/openrouter";
import { mockAppeal } from "@/lib/ai/mock";
import { AppealOpinion, appealPoints, coerceAppeal, finalizeAppeal } from "@/lib/engine/appeal";
import { appealPrompt } from "@/lib/engine/prompts";
import { activeCase, type TrialState } from "@/lib/engine/state";

export const runtime = "nodejs";

interface Body { caseId: string; state: TrialState; brief: string }

export async function POST(req: Request) {
  const { caseId, state, brief } = (await req.json()) as Body;
  const full = getCase(caseId);
  if (!full || !state?.deliberation || typeof brief !== "string" || brief.trim().length < 200) {
    return NextResponse.json({ error: "A brief of at least 200 characters and a decided trial are required." }, { status: 400 });
  }
  const c = activeCase(full, state);
  const done = (o: AppealOpinion, model: string, warning?: string) => {
    const opinion = finalizeAppeal(c, state.deliberation!, o);
    return NextResponse.json({ opinion, points: appealPoints(opinion), model, warning });
  };
  if (!hasKey()) return done(mockAppeal(c, state, brief), "offline-mock");
  try {
    const r = await callModel({
      schema: AppealOpinion,
      schemaName: "appeal_opinion",
      prepare: coerceAppeal,
      timeoutMs: 60000,
      system: "You are an appellate court. You decide appeals on the record and the law, and you write in a court's voice. Output only JSON.",
      user: appealPrompt(c, state, brief),
      temperature: 0.4,
      maxTokens: 4000,
    });
    return done(r.data, r.model);
  } catch (e) {
    const reason = e instanceof Error ? e.message : String(e);
    console.error("[appeal] failed:", reason);
    return done(mockAppeal(c, state, brief), "offline-mock", `AI panel unavailable; an offline panel ruled. Reason: ${reason}`);
  }
}
