# TotalRecalls Browser Companion

This is a loadable Chrome/Edge Manifest V3 extension for saving the **current
conversation** from ChatGPT, Claude, or Gemini as a TotalRecalls browser
handoff JSON file.

## Install (unpacked)

1. Open `chrome://extensions` or `edge://extensions`.
2. Enable **Developer mode**.
3. Choose **Load unpacked** and select this `browser-extension` directory.
4. Open a supported conversation, click the extension, then choose **Save
   current conversation**.

The downloaded `*.handoff.json` can be reviewed and imported locally:

```powershell
python tools\import_browser_handoff.py .\totalrecalls-chatgpt-title-2026-09-02.handoff.json `
  --output "$env:USERPROFILE\TotalRecalls"
```

## Privacy and permissions

- No credentials, cookies, provider APIs, or network requests are used.
- No localhost listener, service worker, telemetry, or remote code is included.
- The extension reads only the active supported provider tab and uses the
  browser's download API to write a local file.
- `activeTab`, `scripting`, and provider host access are used so an already-open
  tab can be handled after installation. `downloads` is used only for the
  explicit save action.

Provider websites change their DOM regularly. The extractors use stable
semantic attributes where available and fail safely when no messages can be
identified. Very long or virtualized chats may require scrolling through the
conversation first so all messages are present in the page. Review the JSON
before importing it.

## Handoff format

The output is version 1 of `totalrecalls-browser-handoff` and contains
`schema_version: 1`, the provider, source URL, title, timestamps, and messages
with `role`, `content_md`, optional model/citation data, and provider message
IDs where available. It is compatible with `totalrecalls.browser_handoff.py`.

## Tests

The extractor tests use Node's built-in test runner and require no package
installation:

```powershell
node --test browser-extension\tests\extractors.test.js
```
