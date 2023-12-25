"use client";

import { FC } from "react";
import {
  QueryClient,
  QueryClientProvider,
  useMutation,
  useQuery,
} from "react-query";

import { User } from "./types";

export const queryClient = new QueryClient();

type ApiProviderProps = {
  children: React.ReactNode;
};

export const ApiProvider: FC<ApiProviderProps> = ({ children }) => (
  <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
);

interface LoginMutationResponse {
  user?: User;
  detail?: string;
}
export const useLoginMutation = () =>
  useMutation<LoginMutationResponse, Error, string>(
    (code: string) =>
      fetch(`${process.env.NEXT_PUBLIC_API_URL}/login?code=${code}`, {
        credentials: "include",
      }).then((res) => res.json()),
    {
      onSuccess: (data) => {
        queryClient.setQueryData("me", data);
      },
    },
  );

interface MeQueryResponse {
  user?: User;
  detail?: string;
}
export const useMeQuery = (onSuccess?: (data: MeQueryResponse) => void) =>
  useQuery<MeQueryResponse>(
    "me",
    () =>
      fetch(`${process.env.NEXT_PUBLIC_API_URL}/me`, {
        credentials: "include",
      }).then((res) => res.json()),
    {
      onSuccess,
      refetchOnWindowFocus: false,
      refetchOnMount: false,
      refetchOnReconnect: false,
    },
  );
