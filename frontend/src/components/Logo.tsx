import { FC } from "react";
import Image from "next/image";

interface LogoProps {
  size?: number;
}

export const Logo: FC<LogoProps> = ({ size = 100 }) => {
  return (
    <Image
      src="/logo.svg"
      alt="logo"
      width={size}
      height={size}
      className="mr-1"
    />
  );
};

export const LogoWithText: FC<LogoProps> = ({ size = 100 }) => {
  return (
    <a className="flex items-center rounded-xl" href="/">
      <Image
        src="/logo-with-text.svg"
        alt="logo"
        width={3.7 * size}
        height={size}
        className="mr-1"
        priority
      />
    </a>
  );
};
