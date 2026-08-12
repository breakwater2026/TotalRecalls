# 14 — Google Takeout Troubleshooting Guide

**Source:** Thread ASSET 16 (L1838–1865). Curated final copy. Guide content — pairs with the Gemini Takeout guide.

## Gemini Takeout Troubleshooting

Gemini exports your conversations through Google Takeout. If TotalRecalls can't read your Takeout folder, check the following:

**1. Use the correct Takeout option**
Select Gemini / Bard in Google Takeout. Download the ZIP and extract it fully.

**2. Point TotalRecalls to the extracted folder**
Choose the folder that contains: `Takeout/Apps/Gemini/` with JSON files inside.

**3. Make sure the ZIP is fully extracted**
Do not point TotalRecalls to the ZIP itself. Windows must extract the files first.

**4. Check for multiple Takeout folders**
If you have several Takeout downloads, use the newest one.

**5. Large exports may take time**
Gemini exports can be big. Let TotalRecalls finish scanning the folder.

If issues persist, contact support@totalrecalls.app.

## Curation notes

- This is the troubleshooting half; the Gemini Takeout guide (how to request/extract) lives in the guides. Implementation plan route: `/guides/gemini-takeout-archive/` (+ troubleshooting section).
