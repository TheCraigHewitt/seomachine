import type { CaseFile } from "@/lib/engine/caseTypes";

export default function EvidencePanel({ c, admitted, excluded }: { c: CaseFile; admitted: string[]; excluded: string[] }) {
  return (
    <div className="panel p-3">
      <h3 className="mb-2 font-serif text-lg">Exhibits</h3>
      <ul className="space-y-1 text-xs">
        {c.evidence.map((e) => {
          const st = excluded.includes(e.id) ? "excluded" : admitted.includes(e.id) ? "admitted" : "pending";
          return (
            <li key={e.id} className="flex items-start gap-2" title={e.description}>
              <span className={`mt-0.5 shrink-0 rounded px-1 text-[10px] uppercase ${st === "excluded" ? "bg-acquit/20 text-acquit line-through" : st === "admitted" ? "bg-guilty/20 text-guilty" : "bg-wood-700 text-ink"}`}>{st}</span>
              <span className={st === "excluded" ? "text-ink line-through" : ""}>{e.name}</span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
