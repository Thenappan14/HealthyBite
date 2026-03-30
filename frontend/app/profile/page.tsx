"use client";

import { useState, useTransition } from "react";
import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import { Card, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { saveProfile } from "@/lib/api";

function splitList(value: string) {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function mergeUnique(values: string[]) {
  return Array.from(new Set(values.filter(Boolean)));
}

const CUISINE_OPTIONS = [
  "japanese",
  "mediterranean",
  "thai",
  "indian",
  "korean",
  "mexican",
  "italian",
  "chinese",
  "vietnamese",
  "middle_eastern",
  "american",
  "greek"
];

const DINING_STYLE_OPTIONS = [
  "street_food",
  "casual_restaurant",
  "healthy_cafe",
  "fine_dining",
  "buffet",
  "family_style",
  "fast_casual",
  "food_court"
];

const emptyProfile = {
  name: "",
  age: 0,
  sex: "female",
  height_cm: 0,
  weight_kg: 0,
  activity_level: "moderately_active",
  primary_goal: "balanced_eating",
  diet_type: "none",
  allergies: [] as string[],
  disliked_foods: [] as string[],
  spice_preference: "medium",
  budget_preference: "15_25",
  preferred_dining_styles: [] as string[],
  preferred_cuisines: [] as string[]
};

function prettyLabel(value: string) {
  return value.replaceAll("_", " ");
}

function FieldShell({
  label,
  helper,
  children
}: {
  label: string;
  helper?: string;
  children: React.ReactNode;
}) {
  return (
    <label className="space-y-2">
      <div>
        <p className="text-lg font-semibold text-foreground">{label}</p>
        {helper ? <p className="text-sm text-muted-foreground">{helper}</p> : null}
      </div>
      {children}
    </label>
  );
}

function SectionTitle({ title }: { title: string }) {
  return (
    <div className="mb-5">
      <h2 className="text-2xl font-semibold text-foreground md:text-3xl">{title}</h2>
    </div>
  );
}

function ChoicePills({
  options,
  selected,
  onToggle
}: {
  options: string[];
  selected: string[];
  onToggle: (value: string) => void;
}) {
  return (
    <div className="flex flex-wrap gap-3">
      {options.map((option) => {
        const active = selected.includes(option);
        return (
          <button
            key={option}
            type="button"
            onClick={() => onToggle(option)}
            className={`rounded-full border px-4 py-2 text-sm font-semibold capitalize transition ${
              active
                ? "border-primary bg-primary text-primary-foreground"
                : "border-border bg-white text-foreground"
            }`}
          >
            {prettyLabel(option)}
          </button>
        );
      })}
    </div>
  );
}

export default function ProfilePage() {
  const router = useRouter();
  const [isPending, startTransition] = useTransition();
  const [status, setStatus] = useState("");
  const [customCuisineInput, setCustomCuisineInput] = useState("");
  const [customDiningInput, setCustomDiningInput] = useState("");
  const [form, setForm] = useState(emptyProfile);
  const [allergiesText, setAllergiesText] = useState("");
  const [dislikedFoodsText, setDislikedFoodsText] = useState("");

  function toggleCuisine(value: string) {
    setForm((current) => ({
      ...current,
      preferred_cuisines: current.preferred_cuisines.includes(value)
        ? current.preferred_cuisines.filter((entry) => entry !== value)
        : [...current.preferred_cuisines, value]
    }));
  }

  function toggleDiningStyle(value: string) {
    setForm((current) => ({
      ...current,
      preferred_dining_styles: current.preferred_dining_styles.includes(value)
        ? current.preferred_dining_styles.filter((entry) => entry !== value)
        : [...current.preferred_dining_styles, value]
    }));
  }

  return (
    <main className="mx-auto max-w-6xl px-4 py-10 md:px-6">
      <Card className="p-8 md:p-10">
        <p className="text-sm font-semibold uppercase tracking-[0.24em] text-muted-foreground">Step 1: profile setup</p>
        <CardTitle className="mt-3 text-4xl md:text-5xl">Tell PlateWise what matters before menus come in</CardTitle>

        <div className="mt-10 space-y-10">
          <section>
            <SectionTitle title="Personal details" />
            <div className="grid gap-5 md:grid-cols-2">
              <FieldShell label="Name" helper="What should PlateWise call you?">
                <Input
                  className="h-14 text-base md:text-lg"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  placeholder="Your full name"
                />
              </FieldShell>
              <FieldShell label="Age" helper="Used as basic profile context only.">
                <Input
                  className="h-14 text-base md:text-lg"
                  value={form.age || ""}
                  onChange={(e) => setForm({ ...form, age: Number(e.target.value || 0) })}
                  placeholder="Age"
                  type="number"
                />
              </FieldShell>
              <FieldShell label="Sex" helper="Select the option that best fits you.">
                <Select
                  className="h-14 text-base md:text-lg"
                  value={form.sex}
                  onChange={(e) => setForm({ ...form, sex: e.target.value })}
                >
                  <option value="female">Female</option>
                  <option value="male">Male</option>
                  <option value="non_binary">Non-binary</option>
                </Select>
              </FieldShell>
              <FieldShell label="Activity level" helper="Choose the option that best describes your typical week.">
                <Select
                  className="h-14 text-base md:text-lg"
                  value={form.activity_level}
                  onChange={(e) => setForm({ ...form, activity_level: e.target.value })}
                >
                  <option value="sedentary">Sedentary</option>
                  <option value="lightly_active">Lightly active</option>
                  <option value="moderately_active">Moderately active</option>
                  <option value="very_active">Very active</option>
                  <option value="athlete_level">Athlete level</option>
                </Select>
              </FieldShell>
              <FieldShell label="Height (cm)" helper="Used for general profile context.">
                <Input
                  className="h-14 text-base md:text-lg"
                  value={form.height_cm || ""}
                  onChange={(e) => setForm({ ...form, height_cm: Number(e.target.value || 0) })}
                  placeholder="Height in centimeters"
                  type="number"
                />
              </FieldShell>
              <FieldShell label="Weight (kg)" helper="Used for general profile context.">
                <Input
                  className="h-14 text-base md:text-lg"
                  value={form.weight_kg || ""}
                  onChange={(e) => setForm({ ...form, weight_kg: Number(e.target.value || 0) })}
                  placeholder="Weight in kilograms"
                  type="number"
                />
              </FieldShell>
            </div>
          </section>

          <section>
            <SectionTitle title="Goals and food rules" />
            <div className="grid gap-5 md:grid-cols-2">
              <FieldShell label="Primary goal" helper="What are you optimizing for most right now?">
                <Select
                  className="h-14 text-base md:text-lg"
                  value={form.primary_goal}
                  onChange={(e) => setForm({ ...form, primary_goal: e.target.value })}
                >
                  <option value="fat_loss">Fat loss</option>
                  <option value="muscle_gain">Muscle gain</option>
                  <option value="maintenance">Maintenance</option>
                  <option value="better_energy">Better energy</option>
                  <option value="balanced_eating">Balanced eating</option>
                </Select>
              </FieldShell>
              <FieldShell label="Dietary restriction" helper="Choose a diet type if you follow one consistently.">
                <Select
                  className="h-14 text-base md:text-lg"
                  value={form.diet_type}
                  onChange={(e) => setForm({ ...form, diet_type: e.target.value })}
                >
                  <option value="none">None</option>
                  <option value="vegetarian">Vegetarian</option>
                  <option value="vegan">Vegan</option>
                  <option value="halal">Halal</option>
                  <option value="hindu_friendly">Hindu-friendly</option>
                  <option value="buddhist_friendly">Buddhist-friendly</option>
                  <option value="no_beef">No beef</option>
                  <option value="no_pork">No pork</option>
                  <option value="pescatarian">Pescatarian</option>
                  <option value="lactose_free">Lactose free</option>
                  <option value="gluten_free">Gluten free</option>
                </Select>
              </FieldShell>
              <FieldShell
                label="Allergies"
                helper="List allergies separated by commas, for example peanuts, shellfish."
              >
                <Textarea
                  className="text-base md:text-lg"
                  value={allergiesText}
                  onChange={(e) => setAllergiesText(e.target.value)}
                  placeholder="Peanuts, shellfish, dairy"
                />
              </FieldShell>
              <FieldShell
                label="Disliked foods"
                helper="List foods you prefer to avoid even if they are technically allowed."
              >
                <Textarea
                  className="text-base md:text-lg"
                  value={dislikedFoodsText}
                  onChange={(e) => setDislikedFoodsText(e.target.value)}
                  placeholder="Mushroom, olives, anchovies"
                />
              </FieldShell>
            </div>
          </section>

          <section>
            <SectionTitle title="Taste and restaurant preferences" />
            <div className="grid gap-5 md:grid-cols-2">
              <FieldShell label="Spice preference" helper="Choose the heat level you usually enjoy.">
                <Select
                  className="h-14 text-base md:text-lg"
                  value={form.spice_preference}
                  onChange={(e) => setForm({ ...form, spice_preference: e.target.value })}
                >
                  <option value="no_spice">No spice</option>
                  <option value="very_mild">Very mild</option>
                  <option value="mild">Mild</option>
                  <option value="medium">Medium</option>
                  <option value="spicy">Spicy</option>
                  <option value="very_spicy">Very spicy</option>
                </Select>
              </FieldShell>
              <FieldShell label="Typical budget" helper="Pick the price range you usually feel comfortable with per person.">
                <Select
                  className="h-14 text-base md:text-lg"
                  value={form.budget_preference}
                  onChange={(e) => setForm({ ...form, budget_preference: e.target.value })}
                >
                  <option value="under_10">Under $10</option>
                  <option value="10_15">$10 to $15</option>
                  <option value="15_25">$15 to $25</option>
                  <option value="25_40">$25 to $40</option>
                  <option value="40_plus">$40+</option>
                </Select>
              </FieldShell>
              <div className="md:col-span-2 space-y-3">
                <FieldShell
                  label="Restaurant styles you enjoy"
                  helper="Pick the kinds of places you feel like going to most often."
                >
                  <ChoicePills
                    options={DINING_STYLE_OPTIONS}
                    selected={form.preferred_dining_styles}
                    onToggle={toggleDiningStyle}
                  />
                </FieldShell>
                <Input
                  className="h-14 text-base md:text-lg"
                  value={customDiningInput}
                  onChange={(e) => setCustomDiningInput(e.target.value)}
                  placeholder="Other restaurant styles, comma separated"
                />
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => {
                    setForm((current) => ({
                      ...current,
                      preferred_dining_styles: mergeUnique([
                        ...current.preferred_dining_styles,
                        ...splitList(customDiningInput).map((value) =>
                          value.toLowerCase().replaceAll(" ", "_")
                        )
                      ])
                    }));
                    setCustomDiningInput("");
                  }}
                >
                  Add other restaurant styles
                </Button>
              </div>
              <div className="md:col-span-2 space-y-3">
                <FieldShell
                  label="Preferred cuisines"
                  helper="Pick common cuisines below and add any others you want."
                >
                  <ChoicePills
                    options={CUISINE_OPTIONS}
                    selected={form.preferred_cuisines}
                    onToggle={toggleCuisine}
                  />
                </FieldShell>
                <Input
                  className="h-14 text-base md:text-lg"
                  value={customCuisineInput}
                  onChange={(e) => setCustomCuisineInput(e.target.value)}
                  placeholder="Other cuisines, comma separated"
                />
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => {
                    setForm((current) => ({
                      ...current,
                      preferred_cuisines: mergeUnique([
                        ...current.preferred_cuisines,
                        ...splitList(customCuisineInput).map((value) =>
                          value.toLowerCase().replaceAll(" ", "_")
                        )
                      ])
                    }));
                    setCustomCuisineInput("");
                  }}
                >
                  Add other cuisines
                </Button>
              </div>
            </div>
          </section>
        </div>

        <div className="mt-8 flex flex-wrap items-center gap-4">
          <Button
            className="h-14 px-6 text-base md:text-lg"
            onClick={() =>
              startTransition(async () => {
                const saved = await saveProfile({
                  ...form,
                  allergies: splitList(allergiesText),
                  disliked_foods: splitList(dislikedFoodsText)
                });
                setForm(saved);
                setAllergiesText(saved.allergies.join(", "));
                setDislikedFoodsText(saved.disliked_foods.join(", "));
                setStatus("Profile saved.");
                router.push("/login");
              })
            }
          >
            {isPending ? "Saving..." : "Save profile and continue"}
          </Button>
          {status ? <p className="text-lg text-muted-foreground">{status}</p> : null}
        </div>
      </Card>
    </main>
  );
}
