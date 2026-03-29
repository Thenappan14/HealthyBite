"use client";

import Link from "next/link";
import { useState, useTransition } from "react";

import { DisclaimerBanner } from "@/components/app/disclaimer-banner";
import { UploadDropzone } from "@/components/app/upload-dropzone";
import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { uploadMenu } from "@/lib/api";

export default function UploadPage() {
  const [message, setMessage] = useState("");
  const [isPending, startTransition] = useTransition();

  return (
    <main className="mx-auto max-w-6xl px-4 py-10 md:px-6">
      <div className="grid gap-6 lg:grid-cols-[1fr_0.8fr]">
        <Card>
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-muted-foreground">Menu upload</p>
          <CardTitle className="mt-3">Drop a screenshot, photo, or PDF</CardTitle>
          <CardDescription className="mt-3">
            PlateWise extracts the menu text, structures dishes, estimates nutrition, and scores the best options for your profile.
          </CardDescription>
          <div className="mt-8">
            <UploadDropzone
              onFileSelected={(file) =>
                startTransition(async () => {
                  const result = await uploadMenu(file);
                  setMessage(
                    `Upload complete. Menu ${result.menu_id} is ready for recommendation generation.`
                  );
                })
              }
            />
          </div>
          {message ? <p className="mt-5 text-sm text-muted-foreground">{message}</p> : null}
          <div className="mt-6 flex gap-3">
            <Button asChild>
              <Link href="/results">View sample results</Link>
            </Button>
            <Button asChild variant="outline">
              <Link href="/analyze-url">Analyze by URL instead</Link>
            </Button>
          </div>
          {isPending ? <p className="mt-4 text-sm text-muted-foreground">Processing upload...</p> : null}
        </Card>
        <div className="space-y-6">
          <DisclaimerBanner />
          <Card>
            <CardTitle className="text-2xl">What gets extracted</CardTitle>
            <div className="mt-5 space-y-3 text-sm text-muted-foreground">
              <p>Dish names, categories, descriptions, and visible prices.</p>
              <p>Likely ingredients inferred from menu wording.</p>
              <p>Estimated calories, protein, carbs, fat, fiber, sugar, sodium, and allergens.</p>
            </div>
          </Card>
        </div>
      </div>
    </main>
  );
}
