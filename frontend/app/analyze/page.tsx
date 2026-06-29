"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, useTransition } from "react";
import { ArrowRight, FileImage, Link2, Sparkles } from "lucide-react";

import { LoadingState } from "@/components/app/loading-state";
import { UploadDropzone } from "@/components/app/upload-dropzone";
import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { analyzeMenu } from "@/lib/api";

export default function AnalyzePage() {
  const router = useRouter();
  const [message, setMessage] = useState("");
  const [isPending, startTransition] = useTransition();

  return (
    <>
      {isPending ? (
        <LoadingState
          fullScreen
          label="Turning your menu into a personalized plate recommendation..."
        />
      ) : null}
      <main className="mx-auto max-w-6xl px-4 py-10 md:px-6">
        <div className="space-y-6">
          <div className="flex items-center justify-between gap-4">
            <h1 className="font-display text-3xl leading-none text-foreground md:text-5xl">
              Quick Menu Analysis
            </h1>
          </div>

          <div className="grid gap-6 lg:grid-cols-[1fr_0.8fr]">
            <Card className="bg-white/90">
              <p className="text-sm font-semibold uppercase tracking-[0.24em] text-muted-foreground">
                Upload menu
              </p>
              <CardTitle className="mt-3 text-4xl">Drop a screenshot, photo, or PDF</CardTitle>
              <CardDescription className="mt-3 text-lg">
                PlateWise extracts the menu text, structures dishes, estimates nutrition, and returns ranked picks in one step.
              </CardDescription>
              <div className="mt-8">
                <UploadDropzone
                  onFileSelected={(file) =>
                    startTransition(async () => {
                      try {
                        const result = await analyzeMenu(file);
                        window.sessionStorage.setItem(
                          `platewise_analyze_${result.menu_id}`,
                          JSON.stringify(result)
                        );
                        router.push(`/results?menuId=${result.menu_id}`);
                      } catch (error) {
                        setMessage(
                          error instanceof Error
                            ? error.message
                            : "Analysis failed. Please sign in and make sure the backend is running."
                        );
                      }
                    })
                  }
                />
              </div>
              {message ? <p className="mt-5 text-base text-muted-foreground">{message}</p> : null}
              <div className="mt-6 flex flex-wrap gap-3">
                <Button asChild className="text-base">
                  <Link href="/profile">
                    Review profile first
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Link>
                </Button>
                <Button asChild variant="outline" className="text-base">
                  <Link href="/analyze-url">Prefer a restaurant link?</Link>
                </Button>
              </div>
            </Card>
            <div className="space-y-6">
              <Card>
                <CardTitle className="text-2xl">What you get back</CardTitle>
                <div className="mt-5 space-y-4">
                  <div className="rounded-3xl bg-white/85 p-4">
                    <div className="flex items-center gap-3">
                      <FileImage className="h-6 w-6 text-primary" />
                      <p className="text-lg font-semibold text-foreground">Structured dishes</p>
                    </div>
                    <p className="mt-2 text-base text-muted-foreground">
                      Dish names, descriptions, categories, and prices when visible.
                    </p>
                  </div>
                  <div className="rounded-3xl bg-white/85 p-4">
                    <div className="flex items-center gap-3">
                      <Sparkles className="h-6 w-6 text-primary" />
                      <p className="text-lg font-semibold text-foreground">Ranked recommendations</p>
                    </div>
                    <p className="mt-2 text-base text-muted-foreground">
                      Top picks, alternatives, and items to avoid based on your goal and restrictions.
                    </p>
                  </div>
                  <div className="rounded-3xl bg-white/85 p-4">
                    <div className="flex items-center gap-3">
                      <Link2 className="h-6 w-6 text-primary" />
                      <p className="text-lg font-semibold text-foreground">Explainable tradeoffs</p>
                    </div>
                    <p className="mt-2 text-base text-muted-foreground">
                      Each dish includes estimated nutrition and clear, cautious reasoning.
                    </p>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </main>
    </>
  );
}

