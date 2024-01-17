import { FC } from "react";
import Image from "next/image";

interface LogoProps {
  size?: number;
}

export const Logo: FC<LogoProps> = ({ size = 100 }) => {
  return (
    <Image
      src="/logo.png"
      alt="logo"
      width={size}
      height={1.2 * size}
      className="mr-1"
    />
  );
};

export const LogoWithText: FC<LogoProps> = ({ size = 100 }) => {
  return (
    <a className="flex items-center rounded-xl text-left" href="/">
      <Logo size={size} />
      <div className="ml-2 flex-1">
        <p className="text-3xl font-bold">InstiGPT</p>
        <p className="text-sm">Insti&apos;s ChatGPT</p>
      </div>
    </a>
  );
};
