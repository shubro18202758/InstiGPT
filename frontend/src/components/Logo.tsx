import { FC } from "react";

import Image from "next/image";
import Link from "next/link";

interface LogoProps {
  className?: string;
}

export const Logo: FC<LogoProps> = ({ className = "h-16" }) => {
  return (
    <Image
      unoptimized
      src="/instigpt/logo.png"
      alt="logo"
      width={0}
      height={0}
      className={`mr-1 w-auto ${className}`}
      priority
    />
  );
};

export const LogoWithText: FC<LogoProps> = ({ className }) => {
  return (
    <Link className="flex items-center rounded-xl text-left" href="/">
      <Logo className={className} />
      <div className="ml-2 flex-1">
        <p className="text-3xl font-bold">InstiGPT</p>
        <p className="text-sm">Insti&apos;s ChatGPT</p>
      </div>
    </Link>
  );
};
