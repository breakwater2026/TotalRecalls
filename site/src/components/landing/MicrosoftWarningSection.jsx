/* Microsoft Warning · 05 — SmartScreen explanation section on the landing page. */
import { ArrowRight } from "lucide-react";
import React from "react";

export default function MicrosoftWarningSection() {
  return (
    <section id="microsoft-warning" className="border-t border-border">
      <div className="mx-auto max-w-[1400px] px-5 md:px-10 py-10 md:py-20">
        <header className="flex flex-col md:flex-row md:items-end md:justify-between gap-6 mb-12">
          <div>
            <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">Microsoft Warning</span>
            <h2 className="font-heading text-3xl md:text-5xl font-bold tracking-tight mt-3">A standard, automated caution.</h2>
          </div>
          <a
            href="/microsoft-warning/"
            className="group inline-flex items-center gap-2 font-mono text-[11px] uppercase tracking-[0.18em] text-primary hover:underline"
          >
            Read the full note <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
          </a>
        </header>
        <div className="bg-card border border-border/80 p-6 md:p-8 space-y-4">
          <p className="font-body text-muted-foreground text-[15px] leading-relaxed">
            When you launch a newly released application or visit a new website, Microsoft Defender SmartScreen may display a warning stating "Windows protected your PC." This is an automated security measure designed to protect you from unfamiliar apps and sites but does not indicate the presence of malware or other threats.
          </p>
          <p className="font-body text-muted-foreground text-[15px] leading-relaxed">
            Because TotalRecalls is a newly launched app, you might see this warning until our site gains more reputation with Microsoft. You can safely bypass this prompt to continue installing or running the app by following the steps below.
          </p>
          <div className="space-y-3 pt-2">
            <p className="font-bold text-foreground">How to proceed safely:</p>
            <ol className="list-decimal list-inside space-y-2 ml-4">
              <li>Click <strong>More info</strong> on the warning dialog to reveal additional options.</li>
              <li>Then click <strong>Run anyway</strong> to launch the application.</li>
            </ol>
            <p>
              Please ensure you are downloading TotalRecalls only from our official website: <a href="https://totalrecalls.app" className="text-primary underline hover:no-underline">totalrecalls.app</a>. If you have any doubts or concerns, contact our support team at <a href="mailto:support@totalrecalls.app" className="text-primary underline hover:no-underline">support@totalrecalls.app</a>.
            </p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-6">
            <img
              src="/smartscreen/smartscreen-alert-annotated.png"
              alt="Microsoft Defender SmartScreen alert — click More info"
              className="w-full rounded-sm border border-border/60"
              loading="lazy"
            />
            <img
              src="/smartscreen/smartscreen-run-annotated.png"
              alt="Microsoft Defender SmartScreen — click Run anyway"
              className="w-full rounded-sm border border-border/60"
              loading="lazy"
            />
          </div>
        </div>
      </div>
    </section>
  );
}
