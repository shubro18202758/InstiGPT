import { FC } from "react";

import { Message } from "ai";

import { ChatMessage } from "./ChatMessage";

interface ChatMessagesProps {
  messages: Message[];
  loading: boolean;
}

export const ChatMessages: FC<ChatMessagesProps> = ({ messages, loading }) => {
  return (
    <div className="scrollbar-custom mr-1 h-full overflow-y-auto">
      <div className="mx-auto flex h-full max-w-4xl flex-col gap-6 px-5 pt-6 sm:gap-8 xl:max-w-5xl">
        {messages.map((message, i) => (
          <ChatMessage
            key={message.id}
            message={message}
            loading={loading && i === messages.length - 1}
          />
        ))}
        <div className="h-44 flex-none" />
      </div>
    </div>
  );
};
