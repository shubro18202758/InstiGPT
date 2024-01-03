"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { useMeQuery } from "@/lib";
import {
  DisclaimerModal,
  ErrorDialog,
  LoadingIndicator,
  Navbar,
} from "@/components";

export default function Layout({ children }: { children: React.ReactNode }) {
  const [disclaimerShown, setDisclaimerShown] = useState<boolean | null>(null);

  const router = useRouter();
  const { data, isLoading, isError, error } = useMeQuery(
    (data) => !data.user && router.replace("/login"),
  );

  useEffect(() => {
    const storedItem = localStorage.getItem("disclaimerShown");
    if (storedItem === "true") {
      setDisclaimerShown(true);
    } else {
      setDisclaimerShown(false);
    }
  }, []);

  return (
    <div className="text-md grid min-h-screen w-screen grid-cols-1 grid-rows-[auto,1fr] overflow-hidden text-gray-300 md:grid-cols-[280px,1fr] md:grid-rows-[1fr]">
      <LoadingIndicator loading={isLoading} />
      <ErrorDialog msg={error?.message ?? data?.detail} />
      <Navbar />
      {!isLoading &&
        !isError &&
        data?.detail === undefined &&
        disclaimerShown === false && (
          <DisclaimerModal
            setShown={() => {
              setDisclaimerShown(true);
              localStorage.setItem("disclaimerShown", "true");
            }}
          />
        )}
      {children}
    </div>
  );
}
