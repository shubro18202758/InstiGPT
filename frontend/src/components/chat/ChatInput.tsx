import { FC, useRef } from "react";

import { PaperAirplaneIcon } from "@heroicons/react/24/solid";

import { LoadingIndicatorWithoutBackdrop } from "../LoadingIndicator";

interface ChatInputProps {
  input: string;
  handleInputChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  handleSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
  isLoading: boolean;
}

export const ChatInput: FC<ChatInputProps> = ({
  input,
  handleInputChange,
  handleSubmit,
  isLoading,
}) => {
  const submitBtnRef = useRef<HTMLButtonElement>(null);

  return (
    <div className="pointer-events-none absolute inset-x-0 bottom-0 z-0 mx-auto flex w-full max-w-3xl flex-col items-center justify-center px-3.5 py-4 sm:px-5 md:py-8 xl:max-w-4xl [&>*]:pointer-events-auto">
      <div className="w-full">
        <form
          onSubmit={handleSubmit}
          className="relative flex w-full max-w-4xl flex-1 items-center rounded-xl border border-primary bg-background-alt focus-within:border-accent"
        >
          <div className="flex w-full flex-1 border-none bg-transparent">
            <div className="relative min-w-0 flex-1">
              <pre
                className="scrollbar-custom invisible max-h-40 overflow-x-hidden overflow-y-scroll whitespace-pre-wrap break-words p-3"
                aria-hidden="true"
              >
                {input + "\n"}
              </pre>
              <textarea
                placeholder="Ask anything"
                value={input}
                className={`scrollbar-custom absolute top-0 m-0 h-full w-full resize-none scroll-p-3 overflow-x-hidden overflow-y-scroll border-0 bg-transparent p-3 outline-none focus:ring-0 focus-visible:ring-0 ${
                  isLoading ? "text-gray-400" : ""
                }`}
                disabled={isLoading}
                onChange={handleInputChange}
                onKeyDown={(e) => {
                  if (!e.shiftKey && e.key === "Enter") {
                    e.preventDefault();
                    submitBtnRef.current?.click();
                  }
                }}
              />
            </div>

            <button
              ref={submitBtnRef}
              className={`mx-1 my-1 inline-flex h-[2.4rem] flex-shrink-0 cursor-pointer
              items-center justify-center self-end whitespace-nowrap rounded-lg bg-transparent
              p-1 px-[0.7rem] text-gray-400 outline-none transition-all focus:ring
              enabled:hover:text-gray-100 disabled:cursor-default disabled:opacity-40`}
              disabled={!input || isLoading}
              type="submit"
            >
              {isLoading ? (
                <LoadingIndicatorWithoutBackdrop loading />
              ) : (
                <PaperAirplaneIcon className="h-full w-full" />
              )}
            </button>
          </div>
        </form>
      </div>
      <div className="mt-2 flex justify-between self-stretch px-1 text-xs text-gray-400/90 max-md:mb-2 max-sm:gap-2">
        <p>Generated content may be inaccurate or false.</p>
      </div>
    </div>
  );
};
