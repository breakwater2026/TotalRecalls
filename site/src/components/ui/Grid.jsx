import { ReactNode } from "react";

export function Grid({ cols = 3, children }) {
  return (
    <div className={`grid grid-cols-1 md:grid-cols-${cols} gap-12`}>
      {children}
    </div>
  );
}
