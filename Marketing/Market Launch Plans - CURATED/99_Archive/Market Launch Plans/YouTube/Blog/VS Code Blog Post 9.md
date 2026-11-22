**Meta title:** How to Use Your Saved AI Chats in VS Code (Windows)

**Meta description:** Your saved AI conversations are Markdown and JSON files, so VS Code can open, search, and compare them. Here's how to set it up and reuse code from your chats safely.

---

# How to Use Your Saved AI Chats in VS Code

Many AI conversations end with something worth keeping: a script, a SQL query, a config file, or a clear explanation of why a build failed. Inside a chat window, those answers are easy to lose. Saved as files, they become a reference you can search and reuse.

VS Code is a good fit for this job. It's a free code editor from Microsoft, and it handles Markdown and JSON well. Every conversation TotalRecalls saves is a Markdown file with a matching JSON file, so VS Code can open your Library folder exactly as it is, with no conversion or import step.

This post shows you how to use your saved AI chats in VS Code on Windows. It takes about seven minutes to read. You'll learn:

- How to open your Library folder and read chats with a clean preview
- How to search every conversation at once, including by provider or month
- How to compare two answers side by side
- How to explore the JSON version of a chat
- How to move code from a chat into a real project
- A few settings that protect your original files and keep your chats on your PC

---

## The Short Answer

The whole idea fits in three points:

- **Open the Library folder in VS Code.** Every provider subfolder appears in one sidebar.
- **Read with the preview, search with Ctrl + Shift + F.** The preview makes chats easy to read, and search covers every file at once.
- **Treat saved chats as a record, not a draft.** Copy code out into your projects instead of editing the originals.

**Takeaway:** VS Code turns your Library folder into a searchable reference shelf for every answer you've saved.

---

## Why VS Code Works Well with Saved AI Chats

Different tools suit different chats. Obsidian is strong when you want to link conversations to your notes and ideas. VS Code is stronger when your chats are full of code, or when you want to work with the JSON files as well.

Here's what VS Code gives you:

- **Syntax highlighting.** Code blocks inside your chats appear in color, matched to their language.
- **Markdown preview.** Headings, lists, tables, and code blocks render cleanly.
- **Flexible search.** Search all chats, one provider, or one month, with optional pattern matching.
- **Readable JSON.** Format and fold the structured version of each conversation.
- **Built-in compare.** See exactly where two answers differ.
- **Workspaces.** Keep your saved chats and your project open in the same window.

### How It Compares to Other Options

|                             | **Notepad**    | **Obsidian**          | **VS Code**                    |
| --------------------------- | -------------- | --------------------- | ------------------------------ |
| **Cost**                    | Free, built in | Free for personal use | Free                           |
| **Markdown preview**        | No             | Yes                   | Yes                            |
| **Code highlighting**       | No             | Yes                   | Yes, for many languages        |
| **JSON formatting**         | No             | Not shown by default  | Yes                            |
| **Search across all chats** | No             | Yes                   | Yes, with filters and patterns |
| **Compare two files**       | No             | No                    | Yes, built in                  |
| **Link chats to notes**     | No             | Yes, very well        | Basic                          |
| **Best for**                | Quick reading  | Notes and ideas       | Code and technical chats       |

**Takeaway:** Reach for VS Code when your saved chats are technical. Reach for Obsidian when they're about ideas and decisions. Both read the same files, so you don't have to pick just one.

---

## Before You Start

You need three things:

1. **Some saved conversations.** The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini (through Google Takeout), Grok, DeepSeek, Mistral, and Qwen.
2. **VS Code for Windows.** Download it from code.visualstudio.com and run the installer. It works on Windows 10 and 11.
3. **Your Library folder location.** By default, that's:

```
C:\TotalRecalls\Library\
```

If your Library lives somewhere else, use your own path wherever you see `C:\TotalRecalls\Library` in this post.

**Takeaway:** Install VS Code and know where your Library folder is. That's all the setup you need.

---

## Step 1: Open Your Library Folder

1. Open VS Code.
2. Choose **File → Open Folder**, or press **Ctrl + K**, then **Ctrl + O**.
3. Select `C:\TotalRecalls\Library` and click **Select Folder**.

The first time you open a folder, VS Code asks whether you trust the authors of its files. Your Library holds plain text conversations, so either choice works for reading. Choosing **No, I don't trust the authors** opens the folder in Restricted Mode. That's a sensible default here, because it turns off features that could run code automatically, while reading, previewing, and searching still work.

Your provider subfolders now appear in the Explorer panel on the left. Click one to see its conversations.

### Jump to Any Chat by Name

Press **Ctrl + P** and type part of a filename, such as `pricing`. VS Code lists matching files as you type. Because saved filenames start with a date, typing `2026-09` lists every chat saved in September 2026.

