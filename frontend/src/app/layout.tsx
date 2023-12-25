import type { Metadata } from "next";
import { Montserrat } from "next/font/google";

import { ApiProvider } from "@/lib/api";
import "./globals.css";

const font = Montserrat({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "InstiGPT",
  description: "Insti's ChatGPT",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link
          rel="apple-touch-icon"
          sizes="180x180"
          href="/apple-touch-icon.png"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="32x32"
          href="/favicon-32x32.png"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="16x16"
          href="/favicon-16x16.png"
        />
        <link rel="manifest" href="/site.webmanifest" />
        <link rel="mask-icon" href="/safari-pinned-tab.svg" color="#9b6eff" />
        <meta name="msapplication-TileColor" content="#da532c" />
        <meta name="theme-color" content="#9b6eff"></meta>
      </head>
      <body className={font.className}>
        <ApiProvider>{children}</ApiProvider>
      </body>
    </html>
  );
}
