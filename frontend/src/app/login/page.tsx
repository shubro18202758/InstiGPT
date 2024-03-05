"use client";

import { useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation";

import { ErrorDialog, LoadingIndicator, LogoWithText } from "@/components";
import { useLoginMutation, useMeQuery } from "@/lib";

export default function Login() {
  const router = useRouter();

  const { isLoading: isMeLoading } = useMeQuery(
    (data) => data.user && router.replace("/"),
  );

  const {
    mutate,
    data,
    isLoading: isLoginLoading,
    isError: isLoginError,
    error: loginError,
  } = useLoginMutation();
  const searchParams = useSearchParams();
  const code = searchParams.get("code");

  useEffect(() => {
    if (!isMeLoading && code !== null) {
      mutate(code, {
        onSuccess: (data) => data.user && router.replace("/"),
      });
    }
  }, [isMeLoading, code, mutate, router]);

  return (
    <>
      <LoadingIndicator loading={isLoginLoading || isMeLoading} />
      <div className="grid h-screen w-screen place-items-center px-10">
        <div className="rounded-xl bg-background-alt p-10 text-center">
          {isLoginError && <ErrorDialog msg={(loginError as Error).message} />}
          {data?.detail && <ErrorDialog msg={data.detail} />}
          <LogoWithText className="h-24" />
          <button className="mt-10 rounded-lg bg-primary-gradient p-3 md:p-5 md:text-xl lg:text-3xl">
            <a href={process.env.NEXT_PUBLIC_SSO_URL}>SSO Login</a>
          </button>
        </div>
      </div>
    </>
  );
}
