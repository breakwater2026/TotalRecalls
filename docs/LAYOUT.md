# TotalRecalls monorepo layout

## Current (Phase 2)

```
.
├── app.py                          # Thin compatibility entry (PyInstaller + tests)
├── app_ui.html                     # v1 UI (Phase 4 → React)
├── totalrecalls/                   # *** Application package ***
│   ├── __init__.py                 # APP_NAME / VERSION / BUILD_TAG
│   ├── core/
│   │   ├── paths.py                # appdata, log, session, single-instance
│   │   ├── export_fs.py            # Spaces/Home layout + indexes
│   │   └── errors.py               # friendly_error
│   ├── adapters/
│   │   └── perplexity/
│   │       ├── http.py             # curl_cffi transport, ApiError
│   │       ├── auth.py             # token extract + validate_session
│   │       ├── discover.py         # multi-source list_threads
│   │       └── thread.py           # get_thread, markdown
│   └── desktop/
│       ├── js_api.py               # pywebview JsApi facade
│       ├── bridge.py               # login + export worker
│       ├── ui_dispatch.py
│       └── main.py                 # entrypoint
├── apps/web-ui/                    # Phase 4 React+Vite (placeholder)
├── site/                           # totalrecalls.app marketing (placeholder)
├── docs/
├── tests/
├── build/ + dist/                  # v1 freeze artifacts (preserved)
└── src/totalrecalls/README.md      # points here (legacy path note)
```

v1 EXE path: `python app.py` or `dist/PerplexityExporter.exe` still valid.
