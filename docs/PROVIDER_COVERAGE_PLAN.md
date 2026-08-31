# Provider Coverage Plan — digging past the 50–100 conversation ceiling

**Goal:** understand why the probe returns ~50–100 conversations per provider and
what it takes to reach "everything the provider will give us."

**Status date:** 2026-08-30 · branch `RedesignV8`

> **Update 2026-08-30 (final):** DeepSeek (keyset cursor), ChatGPT (archived +
> Projects), and Claude (multi-org) are implemented. Mistral + Qwen pagination
> now stops on `has_more`/no-new-IDs. ChatGPT detail fetch gained a plural
> fallback. `devtools_probe record` captures pagination sequences. **Grok is now
> fixed end-to-end** against the live API (`/rest/app-chat/conversations` list +
> `.../{id}/responses` for messages, with timestamps + citations). **Remaining
> (need a live account):** Qwen has no server-side history API; Mistral's
> consumer list endpoint is unpublished.

---

## 1. Why we stall at 50–100

The same symptom has four different causes, and a provider can hit more than one:

1. **Wrong pagination model.** We guess `page`/`page_size` (DeepSeek, Mistral, Qwen),
   `lastId` (Grok), `offset`/`limit` (ChatGPT). Most consumer chat apps use **keyset/cursor
   pagination** or a **"load more" boundary timestamp**. If the param is wrong the server
   ignores it and returns its default first page forever — the classic "exactly 50."
2. **Fragile end-of-list detection.** `if len(items) < 50: break` assumes the server
   honored `page_size=50`. The robust signal is "this page added no *new* IDs" or an
   explicit `has_more`/`total`.
3. **"Recent-only" list endpoints.** Some providers' UI only ever shows recent chats;
   the list endpoint cannot enumerate full history. This is a hard ceiling we must
   route around via containers/archive/search/export, not pagination.
4. **Missing container / archive enumeration.** Threads buried in a Project, Space, or
   archive never appear in the global recent list.

---

## 2. Per-provider status

Legend — *verified* = confirmed against live traffic or an external reverse-engineering
spec; *inferred* = best-effort guess that needs a DevTools capture.

| # | Provider | Current list approach | Real surface (confidence) | Why it caps | Deep lever | Priority |
|---|----------|----------------------|---------------------------|-------------|------------|----------|
| 1 | **Perplexity** | Multi-source: `list_spaces` + `list_threads` + `thread_search` + `space_threads` | Session-cookie, multi-index discovery (verified in-house) | Minimal — already walks spaces + search | None major; keep as reference model | — |
| 2 | **ChatGPT** | 4-pass: `conversations?offset&limit=28&order=updated` + `order=created` + `search_term=""` + `gizmos` walk | `GET /backend-api/conversations?offset&limit&order → {items,total}` (verified) | **Archived chats excluded from default list**; **Projects** live under a different endpoint than GPTs | Add `is_archived=true` pass; walk `/backend-api/gizmos/snorlax/sidebar?owned_only=true` for Projects; verify detail endpoint (singular→plural + `num_turns` truncation) | **P0** |
| 3 | **Claude** | `chat_conversations` cursor pagination (100 pages) + `/projects` walk | `/api/organizations/{org}/chat_conversations` + cursor (verified) | **Only first org** enumerated (`_first_org_id`) | Enumerate *all* orgs, not just the first | **P1** |
| 4 | **Gemini** | Live batchexecute RPC + Google Takeout JSON ingest | RPC returns ~15 (shallow); Takeout is the full path (verified) | Live list is inherently shallow | Takeout remains the deep path; document as such | P1 (doc only) |
| 5 | **Grok** | `/rest/app-chat/conversations` + 6 alt endpoints, `lastId` cursor | No public reverse-engineering; **SSO cookies rejected** (known) | Auth scope; endpoints 401/403 | Needs a real captured session (Bearer + cookies) to even list | **P2 / blocked** |
| 6 | **DeepSeek** | `GET /api/v0/chat/sessions?page&page_size` (guessed) | **`GET /api/v0/chat_session/fetch_page`** with keyset cursor `lte_cursor.updated_at` + `lte_cursor.id`, returns `has_more` *(verified — Aver005/deep-reverse, live 2026-06-27)* | Wrong endpoint + wrong pagination + wrong envelope parse (`business_history_list` is stale) | Rewrite list to `chat_session/fetch_page` keyset cursor; use `POST /api/v0/export_all` as the full-history fallback | **P0** |
| 7 | **Mistral** | `GET /api/chat/conversations?page&page_size` (guessed) | Consumer `chat.mistral.ai` API unverified; Ory cookie auth *(cookie name verified)* | Guessed endpoint + params | Capture the real list XHR via DevTools | **P1** |
| 8 | **Qwen** | `GET /api/v1/chat/sessions?page&page_size` (guessed) | Web API exposes **no history list** (reverse-engineered proxy has only validate/refresh/models/chat/images/delete; "no real history search") | Likely a hard provider limit | Accept recents; surface Qwen export if any | **P2** |

