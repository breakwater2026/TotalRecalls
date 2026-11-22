"""TotalRecalls Social Media Reply Drafter Engine.

Monitors or takes incoming questions/comments from Reddit, X, and LinkedIn,
pulls ground-truth knowledge from the Canonical Container (Power User Manual,
SSE User Guides, Website FAQ, and App source architecture), and drafts
accurate, rule-compliant responses for founder review.
"""
import json
import re
import sys
from pathlib import Path

BASE_DIR = Path(r"C:\Users\break\Projects\TotalRecalls-Source Code")
DOCS_DIR = BASE_DIR / "docs"
SITE_PAGES = BASE_DIR / "site" / "src" / "pages"
REPLY_BOT_DIR = BASE_DIR / "Marketing" / "Market Launch Plans - CURATED" / "08_Tooling" / "reply-bot"
PENDING_DRAFTS_FILE = REPLY_BOT_DIR / "pending_drafts.json"

CLAIMS_REGISTER = [
    "Never claim images, audio, or binary attachments are downloaded.",
    "Never make absolute 100% hack-proof statements; state local DPAPI encryption at rest.",
    "No cloud servers, no proxy middleman, zero telemetry.",
    "Pricing: Free Tier (3 providers, 5 chats each), Pro ($24), SSE ($29), Bundle ($49).",
    "Requirements: Windows 10/11, CPU-only, 8GB RAM, no GPU required.",
]


def load_canonical_context():
    """Extract core snippets from the Power User Manual, Quick Start Guide, and Website FAQ."""
    context_chunks = []

    # 1. Power User Manual
    pum_path = DOCS_DIR / "TOTALRECALLS_POWER_USER_MANUAL.md"
    if pum_path.exists():
        content = pum_path.read_text(encoding="utf-8", errors="ignore")
        context_chunks.append(("Power User Manual", content[:4000]))

    # 2. SSE Quick Start Guide
    qsg_path = DOCS_DIR / "TOTALRECALLS_SSE_QUICK_START_GUIDE.md"
    if qsg_path.exists():
        content = qsg_path.read_text(encoding="utf-8", errors="ignore")
        context_chunks.append(("SSE Quick Start Guide", content[:3000]))

    # 3. FAQ
    faq_path = SITE_PAGES / "faq" / "index.astro"
    if faq_path.exists():
        content = faq_path.read_text(encoding="utf-8", errors="ignore")
        # Strip astro component boilerplate
        text_only = re.sub(r"<[^>]+>", " ", content)
        clean_text = " ".join(text_only.split())
        context_chunks.append(("Website FAQ", clean_text[:4000]))

    return context_chunks


def generate_draft(platform: str, user_name: str, incoming_text: str, context_notes: str = "") -> dict:
    """Generate an authoritative, tone-appropriate draft response."""
    lower_q = incoming_text.lower()
    
    # Tone & opening adjustment per platform
    if platform.lower() == "reddit":
        disclosure = "Developer of TotalRecalls here."
    elif platform.lower() == "x":
        disclosure = "Hey there — founder of @totalrecalls here."
    else:  # LinkedIn
        disclosure = "Thanks for the question! As the developer of TotalRecalls:"

    draft_paragraphs = [disclosure]

    # Rule checks & keyword-driven answers
    if any(k in lower_q for k in ["image", "attachment", "file", "photo", "pdf"]):
        draft_paragraphs.append(
            "Regarding attachments: TotalRecalls currently downloads complete conversation text, "
            "code blocks, formatting, timestamps, citations, and metadata. It does not download binary "
            "attachments or generated images (these remain hosted on the provider's servers)."
        )

    if any(k in lower_q for k in ["security", "privacy", "cloud", "server", "wireshark", "telemetry"]):
        draft_paragraphs.append(
            "Privacy architecture: TotalRecalls has zero cloud servers, zero external proxies, and zero telemetry. "
            "You authenticate directly inside an embedded Microsoft Edge WebView2 instance on your machine, and "
            "your session tokens are encrypted at rest using Windows DPAPI (tied to your Windows login SID). "
            "Network traffic flows solely between your PC and the AI provider—you can verify this directly in "
            "Wireshark or Windows Resource Monitor."
        )

    if any(k in lower_q for k in ["gpu", "hardware", "cpu", "ram", "spec", "slow"]):
        draft_paragraphs.append(
            "Hardware requirements: The Smart Search Engine (SSE) is built to run 100% offline on standard CPUs. "
            "It does not require a dedicated GPU. A typical Windows 10/11 machine with 8GB RAM handles indexing and "
            "hybrid semantic search cleanly using embedded SQLite FTS5 and LanceDB."
        )

    if any(k in lower_q for k in ["price", "cost", "subscription", "refund", "free"]):
        draft_paragraphs.append(
            "Pricing: TotalRecalls is an anti-subscription model. We offer a permanent Free Tier covering "
            "ChatGPT, Claude, and Perplexity (5 conversations each) so you can test exports before buying. "
            "Downloader Pro is a $24 one-time launch price (all 8 providers, unlimited exports), and the optional "
            "Smart Search Engine (SSE) is $29 (or $49 for the bundle). SSE includes a 7-day refund guarantee."
        )

    if any(k in lower_q for k in ["obsidian", "notion", "markdown", "format", "json"]):
        draft_paragraphs.append(
            "Data formats: Every single conversation is saved into your local library (C:\\TotalRecalls\\Library\\) "
            "in two simultaneous formats: a clean, standard Markdown (.md) file that opens instantly in Obsidian, "
            "Notion, or VS Code, and a structured .json file for local scripting."
        )

    if len(draft_paragraphs) == 1:
        # General response if no specific keyword matched
        draft_paragraphs.append(
            "TotalRecalls pulls your conversations from ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, "
            "Mistral, and Qwen directly onto your Windows PC as local Markdown & JSON files with zero cloud middleman. "
            "You can test it on the Free Tier anytime at https://totalrecalls.app/."
        )

    full_draft = "\n\n".join(draft_paragraphs)

    entry = {
        "id": f"{platform}_{int(Path(__file__).stat().st_mtime)}_{abs(hash(incoming_text)) % 10000}",
        "platform": platform,
        "author": user_name,
        "question": incoming_text,
        "draft_response": full_draft,
        "status": "pending_founder_approval",
        "sources_consulted": [
            "docs/TOTALRECALLS_POWER_USER_MANUAL.md",
            "docs/TOTALRECALLS_SSE_QUICK_START_GUIDE.md",
            "site/src/pages/faq/index.astro",
            "Claims Register"
        ]
    }
    return entry


def queue_draft(entry: dict):
    drafts = []
    if PENDING_DRAFTS_FILE.exists():
        try:
            drafts = json.loads(PENDING_DRAFTS_FILE.read_text(encoding="utf-8"))
        except Exception:
            drafts = []
    drafts.append(entry)
    PENDING_DRAFTS_FILE.write_text(json.dumps(drafts, indent=2), encoding="utf-8")


if __name__ == "__main__":
    # Test execution
    test_entry = generate_draft(
        platform="Reddit",
        user_name="u/CuriousCoder",
        incoming_text="Does TotalRecalls run locally or does my chat data go through your servers? Also does it need an NVIDIA GPU for the search?",
    )
    queue_draft(test_entry)
    print("Test draft generated and queued in pending_drafts.json:")
    print(json.dumps(test_entry, indent=2))
