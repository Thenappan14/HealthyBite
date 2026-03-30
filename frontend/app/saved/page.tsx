"use client";

import { useEffect, useState, useTransition } from "react";
import { BookmarkCheck } from "lucide-react";

import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { fetchHistory, setRecommendationSaved } from "@/lib/api";
import { HistoryItem } from "@/lib/types";

export default function SavedPage() {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [isPending, startTransition] = useTransition();

  useEffect(() => {
    void fetchHistory().then(setHistory);
  }, []);

  const savedItems = history.filter((item) => item.saved);
  const visibleItems = savedItems.length ? savedItems : history;

  return (
    <main className="mx-auto max-w-5xl px-4 py-10 md:px-6">
      <Card>
        <div className="flex items-center gap-3">
          <BookmarkCheck className="h-7 w-7 text-primary" />
          <div>
            <CardTitle>Saved recommendations</CardTitle>
            <CardDescription>Review previous recommendation history and revisit strong matches.</CardDescription>
          </div>
        </div>

        <div className="mt-8 space-y-4">
          {visibleItems.map((item) => (
            <div key={item.id} className="rounded-[24px] border border-border bg-white/80 p-5">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <h3 className="text-lg font-semibold text-foreground">{item.dish_name}</h3>
                <div className="flex items-center gap-3">
                  <span className="rounded-full bg-secondary px-3 py-1 text-xs font-semibold text-secondary-foreground">
                    {item.type} - {Math.round(item.score)}
                  </span>
                  <button
                    className="rounded-full border border-border px-3 py-1 text-xs font-semibold text-foreground"
                    onClick={() =>
                      startTransition(async () => {
                        const updated = await setRecommendationSaved(item.id, !item.saved);
                        setHistory((current) =>
                          current.map((entry) => (entry.id === item.id ? updated : entry))
                        );
                      })
                    }
                  >
                    {item.saved ? "Unsave" : "Save"}
                  </button>
                </div>
              </div>
              <p className="mt-2 text-sm text-muted-foreground">{item.summary_reason}</p>
              {item.warnings.length ? (
                <p className="mt-3 text-sm text-amber-900">Warnings: {item.warnings.join(", ")}</p>
              ) : null}
            </div>
          ))}
          {!visibleItems.length ? (
            <p className="text-sm text-muted-foreground">
              No recommendations yet. Generate results from an uploaded menu or restaurant URL first.
            </p>
          ) : null}
        </div>
        {isPending ? <p className="mt-4 text-sm text-muted-foreground">Updating saved state...</p> : null}
      </Card>
    </main>
  );
}
