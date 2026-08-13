import { ReactNode } from "react";

export function GuideCard({ title, text }) {
  return (
    <div className="space-y-3">
      <h3 className="text-xl font-semibold">{title}</h3>
      <p className="text-gray-700">{text}</p>
    </div>
  );
}
