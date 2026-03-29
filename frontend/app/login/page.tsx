import Link from "next/link";

import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export default function LoginPage() {
  return (
    <main className="mx-auto max-w-xl px-4 py-10 md:px-6">
      <Card className="mx-auto max-w-xl">
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-muted-foreground">Welcome back</p>
        <CardTitle className="mt-3">Log in to PlateWise</CardTitle>
        <CardDescription className="mt-3">
          Use the demo account from the README or wire this form to the FastAPI auth endpoints.
        </CardDescription>
        <div className="mt-8 space-y-4">
          <Input placeholder="Email address" type="email" />
          <Input placeholder="Password" type="password" />
          <Button className="w-full">Log in</Button>
        </div>
        <p className="mt-5 text-sm text-muted-foreground">
          New here? <Link href="/signup" className="text-primary">Create an account</Link>
        </p>
      </Card>
    </main>
  );
}

