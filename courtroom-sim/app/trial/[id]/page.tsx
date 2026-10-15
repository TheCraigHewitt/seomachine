import { notFound } from "next/navigation";
import { getCase } from "@/lib/cases";
import { publicCase } from "@/lib/engine/witness";
import Trial from "@/components/Trial";

export const dynamic = "force-dynamic";

export default async function TrialPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const c = getCase(id);
  if (!c) notFound();
  return <Trial c={publicCase(c)} />;
}
