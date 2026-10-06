import "server-only";
import fs from "node:fs";
import path from "node:path";
import type { CaseFile } from "./engine/caseTypes";

const DIR = path.join(process.cwd(), "data", "cases");

export function listCases(): CaseFile[] {
  if (!fs.existsSync(DIR)) return [];
  return fs
    .readdirSync(DIR)
    .filter((f) => f.endsWith(".json"))
    .map((f) => JSON.parse(fs.readFileSync(path.join(DIR, f), "utf8")) as CaseFile)
    .sort((a, b) => a.tier - b.tier || a.title.localeCompare(b.title));
}

export function getCase(id: string): CaseFile | null {
  if (!/^[a-z0-9-]+$/.test(id)) return null;
  const file = path.join(DIR, `${id}.json`);
  return fs.existsSync(file) ? (JSON.parse(fs.readFileSync(file, "utf8")) as CaseFile) : null;
}
