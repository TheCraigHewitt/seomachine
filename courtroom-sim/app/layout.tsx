import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Defense Counsel — Courtroom Simulator",
  description: "Defend clients in simulated criminal trials inspired by real gang, RICO and murder cases. Speak live, object, cross-examine, and win over the jury.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link
          href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@500;600;700&family=Inter:wght@400;500;600&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="min-h-screen antialiased" suppressHydrationWarning>{children}</body>
    </html>
  );
}
