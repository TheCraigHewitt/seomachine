// Diagnostics: open /api/health to see whether the AI court is configured and reachable.
import fs from "node:fs";
import path from "node:path";
import { NextResponse } from "next/server";
import { z } from "zod";
import { callSingleModel, hasKey, maskedKey, models } from "@/lib/ai/openrouter";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const Ping = z.object({ ok: z.boolean() });

async function ping(model: string) {
  const started = Date.now();
  try {
    await callSingleModel(model, {
      schema: Ping,
      schemaName: "ping",
      system: "You are a health check.",
      user: 'Reply with {"ok": true}.',
      maxTokens: 20,
      temperature: 0,
      timeoutMs: 20000,
    });
    return { ok: true, ms: Date.now() - started };
  } catch (e) {
    return { ok: false, error: e instanceof Error ? e.message : String(e) };
  }
}

// Literal paths (not a loop) so the bundler doesn't trace the whole project folder.
function envFilesFound(): string[] {
  const found: string[] = [];
  if (fs.existsSync(path.join(process.cwd(), ".env.local"))) found.push(".env.local");
  if (fs.existsSync(path.join(process.cwd(), ".env"))) found.push(".env");
  if (fs.existsSync(path.join(process.cwd(), ".env.development.local"))) found.push(".env.development.local");
  if (fs.existsSync(path.join(process.cwd(), ".env.local.txt"))) found.push(".env.local.txt");
  if (fs.existsSync(path.join(process.cwd(), ".env.txt"))) found.push(".env.txt");
  return found;
}

export async function GET() {
  const envFiles = envFilesFound();
  const m = models();
  const report: Record<string, unknown> = {
    projectFolder: process.cwd(),
    envFilesFound: envFiles,
    keyLoaded: hasKey(),
    keyPreview: maskedKey(),
    models: m,
  };
  const hints: string[] = [];
  if (envFiles.some((f) => f.endsWith(".txt"))) hints.push("Rename the .txt env file to exactly `.env.local` (Windows hides the .txt extension).");
  if (!hasKey()) {
    if (!envFiles.length) hints.push(`No env file in ${process.cwd()}. Create .env.local there (next to package.json).`);
    hints.push("OPENROUTER_API_KEY isn't loaded. Put `OPENROUTER_API_KEY=sk-or-...` in .env.local, then stop (Ctrl+C) and restart `npm run dev`.");
  } else {
    const [fast, light] = await Promise.all([ping(m.fast), ping(m.light)]);
    report.fastModel = fast;
    report.lightModel = light;
    if (fast.ok && light.ok) hints.push("All good: the AI court is live.");
    else if (fast.ok || light.ok) hints.push("One model works, so the court runs, but fix the failing model ID for speed and reliability.");
    else hints.push("Neither model answered. The court falls back to offline mode until the error above is fixed.");
  }
  report.hints = hints;
  return NextResponse.json(report, { headers: { "Cache-Control": "no-store" } });
}
