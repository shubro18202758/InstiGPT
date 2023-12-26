import { FC } from "react";

import { useChat } from "ai/react";

import { ChatInput } from "./ChatInput";
import { ChatMessages } from "./ChatMessages";

interface ChatWindowProps {}

export const ChatWindow: FC<ChatWindowProps> = () => {
  const { messages, input, handleInputChange, handleSubmit, isLoading } =
    useChat({
      api: "http://localhost:5000/chat",
      credentials: "include",
    });

  return (
    <div className="relative max-h-screen">
      <ChatMessages
        messages={[
          {
            id: "1",
            content:
              "Lorem ipsum dolor sit amet consectetur adipisicing elit. Ad, quasi? Quos repellendus at aspernatur quis nisi! Maiores possimus fugit in dolorem iusto neque iste ex a libero perferendis, expedita molestias earum sequi, ea molestiae distinctio ipsa fugiat eius nulla voluptatem id aliquam asperiores harum. Consequatur qui sequi, velit vitae ea reiciendis debitis esse aperiam nulla. Fugiat impedit omnis in officiis itaque, aut praesentium nihil eius expedita voluptates dolor iste molestiae recusandae aspernatur repellat consectetur dolorem cumque sapiente nostrum similique ut suscipit! Distinctio debitis recusandae minus odio sit reprehenderit voluptatibus eum atque, libero esse et facilis laboriosam expedita inventore exercitationem quam?",
            role: "assistant",
          },
          {
            id: "2",
            content:
              "a short question as the user input is usually not very long",
            role: "user",
          },
          {
            id: "3",
            content:
              "Lorem ipsum dolor sit amet consectetur adipisicing elit. Ad, quasi? Quos repellendus at aspernatur quis nisi! Maiores possimus fugit in dolorem iusto neque iste ex a libero perferendis, expedita molestias earum sequi, ea molestiae distinctio ipsa fugiat eius nulla voluptatem id aliquam asperiores harum. Consequatur qui sequi, velit vitae ea reiciendis debitis esse aperiam nulla. Fugiat impedit omnis in officiis itaque, aut praesentium nihil eius expedita voluptates dolor iste molestiae recusandae aspernatur repellat consectetur dolorem cumque sapiente nostrum similique ut suscipit! Distinctio debitis recusandae minus odio sit reprehenderit voluptatibus eum atque, libero esse et facilis laboriosam expedita inventore exercitationem quam?",
            role: "assistant",
          },
          {
            id: "4",
            content:
              "a short question as the user input is usually not very long",
            role: "user",
          },
          {
            id: "5",
            content:
              "Lorem ipsum dolor sit amet consectetur adipisicing elit. Ad, quasi? Quos repellendus at aspernatur quis nisi! Maiores possimus fugit in dolorem iusto neque iste ex a libero perferendis, expedita molestias earum sequi, ea molestiae distinctio ipsa fugiat eius nulla voluptatem id aliquam asperiores harum. Consequatur qui sequi, velit vitae ea reiciendis debitis esse aperiam nulla. Fugiat impedit omnis in officiis itaque, aut praesentium nihil eius expedita voluptates dolor iste molestiae recusandae aspernatur repellat consectetur dolorem cumque sapiente nostrum similique ut suscipit! Distinctio debitis recusandae minus odio sit reprehenderit voluptatibus eum atque, libero esse et facilis laboriosam expedita inventore exercitationem quam?",
            role: "assistant",
          },
          {
            id: "6",
            content:
              "a short question as the user input is usually not very long",
            role: "user",
          },
          {
            id: "1",
            content:
              "Lorem ipsum dolor sit amet consectetur adipisicing elit. Ad, quasi? Quos repellendus at aspernatur quis nisi! Maiores possimus fugit in dolorem iusto neque iste ex a libero perferendis, expedita molestias earum sequi, ea molestiae distinctio ipsa fugiat eius nulla voluptatem id aliquam asperiores harum. Consequatur qui sequi, velit vitae ea reiciendis debitis esse aperiam nulla. Fugiat impedit omnis in officiis itaque, aut praesentium nihil eius expedita voluptates dolor iste molestiae recusandae aspernatur repellat consectetur dolorem cumque sapiente nostrum similique ut suscipit! Distinctio debitis recusandae minus odio sit reprehenderit voluptatibus eum atque, libero esse et facilis laboriosam expedita inventore exercitationem quam?",
            role: "assistant",
          },
          {
            id: "2",
            content:
              "a short question as the user input is usually not very long",
            role: "user",
          },
          {
            id: "3",
            content:
              "Lorem ipsum dolor sit amet consectetur adipisicing elit. Ad, quasi? Quos repellendus at aspernatur quis nisi! Maiores possimus fugit in dolorem iusto neque iste ex a libero perferendis, expedita molestias earum sequi, ea molestiae distinctio ipsa fugiat eius nulla voluptatem id aliquam asperiores harum. Consequatur qui sequi, velit vitae ea reiciendis debitis esse aperiam nulla. Fugiat impedit omnis in officiis itaque, aut praesentium nihil eius expedita voluptates dolor iste molestiae recusandae aspernatur repellat consectetur dolorem cumque sapiente nostrum similique ut suscipit! Distinctio debitis recusandae minus odio sit reprehenderit voluptatibus eum atque, libero esse et facilis laboriosam expedita inventore exercitationem quam?",
            role: "assistant",
          },
          {
            id: "4",
            content:
              "a short question as the user input is usually not very long",
            role: "user",
          },
          {
            id: "5",
            content:
              "Lorem ipsum dolor sit amet consectetur adipisicing elit. Ad, quasi? Quos repellendus at aspernatur quis nisi! Maiores possimus fugit in dolorem iusto neque iste ex a libero perferendis, expedita molestias earum sequi, ea molestiae distinctio ipsa fugiat eius nulla voluptatem id aliquam asperiores harum. Consequatur qui sequi, velit vitae ea reiciendis debitis esse aperiam nulla. Fugiat impedit omnis in officiis itaque, aut praesentium nihil eius expedita voluptates dolor iste molestiae recusandae aspernatur repellat consectetur dolorem cumque sapiente nostrum similique ut suscipit! Distinctio debitis recusandae minus odio sit reprehenderit voluptatibus eum atque, libero esse et facilis laboriosam expedita inventore exercitationem quam?",
            role: "assistant",
          },
          {
            id: "6",
            content:
              "a short question as the user input is usually not very long",
            role: "user",
          },
        ]}
        loading={isLoading}
      />
      <ChatInput
        input={input}
        handleInputChange={handleInputChange}
        handleSubmit={handleSubmit}
        isLoading={isLoading}
      />
    </div>
  );
};
