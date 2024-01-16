import { FC, Fragment, useRef, useState } from "react";

import { Dialog, Transition } from "@headlessui/react";
import { ShieldCheckIcon } from "@heroicons/react/24/solid";

interface DisclaimerModalProps {
  setShown: () => void;
}

export const DisclaimerModal: FC<DisclaimerModalProps> = ({ setShown }) => {
  const [open, setOpen] = useState(true);
  const okayButtonRef = useRef<HTMLButtonElement>(null);
  const contentDivRef = useRef<HTMLDivElement>(null);

  return (
    <Transition.Root show={open} as={Fragment}>
      <Dialog
        as="div"
        className="relative z-10"
        initialFocus={okayButtonRef}
        onClose={() => setOpen(false)}
      >
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-background bg-opacity-75 transition-opacity" />
        </Transition.Child>

        <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
          <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
              enterTo="opacity-100 translate-y-0 sm:scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 translate-y-0 sm:scale-100"
              leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            >
              <Dialog.Panel className="relative transform overflow-hidden rounded-lg bg-background/75 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
                <div className="bg-background px-4 pb-4 pt-5 text-foreground sm:p-6 sm:pb-4">
                  <div className="sm:flex sm:items-start">
                    <div className="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-yellow-300 sm:mx-0 sm:h-10 sm:w-10">
                      <ShieldCheckIcon
                        className="h-6 w-6 text-yellow-600"
                        aria-hidden="true"
                      />
                    </div>
                    <div
                      ref={contentDivRef}
                      className="scrollbar-custom mt-3 max-h-80 overflow-y-scroll text-center sm:ml-4 sm:mt-0 sm:text-left"
                    >
                      <Dialog.Title
                        as="h3"
                        className="text-xl font-semibold leading-6"
                      >
                        Disclaimer
                      </Dialog.Title>
                      <div className="prose prose-invert mt-2">
                        <h3>Overview</h3>
                        <p className="text-gray-400">
                          This chat bot is intended to provide general
                          information about our insitute only. It is not a
                          substitute for professional advice or guidance. The
                          chat bot may sometimes give inaccurate, incomplete, or
                          outdated results, depending on the input and the
                          availability of data sources. The chat bot does not
                          guarantee the accuracy, reliability, or suitability of
                          any information or content it provides. The user is
                          solely responsible for verifying the information and
                          content before relying on or using it.
                        </p>
                        <h3>Currently the following datasets are added:</h3>
                        <hr />
                        <ul>
                          <li>Apping Guide</li>
                          <li>Non-Core Apping Guide</li>
                          <li>Bluebook</li>
                          <li>Course Info Booklet 2020-21</li>
                          <li>ITC Report</li>
                          <li>MInDS Minor</li>
                          <li>SAC Constitution (March 2018)</li>
                          <li>UG Rulebook</li>
                          <li>ResoBin</li>
                          <li>Department Websites</li>
                          <li>DAMP Websites</li>
                        </ul>
                        <h3>Some points to note:</h3>
                        <hr />
                        <ul>
                          <li>
                            Try to keep a conversation limited to a topic and
                            make a new conversation for every new topic.
                          </li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="bg-background-alt px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
                  <button
                    type="button"
                    className="mt-3 inline-flex w-full justify-center rounded-md bg-background px-3 py-2 text-sm font-semibold shadow-sm ring-1 ring-inset ring-accent hover:bg-background-alt disabled:text-gray-500 disabled:ring-0 sm:mt-0 sm:w-auto"
                    onClick={() => {
                      setOpen(false);
                      setShown();
                    }}
                    disabled={
                      contentDivRef.current === null ||
                      !(
                        Math.round(
                          contentDivRef.current.scrollHeight -
                            contentDivRef.current.scrollTop,
                        ) === contentDivRef.current.clientHeight
                      )
                    }
                    ref={okayButtonRef}
                  >
                    Okay
                  </button>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition.Root>
  );
};
