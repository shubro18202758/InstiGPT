"use client";

import { FC } from "react";
import {
  QueryClient,
  QueryClientProvider,
  useMutation,
  useQuery,
} from "react-query";

import type { User, Conversation, Message } from "./types";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      refetchOnMount: false,
      refetchOnReconnect: false,
    },
  },
});

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

interface LogoutMutationResponse {
  success?: boolean;
  detail?: string;
}
export const useLogoutMutation = () =>
  useMutation<LogoutMutationResponse, Error>(
    () =>
      fetch(`${process.env.NEXT_PUBLIC_API_URL}/logout`, {
        credentials: "include",
      }).then((res) => res.json()),
    {
      onSuccess: () => {
        queryClient.invalidateQueries("me");
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
    },
  );

interface ConversationsQueryResponse {
  conversations?: Conversation[];
  detail?: string;
}
export const useConversationsQuery = () =>
  useQuery<ConversationsQueryResponse>("all-conversations", () =>
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/conversation`, {
      credentials: "include",
    }).then((res) => res.json()),
  );

interface NewConversationMutationResponse {
  conversation?: Conversation;
  detail?: string;
}
export const useNewConversationMutation = () =>
  useMutation<NewConversationMutationResponse, Error, string>(
    (title: string) =>
      fetch(`${process.env.NEXT_PUBLIC_API_URL}/conversation`, {
        method: "POST",
        body: JSON.stringify({ title }),
        credentials: "include",
        headers: {
          "content-type": "application/json",
        },
      }).then((res) => res.json()),
    {
      onSuccess: (data) => {
        if (data.conversation) {
          queryClient.setQueryData(
            "all-conversations",
            (prevData?: ConversationsQueryResponse) => {
              if (!prevData?.conversations) {
                return { conversations: [data.conversation!] };
              }
              return {
                conversations: [data.conversation!, ...prevData.conversations],
              };
            },
          );
        }
      },
    },
  );

interface DeleteConversationMutationResponse {
  success?: boolean;
  detail?: string;
}
export const useDeleteConversationMutation = () =>
  useMutation<DeleteConversationMutationResponse, Error, string>(
    (id: string) =>
      fetch(`${process.env.NEXT_PUBLIC_API_URL}/conversation/${id}`, {
        method: "DELETE",
        credentials: "include",
      }).then((res) => res.json()),
    {
      onSuccess: (data) => {
        if (data.success) {
          queryClient.invalidateQueries("all-conversations");
        }
      },
    },
  );

interface EditConversationVariables {
  id: string;
  newTitle: string;
}
interface EditConversationMutationResponse {
  conversation?: Conversation;
  detail?: string;
}
export const useEditConversationMutation = () =>
  useMutation<
    EditConversationMutationResponse,
    Error,
    EditConversationVariables
  >(
    ({ id, newTitle }) =>
      fetch(`${process.env.NEXT_PUBLIC_API_URL}/conversation/${id}`, {
        method: "PATCH",
        body: JSON.stringify({ title: newTitle }),
        credentials: "include",
        headers: {
          "content-type": "application/json",
        },
      }).then((res) => res.json()),
    {
      onSuccess: (data) => {
        if (data.conversation) {
          queryClient.setQueryData(
            "all-conversations",
            (prevData?: ConversationsQueryResponse) => {
              if (!prevData?.conversations) {
                return { conversations: [data.conversation!] };
              }
              const conversations = [...prevData.conversations];
              const index = conversations.findIndex(
                (c) => c.id === data.conversation!.id,
              );
              if (index !== undefined && index !== -1) {
                conversations[index] = data.conversation!;
              }
              return { conversations: conversations };
            },
          );
        }
      },
    },
  );

export interface ConversationMessagesQueryResponse {
  messages?: Message[];
  detail?: string;
}
export const useConversationMessagesQuery = (
  id?: string,
  onSuccess?: () => void,
) =>
  useQuery<ConversationMessagesQueryResponse, Error>(
    ["messages", id],
    () =>
      fetch(`${process.env.NEXT_PUBLIC_API_URL}/conversation/${id}`, {
        credentials: "include",
      }).then((res) => res.json()),
    { enabled: id !== undefined, onSuccess },
  );

interface ChatCompletionVariables {
  id: string;
  question: string;
}
interface ChatCompletionReponse {
  new_messages?: Message[];
  detail?: string;
}
export const useChatCompletionsMutation = () =>
  useMutation<ChatCompletionReponse, Error, ChatCompletionVariables>(
    ({ id, question }) =>
      fetch(`${process.env.NEXT_PUBLIC_API_URL}/conversation/${id}/chat`, {
        method: "POST",
        body: JSON.stringify({ question }),
        headers: {
          "content-type": "application/json",
        },
        credentials: "include",
      }).then((res) => res.json()),
  );
