import { ReactNode } from "react";

export function Section({ id, bg = "white", children }) {
  return (
    <section id={id} className={`w-full py-20 bg-${bg}`}>
      <div className="max-w-6xl mx-auto px-6">
        {children}
      </div>
    </section>
  );
}
