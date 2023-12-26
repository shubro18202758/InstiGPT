import { FC, useState } from "react";

import { Bars3Icon, XMarkIcon } from "@heroicons/react/24/solid";

import { NavbarContent } from "./NavbarContent";

export const Navbar: FC = () => {
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
