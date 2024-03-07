"use client";

import { FC, useRef, useState } from "react";

import {
  ConversationMessagesQueryResponse,
  queryClient,
  useChatCompletionsMutation,
  useConversationMessagesQuery,
  useEditConversationMutation,
} from "@/lib";
import { ErrorDialog, LoadingIndicator } from "@/components";

import { ChatMessage } from "./ChatMessage";
import { ChatInput } from "./ChatInput";

interface ChatWindowProps {
  conversationId: string;
}

export const ChatWindow: FC<ChatWindowProps> = ({ conversationId }) => {
  const messagesContainerRef = useRef<HTMLDivElement>(null);
  const [question, setQuestion] = useState("");

  const messages = useConversationMessagesQuery(conversationId, scrollToBottom);
  const editConversation = useEditConversationMutation();
  const completion = useChatCompletionsMutation();

  function scrollToBottom() {
    setTimeout(() => {
      if (messagesContainerRef.current) {
        messagesContainerRef.current.scrollTo({
          top: messagesContainerRef.current.scrollHeight,
          behavior: "smooth",
        });
      }
    }, 100);
  }

  return (
    <>
      <LoadingIndicator
        loading={messages.isLoading || editConversation.isLoading}
      />
      <ErrorDialog
        msg={
          messages.error?.message ??
          completion.error?.message ??
          editConversation.error?.message ??
          messages.data?.detail ??
          completion.data?.detail ??
          editConversation.data?.detail
        }
      />
      <div className="relative max-h-screen">
        {messages.data && messages.data.messages && (
          <div
            ref={messagesContainerRef}
            className="scrollbar-custom mr-1 h-full overflow-y-auto"
          >
            <div className="mx-auto flex h-full max-w-4xl flex-col gap-6 px-5 pt-6 sm:gap-8 xl:max-w-5xl">
              {messages.data.messages.map((message) => (
                <ChatMessage key={message.id} message={message} />
              ))}
              {completion.isLoading && completion.variables && (
                <>
                  <ChatMessage
                    message={{
                      id: "None",
                      content: completion.variables.question,
                      conversation_id: completion.variables.id,
                      created_at: new Date().toISOString(),
                      role: "user",
                    }}
                  />
                  <ChatMessage
                    message={{
                      id: "None",
                      content: "",
                      conversation_id: completion.variables.id,
                      created_at: new Date().toISOString(),
                      role: "assistant",
                    }}
                    loading
                  />
                </>
              )}
              <div className="h-44 flex-none" />
            </div>
          </div>
        )}
        <ChatInput
          input={question}
          handleInputChange={(e) => setQuestion(e.target.value)}
          handleSubmit={(e) => {
            e.preventDefault();
            scrollToBottom();

            if (messages.data?.messages?.length === 0)
              editConversation.mutate({
                id: conversationId,
                newTitle: question,
              });

            completion.mutate(
              { id: conversationId, question: question },
              {
                onSuccess: (data) => {
                  if (data.new_messages) {
                    queryClient.setQueryData(
                      ["messages", conversationId],
                      (prevData?: ConversationMessagesQueryResponse) => {
                        if (prevData?.messages) {
                          return {
                            messages: [
                              ...prevData.messages,
                              ...data.new_messages!,
                            ],
                          };
                        }
                        return { messages: [...data.new_messages!] };
                      },
                    );
                  }
                  setQuestion("");
                  scrollToBottom();
                },
              },
            );
          }}
          isLoading={completion.isLoading}
        />
      </div>
    </>
  );
};
