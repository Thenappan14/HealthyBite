"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, useTransition } from "react";
import { ArrowRight, FileImage, Link2, Sparkles } from "lucide-react";

import { UploadDropzone } from "@/components/app/upload-dropzone";
import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { uploadMenu } from "@/lib/api";

export default function UploadPage() {
  const router = useRouter();
  const [message, setMessage] = useState("");
  const [isPending, startTransition] = useTransition();

  return (
    <main className="mx-auto max-w-6xl px-4 py-10 md:px-6">
      <div className="space-y-6">
        <div className="flex items-center justify-between gap-4">
          <h1 className="font-display text-3xl leading-none text-foreground md:text-5xl">
            Menu Analysis
          </h1>
        </div>

        <div className="grid gap-6 lg:grid-cols-[1fr_0.8fr]">
          <Card className="bg-white/90">
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-muted-foreground">Upload menu</p>
            <CardTitle className="mt-3 text-4xl">Drop a screenshot, photo, or PDF</CardTitle>
            <CardDescription className="mt-3 text-lg">
              PlateWise extracts the menu text, structures dishes, estimates nutrition, and scores the best options for your profile.
            </CardDescription>
            <div className="mt-8">
              <UploadDropzone
                onFileSelected={(file) =>
                  startTransition(async () => {
                    try {
                      const result = await uploadMenu(file);
                      setMessage(
                        `Upload complete. Menu ${result.menu_id} is ready for recommendation generation.`
                      );
                      router.push(`/results?menuId=${result.menu_id}`);
                    } catch {
                      setMessage("Upload failed. Please sign in and make sure the backend is running.");
                    }
                  })
                }
              />
            </div>
            {message ? <p className="mt-5 text-base text-muted-foreground">{message}</p> : null}
            <div className="mt-6 flex flex-wrap gap-3">
              <Button asChild className="text-base">
                <Link href="/analyze-url">
                  Prefer a restaurant link?
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
              <Button asChild variant="outline" className="text-base">
                <Link href="/saved">View saved picks</Link>
              </Button>
            </div>
            {isPending ? <p className="mt-4 text-sm text-muted-foreground">Processing upload...</p> : null}
          </Card>
          <div className="space-y-6">
            <Card>
              <CardTitle className="text-2xl">What gets extracted</CardTitle>
              <div className="mt-5 space-y-4">
                <div className="rounded-3xl bg-white/85 p-4">
                  <div className="flex items-center gap-3">
                    <FileImage className="h-6 w-6 text-primary" />
                    <p className="text-lg font-semibold text-foreground">Menu structure</p>
                  </div>
                  <p className="mt-2 text-base text-muted-foreground">
                    Dish names, categories, descriptions, and visible prices.
                  </p>
                </div>
                <div className="rounded-3xl bg-white/85 p-4">
                  <div className="flex items-center gap-3">
                    <Sparkles className="h-6 w-6 text-primary" />
                    <p className="text-lg font-semibold text-foreground">Nutrition guidance</p>
                  </div>
                  <p className="mt-2 text-base text-muted-foreground">
                    Likely ingredients plus estimated calories, protein, carbs, fat, fiber, sugar, sodium, and allergens.
                  </p>
                </div>
                <div className="rounded-3xl bg-white/85 p-4">
                  <div className="flex items-center gap-3">
                    <Link2 className="h-6 w-6 text-primary" />
                    <p className="text-lg font-semibold text-foreground">Alternative input</p>
                  </div>
                  <p className="mt-2 text-base text-muted-foreground">
                    Don&apos;t have a file? Use the restaurant link workflow instead.
                  </p>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </main>
  );
}
