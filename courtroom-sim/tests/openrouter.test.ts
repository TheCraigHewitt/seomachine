import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { callModel } from "@/lib/ai/openrouter";
import { coerceDeliberation, coerceTurn, CourtTurn, Deliberation } from "@/lib/engine/schema";

const valid = {
  lines: [{ speaker: "judge", name: "Judge X", text: "Overruled." }],
  ruling: { on: "Hearsay", result: "overruled", reason: "Not offered for truth.", favorsDefense: false },
  prosecutorObjected: false, evidenceAdmitted: [], evidenceExcluded: [], factsRevealed: [], jurorReactions: [],
  scoreEvents: [], jurorsRevealed: [], contemptWarning: false, witnessExcused: false, countsDismissed: [],
};
const reply = (content: string, status = 200) =>
  new Response(JSON.stringify({ choices: [{ message: { content } }] }), { status });

const opts = { schema: CourtTurn, schemaName: "court_turn", system: "s", user: "u" };

describe("callModel", () => {
  beforeEach(() => {
    process.env.OPENROUTER_API_KEY = "test";
    process.env.COURT_MODEL_FAST = "fast/model";
    process.env.COURT_MODEL_LIGHT = "light/model";
  });
  afterEach(() => vi.unstubAllGlobals());

  it("returns typed data from the fast model and requests a JSON schema", async () => {
    const fetch = vi.fn().mockResolvedValue(reply("```json\n" + JSON.stringify(valid) + "\n```"));
    vi.stubGlobal("fetch", fetch);
    const r = await callModel(opts);
    expect(r).toMatchObject({ model: "fast/model", fellBack: false });
    expect(r.data.lines[0].text).toBe("Overruled.");
    const body = JSON.parse(fetch.mock.calls[0][1].body);
    expect(body.model).toBe("fast/model");
    expect(body.response_format.type).toBe("json_schema");
  });

  it("falls back to the lightweight model on HTTP error or schema mismatch", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValueOnce(reply("", 503)).mockResolvedValueOnce(reply(JSON.stringify(valid))));
    expect(await callModel(opts)).toMatchObject({ model: "light/model", fellBack: true });

    vi.stubGlobal("fetch", vi.fn().mockResolvedValueOnce(reply(JSON.stringify({ lines: "nope" }))).mockResolvedValueOnce(reply(JSON.stringify(valid))));
    expect(await callModel(opts)).toMatchObject({ model: "light/model", fellBack: true });
  });

  it("prefers the light model when asked, and throws when both fail", async () => {
    const fetch = vi.fn().mockImplementation(async () => reply(JSON.stringify(valid)));
    vi.stubGlobal("fetch", fetch);
    await callModel({ ...opts, prefer: "light" });
    expect(JSON.parse(fetch.mock.calls[0][1].body).model).toBe("light/model");

    vi.stubGlobal("fetch", vi.fn().mockImplementation(async () => reply("", 500)));
    await expect(callModel(opts)).rejects.toThrow(/fast\/model.*light\/model/);
  });
});

describe("hardening against real-world model replies", () => {
  beforeEach(() => {
    process.env.OPENROUTER_API_KEY = ' "sk-or-test" ';
    process.env.COURT_MODEL_FAST = "fast/model";
    process.env.COURT_MODEL_LIGHT = "light/model";
  });
  afterEach(() => vi.unstubAllGlobals());

  it("coerces a sloppy reply (missing fields, capitalised enums, string numbers, wrapper key)", async () => {
    const sloppy = {
      court_turn: {
        lines: [{ speaker: "Judge", name: "Judge X", text: "Sustained." }, { speaker: "Prosecution", name: "ADA", text: "Withdrawn." }],
        ruling: { on: "Leading", result: "SUSTAINED", reason: "611(c)", favorsDefense: "true" },
        jurorReactions: [{ seat: "3", delta: "4", reason: "liked it" }],
      },
    };
    vi.stubGlobal("fetch", vi.fn().mockImplementation(async () => reply(JSON.stringify(sloppy))));
    const r = await callModel({ ...opts, prepare: coerceTurn });
    expect(r.fellBack).toBe(false);
    expect(r.data.lines.map((l) => l.speaker)).toEqual(["judge", "prosecutor"]);
    expect(r.data.ruling).toMatchObject({ result: "sustained", favorsDefense: true });
    expect(r.data.jurorReactions[0]).toEqual({ seat: 3, delta: 4, reason: "liked it" });
    expect(r.data.evidenceAdmitted).toEqual([]);
  });

  it("retries with json_object when a provider rejects json_schema, and strips quotes from the key", async () => {
    const fetch = vi.fn()
      .mockImplementationOnce(async () => new Response(JSON.stringify({ error: { message: "response_format json_schema is not supported" } }), { status: 400 }))
      .mockImplementationOnce(async () => reply(JSON.stringify(valid)));
    vi.stubGlobal("fetch", fetch);
    const r = await callModel({ ...opts, prepare: coerceTurn });
    expect(r).toMatchObject({ model: "fast/model", fellBack: false });
    expect(JSON.parse(fetch.mock.calls[1][1].body).response_format).toEqual({ type: "json_object" });
    expect(fetch.mock.calls[0][1].headers.Authorization).toBe("Bearer sk-or-test");
  });

  it("explains a bad key and doesn't wait on the second model", async () => {
    const fetch = vi.fn().mockImplementation(async () => new Response('{"error":{"message":"No auth"}}', { status: 401 }));
    vi.stubGlobal("fetch", fetch);
    await expect(callModel(opts)).rejects.toThrow(/rejected the API key/);
    expect(fetch).toHaveBeenCalledTimes(1);
  });

  it("explains an unknown model id", async () => {
    vi.stubGlobal("fetch", vi.fn().mockImplementation(async () => new Response('{"error":{"message":"jev is not a valid model ID"}}', { status: 400 })));
    await expect(callModel(opts)).rejects.toThrow(/doesn't exist on OpenRouter/);
  });

  it("coerces deliberation verdict wording", () => {
    const d = Deliberation.parse(coerceDeliberation({ verdicts: [{ chargeId: "murder", result: "Not Guilty", votesNotGuilty: "12" }], transcript: [] }));
    expect(d.verdicts[0]).toMatchObject({ result: "not-guilty", votesNotGuilty: 12, lesser: null });
  });
});
