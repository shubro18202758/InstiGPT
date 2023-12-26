import { FC, useState } from "react";
import { useParams } from "next/navigation";

import {
  TrashIcon,
  CheckIcon,
  XMarkIcon,
  PencilIcon,
} from "@heroicons/react/24/solid";

interface Conversation {
  id: number;
  title: string;
  updatedAt: number;
}
interface NavbarConversationItemProps {
  conversation: Conversation;
}

export const NavbarConversationItem: FC<NavbarConversationItemProps> = ({
  conversation,
}) => {
  const [confirmDelete, setConfirmDelete] = useState(false);
  const { id: conversationId } = useParams();

  return (
    <a
      onMouseLeave={() => setConfirmDelete(false)}
      href={`/conversation/${conversation.id}`}
      className={`group flex h-10 flex-none items-center gap-1.5 rounded-lg pl-2.5 pr-2 text-gray-300 hover:bg-gray-700 ${
        conversation.id === parseInt((conversationId as string) || "0")
          ? "bg-primary/50"
          : ""
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
              // TODO: Delete the conversation here
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
              // TODO: Edit the converation title here
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
  );
};
