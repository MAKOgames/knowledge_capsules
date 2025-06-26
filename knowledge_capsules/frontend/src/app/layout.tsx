import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./../styles/globals.css";

import { cn } from "@/lib/utils";
import { AuthProvider } from "@/context/AuthContext";

const fontSans = Inter({
  subsets: ["latin", "cyrillic"],
  variable: "--font-sans",
})

export const metadata: Metadata = {
  title: "Капсулы Знаний",
  description: "Сервис для запоминания ключевых идей из контента",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ru" suppressHydrationWarning>
      <body
        className={cn(
          "min-h-screen bg-background font-sans antialiased",
          fontSans.variable
        )}
      >
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
