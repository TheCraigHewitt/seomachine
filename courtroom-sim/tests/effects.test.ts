import fs from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";

const root = path.join(import.meta.dirname, "..");
const files = ["components", "lib"].flatMap((d) =>
  fs.readdirSync(path.join(root, d), { recursive: true, encoding: "utf8" })
    .filter((f) => /\.tsx?$/.test(f))
    .map((f) => path.join(d, f)),
);

describe("useEffect bodies", () => {
  it.each(files)("%s never returns an expression from an effect", (file) => {
    // An expression-bodied effect returns its value; if that's a Promise (e.g. scrollIntoView
    // in current Chrome), React crashes with "destroy is not a function".
    const src = fs.readFileSync(path.join(root, file), "utf8");
    expect(src).not.toMatch(/useEffect\(\s*\(\)\s*=>\s*[^{\s]/);
  });
});
