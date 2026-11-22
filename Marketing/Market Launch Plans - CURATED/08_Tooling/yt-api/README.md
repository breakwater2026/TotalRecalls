# yt-api — YouTube Data API automation

Python scripts for the TotalRecalls YouTube channel (`@totalrecalls`, channel id
`UChO3ZyrGqRtBFHRuQx2qX1w`). Copied from the source folder's `YouTube/yt-api/`.

**With one exception, these scripts hardcode no credentials** — they read them from files at
runtime. The exception was `exchange_once.py`, which had a live Google OAuth authorisation code
embedded in a string literal; it was **excluded** from this folder and is listed in
`99_Archive/MANIFEST.md`.

---

## ⚠ Credential files were deliberately NOT carried into this folder

The source `YouTube/yt-api/` contained live secrets:

| File | What it holds |
| --- | --- |
| `api_key.txt` | Google API key |
| `credentials.json` | OAuth client id + **client secret** |
| `token.json` | OAuth access token + **refresh token** |
| `capture_in.txt` | A one-time OAuth authorisation code (already consumed) |
| `capture_out.txt` | Auth URL + PKCE challenge |
| `oauth_run.log` | Auth URL containing the client id |

These were excluded during curation. **Do not copy them back from the source folder** — that would
re-introduce live credentials into a marketing directory.

### Before reusing these scripts

1. **Rotate the API key** in Google Cloud Console, and **re-issue the OAuth client** (the client
   secret in the source should be treated as compromised — it sat in a synced project folder).
2. Recreate `api_key.txt` and `credentials.json` in this directory.
3. Run `oauth_final.py` to produce a fresh `token.json`.
4. Delete the old credential files from the source folder once the new ones work.

---

## Scripts kept

| Script | Purpose |
| --- | --- |
| `test_apikey.py` | Cheapest check — confirms the API key works |
| `yt_probe.py` | Probe channel / playlist state |
| `oauth_code_capture.py`, `oauth_code_capture2.py` | Capture the OAuth redirect (loopback on port 9) |
| `oauth_final.py` | Full OAuth flow → writes `token.json` |
| `test_oauth.py`, `test_oauth_v3.py`, `test_oauth_manual.py`, `test_oauth_final.py` | Successive OAuth verification attempts |
| `make_plan.py` | Builds `uploads_plan.json` from a set of files |
| `upload_video.py` | Single upload |
| `upload_batch.py` | Batch upload from `uploads_plan.json` |
| `upload_convergence.py` | Uploads the convergence animation |
| `convergence_finish.py` | Sets thumbnail / playlist position for the convergence video |
| `apply_branding.py` | Applies banner / watermark branding |

## State files NOT carried

`uploads_plan.json`, `upload_result.json`, `upload_batch_result.json`, `result.json`,
`playlist_start_here.json`, `convergence_done.json`, `oauth_err.log`, `oauth_run.log` — these are
October channel state referencing video IDs that were slated for deletion. Regenerate them by
running `make_plan.py` / the upload scripts.

---

## Quota note

YouTube Data API v3 default quota is 10,000 units/day. A read costs ~1 unit; **an upload costs
~1,600 units**, so a batch of 8 uploads is roughly 12,800 units and will exceed the default until a
quota increase is granted. This is why the source folder hit `uploadLimitExceeded` on 2026-10-01
after 9 uploads.

See `../YouTube Data API - Setup Reference.md` for the generic setup walkthrough.
