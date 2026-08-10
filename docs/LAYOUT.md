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
│   │   ├── export_fs.py            # classic Spaces/Home layout + indexes
│   │   ├── schema.py               # UnifiedConversation (Phase 3)
│   │   ├── unified_export.py       # Library/<provider>/ writer + export_via_adapter
│   │   └── errors.py
│   ├── adapters/
│   │   ├── base.py                 # ProviderAdapter protocol + registry
│   │   └── perplexity/
│   │       ├── http.py / auth.py / discover.py / thread.py
│   │       └── adapter.py          # PerplexityAdapter
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
