// OpenRouter client with a fast primary model and a lightweight fallback.
// Output is requested as JSON (json_schema, or json_object for models that reject schemas),
// coerced toward the schema, then validated with zod — callers get a typed value or an error.
import { z } from "zod";

const ENDPOINT = "https://openrouter.ai/api/v1/chat/completions";

export type Tier = "fast" | "light";

export const models = () => ({
  fast: process.env.COURT_MODEL_FAST?.trim() || "google/gemini-2.5-flash",
  light: process.env.COURT_MODEL_LIGHT?.trim() || "meta-llama/llama-3.1-8b-instruct",
});

/** Tolerates quotes and whitespace people often paste around keys in .env files. */
const apiKey = () => (process.env.OPENROUTER_API_KEY ?? "").trim().replace(/^["']|["']$/g, "");
export const hasKey = () => apiKey().length > 0;

interface CallOpts<T extends z.ZodType> {
  schema: T;
  schemaName: string;
  system: string;
  user: string;
  /** Loosely reshapes the parsed JSON before validation (fill defaults, fix enum casing). */
  prepare?: (raw: unknown) => unknown;
  /** Which model to try first. The other one is the fallback. */
  prefer?: Tier;
  temperature?: number;
  maxTokens?: number;
  timeoutMs?: number;
}

export interface CallResult<T> {
  data: T;
  model: string;
  fellBack: boolean;
}

export class ModelError extends Error {}

function extractJson(text: string): unknown {
  const trimmed = text.trim().replace(/^```(?:json)?\s*/i, "").replace(/```$/, "");
  const start = trimmed.indexOf("{");
  const end = trimmed.lastIndexOf("}");
  return JSON.parse(start >= 0 && end > start ? trimmed.slice(start, end + 1) : trimmed);
}

/** Turns OpenRouter HTTP failures into a message a player can act on. */
function explain(model: string, status: number, body: string): string {
  const detail = (() => {
    try { return (JSON.parse(body) as { error?: { message?: string } }).error?.message ?? body; } catch { return body; }
  })().slice(0, 200);
  if (status === 401) return "OpenRouter rejected the API key (401). Check OPENROUTER_API_KEY in .env.local.";
  if (status === 402) return "OpenRouter account is out of credits (402). Add credits at openrouter.ai/credits.";
  if (status === 429) return `${model}: rate limited (429). Wait a moment or pick another model.`;
  if (/not a valid model|model.*not found|no endpoints/i.test(detail)) return `Model "${model}" doesn't exist on OpenRouter. Fix COURT_MODEL_FAST / COURT_MODEL_LIGHT.`;
  return `${model}: HTTP ${status} ${detail}`;
}

const FORMAT_REJECTED = /response_format|json_schema|structured|schema/i;

async function callOnce<T extends z.ZodType>(model: string, o: CallOpts<T>, timeoutMs: number): Promise<z.infer<T>> {
  const { $schema: _drop, ...jsonSchema } = z.toJSONSchema(o.schema, { target: "draft-7" }) as Record<string, unknown>;
  const request = (format: "json_schema" | "json_object") =>
    fetch(ENDPOINT, {
      method: "POST",
      signal: AbortSignal.timeout(timeoutMs),
      headers: {
        Authorization: `Bearer ${apiKey()}`,
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "Defense Counsel Courtroom Sim",
      },
      body: JSON.stringify({
        model,
        temperature: o.temperature ?? 0.8,
        max_tokens: o.maxTokens ?? 1800,
        response_format:
          format === "json_schema"
            ? { type: "json_schema", json_schema: { name: o.schemaName, strict: false, schema: jsonSchema } }
            : { type: "json_object" },
        messages: [
          { role: "system", content: `${o.system}\n\nRespond with ONE JSON object matching this JSON Schema (no prose, no markdown):\n${JSON.stringify(jsonSchema)}` },
          { role: "user", content: o.user },
        ],
      }),
    });

  let res = await request("json_schema");
  if (!res.ok && res.status === 400) {
    const body = await res.text();
    // Some providers don't support json_schema; the schema is also in the prompt, so plain JSON mode works.
    if (!FORMAT_REJECTED.test(body)) throw new ModelError(explain(model, res.status, body));
    res = await request("json_object");
  }
  if (!res.ok) throw new ModelError(explain(model, res.status, await res.text()));

  const body = (await res.json()) as { choices?: Array<{ message?: { content?: string } }>; error?: { message?: string } };
  if (body.error) throw new ModelError(`${model}: ${body.error.message}`);
  const content = body.choices?.[0]?.message?.content;
  if (!content) throw new ModelError(`${model}: empty response`);
  let raw: unknown;
  try { raw = extractJson(content); } catch { throw new ModelError(`${model}: reply wasn't JSON — "${content.slice(0, 80)}…"`); }
  const parsed = o.schema.safeParse(o.prepare ? o.prepare(raw) : raw);
  if (!parsed.success) throw new ModelError(`${model}: reply didn't match the court schema — ${parsed.error.message.slice(0, 200)}`);
  return parsed.data;
}

function describe(e: unknown, model: string): string {
  if (e instanceof ModelError) return e.message;
  if (e instanceof Error && (e.name === "TimeoutError" || e.name === "AbortError")) return `${model}: timed out`;
  return `${model}: ${e instanceof Error ? e.message : String(e)}`;
}

/** One model, no fallback — used by the diagnostics page. */
export async function callSingleModel<T extends z.ZodType>(model: string, o: CallOpts<T>): Promise<z.infer<T>> {
  try {
    return await callOnce(model, o, o.timeoutMs ?? 20000);
  } catch (e) {
    throw new ModelError(describe(e, model));
  }
}

export const maskedKey = () => { const k = apiKey(); return k ? `${k.slice(0, 8)}…${k.slice(-4)} (${k.length} chars)` : null; };

export async function callModel<T extends z.ZodType>(o: CallOpts<T>): Promise<CallResult<z.infer<T>>> {
  const m = models();
  const order: Tier[] = o.prefer === "light" ? ["light", "fast"] : ["fast", "light"];
  const timeout = o.timeoutMs ?? (Number(process.env.COURT_MODEL_TIMEOUT_MS) || 20000);
  const errors: string[] = [];
  for (const [i, tier] of order.entries()) {
    try {
      // The fallback gets extra time: it's the last chance before the turn fails.
      const data = await callOnce(m[tier], o, i === 0 ? timeout : timeout * 2);
      return { data, model: m[tier], fellBack: i > 0 };
    } catch (e) {
      errors.push(describe(e, m[tier]));
      // A bad key or empty balance fails the same way on every model — don't wait twice.
      if (/\(401\)|\(402\)/.test(errors.at(-1)!)) break;
    }
  }
  throw new ModelError(errors.join(" | "));
}
