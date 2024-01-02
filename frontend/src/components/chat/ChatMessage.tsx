import { FC } from "react";

import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { UserIcon } from "@heroicons/react/24/outline";

import { Message } from "@/lib/types";
import { Logo, LoadingIndicatorWithoutBackdrop } from "..";

interface ChatMessageProps {
  message: Message;
  loading?: boolean;
}

export const ChatMessage: FC<ChatMessageProps> = ({
  message,
  loading = false,
}) => {
  return (
    <div
      className={`group relative -mb-8 flex items-start justify-start gap-4 pb-8 leading-relaxed
                ${
                  message.role === "assistant" ? "flex-row" : "flex-row-reverse"
                }`}
      role="presentation"
    >
      <div className="mt-5 grid h-14 w-14 flex-none place-items-center rounded-full bg-primary shadow-lg">
        {message.role === "assistant" ? (
          <span className="m-2">
            <Logo />
          </span>
        ) : (
          <span className="flex items-center justify-center text-foreground">
            <UserIcon className="m-2 h-full w-full" />
          </span>
        )}
      </div>
      <div className="relative min-h-[calc(2rem+theme(spacing[3.5])*2)] min-w-[60px] break-words rounded-2xl border border-gray-800 bg-gradient-to-br from-gray-800/40 px-5 py-3.5 text-gray-300 prose-pre:my-2">
        <div className="max-w-full break-words rounded-2xl px-5 py-3.5 text-gray-400">
          {message.role === "assistant" ? (
            <Markdown
              remarkPlugins={[remarkGfm]}
              className="prose text-gray-400"
            >
              {message.content.trim()}
            </Markdown>
          ) : (
            <div>{message.content.trim()}</div>
          )}
        </div>
        <div className="flex justify-end">
          {loading && <LoadingIndicatorWithoutBackdrop loading />}
        </div>

        {message.role === "assistant" && (
          <div className="mt-4 flex flex-wrap items-center gap-x-2 gap-y-1.5 text-sm">
            <div className="text-gray-400">Sources:</div>
            {["source 1", "source 2"].map((source, i) => (
              <a
                key={i}
                className="flex items-center gap-2 whitespace-nowrap rounded-lg border bg-white px-2 py-1.5 leading-none hover:border-gray-300 dark:border-gray-800 dark:bg-gray-900 dark:hover:border-gray-700"
                href="#"
                target="_blank"
              >
                <div>{source}</div>
              </a>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
