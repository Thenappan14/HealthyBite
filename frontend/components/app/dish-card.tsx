import { AlertTriangle, CircleDollarSign, ShieldAlert } from "lucide-react";

import { ScoreBadge } from "@/components/app/score-badge";
import { Badge } from "@/components/ui/badge";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { Recommendation } from "@/lib/types";

export function DishCard({
  dish,
  tone = "default"
}: {
  dish: Recommendation;
  tone?: "default" | "danger";
}) {
  return (
    <Card className={tone === "danger" ? "border-rose-200 bg-rose-50/80" : ""}>
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <CardTitle className="text-2xl md:text-3xl">{dish.dish_name}</CardTitle>
          <CardDescription className="mt-1 text-base">{dish.category ?? "Menu item"}</CardDescription>
        </div>
        <ScoreBadge score={dish.match_score} />
      </div>

      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        <div className="rounded-2xl bg-stone-50 p-3">
          <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Exact menu name</p>
          <p className="mt-1 text-lg text-foreground">{dish.dish_name}</p>
          {dish.source_text ? (
            <p className="mt-2 text-sm text-muted-foreground">{dish.source_text}</p>
          ) : null}
        </div>
        <div className="rounded-2xl bg-stone-50 p-3">
          <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Menu location</p>
          <p className="mt-1 text-lg text-foreground">
            {dish.source_page ? `PDF page ${dish.source_page}` : "Upload text match"}
            {dish.price !== undefined && dish.price !== null ? ` | S$${dish.price.toFixed(2)}` : ""}
          </p>
        </div>
      </div>

      <p className="mt-4 text-base leading-7 text-foreground md:text-lg">{dish.summary_reason}</p>

      <div className="mt-4 flex flex-wrap gap-2">
        {dish.allergens.map((allergen) => (
          <Badge key={allergen} tone="danger">
            <ShieldAlert className="mr-1 h-3.5 w-3.5" />
            {allergen}
          </Badge>
        ))}
      </div>

      <div className="mt-5 grid gap-3 text-base text-muted-foreground sm:grid-cols-3">
        <div className="rounded-2xl bg-white/80 p-3">
          <p className="text-xs uppercase tracking-[0.2em]">Calories</p>
          <p className="mt-1 text-2xl text-foreground">{dish.nutrition_estimate.calories ?? "--"}</p>
        </div>
        <div className="rounded-2xl bg-white/80 p-3">
          <p className="text-xs uppercase tracking-[0.2em]">Protein</p>
          <p className="mt-1 text-2xl text-foreground">{dish.nutrition_estimate.protein_g ?? "--"}g</p>
        </div>
        <div className="rounded-2xl bg-white/80 p-3">
          <p className="text-xs uppercase tracking-[0.2em]">Sodium</p>
          <p className="mt-1 text-2xl text-foreground">{dish.nutrition_estimate.sodium_mg ?? "--"}mg</p>
        </div>
      </div>

      {dish.why_recommended.length ? (
        <div className="mt-5 space-y-2">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-muted-foreground">
            Why recommended
          </p>
          {dish.why_recommended.map((reason) => (
            <p key={reason} className="text-base leading-7 text-foreground">
              - {reason}
            </p>
          ))}
        </div>
      ) : null}

      {dish.why_not_recommended.length ? (
        <div className="mt-5 space-y-2">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-muted-foreground">
            Considerations
          </p>
          {dish.why_not_recommended.map((reason) => (
            <p key={reason} className="text-base leading-7 text-foreground">
              - {reason}
            </p>
          ))}
        </div>
      ) : null}

      {dish.warnings.length ? (
        <div className="mt-5 rounded-2xl border border-amber-200 bg-amber-50 p-4">
          <div className="mb-2 flex items-center gap-2 text-base font-semibold text-amber-900">
            <AlertTriangle className="h-4 w-4" />
            Warnings
          </div>
          {dish.warnings.map((warning) => (
            <p key={warning} className="text-base leading-7 text-amber-900">
              {warning}
            </p>
          ))}
        </div>
      ) : null}

      <div className="mt-5 flex items-center gap-2 text-sm text-muted-foreground">
        <CircleDollarSign className="h-4 w-4" />
        Based on menu information and estimated nutrition only.
      </div>
    </Card>
  );
}
