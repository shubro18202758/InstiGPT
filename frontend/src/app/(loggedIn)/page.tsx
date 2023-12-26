import { LogoWithText } from "@/components/Logo";

export default function Home() {
  return (
    <div className="mx-auto flex max-w-3xl flex-col justify-center px-3 text-center xl:max-w-4xl">
      <div>
        <div className="mx-10 mb-3 flex items-center text-2xl font-semibold">
          <LogoWithText size={150} />
        </div>
        <p className="text-base text-gray-400">
          Answer to all the questions you have about IIT Bombay.
        </p>
      </div>
      <div className="mt-6">
        <p className="mb-3 text-gray-300">Examples</p>
        <div className="grid gap-3 lg:grid-cols-3 lg:gap-5">
          {["Example 1", "Example 2", "Example 3"].map((example, i) => (
            <button
              key={i}
              type="button"
              className="rounded-xl border border-gray-800 bg-gray-800 p-2.5 text-gray-300 hover:bg-gray-700 sm:p-4"
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
