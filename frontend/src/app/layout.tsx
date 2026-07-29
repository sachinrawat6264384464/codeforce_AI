import "./globals.css";
import "driver.js/dist/driver.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "ContextForge AI - Context-Aware AI Software Engineering Platform",
  description: "Powered by DataHub for Metadata-Aware AI Code Generation",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#030712] text-slate-100 antialiased min-h-screen">
        {children}
      </body>
    </html>
  );
}
