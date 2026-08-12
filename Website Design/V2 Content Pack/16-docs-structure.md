# 16 — Documentation Site Structure (reference)

**Source:** Thread "Full Documentation Site Structure" (L1945–2116). Curated reference — the thread's structure for a future docs hub. NOT a V2 page; keep as `marketing/docs-site-structure.md` reference per implementation plan §7.5.

## Structure (as concluded)

**Home** — What is TotalRecalls · Supported providers · One-time pricing · Download link

**Quick start** — System requirements (Windows 10/11) · Downloading the ZIP · SmartScreen notice · First launch · Choosing a provider · Export basics · Where files are saved

**Provider Guides**
- **ChatGPT** — How ChatGPT stores history · Exporting with TotalRecalls · Folder structure · Markdown + JSON examples · Troubleshooting
- **Claude** — Projects vs conversations · Exporting Claude history · Handling long threads · Folder structure · Troubleshooting
- **Perplexity** — Why Perplexity deletes history · Exporting threads · Research workflows · Folder structure · Troubleshooting
- **Gemini** — Google Takeout overview · How to request a Takeout · Extracting the ZIP · Pointing TotalRecalls to the folder · Troubleshooting (Takeout issues, missing JSON)
- **Grok** — Exporting Grok conversations · Folder structure · Troubleshooting

**Library Format** — Overview of the Library/ folder · Naming conventions · Markdown structure · JSON structure · Metadata fields · How to back up your archive · How to search your archive manually

**Privacy & Security** — Local-only design · No cloud storage · No telemetry · No account required · Session token handling · SmartScreen explanation · Surface Smart App Control limitations · Code-signing roadmap

**Troubleshooting** — SmartScreen · Smart App Control · Gemini Takeout issues · Provider login issues · Missing conversations · Slow exports · Folder permission issues · Antivirus false positives

**Roadmap** — Near-term improvements · Mid-term features · Long-term upgrades · Optional paid add-ons · Principles (local-first, no forced subscription)

**Release Notes** — v1.3.0 · Previous versions · Bug fixes · Performance improvements · Known issues

**Support** — Contact · FAQ · Refund policy · Feature requests · Known provider limitations · Terms of use · Privacy policy

## Curation notes

- This structure influenced the V2 guide routes. The implementation plan's §4 route inventory is the V2 page set; this docs structure is for a LATER docs hub — do not build all of it into V2 (V2 = 40 routes per plan).
