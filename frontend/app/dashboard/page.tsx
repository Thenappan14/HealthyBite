"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { ArrowRight, Link2, ScanSearch, UserRoundCog } from "lucide-react";

import { DisclaimerBanner } from "@/components/app/disclaimer-banner";
import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { fetchHistory, fetchProfile } from "@/lib/api";
import { HistoryItem, Profile } from "@/lib/types";

export default function DashboardPage() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    void Promise.all([fetchProfile(), fetchHistory()]).then(([nextProfile, nextHistory]) => {
      setProfile(nextProfile);
      setHistory(nextHistory);
      setLoaded(true);
    });
  }, []);

  if (!loaded) {
    return <main className="mx-auto max-w-7xl px-4 py-10 md:px-6">Loading dashboard...</main>;
  }

  if (!profile) {
    return (
      <main className="mx-auto max-w-7xl px-4 py-10 md:px-6">
        <Card>
          <CardTitle className="text-3xl">No profile yet</CardTitle>
          <CardDescription className="mt-3 text-lg">
            Sign in and complete your profile before analyzing menus and viewing recommendations.
          </CardDescription>
          <Button asChild className="mt-6">
            <Link href="/profile">Go to profile setup</Link>
          </Button>
        </Card>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-7xl px-4 py-10 md:px-6">
      <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <Card>
          <p className="text-sm font-semibold uppercase tracking-[0.24em] text-muted-foreground">Your profile comes first</p>
          <CardTitle className="mt-3 text-4xl">Welcome back, {profile.name}</CardTitle>
          <CardDescription className="mt-3 text-lg">
            Goal: {profile.primary_goal.replace("_", " ")}. Diet: {profile.diet_type.replace("_", " ")}.
          </CardDescription>
          <div className="mt-6 space-y-2 text-lg text-muted-foreground">
            <p>Allergies: {profile.allergies.join(", ") || "None listed"}</p>
            <p>Preferred cuisines: {profile.preferred_cuisines.join(", ") || "Open to anything"}</p>
            <p>Budget: {profile.budget_preference}</p>
          </div>
          <Button asChild className="mt-6">
            <Link href="/profile">
              Update profile
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
        </Card>

        <div className="grid gap-5 md:grid-cols-3">
          <Card>
            <UserRoundCog className="h-8 w-8 text-primary" />
            <CardTitle className="mt-5 text-3xl">Step 1: profile setup</CardTitle>
            <CardDescription className="mt-3 text-lg">Tune restrictions, preferences, goals, and body metrics before any menu analysis.</CardDescription>
            <Button asChild variant="outline" className="mt-5">
              <Link href="/profile">Open</Link>
            </Button>
          </Card>
          <Card>
            <ScanSearch className="h-8 w-8 text-primary" />
            <CardTitle className="mt-5 text-3xl">Step 2: analyze uploads</CardTitle>
            <CardDescription className="mt-3 text-lg">Once your profile is saved, drop menu screenshots or PDFs for OCR-based parsing.</CardDescription>
            <Button asChild variant="outline" className="mt-5">
              <Link href="/upload">Upload menu</Link>
            </Button>
          </Card>
          <Card>
            <Link2 className="h-8 w-8 text-primary" />
            <CardTitle className="mt-5 text-3xl">Step 2: analyze website</CardTitle>
            <CardDescription className="mt-3 text-lg">Paste a restaurant URL after onboarding and crawl likely menu pages with your profile applied.</CardDescription>
            <Button asChild variant="outline" className="mt-5">
              <Link href="/analyze-url">Paste URL</Link>
            </Button>
          </Card>
        </div>
      </div>

      <div className="mt-8 grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
        <Card>
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-muted-foreground">Recent activity</p>
          <div className="mt-5 space-y-4">
            {history.map((entry) => (
              <div key={entry.id} className="rounded-3xl bg-white/80 p-4">
                <div className="flex items-center justify-between gap-3">
                  <h3 className="font-semibold text-foreground">{entry.dish_name}</h3>
                  <span className="text-sm text-primary">{Math.round(entry.score)}</span>
                </div>
                <p className="mt-2 text-sm text-muted-foreground">{entry.summary_reason}</p>
              </div>
            ))}
          </div>
        </Card>
        <DisclaimerBanner />
      </div>
    </main>
  );
}
