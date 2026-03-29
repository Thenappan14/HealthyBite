import Link from "next/link";

import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export default function SignUpPage() {
  return (
    <main className="mx-auto max-w-xl px-4 py-10 md:px-6">
      <Card className="mx-auto max-w-xl">
        <p className="text-xs font-semibold uppercase tracking-[0.24em] text-muted-foreground">Start here</p>
        <CardTitle className="mt-3">Create your PlateWise account</CardTitle>
        <CardDescription className="mt-3">
          Create a profile first, then upload a menu or paste a restaurant URL to get ranked dishes.
        </CardDescription>
        <div className="mt-8 space-y-4">
          <Input placeholder="Email address" type="email" />
          <Input placeholder="Password" type="password" />
          <Button className="w-full">Sign up</Button>
        </div>
        <p className="mt-5 text-sm text-muted-foreground">
          Already have an account? <Link href="/login" className="text-primary">Log in</Link>
        </p>
      </Card>
    </main>
  );
}

