import type { Metadata } from "next";
import { Fraunces, Manrope } from "next/font/google";

import { Navbar } from "@/components/app/navbar";

import "./globals.css";

const display = Fraunces({ subsets: ["latin"], variable: "--font-display" });
const sans = Manrope({ subsets: ["latin"], variable: "--font-sans" });

export const metadata: Metadata = {
  title: "PlateWise",
  description: "Personalized food recommendations from restaurant menus."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={`${display.variable} ${sans.variable}`}>
        <Navbar />
        {children}
      </body>
    </html>
  );
}

