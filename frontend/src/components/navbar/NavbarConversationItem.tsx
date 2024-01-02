import { FC, useState } from "react";
import { useParams, useRouter } from "next/navigation";

import {
  TrashIcon,
  CheckIcon,
  XMarkIcon,
  PencilIcon,
} from "@heroicons/react/24/solid";

import { Conversation } from "@/lib/types";
import {
  useDeleteConversationMutation,
  useEditConversationMutation,
} from "@/lib";
import { ErrorDialog, LoadingIndicator } from "..";

interface NavbarConversationItemProps {
  conversation: Conversation;
}

export const NavbarConversationItem: FC<NavbarConversationItemProps> = ({
  conversation,
}) => {
  const router = useRouter();
  const [confirmDelete, setConfirmDelete] = useState(false);
  const { id: conversationId } = useParams();

  const deleteConversation = useDeleteConversationMutation();
  const editConversation = useEditConversationMutation();

  return (
    <>
      <LoadingIndicator
        loading={deleteConversation.isLoading || editConversation.isLoading}
      />
      <ErrorDialog
        msg={
          deleteConversation.error?.message ??
          editConversation.error?.message ??
          deleteConversation.data?.detail ??
          editConversation.data?.detail
        }
      />
      <a
        onMouseLeave={() => setConfirmDelete(false)}
        href={`/conversation/${conversation.id}`}
        className={`group flex h-10 flex-none items-center gap-1.5 rounded-lg pl-2.5 pr-2 text-gray-300 hover:bg-gray-700 ${
          conversation.id === (conversationId as string) ? "bg-primary/50" : ""
        }`}
      >
        <div className="flex-1 truncate">
          {confirmDelete && <span className="font-semibold"> Delete </span>}
          {conversation.title}
        </div>

        {confirmDelete ? (
          <>
            <button
              type="button"
              className="flex h-5 w-5 items-center justify-center rounded md:hidden md:group-hover:flex"
              title="Confirm delete action"
              onClick={(e) => {
                e.preventDefault();
                deleteConversation.mutate(conversation.id, {
                  onSuccess: () => {
                    setConfirmDelete(false);
                    if (conversation.id === conversationId) {
                      router.push("/");
                    }
                  },
                });
              }}
            >
              <CheckIcon className="text-gray-400 hover:text-gray-300" />
            </button>
            <button
              type="button"
              className="flex h-5 w-5 items-center justify-center rounded md:hidden md:group-hover:flex"
              title="Cancel delete action"
              onClick={(e) => {
                e.preventDefault();
                setConfirmDelete(false);
              }}
            >
              <XMarkIcon className="text-gray-400 hover:text-gray-300" />
            </button>
          </>
        ) : (
          <>
            <button
              type="button"
              className="flex h-5 w-5 items-center justify-center rounded md:hidden md:group-hover:flex"
              title="Edit conversation title"
              onClick={(e) => {
                e.preventDefault();

                const newTitle = prompt(
                  "Edit this conversation title:",
                  conversation.title,
                );
                if (!newTitle) return;
                editConversation.mutate({ id: conversation.id, newTitle });
              }}
            >
              <PencilIcon className="text-xs text-gray-400 hover:text-gray-300" />
            </button>

            <button
              type="button"
              className="flex h-5 w-5 items-center justify-center rounded md:hidden md:group-hover:flex"
              title="Delete conversation"
              onClick={(e) => {
                e.preventDefault();
                setConfirmDelete(true);
              }}
            >
              <TrashIcon className="text-xs text-gray-400  hover:text-gray-300" />
            </button>
          </>
        )}
      </a>
    </>
  );
};
