import React from "react";
import { Check } from "lucide-react";
import { Container, Section, Eyebrow, Btn, Chip } from "./ui";

/* ============================================================================
 * Pricing — one ladder for the whole product.
 *
 *   Free            $0
 *   Downloader Pro  $24 launch / $48 regular
 *   Pro + SSE       $49.89 launch / $99.89 regular   ← best value, one checkout
 *   SSE add-on      $29 launch / $58 regular        ← requires Pro
 *
 * The bundle is the featured card: it is the best value and the only SSE
 * checkout a new buyer needs. The add-on card is visually subordinate because
 * it only makes sense once you already own the Downloader.
 *
 * Launch prices have no end date. The price-change line is shared, not repeated.
 * ========================================================================== */

function Price({ amount, regular, large = false }) {
  return (
    <div className="flex flex-wrap items-baseline gap-x-2 gap-y-1">
      <span
        className={`font-heading font-bold tracking-[-0.02em] text-tr-paper tabular-nums ${
          large ? "text-[34px] md:text-[42px]" : "text-[30px] md:text-[38px]"
        }`}
      >
        {amount}
      </span>
      {regular ? (
        <span className="font-body text-[14px] text-tr-dust line-through tabular-nums">{regular}</span>
      ) : null}
    </div>
  );
}

function Card({ name, tag, tagTone = "slate", featured = false, price, regular, per, blurb, features, cta }) {
  return (
    <div
      className={`flex flex-col rounded-card border p-6 md:p-7 ${
        featured ? "border-tr-amber bg-tr-obsidian" : "border-tr-slate bg-tr-obsidian"
      }`}
    >
      <div className="flex flex-wrap items-center gap-2">
        <span className="font-heading text-[16px] font-semibold text-tr-paper">{name}</span>
        {tag ? <Chip tone={tagTone}>{tag}</Chip> : null}
      </div>

      <div className="mt-5">
        <Price amount={price} regular={regular} large={featured} />
        {per ? <div className="mt-1 font-body text-[13px] text-tr-dust">{per}</div> : null}
      </div>

      {blurb ? (
        <p className="mt-3 font-body text-[14px] leading-[1.55] text-tr-mist">{blurb}</p>
      ) : null}

      <ul className="mt-5 space-y-2.5">
        {features.map((f) => (
          <li key={f.text} className="flex items-start gap-2.5">
            {f.included ? (
              <Check className="mt-0.5 h-3.5 w-3.5 shrink-0 text-tr-green" strokeWidth={2.5} />
            ) : (
              <span className="mt-0.5 w-3.5 shrink-0 text-center font-body text-[13px] leading-[1.5] text-tr-dust">
                —
              </span>
            )}
            <span
              className={`font-body text-[13.5px] leading-[1.5] ${
                f.included ? "text-tr-mist" : "text-tr-dust"
              }`}
            >
              {f.text}
            </span>
          </li>
        ))}
      </ul>

      <div className="mt-auto pt-7">
        <Btn
          href={cta.href}
          variant={cta.variant || "secondary"}
          className="w-full"
          data-tr-buy={cta.checkout ? true : undefined}
          data-tr-price-id={cta.priceId}
        >
          {cta.label}
        </Btn>
        {cta.note ? (
          <p className="mt-2.5 text-center font-body text-[12px] leading-[1.5] text-tr-dust">{cta.note}</p>
        ) : null}
      </div>
    </div>
  );
}

const SSE_POINTS = [
  "Search by meaning, by keyword, or both together",
  "Ask questions about your archive in plain English, like “how many Claude chats did I have in 2026?”",
  "Chat with your archive (works without any AI model; a local model is optional)",
  "Every result links to the original file",
  "Connects to Obsidian and Notion",
  "Keeps itself up to date",
];

