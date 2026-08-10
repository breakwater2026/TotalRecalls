"""Perplexity thread detail fetch and markdown rendering."""

from __future__ import annotations

from totalrecalls.adapters.perplexity.http import API_VERSION, request

def get_thread(token: str, uuid: str) -> dict:
    path = (f"/rest/thread/{uuid}?with_schematized_response=true&version={API_VERSION}"
            f"&source=default&limit=50&offset=0&from_first=true"
            f"&supported_block_use_cases=answer_modes&supported_block_use_cases=preserve_latex")
    status, data = request(path, token)
    detail = data if isinstance(data, dict) else {"entries": []}
    entries = detail.get("entries", []) or []
    seen, uniq = set(), []
    for e in entries:
        eid = e.get("uuid") or id(e)
        if eid in seen:
            continue
        seen.add(eid)
        uniq.append(e)
    detail["entries"] = uniq
    return detail


def extract_entry(entry: dict) -> dict:
    blocks = entry.get("blocks", []) or []
    answer = ""
    for b in blocks:
        mb = b.get("markdown_block")
        if mb and b.get("intended_usage") == "ask_text_0_markdown" and mb.get("answer"):
            answer = mb["answer"]
            break
    if not answer:
        for b in blocks:
            mb = b.get("markdown_block")
            if mb and b.get("intended_usage") == "ask_text" and mb.get("answer"):
                answer = mb["answer"]
                break
    sources = []
    for b in blocks:
        wr = b.get("web_result_block")
        if wr and b.get("intended_usage") == "web_results":
            for s in wr.get("web_results", []) or []:
                if s.get("name") and s.get("url"):
                    sources.append({"title": s["name"], "url": s["url"],
                                    "snippet": s.get("snippet", "")})
            break
    return {
        "uuid": entry.get("uuid"),
        "query": entry.get("query_str", ""),
        "model": entry.get("display_model", ""),
        "search_focus": entry.get("search_focus", ""),
        "created_at": entry.get("entry_created_datetime", ""),
        "updated_at": entry.get("entry_updated_datetime", ""),
        "answer": answer,
        "sources": sources,
    }


def render_markdown(meta: dict, entries: list[dict]) -> str:
    lines = [f"# {meta.get('title') or 'Untitled thread'}",
             "", f"- **Created:** {meta.get('created_at', '')}",
             f"- **Updated:** {meta.get('updated_at', '')}",
             f"- **Thread UUID:** {meta.get('uuid', '')}",
             f"- **Mode:** {meta.get('mode', '')}", ""]
    if meta.get("space"):
        lines.append(f"- **Space:** {meta['space']}")
        lines.append("")
    for i, e in enumerate(entries, 1):
        lines.append("---")
        lines.append("")
        lines.append(f"## Q{i}: {e.get('query') or '(no question text)'}")
        lines.append("")
        if e.get("model"):
            lines.append(f"*Model: {e['model']}*")
            lines.append("")
        lines.append(e.get("answer") or "_(no answer text captured)_")
        lines.append("")
        if e.get("sources"):
            lines.append("### Sources")
            for s in e["sources"]:
                lines.append(f"- [{s['title']}]({s['url']})")
            lines.append("")
    return "\n".join(lines)

