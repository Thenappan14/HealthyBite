import { BookmarkCheck } from "lucide-react";

import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { fetchHistory } from "@/lib/api";

export default async function SavedPage() {
  const history = await fetchHistory();

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
          {history.map((item) => (
            <div key={item.id} className="rounded-[24px] border border-border bg-white/80 p-5">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <h3 className="text-lg font-semibold text-foreground">{item.dish_name}</h3>
                <span className="rounded-full bg-secondary px-3 py-1 text-xs font-semibold text-secondary-foreground">
                  {item.type} - {Math.round(item.score)}
                </span>
              </div>
              <p className="mt-2 text-sm text-muted-foreground">{item.summary_reason}</p>
              {item.warnings.length ? (
                <p className="mt-3 text-sm text-amber-900">Warnings: {item.warnings.join(", ")}</p>
              ) : null}
            </div>
          ))}
        </div>
      </Card>
    </main>
  );
}