**Takeaway:** Open the Library folder once, and every saved chat is a few keystrokes away.

---

## Step 2: Read Chats with Markdown Preview

Raw Markdown is readable, but the preview is easier on the eyes, especially for long answers with lists and code.

| What You Want                        | Shortcut                 |
| ------------------------------------ | ------------------------ |
| Open the preview in its own tab      | **Ctrl + Shift + V**     |
| Open the preview beside the raw file | **Ctrl + K**, then **V** |

The preview shows headings, lists, tables, and code blocks much as they appeared in the original chat. It's also a safe way to read, because you can't type into the preview. Nothing changes by accident.

### Use the Outline for Long Chats

Long conversations can be tiring to scroll. Open the **Outline** section at the bottom of the Explorer panel. It lists every heading in the current file, including each message label, so you can jump straight to the part you need.

**Takeaway:** Read in preview, and use the Outline to move around long conversations.

---

## Step 3: Search Every Conversation at Once

Press **Ctrl + Shift + F** to open search. Type a word or phrase, and VS Code lists every match across every provider, grouped by file. Click any result to jump to that line.

To narrow your search, click the three dots under the search box. That reveals two fields: **files to include** and **files to exclude**.

| What You Want                    | What to Enter                      |
| -------------------------------- | ---------------------------------- |
| Search Claude chats only         | Files to include: `claude/**`      |
| Search Markdown files only       | Files to include: `*.md`           |
| Search chats from September 2026 | Files to include: `*2026-09*`      |
| Skip the JSON files              | Files to exclude: `*.json`         |
| Match exact capital letters      | Click **Aa**, or press **Alt + C** |
| Match whole words only           | Click **ab**, or press **Alt + W** |

Excluding `*.json` is worth doing most of the time. Each conversation exists in both formats, so without it, you'll see every match twice.

### Find Answers by Their Shape

Sometimes you remember what an answer looked like, but not its exact words. Turn on pattern matching by clicking **.\***, or pressing **Alt + R**. A few useful patterns:

