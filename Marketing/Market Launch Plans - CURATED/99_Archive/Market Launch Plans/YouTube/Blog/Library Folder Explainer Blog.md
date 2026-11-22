# Where TotalRecalls Saves Your Files

You just downloaded your first conversation with TotalRecalls. The app says it's done, and somewhere on your PC there are now two new files. This post shows you where they are, how they're organized, and what you'll see when you open them.

It takes about five minutes to read. By the end, you'll know exactly what you have and how to use it with tools already on your computer.

---

## Your Files Live in the Library Folder

Everything TotalRecalls saves goes into one place: the **Library folder**. It's a regular Windows folder on your own drive. You can open it in File Explorer, copy it, back it up, or search it like any other folder.

By default, you'll find it here:

```
C:\Users\[YourName]\Documents\TotalRecalls\Library
```

Replace `[YourName]` with your Windows user name.

### Three Quick Ways to Get There

**1. Through File Explorer**

Open File Explorer, click **Documents** in the left panel, then open **TotalRecalls**, then **Library**.

**2. Through the address bar**

Open File Explorer, click the address bar at the top, paste this line, and press Enter:

```
%USERPROFILE%\Documents\TotalRecalls\Library
```

The `%USERPROFILE%` part fills in your user name automatically.

**3. Through the Run box**

Press **Windows key + R**, paste the same line, and press Enter. File Explorer opens straight to the folder.

### Keep It One Click Away

Once you're in the Library folder, right-click it in the left panel or the address bar and choose **Pin to Quick access**. It will then appear in File Explorer's sidebar every time you open it, on both Windows 10 and Windows 11.

---

## How the Library Folder Is Organized

Inside the Library folder, each AI provider gets its own subfolder. Each conversation you download becomes a pair of files with the same name, one ending in `.md` and one ending in `.json`.

Here's what a Library might look like after a few downloads:

```
Library
├── chatgpt
│   ├── pricing-research.md
│   ├── pricing-research.json
│   ├── trip-planning-lisbon.md
│   └── trip-planning-lisbon.json
├── claude
│   ├── quarterly-report-draft.md
│   └── quarterly-report-draft.json
└── perplexity
    ├── laptop-comparison.md
    └── laptop-comparison.json
```

A few things are worth knowing:

- **One folder per provider.** ChatGPT conversations go in `chatgpt`, Claude in `claude`, and so on. If you use Pro, you'll also see folders for Gemini, Grok, DeepSeek, Mistral, and Qwen as you download from them.
- **File names come from the conversation.** They're based on the conversation's title, so you can usually recognize a chat at a glance.
- **Two files, same content.** The `.md` and `.json` files hold the same conversation in two different formats. You don't need both, but having both gives you options.

A provider's folder only appears after you download something from it. If you've only saved ChatGPT chats, you'll only see a `chatgpt` folder for now.

---

## What a Markdown File Looks Like

The `.md` file is the one most people open first. Markdown is plain text with a few simple marks for headings and emphasis. It's easy to read as is, and many apps display it neatly.

Here's an example of what you might see:

```
# Pricing research

**Provider:** ChatGPT
**Saved:** 2026-10-02

---

## You

What are common pricing models for small desktop software tools?

## ChatGPT

Most small desktop tools use one of three models:

1. **One-time purchase.** Pay once and keep the version you bought.
2. **Subscription.** Pay monthly or yearly for continued access.
3. **Freemium.** A free version with paid upgrades.
```

Your files may differ slightly in layout, but the idea is the same: each message is labeled, in order, as readable text.

### How to Open a Markdown File

You already have a tool that can open it. Some good options:

- **Notepad.** Built into Windows. Shows the raw text, including the `#` and `**` marks.
- **VS Code.** A free code editor. It can show a formatted preview of Markdown.
- **A note-taking app.** Many note apps can import or open Markdown files directly.

If Windows asks how you want to open a `.md` file, right-click it and choose **Open with**, then pick **Notepad** or another app. Check **Always use this app to open .md files** to skip the question next time.

### When Markdown Is Most Useful

- Rereading an old conversation
- Copying part of a chat into a document or email
- Keeping notes from AI work alongside your other notes
- Sharing a single conversation with a coworker

---

## What a JSON File Looks Like

