**Meta title:** How to Search Your Saved AI Chats with Windows Search

**Meta description:** Your saved AI conversations are ordinary files on your PC. Here's how to find any of them in seconds with the search tools already built into Windows.

---

# How to Search Your Saved AI Conversations with Windows Search

Once you've saved a few dozen conversations with TotalRecalls, a new question comes up. Where was that answer about pricing? Which chat had the email draft you liked? Was it in ChatGPT or Claude?

You don't need a special tool to find out. Every conversation in your Library folder is a normal Markdown and JSON file, so Windows can search it like any other document on your PC.

This post shows you how to search your saved AI conversations with Windows Search. It takes about six minutes to read. You'll learn:

- Where to search, and which search box works best
- How to search inside your files, not just their names
- A few simple filters that narrow results fast
- How to make sure Windows can actually see what's inside your files

---

## The Short Answer

The whole idea fits in three points:

- **Search from inside your Library folder.** Open it in File Explorer and use the search box in the top-right corner.
- **Search the contents, not just the names.** Type `content:` before a word or phrase to search the text of every saved conversation.
- **Filter to Markdown files.** Add `ext:.md` so each conversation shows up once, in the format you'll want to read.

**Takeaway:** Open your Library folder, type `content:"your phrase" ext:.md`, and press Enter.

---

## Why Searching Your Files Works So Well

When a conversation lives only inside an AI provider's website, you can search it only with that provider's tools. And you can search only one provider at a time.

Saved files change that. Your ChatGPT, Claude, and Perplexity conversations sit side by side in one folder:

```
Library
├── chatgpt
│   ├── pricing-research.md
│   └── pricing-research.json
├── claude
│   ├── quarterly-report-draft.md
│   └── quarterly-report-draft.json
└── perplexity
    ├── laptop-battery-comparison.md
    └── laptop-battery-comparison.json
```

One search covers all of them. If you're on Pro, the same goes for Gemini, Grok, DeepSeek, Mistral, and Qwen.

It also happens on your own computer. Searching files in File Explorer looks through your own drive, and you don't need an internet connection to do it.

**Takeaway:** One folder, one search box, every provider at once.

---

## Step 1: Open Your Library Folder

Start in the right place. Searching from your Library folder keeps results focused on your saved conversations instead of your whole PC.

1. Open File Explorer.
2. Go to your Library folder.
3. Click the search box in the top-right corner of the window.

The search box says something like "Search Library." That means it will look through the Library folder and every provider subfolder inside it.

### Make the Folder Easy to Reach

If you search often, pin the Library folder so it's always one click away:

1. Right-click the Library folder.
2. Choose **Pin to Quick Access** (Windows 10) or **Pin to Quick access** from the menu (Windows 11).

It now appears in the left-hand panel of every File Explorer window.

**Takeaway:** Always search from inside the Library folder. It keeps results relevant and fast.

---

## Step 2: Search Inside Your Conversations

Typing a plain word in the search box usually matches file names first. That's useful if you remember what a conversation was called. Most of the time, though, you remember what was *said*, not the title.

To search the text inside your files, add `content:` before your search term.

### Basic Content Searches

| What You Type                        | What It Finds                                       |
| ------------------------------------ | --------------------------------------------------- |
| `content:pricing`                    | Conversations that mention "pricing" anywhere       |
| `content:"renewal rate"`             | Conversations with that exact phrase                |
| `content:invoice OR content:receipt` | Conversations mentioning either word                |
| `content:budget NOT content:2025`    | Conversations about budgets that don't mention 2025 |

A few small rules make these work:

- **Use quotes for exact phrases.** Without them, Windows may match the words separately.
- **Write AND, OR, and NOT in capitals.** In lowercase, Windows treats them as ordinary words.
- **Don't worry about capitalization in your search terms.** `content:Pricing` and `content:pricing` find the same files.

### Example: Finding an Old Answer

Say you remember asking an AI for help with a cover letter months ago, but not which provider. In your Library folder, type:

```
content:"cover letter" ext:.md
```

Every matching conversation appears, from every provider, in one list. The folder path under each result shows which provider it came from.

**Takeaway:** `content:` turns the search box from a file-name finder into a full-text search of every saved chat.

---

## Step 3: Narrow Your Results with Filters

Filters help when a search returns too much. You can combine them with `content:` searches in the same box.

### Show Each Conversation Only Once

Every conversation is saved as two files, so a content search often shows each match twice: once as `.md` and once as `.json`. Add `ext:.md` to see only the readable version:

```
content:"onboarding checklist" ext:.md
```

If you're looking for structured data for a script or another tool, use `ext:.json` instead.

### Filter by Date

If you remember roughly when a conversation was saved, filter by date:

| What You Type              | What It Finds                                  |
| -------------------------- | ---------------------------------------------- |
| `datemodified:today`       | Files saved or changed today                   |
| `datemodified:this week`   | Files from this week                           |
| `datemodified:last month`  | Files from last month                          |
| `datemodified:>2026-09-01` | Files saved or changed after September 1, 2026 |

Keep in mind that this date reflects when the file was saved to your PC or last edited. It isn't always the day you had the conversation with the AI provider.

### Filter by Provider

Each provider has its own subfolder. To search only one provider, open that subfolder first, such as `Library\claude`, then search from there.

### Filter by File Name