| Pattern          | What It Finds                        |
| ---------------- | ------------------------------------ |
| `^```python`     | The start of every Python code block |
| `def \w+\(`      | Python function definitions          |
| `SELECT .* FROM` | SQL queries                          |
| `https?://\S+`   | Links mentioned in your chats        |

You don't need to learn patterns to use VS Code well. Plain words work for most searches. Patterns simply help when the shape of an answer is easier to recall than its wording.

**Takeaway:** Plain search finds words. "Files to include" narrows it to one provider or month. Patterns find code by its shape.

---

## Step 4: Compare Two Answers Side by Side

If you asked ChatGPT and Claude the same question, VS Code can show you exactly how their answers differ.

1. In the Explorer panel, right-click the first file and choose **Select for Compare**.
2. Right-click the second file and choose **Compare with Selected**.

VS Code opens both files side by side, with changed lines highlighted. Use the arrows at the top of the compare view to step from one difference to the next.

This also works for two versions of the same conversation. If you saved a chat again after it grew, comparing the two files shows exactly what was added.

**Takeaway:** Built-in compare makes it easy to see how two providers, or two versions of one chat, answered differently.

---

## Step 5: Look Inside the JSON Files

The Markdown file is for reading. The JSON file holds the same conversation in a structured format, with labeled fields for details like the title, provider, and each message. That's useful if you ever want to write scripts or build tools on top of your chats.

To make a JSON file easier to read:

1. Open the `.json` file.
2. Press **Shift + Alt + F** to format it neatly, if it isn't already.
3. Use the small arrows beside the line numbers to fold and unfold sections, such as the full list of messages.

VS Code also adds color to field names and values, which makes the structure easier to follow.

Take a few minutes to see how the data is laid out before writing anything that depends on it. Field details can vary between providers, so check one file from each provider you use. If you only plan to read your chats, you can ignore the JSON files completely.

**Takeaway:** You don't need the JSON files to read your chats, but VS Code makes them easy to explore when you want structured data.

---

## Step 6: Move Code from a Chat into a Project

This is where saved chats pay off. Instead of scrolling through an old chat window, you can find the code you need in seconds and bring it into your work.

### Use a Workspace with Two Folders

A workspace lets you open your Library folder and a project folder in the same window.

1. Open your project folder in VS Code.
2. Choose **File → Add Folder to Workspace** and select `C:\TotalRecalls\Library`.
3. Choose **File → Save Workspace As** and save the workspace file outside the Library folder, such as in your Documents folder or your project folder.

Both folders now appear in the sidebar. Search covers both at once, and you can drag a saved chat into a split view beside the file you're working on.

### Copy, Then Make It Your Own

1. Find the code block in the saved chat.
2. Select it and copy it with **Ctrl + C**.
3. Paste it into a new or existing file in your project.
4. Read it carefully, test it, and adjust it to fit your project.

AI-written code can contain mistakes, outdated methods, or assumptions that don't match your setup. Treat it as a starting point you review, not a finished answer.

### Leave a Pointer Back to the Source

Add a short comment above the pasted code so you know where it came from:

```
# Based on Claude chat: claude/2026-09-18-quarterly-report-draft.md
```

Months later, you can open the original conversation and read the full reasoning behind the code, including any warnings or alternatives the AI mentioned.

**Takeaway:** Keep chats and projects in one workspace. Copy code out, test it, and note which chat it came from.

---

## Step 7: Protect Your Originals and Keep Things Local

### Make the Library Read-Only in VS Code

Your saved chats are a record of what was said. You can tell VS Code to block edits to them.

1. Press **Ctrl + Shift + P** to open the Command Palette.
2. Type **Preferences: Open Workspace Settings (JSON)** and press Enter.
3. Add this setting:

```
"files.readonlyInclude": {
  "C:/TotalRecalls/Library/**": true
}
```

Use forward slashes in the path, even on Windows. If you saved a workspace file in Step 6, this setting lives in that file, so nothing new gets added inside your Library folder.

For a quick one-off, you can also run **File: Set Active Editor Read-only in Session** from the Command Palette. It locks just the file you have open, until you close VS Code.

### Decide What Leaves Your PC

Your saved conversations aren't sent to our servers. VS Code itself works with files on your own drive, but some of its features can connect to the internet. It's worth knowing which ones:

- **AI assistants.** Built-in chat features and extensions such as GitHub Copilot can send file contents to their service when you use them. Keep them away from conversations you consider private.
- **Extensions.** Some extensions connect online. Read what each one does before installing it.
- **Telemetry.** VS Code sends usage data to Microsoft by default. To turn it off, open **Settings** with **Ctrl + ,**, search for `telemetry`, and set **Telemetry Level** to **off**.
- **Settings Sync.** If you turn it on, your editor settings sync to your account. Your chat files don't sync, but your settings, including any paths you've added, may.

**Takeaway:** Lock your saved chats as read-only, and choose on purpose which online features you use with them.

---

## Common Mistakes to Avoid

- **Editing original chats.** Copy code out instead, so your saved record stays accurate.
- **Saving the workspace file inside the Library folder.** Keep it in Documents or your project folder, so your Library holds only saved chats.
- **Pasting AI code without testing it.** Read it, run it, and check it fits your project before you rely on it.
- **Using AI assistants on private chats.** These tools may send file contents online when you use them.
- **Searching JSON and Markdown together.** You'll see every match twice. Exclude `*.json` when you only want readable results.
- **Installing extensions without checking them.** Fewer, well-understood extensions keep your setup simple and predictable.

---

## Common Questions

### Do I need TotalRecalls open to use my chats in VS Code?

No. Your saved conversations are standard Markdown and JSON files. VS Code reads them whether TotalRecalls is open or not.

### Will VS Code change my saved files?

Not unless you edit a file and save it. Reading, previewing, searching, and comparing don't change anything. The read-only setting adds an extra layer of protection.

### Can I use VS Code and Obsidian on the same folder?

Yes. They read the same files. Many people use Obsidian for notes and idea-heavy chats, and VS Code for code-heavy ones.

### Does Restricted Mode limit what I can do?

For reading and searching, no. Restricted Mode mainly turns off features and extensions that could run code from the folder. Markdown preview, search, and compare all still work.

### Is VS Code hard to learn?

Not for this. Opening a folder, reading, searching, and comparing use the handful of shortcuts covered above. You can safely ignore everything else.

### Does this work on Mac or Linux?

TotalRecalls runs on Windows 10 and 11. macOS and Linux versions are in development.

---

## The Recommendation for Most People

**Open the folder and search.** Start with **Ctrl + Shift + F**, and exclude `*.json`. It's the fastest way to find an answer you've already saved.

**Read in preview.** **Ctrl + Shift + V** keeps chats readable and safe from accidental edits.

**Build one workspace.** Pair your Library folder with the project you work on most. Copy code out as you need it, test it, and leave a pointer back to the source chat.

---

## Your Saved Answers, Ready to Reuse

Saving your AI conversations as files means they belong to you. Searching, organizing, and backing them up keeps them useful and safe. Opening them in VS Code puts the code and fixes you've already asked for right beside the work you're doing now.

Open your Library folder in VS Code, search for one problem you solved with AI last month, and see how quickly the answer comes back.

If you haven't tried TotalRecalls yet, the Free Tier covers ChatGPT, Claude, and Perplexity on Windows 10 and 11. You can save your first conversations in a few minutes and open them in VS Code the same day.

**Download free at totalrecalls.app.**
