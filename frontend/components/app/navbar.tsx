import Link from "next/link";

import { OwlCluster } from "@/components/app/owl-cluster";
import { Button } from "@/components/ui/button";

const links = [
  { href: "/profile", label: "Profile" },
  { href: "/dashboard", label: "Dashboard" },
  { href: "/upload", label: "Menu Analysis" },
  { href: "/saved", label: "Saved" }
];

export function Navbar() {
  return (
    <header className="sticky top-0 z-20 border-b border-white/30 bg-background/85 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center gap-4 px-4 py-4 md:px-6">
        <Link href="/" className="shrink-0 font-display text-4xl text-foreground md:text-5xl">
          PlateWise
        </Link>
        <nav className="hidden flex-1 items-center justify-center gap-6 md:flex lg:gap-8">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="whitespace-nowrap text-lg text-muted-foreground transition hover:text-foreground md:text-xl"
            >
              {link.label}
            </Link>
          ))}
        </nav>
        <div className="ml-auto flex shrink-0 items-center gap-2 md:gap-3">
          <OwlCluster compact />
          <Button variant="outline" size="sm" asChild className="whitespace-nowrap px-4 text-base md:text-lg">
            <Link href="/login">Log in</Link>
          </Button>
          <Button size="sm" asChild className="whitespace-nowrap px-4 text-base md:text-lg">
            <Link href="/signup">Sign up</Link>
          </Button>
        </div>
      </div>
    </header>
  );
}
