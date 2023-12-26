"use client";

import { useParams } from "next/navigation";

export default function Conversation({}) {
  const { id: conversationId } = useParams();

  return (
    <div>
      <h1>Conversation: {conversationId}</h1>
    </div>
  );
}
