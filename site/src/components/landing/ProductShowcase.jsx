export default function ProductShowcase() {
  return (
    <section className="border-t border-border bg-background text-foreground">
      <div className="mx-auto max-w-[1400px] px-5 md:px-10 py-16 md:py-24">
        <div className="max-w-2xl">
          <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">See it work</span>
          <h2 className="font-heading text-3xl md:text-4xl font-bold tracking-tight mt-4">
            Watch a real download in action.
          </h2>
          <p className="font-body text-muted-foreground text-[15.5px] leading-relaxed mt-4">
            A short walkthrough of pulling a conversation out of a provider and saving it as
            Markdown + JSON on your own machine.
          </p>
        </div>

        <div className="mt-10 rounded-lg border border-border bg-card/40 p-2 md:p-3">
          <video
            className="w-full rounded-md border border-border/70 bg-black"
            src="/demo/totalrecalls-demo.mp4"
            controls
            autoPlay
            muted
            loop
            playsInline
            preload="metadata"
            aria-label="Demo of TotalRecalls downloading a conversation"
          />
        </div>

        <p className="font-mono text-[11px] text-muted-foreground mt-4">
          Demo footage of the Windows app. Your real conversations never leave your machine.
        </p>
      </div>
    </section>
  );
}
