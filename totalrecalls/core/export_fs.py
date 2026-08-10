"""Human-friendly export layout (Spaces/Home folders + indexes)."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from totalrecalls import APP_VERSION
from totalrecalls.adapters.perplexity.thread import render_markdown

HOME_SPACE_NAME = "Home"
SPACES_DIRNAME = "Spaces"
LEGACY_THREADS_DIRNAME = "threads"


def space_label_from_collection(col: dict | None, meta: dict | None = None) -> str:
    """Human Space name from list-item collection or thread_metadata.collection_info."""
    col = col or {}
    meta = meta or {}
    ci = meta.get("collection_info") if isinstance(meta.get("collection_info"), dict) else {}
    title = (col.get("title") or col.get("name") or ci.get("title") or ci.get("name") or "").strip()
    return title or HOME_SPACE_NAME


def safe_name(s: str, max_len: int = 80) -> str:
    """Filesystem-safe single path segment. Keeps spaces for readability."""
    s = (s or "").replace("\n", " ").replace("\r", " ")
    # Windows-forbidden filename chars + control chars
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", s)
    s = re.sub(r"[^A-Za-z0-9 _.\(\)\[\]+\-]", "_", s)
    s = re.sub(r"\s+", " ", s).strip().strip(".")
    if len(s) > max_len:
        s = s[:max_len].rstrip().rstrip(".")
    return s or "untitled"


def short_id(uuid: str) -> str:
    u = (uuid or "").replace("-", "")
    return (u[:8] if u else "00000000").lower()


def thread_folder_name(title: str, uuid: str) -> str:
    """e.g. 'Google cloud setup -- a1b2c3d4' — readable + unique."""
    base = safe_name(title or "Untitled conversation", max_len=72)
    return f"{base} -- {short_id(uuid)}"


def space_dir_name(space: str) -> str:
    if not space or space == HOME_SPACE_NAME:
        return HOME_SPACE_NAME
    return safe_name(space, max_len=60) or "Space"


def thread_rel_path(space: str, title: str, uuid: str) -> str:
    """Relative path from export root to the thread folder (posix-ish for manifest)."""
    sn = space_dir_name(space)
    fn = thread_folder_name(title, uuid)
    if sn == HOME_SPACE_NAME:
        return str(Path(HOME_SPACE_NAME) / fn)
    return str(Path(SPACES_DIRNAME) / sn / fn)


def thread_abs_folder(outdir: str, space: str, title: str, uuid: str) -> str:
    return os.path.join(outdir, thread_rel_path(space, title, uuid).replace("/", os.sep))


def load_uuid_index(outdir: str) -> dict:
    path = os.path.join(outdir, "uuid_index.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_uuid_index(outdir: str, index: dict):
    path = os.path.join(outdir, "uuid_index.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


def find_existing_thread_folder(outdir: str, uuid: str, uuid_index: dict | None = None) -> str | None:
    """Locate a thread folder by uuid (new layout, index, or legacy flat threads/)."""
    if not uuid:
        return None
    idx = uuid_index if uuid_index is not None else load_uuid_index(outdir)
    rel = idx.get(uuid)
    if rel:
        abs_p = os.path.join(outdir, rel.replace("/", os.sep))
        if os.path.isdir(abs_p) and os.path.exists(os.path.join(abs_p, "thread.json")):
            return abs_p

    # Legacy: threads/<slug-or-uuid>/
    legacy_root = os.path.join(outdir, LEGACY_THREADS_DIRNAME)
    if os.path.isdir(legacy_root):
        # direct uuid folder
        cand = os.path.join(legacy_root, uuid)
        if os.path.exists(os.path.join(cand, "thread.json")):
            return cand
        # scan shallow (legacy is flat)
        try:
            for name in os.listdir(legacy_root):
                folder = os.path.join(legacy_root, name)
                jp = os.path.join(folder, "thread.json")
                if not os.path.isfile(jp):
                    continue
                if name == uuid or name.endswith(uuid) or uuid[:8] in name:
                    return folder
                try:
                    with open(jp, encoding="utf-8") as f:
                        data = json.load(f)
                    meta = data.get("thread_metadata") or {}
                    if meta.get("uuid") == uuid or data.get("uuid") == uuid:
                        return folder
                    # list item uuid sometimes only on disk path
                    if (data.get("thread_metadata") or {}).get("thread_url", "").find(uuid) >= 0:
                        return folder
                except Exception:
                    continue
        except Exception:
            pass

    # New layout scan (Home + Spaces/*) — only if index missed
    for root_name in (HOME_SPACE_NAME, SPACES_DIRNAME):
        root = os.path.join(outdir, root_name)
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            if "thread.json" in filenames:
                if short_id(uuid) in os.path.basename(dirpath).lower() or uuid in dirpath:
                    return dirpath
    return None


def entry_stats(entries: list[dict]) -> dict:
    answer_chars = 0
    empty_answers = 0
    sources = 0
    for e in entries or []:
        a = e.get("answer") or ""
        answer_chars += len(a)
        if not a.strip():
            empty_answers += 1
        sources += len(e.get("sources") or [])
    return {
        "entries": len(entries or []),
        "answer_chars": answer_chars,
        "empty_answer_entries": empty_answers,
        "sources": sources,
        "all_answers_empty": bool(entries) and empty_answers == len(entries),
    }


def write_conversation_markdown(path: str, meta: dict, entries: list[dict]):
    with open(path, "w", encoding="utf-8") as f:
        f.write(render_markdown(meta, entries))


def build_space_readme(space_name: str, threads: list[dict]) -> str:
    lines = [
        f"# {space_name}",
        "",
        f"{len(threads)} conversation(s) in this Space.",
        "",
        "| Conversation | Turns | Answer text | Sources |",
        "|---|---:|---:|---:|",
    ]
    for t in sorted(threads, key=lambda x: (x.get("title") or "").lower()):
        rel = t.get("folder_name") or t.get("rel_path", "").replace("\\\\", "/").split("/")[-1]
        title = t.get("title") or rel
        md_link = f"[{title.replace('|', '/')}]({rel}/conversation.md)" if rel else title
        st = t.get("stats") or {}
        warn = " ⚠️ empty" if t.get("empty_answers") else ""
        lines.append(
            f"| {md_link}{warn} | {st.get('entries', t.get('entries', '—'))} | "
            f"{st.get('answer_chars', '—')} chars | {st.get('sources', '—')} |"
        )
    lines.append("")
    return "\n".join(lines)


def build_root_readme(account: str, exported_at: str, by_space: dict, warnings: list[str]) -> str:
    total = sum(len(v) for v in by_space.values())
    lines = [
        "# Your Perplexity export",
        "",
        "Conversations are grouped the same way as in Perplexity: **Spaces** are folders.",
        "Threads with no Space live under **Home**.",
        "",
        f"- **Account:** {account or '—'}",
        f"- **Exported:** {exported_at}",
        f"- **Conversations:** {total}",
        f"- **Spaces (incl. Home):** {len(by_space)}",
        "",
        "## Browse by Space",
        "",
    ]
    # Home first, then alpha
    names = sorted(by_space.keys(), key=lambda n: (n != HOME_SPACE_NAME, n.lower()))
    for name in names:
        threads = by_space[name]
        if name == HOME_SPACE_NAME:
            link = f"./{HOME_SPACE_NAME}/README.md"
        else:
            link = f"./{SPACES_DIRNAME}/{space_dir_name(name)}/README.md"
        lines.append(f"- **[{name}]({link})** — {len(threads)} conversation(s)")
    lines.append("")
    lines.append("## All conversations")
    lines.append("")
    lines.append("| Space | Conversation | Turns | Notes |")
    lines.append("|---|---|---:|---|")
    for name in names:
        for t in sorted(by_space[name], key=lambda x: (x.get("title") or "").lower()):
            title = (t.get("title") or "Untitled").replace("|", "/")
            rel = (t.get("rel_path") or "").replace("\\\\", "/")
            link = f"[{title}]({rel}/conversation.md)" if rel else title
            st = t.get("stats") or {}
            note = ""
            if t.get("empty_answers"):
                note = "⚠️ no answer text captured"
            lines.append(
                f"| {name} | {link} | {st.get('entries', t.get('entries', '—'))} | {note} |"
            )
    if warnings:
        lines.append("")
        lines.append("## Warnings")
        lines.append("")
        for w in warnings:
            lines.append(f"- {w}")
        lines.append("")
    lines.append("")
    lines.append("---")
    lines.append("Each conversation folder contains `conversation.md` (readable) and `thread.json` (full data).")
    lines.append("")
    return "\n".join(lines)


def write_export_indexes(outdir: str, account: str, thread_records: list[dict],
                         exported_at: str | None = None) -> dict:
    """Write README.md, per-Space READMEs, manifest.json, uuid_index.json."""
    exported_at = exported_at or datetime.now(timezone.utc).isoformat()
    by_space: dict[str, list] = {}
    uuid_index = {}
    warnings = []
    empty_list = []

    for rec in thread_records:
        sp = rec.get("space") or HOME_SPACE_NAME
        by_space.setdefault(sp, []).append(rec)
        if rec.get("uuid") and rec.get("rel_path"):
            uuid_index[rec["uuid"]] = rec["rel_path"].replace("\\\\", "/")
        if rec.get("empty_answers"):
            empty_list.append(rec.get("title") or rec.get("uuid") or "?")

    if empty_list:
        warnings.append(
            f"{len(empty_list)} conversation(s) have no captured answer text: "
            + ", ".join(empty_list[:12])
            + ("…" if len(empty_list) > 12 else "")
        )

    # Root README
    with open(os.path.join(outdir, "README.md"), "w", encoding="utf-8") as f:
        f.write(build_root_readme(account, exported_at, by_space, warnings))

    # Per-space README + ensure dirs
    for sp, threads in by_space.items():
        if sp == HOME_SPACE_NAME:
            sdir = os.path.join(outdir, HOME_SPACE_NAME)
        else:
            sdir = os.path.join(outdir, SPACES_DIRNAME, space_dir_name(sp))
        os.makedirs(sdir, exist_ok=True)
        # folder_name for relative links inside space readme
        for t in threads:
            rel = (t.get("rel_path") or "").replace("\\\\", "/")
            t["folder_name"] = rel.split("/")[-1] if rel else thread_folder_name(t.get("title") or "", t.get("uuid") or "")
        with open(os.path.join(sdir, "README.md"), "w", encoding="utf-8") as f:
            f.write(build_space_readme(sp, threads))

    spaces_summary = []
    for sp, threads in sorted(by_space.items(), key=lambda kv: (kv[0] != HOME_SPACE_NAME, kv[0].lower())):
        spaces_summary.append({
            "name": sp,
            "path": HOME_SPACE_NAME if sp == HOME_SPACE_NAME else f"{SPACES_DIRNAME}/{space_dir_name(sp)}",
            "thread_count": len(threads),
            "entries": sum((t.get("stats") or {}).get("entries", 0) for t in threads),
            "answer_chars": sum((t.get("stats") or {}).get("answer_chars", 0) for t in threads),
            "empty_answer_threads": sum(1 for t in threads if t.get("empty_answers")),
        })

    manifest = {
        "tool": "Perplexity Exporter",
        "layout": "spaces-v1",
        "version": APP_VERSION if "APP_VERSION" in globals() else "1.0.0",
        "exported_at": exported_at,
        "account": account or "",
        "total_threads": len(thread_records),
        "exported_threads": len(thread_records),
        "formats": ["json", "markdown"],
        "spaces": spaces_summary,
        "warnings": {"empty_answer_threads": empty_list},
        "threads": [
            {
                "uuid": t.get("uuid"),
                "title": t.get("title"),
                "space": t.get("space") or HOME_SPACE_NAME,
                "path": (t.get("rel_path") or "").replace("\\\\", "/"),
                "updated_at": t.get("updated_at") or "",
                "entries": (t.get("stats") or {}).get("entries"),
                "answer_chars": (t.get("stats") or {}).get("answer_chars"),
                "sources": (t.get("stats") or {}).get("sources"),
                "empty_answers": bool(t.get("empty_answers")),
            }
            for t in thread_records
        ],
    }
    with open(os.path.join(outdir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    save_uuid_index(outdir, uuid_index)
    return manifest

