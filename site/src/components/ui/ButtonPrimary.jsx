import { ReactNode } from "react";

export function ButtonPrimary({ href, children }) {
  return (
    <a
      href={href}
      className="px-6 py-3 bg-black text-white rounded-lg font-medium hover:bg-gray-800"
    >
      {children}
    </a>
  );
}