The `.json` file holds the same conversation in a structured format. It's less pleasant to read, but it's very easy for software to work with.

A simplified example:

```
{
  "title": "Pricing research",
  "provider": "chatgpt",
  "saved_at": "2026-10-02T14:31:00Z",
  "messages": [
    {
      "role": "user",
      "content": "What are common pricing models for small desktop software tools?"
    },
    {
      "role": "assistant",
      "content": "Most small desktop tools use one of three models..."
    }
  ]
}
```

The exact fields in your files may vary, but the shape is the same: details about the conversation at the top, then each message in order, labeled by who sent it.

### How to Open a JSON File

- **Notepad** opens it fine, though long files can be hard to scan.
- **VS Code** adds color and lets you fold sections, which makes it much easier to read.
- **Microsoft Edge** can display JSON files in a tidy, readable layout. Drag the file into a browser window to try it.

### When JSON Is Most Useful

- Importing conversations into another tool or personal database
- Processing many conversations with a script
- Keeping a complete, structured record alongside the readable version

If you're not sure you'll ever need it, that's okay. Leave it in the folder. It takes up very little space.

---

## Finding a Conversation Later

As your Library grows, you'll want to find things quickly. Windows has good tools for this already.

### Search in File Explorer

Open the Library folder and type in the search box at the top right. File Explorer searches file names in the folder and all its subfolders. To search one provider only, open that provider's folder first.

### Search Inside Files

Windows can also search the text inside your files, not just their names. Results depend on whether Windows has indexed the folder. Because the Library folder lives under Documents, Windows usually indexes it by default.

If a search doesn't find words you know are in a file, check your indexing settings:

- **Windows 11:** Settings → Privacy & security → Searching Windows
- **Windows 10:** Settings → Search → Searching Windows

Make sure your Documents folder is included.

### Sort by Date

In File Explorer, switch to **Details** view and click the **Date modified** column. Your most recent downloads move to the top. This is the fastest way to find something you saved earlier today.

---

## Why Local Files Matter

TotalRecalls saves conversations as ordinary files on your PC for a few simple reasons.

**They're yours to keep.** Your saved files don't depend on a TotalRecalls account, because there isn't one. They don't depend on the app either. You can open them with Notepad years from now.

**They work with tools you already use.** Search, backup software, editors, note apps, and scripts all understand plain files. Nothing is locked in a format only one app can read.

**You decide where they go.** Your conversations aren't sent to our servers. When you download, the app connects directly from your PC to the AI provider you signed in to, and the files are written to your drive. After that, opening a saved file doesn't need TotalRecalls or an internet connection.

One thing to check: some Windows setups sync the Documents folder to OneDrive automatically. If yours does, your Library folder will sync too, just like the rest of Documents. That's a Windows setting, not a TotalRecalls one. You can look for the OneDrive icon in File Explorer's sidebar to see whether it applies to you.

---

## A Few Good Habits

- **Back up the Library folder now and then.** Copy it to an external drive or another backup location you trust. It's a single folder, so this is quick.
- **Copy before you reorganize.** If you'd like to sort conversations by project, copy files into a separate folder rather than moving the originals. That keeps the Library just as TotalRecalls expects it.
- **Keep both formats.** Markdown is for reading. JSON is for tools. Together, they cover nearly anything you might want to do later.

---

## Quick Reference

| Question                        | Answer                                               |
| ------------------------------- | ---------------------------------------------------- |
| **Where's the Library folder?** | `C:\Users\[YourName]\Documents\TotalRecalls\Library` |
| **How is it organized?**        | One subfolder per provider                           |
| **What files do I get?**        | A `.md` and a `.json` file for each conversation     |
| **What opens Markdown?**        | Notepad, VS Code, or a note-taking app               |
| **What opens JSON?**            | Notepad, VS Code, or Microsoft Edge                  |
| **How do I find a chat?**       | File Explorer search, or sort by Date modified       |
| **Which Windows versions?**     | Windows 10 and 11                                    |

---

That's all there is to it. Your conversations are now regular files in a regular folder, on your own PC, ready to read, search, and keep.

If you haven't tried TotalRecalls yet, the Free Tier covers ChatGPT, Claude, and Perplexity, and you can save your first conversation in a few minutes.

**Download free at totalrecalls.app.**
