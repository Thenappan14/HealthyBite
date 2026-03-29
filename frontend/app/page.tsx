import Link from "next/link";
import { ArrowRight, ShieldCheck, Sparkles, UploadCloud } from "lucide-react";

import { DisclaimerBanner } from "@/components/app/disclaimer-banner";
import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";

const features = [
  {
    icon: UploadCloud,
    title: "Upload menus in seconds",
    description: "Drag in restaurant screenshots, images, or PDFs and PlateWise structures the dishes for review."
  },
  {
    icon: Sparkles,
    title: "Rank dishes to fit your goals",
    description: "Hybrid scoring balances calorie appropriateness, protein, fiber, sugar, sodium, budget, and preferences."
  },
  {
    icon: ShieldCheck,
    title: "Surface likely risks clearly",
    description: "Allergens, diet conflicts, and lower-confidence ingredient estimates are called out before you choose."
  }
];

export default function HomePage() {
  return (
    <main className="mx-auto max-w-7xl px-4 py-10 md:px-6 md:py-16">
      <section className="grid items-center gap-8 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="space-y-6">
          <p className="inline-flex rounded-full bg-white/80 px-4 py-2 text-xs font-semibold uppercase tracking-[0.24em] text-muted-foreground">
            Personalized menu intelligence
          </p>
          <h1 className="max-w-3xl font-display text-5xl leading-tight text-foreground md:text-7xl">
            Eat out with recommendations that actually fit your body, goals, and guardrails.
          </h1>
          <p className="max-w-2xl text-lg text-muted-foreground">
            PlateWise turns restaurant menus into structured dishes, estimates likely nutrition, filters unsafe items, and explains the best options for you.
          </p>
          <div className="flex flex-wrap gap-3">
            <Button asChild size="lg">
              <Link href="/signup">
                Create profile
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg">
              <Link href="/upload">Try a menu upload</Link>
            </Button>
          </div>
          <DisclaimerBanner />
        </div>

        <Card className="overflow-hidden bg-white/85">
          <div className="space-y-5">
            <div className="rounded-[24px] bg-secondary/60 p-5">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-muted-foreground">Top pick</p>
              <h2 className="mt-3 font-display text-3xl">Salmon Power Bowl</h2>
              <p className="mt-2 text-sm text-muted-foreground">
                Estimated as a strong match for better energy with likely solid protein, vegetables, and practical calories.
              </p>
            </div>
            <div className="grid gap-4 sm:grid-cols-3">
              <div className="rounded-3xl bg-white p-4">
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Match score</p>
                <p className="mt-2 text-3xl font-semibold">88</p>
              </div>
              <div className="rounded-3xl bg-white p-4">
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Protein</p>
                <p className="mt-2 text-3xl font-semibold">30g</p>
              </div>
              <div className="rounded-3xl bg-white p-4">
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Confidence</p>
                <p className="mt-2 text-3xl font-semibold">0.85</p>
              </div>
            </div>
          </div>
        </Card>
      </section>

      <section className="mt-14 grid gap-5 md:grid-cols-3">
        {features.map((feature) => (
          <Card key={feature.title}>
            <feature.icon className="h-8 w-8 text-primary" />
            <CardTitle className="mt-5 text-2xl">{feature.title}</CardTitle>
            <CardDescription className="mt-3">{feature.description}</CardDescription>
          </Card>
        ))}
      </section>
    </main>
  );
}
