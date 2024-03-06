"use client";

import { FC, useState } from "react";
import { useRouter } from "next/navigation";

import { PlusIcon } from "@heroicons/react/24/solid";

import { useNewConversationMutation } from "@/lib";
import { ErrorDialog, LoadingIndicator } from "@/components";
import { EnterTitleModal } from "./EnterTitleModal";

interface NewChatButtonProps {
  close?: () => void;
}

export const NewChatButton: FC<NewChatButtonProps> = ({ close }) => {
  const router = useRouter();
  const { mutate, data, isLoading, error } = useNewConversationMutation();

  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <>
      <EnterTitleModal
        isOpen={isModalOpen}
        closeModal={() => setIsModalOpen(false)}
        isLoading={isLoading}
        title="New Conversation"
        onSubmit={(title) => {
          if (title !== null && title !== "") {
            mutate(title, {
              onSuccess: (data) => {
                if (data?.conversation === undefined) return;

                close?.();
                router.push(`/conversation/${data?.conversation.id}`);
              },
              onSettled: () => setIsModalOpen(false),
            });
          }
        }}
      />
      <LoadingIndicator loading={isLoading} />
      <ErrorDialog msg={error?.message ?? data?.detail} />
      <button
        className="m-2 flex w-full max-w-full items-center justify-center rounded-lg border bg-primary-gradient px-2 py-1 font-bold uppercase text-foreground shadow-sm hover:shadow-none"
        onClick={() => setIsModalOpen(true)}
      >
        New Chat <PlusIcon className="ml-1 h-5 w-5" />
      </button>
    </>
  );
};
