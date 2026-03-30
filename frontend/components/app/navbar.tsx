import Link from "next/link";

import { OwlCluster } from "@/components/app/owl-cluster";
import { Button } from "@/components/ui/button";

const links = [
  { href: "/profile", label: "Profile" },
  { href: "/dashboard", label: "Dashboard" },
  { href: "/upload", label: "Upload" },
  { href: "/analyze-url", label: "Restaurant URL" },
  { href: "/results", label: "Results" },
  { href: "/saved", label: "Saved" }
];

export function Navbar() {
  return (
    <header className="sticky top-0 z-20 border-b border-white/30 bg-background/85 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 md:px-6">
        <Link href="/" className="font-display text-3xl text-foreground md:text-4xl">
          PlateWise
        </Link>
        <nav className="hidden items-center gap-5 md:flex">
          {links.map((link) => (
            <Link key={link.href} href={link.href} className="text-base text-muted-foreground transition hover:text-foreground">
              {link.label}
            </Link>
          ))}
        </nav>
        <div className="flex items-center gap-3">
          <OwlCluster compact />
          <Button variant="outline" size="sm" asChild className="text-base">
            <Link href="/login">Log in</Link>
          </Button>
          <Button size="sm" asChild className="text-base">
            <Link href="/signup">Sign up</Link>
          </Button>
        </div>
      </div>
    </header>
  );
}
