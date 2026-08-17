/* Microsoft Warning · 05 — SmartScreen explanation section on the landing page. */
import { ArrowRight } from "lucide-react";

export default function MicrosoftWarningSection() {
  return (
    <section id="microsoft-warning" className="border-t border-border">
      <div className="mx-auto max-w-[1400px] px-5 md:px-10 py-20 md:py-28">
        <header className="flex flex-col md:flex-row md:items-end md:justify-between gap-6 mb-12">
          <div>
            <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">Microsoft Warning · 05</span>
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
            This website may occasionally trigger a Microsoft Defender SmartScreen warning (“Windows protected your PC” or similar) when accessed or when files are downloaded from it. This is a standard, automated caution — not an indication of malware or malicious content.
          </p>
          <p className="font-body text-muted-foreground text-[15px] leading-relaxed">
            SmartScreen builds trust in new domains gradually, based on cumulative traffic volume, download history, and user feedback over time. Since this site is newly launched, it simply hasn’t yet accumulated the reputation signals SmartScreen uses to classify it as “known safe,” which is why the warning appears.
          </p>
          <p className="font-body text-muted-foreground text-[15px] leading-relaxed">
            This is common and expected for new websites, and the warning typically resolves on its own as visitor traffic grows and no unsafe activity is reported.
          </p>
          <img
            src="/smartscreen/smartscreen-alert-annotated.png"
            alt="Microsoft Defender SmartScreen alert — click More info"
            className="mt-6 w-full max-w-xl mx-auto rounded-sm border border-border/60"
            loading="lazy"
          />
        </div>
      </div>
    </section>
  );
}
