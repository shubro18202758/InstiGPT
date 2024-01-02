import { FC, useMemo } from "react";

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
  const sources = useMemo(() => {
    if (!message.sources) return [];

    return message.sources.split(",").map((source) => {
      try {
        const url = new URL(source);
        return { name: url.hostname, link: source };
      } catch {
        return { name: source, link: null };
      }
    });
  }, [message.sources]);

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
              className="prose prose-invert"
            >
              {message.content.trim()}
            </Markdown>
          ) : (
            <div>{message.content.trim()}</div>
          )}
        </div>
        <div className="flex justify-end">
          {loading && (
            <div className="flex items-center justify-center gap-4">
              Generating response... <LoadingIndicatorWithoutBackdrop loading />
            </div>
          )}
        </div>

        {message.role === "assistant" && sources.length > 0 && (
          <div className="mt-4 flex flex-wrap items-center gap-x-2 gap-y-1.5 text-sm">
            <div className="text-gray-400">Sources:</div>
            {sources.map(({ name, link }, i) => (
              <a
                key={i}
                className="flex max-w-[150px] items-center gap-2 whitespace-nowrap rounded-lg border border-gray-800 bg-gray-900 px-2 py-1.5 leading-none hover:border-gray-700"
                href={link || "#"}
                target="_blank"
              >
                <span className="truncate">{name}</span>
              </a>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
