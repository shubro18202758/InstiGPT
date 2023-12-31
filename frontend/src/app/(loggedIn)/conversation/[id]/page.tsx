"use client";

import { useParams } from "next/navigation";

import { ChatWindow } from "@/components";
import Head from "next/head";

export default function Conversation() {
  const { id: conversationId } = useParams();

  return (
    <>
      <Head>
        <title>Conversation {conversationId} | InstiGPT</title>
      </Head>
      <ChatWindow conversationId={conversationId as string} />
    </>
  );
}
