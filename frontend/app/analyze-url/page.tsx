"use client";

import { useState, useTransition } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { DisclaimerBanner } from "@/components/app/disclaimer-banner";
import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ingestRestaurantUrl } from "@/lib/api";

export default function AnalyzeUrlPage() {
  const router = useRouter();
  const [url, setUrl] = useState("https://example.com/menu");
  const [message, setMessage] = useState("");
  const [isPending, startTransition] = useTransition();

  return (
    <main className="mx-auto max-w-5xl px-4 py-10 md:px-6">
      <Card>
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-muted-foreground">Restaurant URL analysis</p>
        <CardTitle className="mt-3">Paste a restaurant website URL</CardTitle>
        <CardDescription className="mt-3">
          The backend crawls likely menu pages, extracts candidate dishes, and normalizes them into structured JSON.
        </CardDescription>
        <div className="mt-8 flex flex-col gap-4 md:flex-row">
          <Input value={url} onChange={(e) => setUrl(e.target.value)} placeholder="https://restaurant.com/menu" />
          <Button
            className="md:min-w-40"
            onClick={() =>
              startTransition(async () => {
                const menu = await ingestRestaurantUrl(url);
                setMessage(`Parsed ${menu.items.length} menu items from ${menu.source_url ?? url}.`);
                router.push(`/results?menuId=${menu.id}`);
              })
            }
          >
            {isPending ? "Analyzing..." : "Analyze URL"}
          </Button>
        </div>
        {message ? <p className="mt-5 text-sm text-muted-foreground">{message}</p> : null}
        <div className="mt-6 flex gap-3">
          <Button asChild variant="outline">
            <Link href="/results">Open results</Link>
          </Button>
        </div>
      </Card>
      <div className="mt-6">
        <DisclaimerBanner />
      </div>
    </main>
  );
}