If you remember part of a title, use `name:`:

```
name:pricing
```

This matches file names that include "pricing," like `pricing-research.md`.

### Combining Filters

Filters stack. Here's a search for a phrase in Markdown files from the past month:

```
content:"launch plan" ext:.md datemodified:last month
```

**Takeaway:** Start with `content:` and `ext:.md`. Add a date or a provider subfolder when you need fewer results.

---

## Step 4: Make Sure Windows Can See Inside Your Files

Sometimes a content search comes back empty, even when you know the phrase is there. This usually means Windows isn't set up to read the contents of `.md` or `.json` files. A one-time setup fixes it.

### Option A: Turn On Content Search in File Explorer

This is the quickest fix.

1. Open File Explorer.
2. Open **Folder Options**. In Windows 10, click **View**, then **Options**. In Windows 11, click the **three-dot menu** in the toolbar, then **Options**.
3. Go to the **Search** tab.
4. Check **Always search file names and contents**.
5. Click **OK**.

Searches may run a little slower with this on, especially in very large folders. For most Library folders, the difference is small.

### Option B: Add Your Library Folder to the Windows Index

The Windows index is a catalog your PC builds so it can search faster. Adding your Library folder speeds up content searches, especially as your collection grows.

1. Search for **Indexing Options** in the Start menu and open it.
2. Click **Modify**.
3. Find your Library folder and check its box.
4. Click **OK**.

### Check That Markdown and JSON Contents Are Indexed

Indexing a folder doesn't always mean indexing what's inside every file type. Check these two:

1. In **Indexing Options**, click **Advanced**.
2. Open the **File Types** tab.
3. Find `md` in the list. If it's missing, type `md` in the box at the bottom and click **Add**.
4. Select `md` and choose **Index Properties and File Contents**.
5. Repeat for `json`.
6. Click **OK**.

Windows may take a while to rebuild the index after these changes. Searches will improve once it finishes.

**Takeaway:** If content searches miss files you know are there, turn on content search or check that `.md` and `.json` contents are indexed.

---

## Search Methods Side by Side

|                                            | **Start Menu Search**           | **File Explorer Search**         | **File Explorer + Filters**        |
| ------------------------------------------ | ------------------------------- | -------------------------------- | ---------------------------------- |
| **Where you use it**                       | Taskbar or Start menu           | Search box in the Library folder | Search box in the Library folder   |
| **Searches only your saved chats?**        | No, searches your whole PC      | Yes                              | Yes                                |
| **Searches inside files?**                 | Indexed files only              | Yes, with `content:`             | Yes, with `content:`               |
| **Can filter by date or file type?**       | Limited                         | Yes                              | Yes                                |
| **Shows which provider a chat came from?** | Sometimes                       | Yes, in the folder path          | Yes, in the folder path            |
| **May include web results?**               | Yes, depending on your settings | No                               | No                                 |
| **Best for**                               | Quick lookups by file name      | Most everyday searches           | Large libraries and specific needs |

The Start menu can be handy for opening a file you know by name. Depending on your Windows settings, though, it may also suggest web results for what you type. If you'd like your searches to stay on your computer, use File Explorer from inside your Library folder.

**Takeaway:** For searching saved conversations, File Explorer is the better choice. It's focused, local, and supports filters.

---

## Common Questions

### Why does each result show up twice?

Every conversation is saved as a Markdown file and a JSON file with the same name. Both contain the same text, so both match. Add `ext:.md` to your search to see each conversation once.

### Can I search across every provider at once?

Yes. Search from the top of the Library folder, and Windows looks through every provider subfolder inside it. To search just one provider, open its subfolder first.

### Do I need TotalRecalls open to search my chats?

No. Your saved conversations are standard files, so Windows can search them whether TotalRecalls is open or not.

### Does searching send my conversations anywhere?

Searching in File Explorer looks through files on your own drive. Your conversations aren't sent to our servers when you save them, and searching them in File Explorer doesn't change that. If your Library folder sits inside a cloud-synced folder, that service already stores a copy under its own policies.

### My search is slow. What can I do?

Add your Library folder to the Windows index, as described in Step 4. Indexed searches are much faster than searches that read every file each time.

### Can I search my backups too?

Yes. Open your backup location in File Explorer and search the same way. A zip archive needs to be extracted first, since Windows can't search reliably inside compressed files.

### Does this work on Mac or Linux?

TotalRecalls runs on Windows 10 and 11. macOS and Linux versions are in development.

---

## The Recommendation for Most People

**Pin your Library folder.** Put it in Quick Access so it's always one click away.

**Learn one search.** For nearly everything, this is all you need:

```
content:"your phrase" ext:.md
```

**Fix it once if results look thin.** If searches miss conversations you know exist, turn on content search in Folder Options or add `.md` and `.json` to the Windows index. After that, search should just work.

---

## Your Chats, Easy to Find

Saving your AI conversations as files means they belong to you. Being able to search them means you can actually use them. With one folder and one search box, every saved conversation from every provider is a few keystrokes away.

Open your Library folder, try a `content:` search for something you remember asking, and see how fast the right conversation turns up.

If you haven't tried TotalRecalls yet, the Free Tier covers ChatGPT, Claude, and Perplexity on Windows 10 and 11. You can save your first few conversations in minutes, then search them the same day.

**Download free at totalrecalls.app.**
