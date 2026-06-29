import { Suspense } from "react";

import { Card, CardDescription, CardTitle } from "@/components/ui/card";

import { ResultsClient } from "./results-client";

export default function ResultsPage() {
  return (
    <Suspense
      fallback={
        <main className="mx-auto max-w-7xl px-4 py-10 md:px-6">
          <Card>
            <CardTitle className="text-3xl">Loading results...</CardTitle>
            <CardDescription className="mt-3 text-lg">Fetching your latest menu recommendations.</CardDescription>
          </Card>
        </main>
      }
    >
      <ResultsClient />
    </Suspense>
  );
}

