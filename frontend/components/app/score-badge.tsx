import { Badge } from "@/components/ui/badge";

export function ScoreBadge({ score }: { score: number }) {
  const tone = score >= 80 ? "success" : score >= 60 ? "warning" : "danger";
  return <Badge tone={tone}>Match {Math.round(score)}</Badge>;
}

