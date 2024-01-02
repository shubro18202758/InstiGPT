"use client";

import { useRouter } from "next/navigation";

import { useMeQuery } from "@/lib";
import { ErrorDialog, LoadingIndicator, Navbar } from "@/components";

export default function Layout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { data, isLoading, error } = useMeQuery(
    (data) => !data.user && router.replace("/login"),
  );

  return (
    <div className="text-md grid min-h-screen w-screen grid-cols-1 grid-rows-[auto,1fr] overflow-hidden text-gray-300 md:grid-cols-[280px,1fr] md:grid-rows-[1fr]">
      <LoadingIndicator loading={isLoading} />
      <ErrorDialog msg={error?.message ?? data?.detail} />
      <Navbar />
      {children}
    </div>
  );
}
