# TotalRecalls monorepo layout (scaffolding)

This repo currently still runs the v1 Perplexity desktop app from the **repository root**
(`app.py`, `app_ui.html`, `dist/`, `build/`). That root IS the frozen v1 product surface.

The directories below are the **target layout** for multi-provider work. They start empty
(or nearly empty) so we do not break the working EXE path while refactoring.

```
.
├── app.py, app_ui.html, dist/, build/   # v1 Perplexity Exporter (PRESERVE)
├── docs/                                # decisions, adapter spec, schema
├── apps/
│   └── web-ui/                          # React + Vite UI (Phase 4)
├── packages/                            # future shared TS packages
├── src/                                 # Python package split (Phase 2)
│   └── totalrecalls/                    # adapters + core (to be filled)
└── site/                                # totalrecalls.app marketing (Phase 1)
```

See `docs/DECISIONS.md` for locked product decisions.
See `.hermes/plans/` for the full commercialization plan.