export default function Pricing() {
  return (
    <Section id="pricing" className="bg-tr-graphite">
      <Container>
        <Eyebrow>Pricing</Eyebrow>

        <h2 className="mt-3 max-w-[680px] font-heading text-[28px] md:text-[36px] font-semibold leading-[1.15] tracking-[-0.01em] text-tr-paper">
          Start free. Pay once when you want all eight.
        </h2>

        <p className="mt-4 max-w-[680px] font-body text-[18px] md:text-[20px] leading-[1.55] text-tr-mist">
          Test TotalRecalls on your own chats before you spend anything. When you're ready,
          one payment unlocks every provider. No subscription.
        </p>

        {/* ---- One ladder: Free → Pro → Pro + SSE → SSE add-on ---- */}
        <div className="mt-12 grid gap-5 md:grid-cols-2 lg:grid-cols-4 lg:gap-6 items-stretch">
          <Card
            name="Free"
            tag="Free Tier"
            tagTone="mist"
            price="$0"
            per="forever"
            blurb="Try the app on your real conversations."
            features={[
              { text: "ChatGPT, Claude, and Perplexity", included: true },
              { text: "5 conversations per download", included: true },
              { text: "Markdown and JSON files", included: true },
              { text: "Saved locally to C:\\TotalRecalls\\Library\\", included: true },
              { text: "Gemini, Grok, DeepSeek, Mistral, and Qwen", included: false },
              { text: "Unlimited downloads", included: false },
            ]}
            cta={{ label: "Download free", href: "/download/" }}
          />

          <Card
            name="Downloader Pro"
            tag="Launch price"
            price="$24"
            regular="$48"
            per="one-time"
            blurb="Every provider. Every conversation. No subscription."
            features={[
              { text: "All 8 providers: ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen", included: true },
              { text: "Unlimited downloads", included: true },
              { text: "Markdown and JSON files, saved locally", included: true },
              { text: "Up to 3 device activations", included: true },
              { text: "Free updates (bug fixes) for the life of the product", included: true },
              { text: "License key delivered by email", included: true },
            ]}
            cta={{ label: "Get Pro — $24", href: "/buy/", variant: "secondary", checkout: true }}
          />

          <Card
            name="Pro + SSE"
            tag="Best value"
            tagTone="amber"
            featured
            price="$49.89"
            regular="$99.89"
            per="one-time · launch price"
            blurb="The Downloader and the Smart Search Engine together, in one checkout."
            features={[
              { text: "Everything in Downloader Pro", included: true },
              { text: "Smart Search Engine included", included: true },
              { text: "Plain-English search across all eight providers", included: true },
              { text: "Obsidian and Notion connections", included: true },
              { text: "Free updates (bug fixes) to both", included: true },
            ]}
            cta={{
              label: "Get the bundle — $49.89",
              href: "/buy/",
              variant: "primary",
              checkout: true,
              priceId: "bundle",
              note: "One checkout. Both products unlocked.",
            }}
          />

          <Card
            name="SSE add-on"
            tag="Requires Pro"
            price="$29"
            regular="$58"
            per="one-time · launch price"
            blurb="Add the Smart Search Engine to a Downloader Pro license you already own."
            features={[
              { text: "Same Smart Search Engine feature set", included: true },
              { text: "Attaches to your Pro license", included: true },
              { text: "Search by meaning, keyword, or both", included: true },
              { text: "Free updates (bug fixes) to SSE", included: true },
              { text: "New modules and upgrades are separate purchases", included: false },
            ]}
            cta={{
              label: "Add SSE — $29",
              href: "/buy/",
              variant: "secondary",
              checkout: true,
              priceId: "sse",
              note: "Same $29 launch price for everyone.",
            }}
          />
        </div>

        {/* ---- Then make it searchable: narrative + reserved SSE GUI image slot ---- */}
        <div className="mt-16 grid items-center gap-10 lg:grid-cols-2 lg:gap-16">
          <div className="max-w-[680px]">
            <h3 className="mt-0 font-heading text-[24px] md:text-[28px] font-semibold leading-[1.2] text-tr-paper">
              Then make it searchable.
            </h3>
            <p className="mt-4 font-body text-[16px] leading-[1.6] text-tr-mist">
              Smart Search Engine finds the one you need. Ask in plain English, and it looks
              through every conversation from every provider. Your downloaded files are already
              searchable on their own — Windows Explorer's search bar, Norton, Obsidian and other
              local tools all read them. Smart Search Engine is the optional add-on for finding
              things by meaning rather than by filename.
            </p>
            <ul className="mt-6 space-y-3">
              {SSE_POINTS.map((b) => (
                <li key={b} className="flex items-start gap-3">
                  <Check className="mt-0.5 h-4 w-4 shrink-0 text-tr-green" strokeWidth={2.5} />
                  <span className="font-body text-[15px] leading-[1.5] text-tr-mist">{b}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Reserved image slot — drop the SSE GUI capture at
              public/images/smart-search-engine-gui.png and replace this figure. */}
          <figure className="m-0">
            <div className="flex aspect-[3/2] w-full flex-col items-center justify-center gap-3 rounded-card border border-dashed border-tr-slate bg-tr-obsidian/50 p-8 text-center">
              <span className="font-mono text-[11px] uppercase tracking-[0.18em] text-tr-dust">
                Image slot
              </span>
              <span className="font-heading text-[18px] font-semibold text-tr-mist">
                Smart Search Engine GUI
              </span>
              <span className="max-w-[280px] font-body text-[13px] leading-[1.55] text-tr-dust">
                1200 × 800 recommended. Save the capture as{" "}
                <code className="font-mono text-[12px] text-tr-steel">
                  site/public/images/smart-search-engine-gui.png
                </code>{" "}
                and this placeholder is replaced.
              </span>
            </div>
            <figcaption className="mt-4 text-center font-mono text-[12px] leading-relaxed text-tr-steel">
              Smart Search Engine — click a result to open the original conversation file.
            </figcaption>
          </figure>
        </div>

        <div className="mt-10 text-center">
          <p className="mx-auto max-w-[680px] font-body text-[14px] leading-[1.5] text-tr-dust">
            Windows 10 and 11. $24 is a discounted launch price. Add-ons, like Smart Search Engine,
            are sold separately. Your Downloader Pro updates stay free. Prices may change at any
            time without advance notice.
          </p>
          <div className="mt-5 flex flex-wrap justify-center gap-2">
            {["One-time", "No subscription", "No account", "Windows 10/11"].map((t) => (
              <Chip key={t} tone="slate">{t}</Chip>
            ))}
          </div>
        </div>
      </Container>
    </Section>
  );
}
