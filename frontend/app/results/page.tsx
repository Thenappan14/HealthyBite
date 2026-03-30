"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

import { DishCard } from "@/components/app/dish-card";
import { DisclaimerBanner } from "@/components/app/disclaimer-banner";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { fetchMenu, fetchMenus, fetchRecommendations } from "@/lib/api";
import { MenuResponse, RecommendationResponse } from "@/lib/types";

export default function ResultsPage() {
  const searchParams = useSearchParams();
  const [menu, setMenu] = useState<MenuResponse | null>(null);
  const [results, setResults] = useState<RecommendationResponse | null>(null);
  const requestedMenuId = Number(searchParams.get("menuId") ?? "0");

  useEffect(() => {
    void (async () => {
      const menus = await fetchMenus();
      const fallbackMenuId = menus[0]?.id ?? 1;
      const activeMenuId = requestedMenuId || fallbackMenuId;
      const [nextMenu, nextResults] = await Promise.all([
        fetchMenu(activeMenuId),
        fetchRecommendations(activeMenuId)
      ]);
      setMenu(nextMenu);
      setResults(nextResults);
    })();
  }, [requestedMenuId]);

  if (!menu || !results) {
    return <main className="mx-auto max-w-7xl px-4 py-10 md:px-6">Loading results...</main>;
  }

  const activeMenuId = requestedMenuId || menu.id;

  return (
    <main className="mx-auto max-w-7xl px-4 py-10 md:px-6">
      <div className="space-y-3">
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-muted-foreground">Results</p>
        <h1 className="font-display text-5xl">Ranked dishes with estimated nutrition and reasoning</h1>
        <p className="max-w-3xl text-muted-foreground">
          Each result balances hard exclusions with softer profile fit signals like protein, calories, fiber, sodium, sugar, preferences, and budget.
        </p>
        <p className="text-sm text-muted-foreground">
          Showing recommendations for menu #{activeMenuId} from {menu.source_filename ?? menu.source_url ?? "your latest analysis"}.
        </p>
      </div>

      <div className="mt-8">
        <DisclaimerBanner />
      </div>

      <section className="mt-8">
        <Card>
          <CardTitle>Top 3 recommendations</CardTitle>
          <CardDescription className="mt-2">Best overall fit based on provided profile information and menu details.</CardDescription>
          <div className="mt-6 grid gap-5 lg:grid-cols-3">
            {results.top_recommendations.map((dish) => (
              <DishCard key={dish.menu_item_id} dish={dish} />
            ))}
          </div>
        </Card>
      </section>

      <section className="mt-8 grid gap-8 lg:grid-cols-2">
        <Card>
          <CardTitle>Alternative options</CardTitle>
          <div className="mt-6 space-y-5">
            {results.alternatives.length ? (
              results.alternatives.map((dish) => <DishCard key={dish.menu_item_id} dish={dish} />)
            ) : (
              <p className="text-sm text-muted-foreground">No additional alternatives were generated for this menu.</p>
            )}
          </div>
        </Card>
        <Card>
          <CardTitle>Dishes to avoid</CardTitle>
          <div className="mt-6 space-y-5">
            {results.dishes_to_avoid.map((dish) => (
              <DishCard key={dish.menu_item_id} dish={dish} tone="danger" />
            ))}
          </div>
        </Card>
      </section>
    </main>
  );
}
