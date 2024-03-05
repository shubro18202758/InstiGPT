import { LogoWithText } from "@/components/Logo";
import { NewChatButton } from "@/components/navbar/NewChatButton";

export default function Home() {
  return (
    <div className="mx-auto flex max-w-3xl flex-col justify-center px-3 text-center xl:max-w-4xl">
      <div>
        <div className="mb-3 flex items-center justify-center font-semibold">
          <LogoWithText className="h-24" />
        </div>
        <p className="text-base text-gray-400">
          Answer to all the questions you have about IIT Bombay.
        </p>
      </div>
      <div className="mt-6 w-80 max-w-full self-center md:hidden">
        <NewChatButton />
      </div>
      <div className="mt-6">
        <p className="mb-3 text-gray-300">Examples</p>
        <div className="grid gap-3 lg:grid-cols-3 lg:gap-5">
          {[
            "What are the required credits to complete Honors degree?",
            "Who is Prof Manjesh K Hanawal?",
            "Recommend me 3 courses if I want to pursue Biomechanics",
          ].map((example, i) => (
            <span
              key={i}
              className="rounded-xl border border-gray-800 bg-gray-800 p-2.5 text-sm text-gray-300 hover:bg-gray-700 sm:p-4 md:text-base"
            >
              {example}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
