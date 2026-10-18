# HANDOFF — 2026-10-18 — marketing / YouTube channel

Read `totalrecalls-youtube-upload` skill first: it holds the channel id, playlist id,
the OAuth re-auth procedure, the upload script and the quota behaviour. This note
carries only what the skill does not.

## Product facts (use these, don't re-derive)
- TotalRecalls: Windows app, exports AI chat history from **8 providers** (ChatGPT,
  Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, Qwen Chat) to local
  Markdown + JSON. No account, no cloud, no telemetry.
- Price **$24 one-time**. Free Tier: 3 providers, 5 conversations per download.
- Site: totalrecalls.app (Astro, Cloudflare Pages, production branch `main`).
  Checkout: Paddle. Verify copy on /pricing before quoting it anywhere.

## Already done — do not redo
- **8 per-provider demo videos**, cut, verified and live at
  `video.totalrecalls.app/TR_website_<provider>.mp4`, wired into `/see-it-work/`
  with per-provider pages. Local renders + durations: skill, "Demo-video set" table.
- Site pages for all 8 providers, release date 2026-10-17, free-tier ZIP rebuilt with
  the Qwen login fix (sha `2f3f8445…`), `tools/release_gate.py` green.
- Channel exists and is **private**: @totalrecalls, UChO3ZyrGqRtBFHRuQx2qX1w;
  "Start Here" playlist PLHGgAPo4_vi8 already holds the earlier launch set.

## Blocking item, do this first
**Phone-verify the channel in YouTube Studio.** An unverified channel allows ~9–10
uploads then returns `uploadLimitExceeded`, and custom thumbnails 403. Both gates
lift with one phone verification. Do not start an 8-video batch before it.

## Decisions the user has not made yet
1. **Aspect for YouTube.** The demos are 3440×1440 (2.39:1). YouTube letterboxes
   that fine, but four-panel text is small on a phone. Options: upload wide as-is;
   add a 16:9 app-panel crop for Shorts/social; or both.
2. **Audio.** All demos are silent. Minimum is the anullsrc pass in the skill.
   Music or narration is a separate call.
3. **Channel visibility + trailer.** Publishing flips the channel public; the
   convergence "how it works" video is built and is meant to be the trailer, but
   pinning it is a Studio-only step (the API cannot do it).
4. **Lemon Squeezy.** An LS reply (pricing / video link / social URLs / product
   description) was drafted in September and never sent; the store moved to Paddle
   since. Ask whether LS is still in play before reviving that draft.

## Don'ts
- Do not re-shoot any demo video. All 8 are locked, gate-verified and on the site.
- Do not change price/privacy/claim copy on the site without explicit sign-off.
- Do not quote the "4x speed" line for a provider whose cut has no ramp — the
  per-video `intro` strings in `SeeItWorkDemos.js` are the source of truth.
- Do not run `app.py --loginprobe` while testing: it opens a real login flow against
  a singleton profile.


## Update before the marketing session (2026-10-18, later same day)

**Open question 4 is closed: Lemon Squeezy is out.** Paddle is the only store.
The site's copy, the ZIP README's "Buy at" line and the in-app Buy button all point
at Paddle; the last LS-era asset was removed and now 410s.

**Site state you can rely on (all verified live today):**
- Two email entry points only: `support@totalrecalls.app` (technical) and
  `contact@totalrecalls.app` (general). `legal@`, `privacy@` and `press@` no longer exist.
- `/roadmap/`, `/press/`, `/feature-requests/` and the six `/previews/*` pages now
  carry real copy; the six previews are linked from `/roadmap/` and each other.
- `/roadmap/` lists **code signing** as the highest-value next item — keep that framing
  in marketing material, it is the honest answer to "why does Windows warn me?".
- 60/60 sitemap URLs return 200, 0 broken internal links.
- Fresh screenshots of all 60 pages: `site/_shots/` (+ `INDEX.md`, + a ZIP, committed).

**The one buyer-facing risk worth carrying into the marketing plan:** the app is
unsigned and Defender has flagged this ZIP family as `Trojan:Win32/Bearfoos.A!ml`
(a container-level `!ml` false positive on the bundled EXE). The current build scans
clean, but any given customer may see "Download Failed: File not found" in Edge.
That is a support-load risk for launch, and code signing is the fix. Do not promise
"no antivirus warnings" anywhere in marketing copy.

**Videos:** 8/8 per-provider demo cuts are final, gate-verified and live on
`video.totalrecalls.app` — see the YouTube skill for the upload prep (they are silent;
an audio pass is required) and for the phone-verification step that must happen before
any batch upload.
