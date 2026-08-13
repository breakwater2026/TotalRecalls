
Below is the machine‑language specification of every required change, expressed as a strict, deterministic JSON‑like DSL that your coding agent can ingest without interpretation or creativity.

This is not prose.
This is not guidance.
This is the authoritative machine‑readable change‑set.

✅ TOTALRECALLS_ASTRO_CHANGESET_SPEC v1.0
json


Copy
{
  "project": "TotalRecalls Web Redesign",
  "framework": "Astro",
  "status": "locked",
  "changes": {

    "global": {
      "enforce_tailwind": true,
      "enforce_spacing_rhythm": true,
      "remove_all_inline_styles": true,
      "remove_all_non_tailwind_classes": true,
      "remove_all_redundant_wrappers": true,
      "remove_all_double_dollar_signs": true,
      "remove_all_price_strikethroughs": true,
      "remove_all_version_price_artifacts": true
    },

    "structure": {
      "replace_current_page_with_component_split": true,
      "astro_page": "src/pages/index.astro",
      "react_islands": true,
      "sections_order": [
        "Header",
        "Hero",
        "Why",
        "How",
        "Providers",
        "Screenshots",
        "Guides",
        "StraightTalk",
        "Pricing",
        "Footer"
      ]
    },

    "components": {
      "create_or_replace": {
        "Header": {
          "type": "react",
          "path": "src/components/Header.jsx",
          "status": "replace_existing",
          "requirements": {
            "nav_links": [
              "Home",
              "How It Works",
              "Guides",
              "Compare",
              "Pricing",
              "Download"
            ],
            "tailwind": [
              "w-full",
              "border-b",
              "bg-white",
              "max-w-6xl",
              "mx-auto",
              "px-6",
              "py-4",
              "flex",
              "items-center",
              "justify-between"
            ]
          }
        },

        "Hero": {
          "type": "react",
          "path": "src/components/Hero.jsx",
          "status": "replace_existing",
          "requirements": {
            "headline": "Own every AI conversation.",
            "description": "A small Windows app that saves your ChatGPT, Claude, Perplexity, Gemini, and Grok chats into a private folder on your computer — readable Markdown + JSON you keep forever.",
            "price": "$24 launch price",
            "cta_primary": "Buy TotalRecalls — $24",
            "cta_secondary": "Download ZIP",
            "screenshots": [
              "/img/library.png",
              "/img/markdown.png"
            ],
            "tailwind": [
              "bg-gray-50",
              "py-20",
              "grid",
              "grid-cols-1",
              "md:grid-cols-2",
              "gap-16",
              "items-center"
            ]
          }
        },

        "Why": {
          "type": "react",
          "path": "src/components/Why.jsx",
          "status": "replace_existing",
          "requirements": {
            "title": "Why TotalRecalls",
            "pillars": [
              {
                "title": "Your AI history shouldn’t vanish",
                "text": "Tabs close. Exports break. Interfaces change. A folder of Markdown on your PC still opens in ten years."
              },
              {
                "title": "One library for every assistant",
                "text": "Export everything into a single, predictable folder structure."
              },
              {
                "title": "Private by design",
                "text": "Local sign-in. No cloud locker. No account. No subscription."
              }
            ],
            "tailwind": [
              "py-20",
              "max-w-6xl",
              "mx-auto",
              "px-6",
              "grid",
              "grid-cols-1",
              "md:grid-cols-3",
              "gap-12"
            ]
          }
        },

        "How": {
          "type": "react",
          "path": "src/components/How.jsx",
          "status": "replace_existing",
          "requirements": {
            "title": "How It Works",
            "steps": [
              "1. Buy once",
              "2. Install",
              "3. Pick a provider",
              "4. Export"
            ],
            "tailwind": [
              "py-20",
              "bg-gray-50",
              "grid",
              "grid-cols-1",
              "md:grid-cols-4",
              "gap-12"
            ]
          }
        },

        "Providers": {
          "type": "react",
          "path": "src/components/Providers.jsx",
          "status": "new",
          "requirements": {
            "title": "Supported Providers",
            "providers": [
              "ChatGPT",
              "Claude",
              "Perplexity",
              "Gemini",
              "Grok"
            ],
            "tailwind": [
              "grid",
              "grid-cols-2",
              "md:grid-cols-5",
              "gap-8",
              "text-center"
            ]
          }
        },

        "Screenshots": {
          "type": "react",
          "path": "src/components/Screenshots.jsx",
          "status": "new",
          "requirements": {
            "sections": [
              {
                "title": "Your Library, organized",
                "text": "Clean folder structure you can browse, search, and back up.",
                "image": "/img/library.png"
              },
              {
                "title": "Readable Markdown",
                "text": "Predictable formatting. Easy to diff, annotate, or feed into your own tools.",
                "image": "/img/markdown.png"
              }
            ],
            "tailwind": [
              "py-20",
              "bg-gray-50",
              "grid",
              "grid-cols-1",
              "md:grid-cols-2",
              "gap-16"
            ]
          }
        },

        "Guides": {
          "type": "react",
          "path": "src/components/Guides.jsx",
          "status": "replace_existing",
          "requirements": {
            "title": "Guides",
            "cards": [
              "Export ChatGPT conversations",
              "Download your Claude history",
              "Backup Perplexity threads",
              "Gemini Takeout → Markdown",
              "Own your AI chat data"
            ],
            "tailwind": [
              "grid",
              "grid-cols-1",
              "md:grid-cols-3",
              "gap-12"
            ]
          }
        },

        "StraightTalk": {
          "type": "react",
          "path": "src/components/StraightTalk.jsx",
          "status": "replace_existing",
          "requirements": {
            "title": "Straight Talk",
            "bullets": [
              "Windows app today (WebView2). Mac later if demand is real.",
              "Gemini uses your Google Takeout JSON.",
              "Unsigned builds may show SmartScreen until code-signing is complete.",
              "SP8 Smart App Control may block unsigned apps.",
              "You must follow each provider’s terms.",
              "No AdSense clutter."
            ],
            "tailwind": [
              "py-20",
              "bg-gray-50",
              "list-disc",
              "pl-6",
              "space-y-2"
            ]
          }
        },

        "Pricing": {
          "type": "react",
          "path": "src/components/Pricing.jsx",
          "status": "new",
          "requirements": {
            "title": "Pricing",
            "price": "$24 launch price",
            "cta": "Buy TotalRecalls — $24",
            "tailwind": [
              "py-20",
              "text-center",
              "space-y-6"
            ]
          }
        },

        "Footer": {
          "type": "react",
          "path": "src/components/Footer.jsx",
          "status": "replace_existing",
          "requirements": {
            "text": "Not affiliated with OpenAI, Anthropic, Perplexity, Google, or xAI. © TotalRecalls",
            "tailwind": [
              "w-full",
              "py-12",
              "bg-gray-100",
              "text-gray-600",
              "text-sm"
            ]
          }
        }
      }
    },

    "astro_page": {
      "index.astro": {
        "replace_body_with": [
          "<Header />",
          "<Hero />",
          "<Why />",
          "<How />",
          "<Providers />",
          "<Screenshots />",
          "<Guides />",
          "<StraightTalk />",
          "<Pricing />",
          "<Footer />"
        ],
        "import_all_components": true,
        "react_islands": true,
        "remove_all_old_markup": true
      }
    },

    "assets": {
      "required": [
        "/img/library.png",
        "/img/markdown.png"
      ],
      "remove_unused_assets": true
    },

    "pricing_cleanup": {
      "remove_strikethrough_49": true,
      "remove_double_dollar_sign": true,
      "remove_version_price_artifact": true,
      "final_price": "$24"
    }
  }
}
⭐ This is the machine‑language version of every change required.
It is:

Deterministic

Unambiguous

Fully Astro‑compatible

Fully aligned with your locked spec

Ready for ingestion by your coding agent

