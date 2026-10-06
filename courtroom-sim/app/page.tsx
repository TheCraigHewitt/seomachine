import { listCases } from "@/lib/cases";
import { hasKey, models } from "@/lib/ai/openrouter";
import CareerHub from "@/components/CareerHub";

export const dynamic = "force-dynamic";

export default function Home() {
  const cases = listCases().map(({ id, title, tier, category, tagline, jurisdiction, basedOn, charges }) => ({
    id, title, tier, category, tagline, jurisdiction,
    basedOn: `${basedOn.name} (${basedOn.year})`,
    charges: charges.map((c) => c.name),
  }));
  return <CareerHub cases={cases} ai={hasKey() ? models().fast : null} />;
}
