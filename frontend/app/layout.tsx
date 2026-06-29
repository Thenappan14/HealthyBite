import type { Metadata } from "next";

import { Navbar } from "@/components/app/navbar";

import "./globals.css";

export const metadata: Metadata = {
  title: "PlateWise",
  description: "Personalized food recommendations from restaurant menus."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <Navbar />
        {children}
      </body>
    </html>
  );
}
