import { FolderOpen, HardDrive, ShieldCheck, Truck } from "lucide-react";

const ITEMS = [
  {
    icon: HardDrive,
    title: "Own your files",
    body: "Every conversation is saved on your own disk as Markdown + JSON. No account, no cloud library, no lock-in.",
  },
  {
    icon: FolderOpen,
    title: "Open with anything",
    body: "Plain, standard formats. Search them, back them up, diff them, or load them into any other tool you already use.",
  },
  {
    icon: Truck,
    title: "Move machines freely",
    body: "Copy your download folder to a new PC and it just works. Your library follows you without a login.",
  },
  {
    icon: ShieldCheck,
    title: "Never uploaded",
    body: "Everything runs locally. Your conversations never leave your machine.",
  },
];

export default function PortabilitySection() {
  return (
    <section className="border-t border-border bg-background text-foreground">
      <div className="mx-auto max-w-[1400px] px-5 md:px-10 py-16 md:py-24">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left: copy */}
          <div>
            <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">Portability</span>
            <h2 className="font-heading text-3xl md:text-4xl font-bold tracking-tight mt-4">
              Your library travels with you.
            </h2>
            <p className="font-body text-muted-foreground text-[15.5px] leading-relaxed mt-4 max-w-lg">
              No cloud account to lose, no proprietary format to be trapped in. Your conversations
              are ordinary files on your own machine — move them, back them up, or hand them to
              another tool without asking permission.
            </p>
            <ul className="mt-8 space-y-5">
              {ITEMS.map(({ icon: Icon, title, body }) => (
                <li key={title} className="flex items-start gap-4">
                  <Icon className="w-5 h-5 text-primary shrink-0 mt-1" />
                  <div>
                    <p className="font-body text-foreground font-semibold text-[15px]">{title}</p>
                    <p className="font-body text-muted-foreground text-[14px] leading-relaxed mt-0.5">{body}</p>
                  </div>
                </li>
              ))}
            </ul>
          </div>

          {/* Right: portability visual */}
          <div className="rounded-lg border border-border bg-card/40 p-6">
            <div className="flex items-center justify-between gap-6 flex-wrap">
              {/* Machine A */}
              <div className="flex-1 min-w-[160px] rounded-md border border-border bg-background p-3">
                <p className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground mb-2">This PC</p>
                <ul className="space-y-1.5">
                  <li className="font-mono text-[11px] text-foreground/90 bg-muted/40 px-2 py-1 rounded-sm">claude.md</li>
                  <li className="font-mono text-[11px] text-foreground/90 bg-muted/40 px-2 py-1 rounded-sm">gpt.md</li>
                  <li className="font-mono text-[11px] text-foreground/90 bg-muted/40 px-2 py-1 rounded-sm">perplexity.json</li>
                </ul>
              </div>
              {/* Arrow */}
              <div className="shrink-0 text-muted-foreground">
                <Truck className="w-6 h-6" />
              </div>
              {/* Machine B */}
              <div className="flex-1 min-w-[160px] rounded-md border border-border bg-background p-3">
                <p className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground mb-2">New PC</p>
                <ul className="space-y-1.5">
                  <li className="font-mono text-[11px] text-foreground/90 bg-muted/40 px-2 py-1 rounded-sm">deepseek.md</li>
                  <li className="font-mono text-[11px] text-foreground/90 bg-muted/40 px-2 py-1 rounded-sm">gemini.json</li>
                  <li className="font-mono text-[11px] text-foreground/90 bg-muted/40 px-2 py-1 rounded-sm">mistral.md</li>
                </ul>
              </div>
            </div>
            <p className="font-mono text-[10px] text-muted-foreground text-center mt-4">
              Copy the download folder — that's the whole migration.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
