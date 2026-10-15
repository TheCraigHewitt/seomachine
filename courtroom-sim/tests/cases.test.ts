import fs from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";
import type { CaseFile } from "@/lib/engine/caseTypes";

const dir = path.join(import.meta.dirname, "..", "data", "cases");
const files = fs.readdirSync(dir).filter((f) => f.endsWith(".json"));

describe.each(files)("case file %s", (file) => {
  const c = JSON.parse(fs.readFileSync(path.join(dir, file), "utf8")) as CaseFile;
  it("is well-formed", () => {
    expect(`${c.id}.json`).toBe(file);
    expect([1, 2, 3]).toContain(c.tier);
    expect(c.charges.length).toBeGreaterThan(0);
    c.charges.forEach((ch) => expect(ch.elements.length).toBeGreaterThan(0));
    expect(c.witnesses.filter((w) => w.side === "prosecution").length).toBeGreaterThan(0);
    expect(c.startingLean).toBeGreaterThanOrEqual(0);
    expect(c.startingLean).toBeLessThanOrEqual(100);
    expect(c.basedOn.sources.length).toBeGreaterThan(0);
  });
  it("has unique ids and valid references", () => {
    const ev = new Set(c.evidence.map((e) => e.id));
    const wi = c.witnesses.map((w) => w.id);
    expect(ev.size).toBe(c.evidence.length);
    expect(new Set(wi).size).toBe(wi.length);
    expect(wi).not.toContain("defendant");
    c.pretrialMotions.forEach((m) => (m.targets ?? []).forEach((t) => expect(ev, `${m.id} -> ${t}`).toContain(t)));
  });
  it("keeps real names out of the playable narrative", () => {
    const COMMON = new Set(["State", "People", "Commonwealth", "United", "States", "Central", "Park", "Five", "Exonerated", "Marie", "Florida", "Maryland", "Wisconsin", "Georgia", "California", "Massachusetts", "Illinois", "America"]);
    const realName = (c.basedOn.name.split(/\bv\.?\s/)[1] ?? "")
      .split(/[^A-Za-z]+/)
      .filter((w) => /^[A-Z][a-z]{3,}$/.test(w) && !COMMON.has(w));
    // Character names and narrative only: legal citations (e.g. "United States v. Mejia" as precedent) are fine.
    const playable = JSON.stringify([
      c.title, c.tagline, c.caseSummary, c.prosecutionTheory, c.defendant, c.judge.name, c.prosecutor.name,
      c.witnesses.map((w) => [w.name, w.publicTestimony, w.hiddenFacts, w.priorStatements]),
    ]);
    realName.forEach((n) => expect(playable.includes(n), `real name "${n}" leaked`).toBe(false));
  });
});
