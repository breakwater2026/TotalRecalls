"""Build uploads_plan_gen_d.json for the 8 narrated provider walkthroughs.

Sources:
  * Titles / descriptions / tags / pinned comments  -> YOUTUBE-UPLOAD-PACK.md
    (both copies are identical; the CURATED 03_YouTube copy is parsed).
  * ABOUT TOTALRECALLS + trademark footer           -> Market Launch Strategy
    Implementation Content.md Part 2.2 ("Standard ABOUT TOTALRECALLS Footer"),
    appended to each description so the upload copy carries the mandatory
    Gen D boilerplate and trademark line.

No YouTube API calls are made here — this only writes the local manifest.
"""
import json
import os
import re
import textwrap

BASE = os.path.dirname(os.path.abspath(__file__))
CURATED = os.path.abspath(os.path.join(BASE, "..", ".."))
UPLOAD_PACK = os.path.join(
    CURATED, "03_YouTube", "Upload Pack - 8 Provider Walkthroughs (2026-11-15).md"
)
OUT = os.path.join(BASE, "uploads_plan_gen_d.json")

VIDEOS_DIR = r"C:\Users\break\Projects\TotalRecalls-Source Code\Videos\TR-demo-shoot"
THUMB_DIR = os.path.join(CURATED, "07_Assets", "thumbnails_3440")

# Video order in the Upload Pack -> provider key
ORDER = [
    ("chatgpt", "ChatGPT"),
    ("claude", "Claude"),
    ("perplexity", "Perplexity"),
    ("deepseek", "DeepSeek"),
    ("gemini", "Google Gemini"),
    ("grok", "Grok (xAI)"),
    ("mistral", "Mistral (Le Chat)"),
    ("qwen", "Qwen Chat"),
]

ABOUT_BLOCK = """ABOUT TOTALRECALLS
TotalRecalls is a Windows app that saves your AI conversations to your PC as Markdown and JSON files. You sign in to each provider inside the app, on your own computer. Your conversations aren't sent to our servers, and there's no TotalRecalls account to create.

Free Tier covers ChatGPT, Claude, and Perplexity — 5 conversations each, no card, no account. Downloader Pro ($24 one-time launch price) unlocks all 8 providers: ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen Chat. Add the Smart Search Engine (SSE) for $29, or get the Pro + SSE Bundle for $49 one-time.

Real screen recording. Personal details are blurred.
Windows 10 and 11. Recorded with TotalRecalls version 1.0.0.
TotalRecalls is not affiliated with OpenAI, Anthropic, Perplexity, Google, xAI, DeepSeek, Mistral, or Qwen. (I'm the developer of TotalRecalls.)"""


def parse_upload_pack(path):
    """Return {provider_key: {title, description, tags, pinned_comment}}."""
    text = open(path, encoding="utf-8").read()
    sections = re.split(r"^## ", text, flags=re.M)[1:]
    out = {}
    for sec in sections:
        head = sec.splitlines()[0]
        m = re.match(r"Video\s+\d+:\s*(.*?)\s*Walkthrough", head)
        if not m:
            continue
        name = m.group(1).strip().lower()
        key = None
        for k, label in ORDER:
            if label.lower() in name:
                key = k
                break
        if key is None:
            raise SystemExit(f"unmatched video heading: {head!r}")

        tm = re.search(r"\*\*Title:\*\*\s*`(.*?)`", sec, re.S)
        dm = re.search(r"```text\n(.*?)```", sec, re.S)
        gm = re.search(r"\*\*Tags:\*\*\s*`(.*?)`", sec, re.S)
        pm = re.search(r"\*\*Pinned Comment:\*\*\n((?:\s*> .*\n?)+)", sec)

        title = tm.group(1).strip()
        desc = textwrap.dedent(dm.group(1)).strip("\n")
        tags = [t.strip() for t in gm.group(1).split(",") if t.strip()]
        pinned = "\n".join(
            ln.strip()[2:].strip() for ln in pm.group(1).strip().splitlines()
        )

        # insert the mandatory ABOUT TOTALRECALLS + trademark footer before
        # the hashtag line (hashtags stay last, per YouTube convention)
        lines = desc.split("\n")
        idx = next((i for i, ln in enumerate(lines) if ln.lstrip().startswith("#")), len(lines))
        desc = "\n".join(lines[:idx]).rstrip("\n") + "\n\n" + ABOUT_BLOCK
        if idx < len(lines):
            desc += "\n\n" + "\n".join(lines[idx:])

        out[key] = {
            "provider": key,
            "video_path": os.path.join(VIDEOS_DIR, f"TR_website_{key}_pro_sse.mp4"),
            "thumb_path": os.path.join(THUMB_DIR, f"tr_thumb_{key}.jpg"),
            "title": title,
            "description": desc,
            "tags": tags,
            "pinned_comment": pinned,
        }
    return out


def main():
    plan = parse_upload_pack(UPLOAD_PACK)
    missing = [k for k, _ in ORDER if k not in plan]
    if missing:
        raise SystemExit(f"missing providers in upload pack: {missing}")

    ordered = [plan[k] for k, _ in ORDER]
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(ordered, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"{len(ordered)} entries -> {OUT}")
    for p in ordered:
        print(f"  {p['provider']:11s} {len(p['title']):3d}ch title, "
              f"{len(p['description']):5d}ch desc, {len(p['tags'])} tags")


if __name__ == "__main__":
    main()