---

## 3. What a real-account capture session must record

For each provider, in Chrome DevTools → Network → XHR/Fetch, while signed in:

1. **The list request** — exact URL + query string when the sidebar loads and when
   "load more"/infinite-scroll fires. This is the source of truth for the endpoint
   *and* the pagination params.
2. **The pagination sequence** — the 2nd and 3rd page requests (what changes: cursor,
   offset, timestamp?). Watch for `has_more`/`total`/`next` in the response.
3. **Container enumeration** — Projects/Spaces/archived/custom-GPT requests
   (e.g. ChatGPT `gizmos/snorlax/sidebar`, Claude `/projects`).
4. **Search** — one search request (empty term if the UI allows).
5. **The detail request** — one "open conversation" request (flags like
   `include_has_versions`, `num_turns`, `tree=True`, `render_all_tools`).
6. **Auth** — the exact `Authorization` header and/or `Cookie` header on those requests.

`totalrecalls/tools/devtools_probe.py` (`record` / `replay` / `diff`) already exists for
exactly this — extend it to record a **pagination sequence** rather than one GET.

---

## 4. Prioritized next moves

**P0 (highest coverage-per-hour, unblocks real users):**
1. **DeepSeek** — rewrite `list_conversations` to `GET /api/v0/chat_session/fetch_page`
   (keyset cursor, `has_more`), fix the envelope parse (`data.biz_data.chat_sessions`),
   fix `validate`/`fetch` endpoints (`/api/v0/chat_session/…`), and add
   `POST /api/v0/export_all` as the deep fallback. Update the stale fixture.
2. **ChatGPT** — add an `is_archived=true` pass and a Projects walk
   (`/backend-api/gizmos/snorlax/sidebar`); verify the detail endpoint still returns the
   full tree (the new `num_turns`-based endpoint truncates long threads).

**P1:**
3. **Claude** — enumerate all orgs (`/api/organizations`) and merge, not just the first.
4. **Mistral** — capture the real consumer list endpoint and fix params.

**P2 (needs a live account, or is a hard provider limit):**
5. **Grok** — capture a full Bearer+cookie session; confirm whether any list endpoint
   works before more code.
6. **Qwen** — confirm there is no history API; decide between "recents only" and
   shipping Qwen's own export path.

---

## 5. References

- DeepSeek: `github.com/Aver005/deep-reverse` — `docs/04-chat-sessions.md`,
  `docs/01-common.md` (pagination), `docs/12-export.md` (live-verified 2026-06-27).
- ChatGPT: `gunbark.dev` adapter notes; `gist.github.com/c4nc/c7f2e79adc5c9d70adf10af9cdd1f8c6`
  (Projects `gizmos/snorlax/sidebar`, `INCLUDE_ARCHIVED`); `codex-chats-mcp`.
- Mistral: `docs.mistral.ai/api/endpoint/beta/conversations` (developer API — a
  different surface than consumer `chat.mistral.ai`); Ory `ory_session_*` cookie policy.
- Qwen: `github.com/encryptarun/qwen-api` (web API surface — no history list).
- Gemini/Grok in-house: `docs/Gemini Login Hurdle.md`, `totalrecalls/adapters/grok/`.
