"use client";

import { FC } from "react";
import { useRouter } from "next/navigation";

import { PlusIcon } from "@heroicons/react/24/solid";

import { useNewConversationMutation } from "@/lib";
import { ErrorDialog, LoadingIndicator } from "..";

export const NewChatButton: FC = () => {
  const router = useRouter();
  const { mutate, data, isLoading, isError, error } =
    useNewConversationMutation();
  return (
    <>
      <LoadingIndicator loading={isLoading} />
      {isError && <ErrorDialog msg={(error as Error).message} />}
      {data?.detail && <ErrorDialog msg={JSON.stringify(data.detail)} />}
      <button
        className="m-2 flex items-center justify-center rounded-lg border bg-primary-gradient px-2 py-1 font-bold uppercase text-foreground shadow-sm hover:shadow-none"
        onClick={(e) => {
          e.preventDefault();
          // TODO: Show a modal to create a new chat instead
          const title = prompt("Enter a title for the conversation");
          if (title !== null && title !== "") {
            mutate(title, {
              onSuccess: (data) => {
                if (data?.conversation === undefined) return;

                router.push(`/conversation/${data?.conversation.id}`);
              },
            });
          }
        }}
      >
        New Chat <PlusIcon className="ml-1 h-5 w-5" />
      </button>
    </>
  );
};
