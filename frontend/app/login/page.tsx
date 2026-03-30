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
  const [email, setEmail] = useState("demo@platewise.app");
  const [password, setPassword] = useState("demo1234");
  const [message, setMessage] = useState("");
  const [isPending, startTransition] = useTransition();

  return (
    <main className="mx-auto max-w-xl px-4 py-10 md:px-6">
      <Card className="mx-auto max-w-xl">
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-muted-foreground">Welcome back</p>
        <CardTitle className="mt-3">Log in to PlateWise</CardTitle>
        <CardDescription className="mt-3">
          Use the demo account from the README or wire this form to the FastAPI auth endpoints.
        </CardDescription>
        <div className="mt-8 space-y-4">
          <Input placeholder="Email address" type="email" value={email} onChange={(event) => setEmail(event.target.value)} />
          <Input placeholder="Password" type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
          <Button
            className="w-full"
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
        {message ? <p className="mt-5 text-sm text-muted-foreground">{message}</p> : null}
        <p className="mt-5 text-sm text-muted-foreground">
          New here? <Link href="/signup" className="text-primary">Create an account</Link>
        </p>
      </Card>
    </main>
  );
}
