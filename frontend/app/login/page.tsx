"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, useTransition } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { login, persistAuthSession } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [isPending, startTransition] = useTransition();

  return (
    <main className="mx-auto max-w-2xl px-4 py-10 md:px-6">
      <Card className="mx-auto max-w-2xl p-8 md:p-10">
        <p className="text-sm font-semibold uppercase tracking-[0.24em] text-muted-foreground">Welcome back</p>
        <CardTitle className="mt-3 text-4xl md:text-5xl">Log in to PlateWise</CardTitle>
        <CardDescription className="mt-4 text-lg md:text-xl">
          Sign in to continue with your saved profile, menu analysis, and recommendation history.
        </CardDescription>
        <div className="mt-8 space-y-4">
          <Input
            className="h-14 text-base md:text-lg"
            placeholder="Email address"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />
          <Input
            className="h-14 text-base md:text-lg"
            placeholder="Password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
          <Button
            className="h-14 w-full text-base md:text-lg"
            onClick={() =>
              startTransition(async () => {
                try {
                  const auth = await login(email, password);
                  persistAuthSession(auth);
                  setMessage("Logged in successfully.");
                  router.push("/dashboard");
                } catch {
                  setMessage("Login failed. Check your credentials and backend.");
                }
              })
            }
          >
            {isPending ? "Logging in..." : "Log in"}
          </Button>
        </div>
        {message ? <p className="mt-5 text-base text-muted-foreground">{message}</p> : null}
        <p className="mt-6 text-base md:text-lg text-muted-foreground">
          New here? <Link href="/signup" className="text-primary">Create an account</Link>
        </p>
      </Card>
    </main>
  );
}
