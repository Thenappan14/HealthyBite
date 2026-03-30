import Link from "next/link";
import { ArrowRight, Link2, ShieldCheck, Sparkles, UploadCloud, UserRoundCog } from "lucide-react";

import { DisclaimerBanner } from "@/components/app/disclaimer-banner";
import { OwlCluster } from "@/components/app/owl-cluster";
import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";

const features = [
  {
    icon: UserRoundCog,
    title: "Start with your profile",
    description: "Set your goal, dietary restrictions, allergies, preferences, spice comfort, and budget before any menu gets ranked."
  },
  {
    icon: UploadCloud,
    title: "Then analyze menus",
    description: "Drag in restaurant screenshots, images, or PDFs after onboarding and PlateWise structures the dishes for review."
  },
  {
    icon: Link2,
    title: "Or paste a restaurant link",
    description: "Use a restaurant URL once your profile is ready and get goal-aware menu recommendations with clear reasoning."
  }
];

export default function HomePage() {
  return (
    <main className="mx-auto max-w-7xl px-4 py-10 md:px-6 md:py-16">
      <section className="grid items-center gap-10 lg:grid-cols-[1.1fr_0.9fr]">
        <div className="space-y-7">
          <p className="inline-flex rounded-full bg-white/80 px-5 py-2.5 text-sm font-semibold uppercase tracking-[0.24em] text-muted-foreground">
            Profile-first food guidance
          </p>
          <h1 className="max-w-4xl font-display text-6xl leading-[1.05] text-foreground md:text-8xl">
            Build your food profile first, then let PlateWise guide every restaurant choice.
          </h1>
          <p className="max-w-3xl text-2xl leading-relaxed text-muted-foreground">
            New users start by choosing goals, dietary restrictions, allergies, dislikes, spice comfort, budget, and favorite cuisines. After that, PlateWise analyzes menus and restaurant links with much smarter recommendations.
          </p>
          <div className="flex flex-wrap gap-4">
            <Button asChild size="lg">
              <Link href="/signup">
                Start with profile setup
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg">
              <Link href="/login">Log in</Link>
            </Button>
          </div>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="rounded-[28px] bg-white/85 p-5">
              <p className="text-sm font-semibold uppercase tracking-[0.2em] text-muted-foreground">Step 1</p>
              <p className="mt-3 text-xl font-semibold text-foreground">Tell us your goal and preferences</p>
            </div>
            <div className="rounded-[28px] bg-white/85 p-5">
              <p className="text-sm font-semibold uppercase tracking-[0.2em] text-muted-foreground">Step 2</p>
              <p className="mt-3 text-xl font-semibold text-foreground">Upload a menu or paste a restaurant link</p>
            </div>
            <div className="rounded-[28px] bg-white/85 p-5">
              <p className="text-sm font-semibold uppercase tracking-[0.2em] text-muted-foreground">Step 3</p>
              <p className="mt-3 text-xl font-semibold text-foreground">See recommended dishes and warnings</p>
            </div>
          </div>
          <DisclaimerBanner />
        </div>

        <div className="space-y-6">
          <Card className="overflow-hidden bg-white/85">
            <div className="space-y-5">
              <div className="flex items-center justify-between gap-4 rounded-[24px] bg-secondary/60 p-6">
                <div>
                  <p className="text-sm font-semibold uppercase tracking-[0.24em] text-muted-foreground">Your healthy guides</p>
                  <h2 className="mt-3 font-display text-4xl">Wise owls, clear choices</h2>
                  <p className="mt-3 text-lg text-muted-foreground">
                    A warmer onboarding flow that nudges people to set their needs first and explore menus second.
                  </p>
                </div>
                <OwlCluster />
              </div>
              <div className="grid gap-4 sm:grid-cols-3">
                <div className="rounded-3xl bg-white p-5">
                  <p className="text-sm uppercase tracking-[0.2em] text-muted-foreground">Profile signals</p>
                  <p className="mt-2 text-4xl font-semibold">10+</p>
                </div>
                <div className="rounded-3xl bg-white p-5">
                  <p className="text-sm uppercase tracking-[0.2em] text-muted-foreground">Warnings surfaced</p>
                  <p className="mt-2 text-4xl font-semibold">Clear</p>
                </div>
                <div className="rounded-3xl bg-white p-5">
                  <p className="text-sm uppercase tracking-[0.2em] text-muted-foreground">Decision style</p>
                  <p className="mt-2 text-4xl font-semibold">Goal-led</p>
                </div>
              </div>
            </div>
          </Card>
          <Card>
            <CardTitle className="text-3xl">What happens after onboarding</CardTitle>
            <CardDescription className="mt-3 text-lg">
              PlateWise ranks dishes to fit your goals, then clearly surfaces allergens, diet conflicts, and lower-confidence ingredient guesses.
            </CardDescription>
            <div className="mt-6 grid gap-4 md:grid-cols-2">
              <div className="rounded-3xl bg-white/85 p-5">
                <Sparkles className="h-8 w-8 text-primary" />
                <p className="mt-4 text-2xl font-semibold text-foreground">Goal-aware scoring</p>
                <p className="mt-2 text-lg text-muted-foreground">
                  Calories, protein, fiber, sodium, sugar, budget, and preference signals all shape the ranking.
                </p>
              </div>
              <div className="rounded-3xl bg-white/85 p-5">
                <ShieldCheck className="h-8 w-8 text-primary" />
                <p className="mt-4 text-2xl font-semibold text-foreground">Clear safety flags</p>
                <p className="mt-2 text-lg text-muted-foreground">
                  Allergy conflicts and strict diet mismatches are filtered before recommendations are shown.
                </p>
              </div>
            </div>
          </Card>
        </div>
      </section>

      <section className="mt-14 grid gap-5 md:grid-cols-3">
        {features.map((feature) => (
          <Card key={feature.title}>
            <feature.icon className="h-8 w-8 text-primary" />
            <CardTitle className="mt-5 text-3xl">{feature.title}</CardTitle>
            <CardDescription className="mt-3 text-lg">{feature.description}</CardDescription>
          </Card>
        ))}
      </section>
    </main>
  );
}
