"use client";

import { useState, useTransition } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { defaultProfile } from "@/lib/mock-data";
import { saveProfile } from "@/lib/api";

function splitList(value: string) {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

export default function ProfilePage() {
  const [isPending, startTransition] = useTransition();
  const [status, setStatus] = useState("");
  const [form, setForm] = useState(defaultProfile);

  return (
    <main className="mx-auto max-w-5xl px-4 py-10 md:px-6">
      <Card>
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-muted-foreground">Profile setup</p>
        <CardTitle className="mt-3">Tell PlateWise how to rank menus for you</CardTitle>
        <CardDescription className="mt-3">
          Your profile is used to filter incompatible dishes and tune the estimated scoring logic.
        </CardDescription>

        <div className="mt-8 grid gap-4 md:grid-cols-2">
          <Input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="Name" />
          <Input value={form.age} onChange={(e) => setForm({ ...form, age: Number(e.target.value) })} placeholder="Age" type="number" />
          <Select value={form.sex} onChange={(e) => setForm({ ...form, sex: e.target.value })}>
            <option value="female">Female</option>
            <option value="male">Male</option>
            <option value="non_binary">Non-binary</option>
          </Select>
          <Select value={form.activity_level} onChange={(e) => setForm({ ...form, activity_level: e.target.value })}>
            <option value="lightly_active">Lightly active</option>
            <option value="moderately_active">Moderately active</option>
            <option value="very_active">Very active</option>
          </Select>
          <Input value={form.height_cm} onChange={(e) => setForm({ ...form, height_cm: Number(e.target.value) })} placeholder="Height (cm)" type="number" />
          <Input value={form.weight_kg} onChange={(e) => setForm({ ...form, weight_kg: Number(e.target.value) })} placeholder="Weight (kg)" type="number" />
          <Select value={form.primary_goal} onChange={(e) => setForm({ ...form, primary_goal: e.target.value })}>
            <option value="fat_loss">Fat loss</option>
            <option value="muscle_gain">Muscle gain</option>
            <option value="maintenance">Maintenance</option>
            <option value="better_energy">Better energy</option>
            <option value="balanced_eating">Balanced eating</option>
          </Select>
          <Select value={form.diet_type} onChange={(e) => setForm({ ...form, diet_type: e.target.value })}>
            <option value="none">None</option>
            <option value="vegetarian">Vegetarian</option>
            <option value="vegan">Vegan</option>
            <option value="halal">Halal</option>
            <option value="pescatarian">Pescatarian</option>
            <option value="lactose_free">Lactose free</option>
            <option value="gluten_free">Gluten free</option>
          </Select>
          <Select value={form.spice_preference} onChange={(e) => setForm({ ...form, spice_preference: e.target.value })}>
            <option value="mild">Mild</option>
            <option value="medium">Medium</option>
            <option value="hot">Hot</option>
          </Select>
          <Select value={form.budget_preference} onChange={(e) => setForm({ ...form, budget_preference: e.target.value })}>
            <option value="budget">Budget</option>
            <option value="moderate">Moderate</option>
            <option value="flexible">Flexible</option>
          </Select>
          <Textarea
            className="md:col-span-2"
            value={form.allergies.join(", ")}
            onChange={(e) => setForm({ ...form, allergies: splitList(e.target.value) })}
            placeholder="Allergies, comma separated"
          />
          <Textarea
            className="md:col-span-2"
            value={form.disliked_foods.join(", ")}
            onChange={(e) => setForm({ ...form, disliked_foods: splitList(e.target.value) })}
            placeholder="Disliked foods, comma separated"
          />
          <Textarea
            className="md:col-span-2"
            value={form.preferred_cuisines.join(", ")}
            onChange={(e) => setForm({ ...form, preferred_cuisines: splitList(e.target.value) })}
            placeholder="Preferred cuisines, comma separated"
          />
        </div>

        <div className="mt-6 flex flex-wrap items-center gap-3">
          <Button
            onClick={() =>
              startTransition(async () => {
                const saved = await saveProfile(form);
                setForm(saved);
                setStatus("Profile saved.");
              })
            }
          >
            {isPending ? "Saving..." : "Save profile"}
          </Button>
          {status ? <p className="text-sm text-muted-foreground">{status}</p> : null}
        </div>
      </Card>
    </main>
  );
}

