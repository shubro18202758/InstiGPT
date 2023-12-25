"use client";

import Image from "next/image";
import { useRouter } from "next/navigation";

import { useMeQuery } from "@/lib";
import { ErrorDialog, LoadingIndicator } from "@/components";

export default function Layout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { data, isLoading, isError, error } = useMeQuery(
    (data) => !data.user && router.replace("/login"),
  );

  return (
    <>
      <LoadingIndicator loading={isLoading} />
      {isError && <ErrorDialog msg={(error as Error).message} />}
      {data?.message && <ErrorDialog msg={data.message} />}
      <nav className="grid place-items-center bg-background-alt p-4">
        <Image
          src="/logo-with-text.svg"
          alt="logo"
          width={3.7 * 60}
          height={60}
        />
      </nav>
      {children}
    </>
  );
}
