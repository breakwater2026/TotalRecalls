import { ReactNode } from "react";

export function ButtonSecondary({ href, children }) {
  return (
    <a
      href={href}
      className="px-6 py-3 bg-white border rounded-lg font-medium hover:bg-gray-100"
    >
      {children}
    </a>
  );
}
