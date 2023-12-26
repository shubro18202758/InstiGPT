import { FC, useState } from "react";
import Image from "next/image";

import { Bars3Icon, PlusIcon, XMarkIcon } from "@heroicons/react/24/solid";

import { NavbarConversationItem } from "./NavbarConversationItem";

interface NavbarProps {}

const conversations = [
  {
    id: 1,
    title: "Conversation 1",
    updatedAt: new Date().setDate(new Date().getDate()),
  },
  {
    id: 2,
    title: "Conversation 2",
    updatedAt: new Date().setDate(new Date().getDate() - 1),
  },
  {
    id: 3,
    title: "Conversation 3",
    updatedAt: new Date().setDate(new Date().getDate() - 3),
  },
  {
    id: 4,
    title: "Conversation 4",
    updatedAt: new Date().setDate(new Date().getDate() - 7),
  },
  {
    id: 5,
    title: "Conversation 5",
    updatedAt: new Date().setDate(new Date().getDate() - 10),
  },
  {
    id: 6,
    title: "Conversation 6",
    updatedAt: new Date().setDate(new Date().getDate() - 33),
  },
];
const dateRanges = [
  new Date().setDate(new Date().getDate() - 1),
  new Date().setDate(new Date().getDate() - 7),
  new Date().setMonth(new Date().getMonth() - 1),
];
const groupedConversations = {
  today: conversations.filter(({ updatedAt }) => updatedAt > dateRanges[0]),
  week: conversations.filter(
    ({ updatedAt }) => updatedAt > dateRanges[1] && updatedAt < dateRanges[0],
  ),
  month: conversations.filter(
    ({ updatedAt }) => updatedAt > dateRanges[2] && updatedAt < dateRanges[1],
  ),
  older: conversations.filter(({ updatedAt }) => updatedAt < dateRanges[2]),
};
const titles: { [key: string]: string } = {
  today: "Today",
  week: "This week",
  month: "This month",
  older: "Older",
} as const;

export const Navbar: FC<NavbarProps> = () => {
  const [open, setOpen] = useState(false);

  return (
    <>
      {/* Desktop Navbar */}
      <nav className="grid max-h-screen grid-cols-1 grid-rows-[auto,auto,1fr,auto] max-md:hidden">
        <NavbarContent />
      </nav>

      {/* Mobile Navbar closed */}
      <nav className="flex h-12 items-center border-b bg-background-alt px-4 md:hidden">
        <button
          type="button"
          className="-ml-3 flex h-9 w-9 shrink-0 items-center justify-center"
          onClick={() => setOpen(true)}
          aria-label="Open menu"
        >
          <Bars3Icon />
        </button>
        <span className="truncate px-4 text-lg font-semibold">
          Conversation Title
        </span>
      </nav>

      {/* Mobile Navbar open */}
      <nav
        className={`${
          open ? "block" : "hidden"
        } fixed inset-0 z-30 grid max-h-screen
		grid-cols-1 grid-rows-[auto,auto,auto,1fr,auto]
		bg-background-alt`}
      >
        <div className="flex h-12 items-center px-4">
          <button
            type="button"
            className="-mr-3 ml-auto flex h-9 w-9 items-center justify-center"
            onClick={() => setOpen(false)}
            aria-label="Close menu"
          >
            <XMarkIcon />
          </button>
        </div>
        <NavbarContent />
      </nav>
    </>
  );
};

const NavbarContent: FC = () => {
  return (
    <>
      <div className="sticky top-0 flex flex-none items-center justify-between px-3 py-3.5 max-sm:pt-0">
        <a
          className="flex items-center rounded-xl text-lg font-semibold"
          href="/"
        >
          <Image
            src="/logo-with-text.svg"
            alt="logo"
            width={3.7 * 100}
            height={100}
            className="mr-1"
          />
        </a>
      </div>
      <button
        className="m-2 flex items-center justify-center rounded-lg border bg-primary-gradient px-2 py-1 font-bold uppercase text-foreground shadow-sm hover:shadow-none"
        onClick={(e) => {
          e.preventDefault();
          // TODO: Create a new conversation here
        }}
      >
        New Chat <PlusIcon className="ml-1 h-5 w-5" />
      </button>

      <div className="scrollbar-custom flex flex-col gap-1 overflow-y-auto rounded-r-xl bg-background-alt px-3 pb-3 pt-2">
        {Object.entries(groupedConversations).map(([group, convs], i) => (
          <div key={i}>
            <h4 className="mb-1.5 mt-4 pl-0.5 text-sm text-gray-500 first:mt-0">
              {titles[group]}
            </h4>
            {convs.map((conversation) => (
              <NavbarConversationItem
                key={conversation.id}
                conversation={conversation}
              />
            ))}
          </div>
        ))}
      </div>
      <div className="mt-0.5 flex flex-col gap-1 rounded-r-xl bg-background-alt p-3 text-sm md:bg-gradient-to-l">
        <span className="flex h-9 flex-none items-center gap-1.5 rounded-lg pl-2.5 pr-2 text-gray-400 hover:bg-gray-700">
          Full Name
        </span>
        <a
          href="/logout"
          className="flex h-9 flex-none items-center gap-1.5 rounded-lg pl-2.5 pr-2 text-gray-400 hover:bg-gray-700"
          onClick={(e) => {
            e.preventDefault();
            // TODO: Logout here
          }}
        >
          Sign Out
        </a>
        <a
          href="#"
          target="_blank"
          rel="noreferrer"
          className="flex h-9 flex-none items-center gap-1.5 rounded-lg pl-2.5 pr-2 text-gray-400 hover:bg-gray-700"
        >
          Feedback
        </a>
      </div>
    </>
  );
};
