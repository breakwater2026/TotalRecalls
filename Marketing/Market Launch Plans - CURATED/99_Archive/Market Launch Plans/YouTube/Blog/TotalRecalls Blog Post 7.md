**Meta title:** How to Open Your Saved AI Chats in Obsidian (Windows)

**Meta description:** Your saved AI conversations are Markdown files, so Obsidian can open them directly. Here's how to set it up, link chats to your notes, and keep originals safe.

---

# How to Open Your Saved AI Chats in Obsidian

Searching your saved conversations helps you find one answer. Sometimes you want more than that. You want to read a chat next to your own notes, link it to a project, or come back to it as part of a bigger body of work.

Obsidian is a good fit for this. It's a note-taking app that works with plain Markdown files stored in a folder on your PC. Every conversation TotalRecalls saves is already a Markdown file, so Obsidian can open your saved AI chats with no conversion step.

This post shows you how to open your saved AI chats in Obsidian on Windows. It takes about seven minutes to read. You'll learn:

- Three ways to set it up, and which one suits you
- How to browse, search, and link your saved conversations
- How to keep your original files safe while you work with them
- A few settings that keep everything on your own computer

---

## The Short Answer

The whole idea fits in three points:

- **Obsidian reads folders of Markdown files.** It calls a folder a "vault," and your Library folder can become one.
- **Pick one setup and stick with it.** Open the Library folder as its own vault, or place it inside a vault you already use.
- **Keep the originals as they are.** Write your thoughts in separate notes that link back to each saved chat.

**Takeaway:** Open your Library folder in Obsidian, then add your own notes alongside your chats instead of inside them.

---

## Why Obsidian Works Well with Saved AI Chats

Obsidian doesn't store your notes in its own database or on its own servers. It reads and writes ordinary `.md` files in a folder you choose. That's the same format TotalRecalls saves your conversations in.

So nothing needs to be imported, exported, or converted. Your saved chats stay where they are on your drive, and Obsidian simply shows them to you in a more useful way.

Here's what that gives you:

- **Readable formatting.** Headings, lists, tables, and code blocks display cleanly.
- **Fast switching.** Jump between conversations by typing part of a title.
- **Links between ideas.** Connect a Claude chat to a ChatGPT chat, or to your own project notes.
- **A clear exit.** If you stop using Obsidian, your files are still plain Markdown in the same folder.

**Takeaway:** Obsidian adds a reading and linking layer on top of your files without taking them over.

---

## Before You Start

You need three things:

1. **Some saved conversations.** At least a few chats in your Library folder. The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini, Grok, DeepSeek, Mistral, and Qwen.
2. **Obsidian for Windows.** Download it from obsidian.md and run the installer. It works on Windows 10 and 11, and it's free to download and use.
3. **Your Library folder location.** By default, that's:

```
C:\TotalRecalls\Library\
```

Inside it, each provider has its own subfolder:

```
Library
├── chatgpt
│   ├── 2026-09-14-pricing-research.md
│   └── 2026-09-14-pricing-research.json
├── claude
│   ├── 2026-09-18-quarterly-report-draft.md
│   └── 2026-09-18-quarterly-report-draft.json
└── perplexity
    ├── 2026-09-22-laptop-battery-comparison.md
    └── 2026-09-22-laptop-battery-comparison.json
```

**Takeaway:** Install Obsidian and know where your Library folder lives. That's all the preparation you need.

---

## Step 1: Choose How to Set Up Your Vault

There are three sensible ways to bring your saved chats into Obsidian. Each one has trade-offs, so pick the one that matches how you already work.

### Option A: Open the Library Folder as Its Own Vault

This is the simplest choice if you're new to Obsidian.

1. Open Obsidian.
2. Choose **Open folder as vault**.
3. Select your Library folder and click **Select Folder**.

Obsidian opens with every provider subfolder in the left-hand panel. Obsidian also adds a small hidden `.obsidian` folder inside Library to store its settings. Your conversation files aren't changed.

### Option B: Move the Library Folder into a Vault You Already Use

If you already keep notes in Obsidian, you may want your chats in the same place.

1. Close TotalRecalls.
2. Move the Library folder into your existing vault folder.
3. If TotalRecalls lets you choose a save location, point it at the new path.
4. Open your vault in Obsidian. The Library folder appears alongside your other notes.

Check the save location carefully. If TotalRecalls keeps saving to the old path, new chats won't show up in your vault.

### Option C: Copy Selected Chats into Your Vault

If you only want a handful of important conversations in your notes, copy them across.

1. Open your Library folder in File Explorer.
2. Copy the `.md` files you want.
3. Paste them into a folder inside your vault, such as `AI Chats`.

This keeps your vault tidy. The downside is that new chats won't appear on their own, and you'll have two copies of each file you move.

### Setup Options Side by Side

|                                      | **A: Library as Its Own Vault** | **B: Library Inside Your Vault** | **C: Copy Selected Chats** |
| ------------------------------------ | ------------------------------- | -------------------------------- | -------------------------- |
| **Effort to set up**                 | Lowest                          | Medium                           | Low, but repeated          |
| **New chats appear automatically?**  | Yes                             | Yes, if the save path is updated | No                         |
| **Mixes chats with your own notes?** | No, separate vault              | Yes                              | Yes                        |
| **Duplicate files?**                 | No                              | No                               | Yes                        |
| **Easy to undo?**                    | Yes, close the vault            | Move the folder back             | Delete the copies          |
| **Best for**                         | New Obsidian users              | Existing Obsidian users          | Keeping only key chats     |

**Takeaway:** Start with Option A. Move to Option B once you know you want chats and notes in one place.

---

## Step 2: Browse Your Saved Conversations

Once your vault is open, the left-hand panel shows your folders. Click a provider subfolder, then click any file to read it.

### Why You Won't See the JSON Files

By default, Obsidian only shows file types it can open as notes. Your `.json` files are still in the folder, but Obsidian hides them. That's helpful, because each conversation appears once in the readable Markdown version.

If you ever want to see them, go to **Settings → Files and links** and turn on **Detect all file extensions**. Most people can leave this off.

### Switch Between Chats Quickly

Press **Ctrl + O** to open the Quick Switcher. Type part of a file name, such as `pricing`, and press Enter. Because filenames start with a date, typing `2026-09` also shows every chat saved that month.

### Read in Reading View

Press **Ctrl + E** to switch between editing and reading view. Reading view displays the conversation cleanly and makes accidental edits less likely.

**Takeaway:** Use the Quick Switcher to move between chats, and reading view to read them safely.

---

## Step 3: Search Across Every Provider

Obsidian has its own search, and it covers every file in your vault at once.

1. Press **Ctrl + Shift + F** to open search.
2. Type a word or phrase.
3. Click a result to jump straight to that part of the conversation.

A few search tips work well with saved chats:

| What You Type        | What It Finds                             |
| -------------------- | ----------------------------------------- |
| `"renewal rate"`     | That exact phrase                         |
| `path:claude budget` | "Budget" in Claude conversations only     |
| `file:pricing`       | Files with "pricing" in the name          |
| `invoice OR receipt` | Either word                               |
| `budget -2025`       | "Budget" in chats that don't mention 2025 |

This works alongside Windows Search, not instead of it. Windows Search is useful from File Explorer and needs no extra app. Obsidian search is faster to use while you're already reading and writing notes.

**Takeaway:** Use `path:` to search one provider, and plain words or quoted phrases to search all of them.

---

## Step 4: Link Chats to Your Own Notes

This is where Obsidian earns its place. You can connect conversations to each other and to your own thinking.

### Keep the Original Conversation Unchanged

Treat each saved chat as a record of what was said. If you edit it, you lose that record. Instead, write your notes in a separate file and link to the chat.

This also avoids surprises if you save the same conversation again later. Your notes live in your own file, so they stay safe whatever happens to the original.

### Create a Note That Links to a Chat

1. Create a new note with **Ctrl + N**.
2. Give it a clear title, such as `Pricing decision`.
3. Type `[[` and start typing the chat's filename.
4. Pick the conversation from the list.

Your note now contains a link like this:

```
## Pricing decision

Went with the one-time model. Reasoning is in the original research chat:
[[2026-09-14-pricing-research]]

Follow-up questions I asked Claude:
[[2026-09-18-quarterly-report-draft]]
```

Click either link and Obsidian opens that conversation.

### See Where a Chat Is Referenced

Open any saved conversation and look at the **Backlinks** panel. It lists every note that links to it. Over time, this shows you which conversations you actually rely on.

### Use a Simple Folder for Your Notes

Keep your own notes out of the provider subfolders. A structure like this keeps things clear:

```
Vault
├── Library
│   ├── chatgpt
│   ├── claude
│   └── perplexity
└── Notes
    ├── Pricing decision.md
    └── Q4 planning.md
```

**Takeaway:** Saved chats are your source material. Your notes are where you add meaning, and links tie the two together.

---

## Step 5: Keep Everything on Your Computer

Your saved chats aren't sent to our servers. Obsidian, by default, also works with files on your own drive. A few choices decide whether things stay that way.

- **Community plugins.** Obsidian starts with community plugins turned off, in what it calls Restricted mode. Some plugins connect to the internet. If you turn plugins on, read what each one does before you install it.
- **Sync services.** Obsidian offers an optional paid sync service. If you use it, or put your vault in a cloud-synced folder such as OneDrive, a copy of your files is stored by that service under its own policies.
- **Backups.** A vault is just a folder. Back it up the same way you back up your Library folder, such as copying it to an external drive.

If you want everything local, leave plugins off, skip sync, and keep the vault outside any cloud-synced folder.

**Takeaway:** Obsidian's defaults keep files local. Plugins and sync are choices you make on purpose.

---

## Common Mistakes to Avoid

- **Editing original chats.** Write notes in separate files and link to the chat instead.
- **Moving the Library folder without updating the save path.** New chats keep going to the old location.
- **Opening the same folder as two different vaults.** It works, but settings get confusing. Pick one.
- **Installing plugins without checking them.** Some send data online. Read before you enable.
- **Copying chats and then forgetting which copy is current.** If you use Option C, treat the Library folder as the original.

---

## Common Questions

### Do I need TotalRecalls open to read chats in Obsidian?

No. Your saved conversations are standard Markdown files. Obsidian reads them whether TotalRecalls is open or not.

### Will Obsidian change my saved conversation files?

Not unless you edit them. Opening, reading, and searching don't change your files. Obsidian does add a hidden `.obsidian` settings folder to the vault.

### Can I open chats from every provider in one vault?

Yes. Each provider has its own subfolder, and Obsidian shows them all together. On the Free Tier, that's ChatGPT, Claude, and Perplexity. Pro adds Gemini, Grok, DeepSeek, Mistral, and Qwen.

### What about the JSON files?

They stay in your Library folder for scripts, tools, or anything that needs structured data. Obsidian hides them by default, so you only see the readable Markdown version.

### Do I have to use Obsidian?

No. Your files open in Notepad, VS Code, Typora, or any text editor. Obsidian is one good option for reading and linking chats, not a requirement.

### Does this work on Mac or Linux?

TotalRecalls runs on Windows 10 and 11. macOS and Linux versions are in development.

---

## The Recommendation for Most People

**Start simple.** Open your Library folder as its own vault. You can always reorganize later.

**Read, don't rewrite.** Use reading view for saved chats, and keep the originals unchanged.

**Add your own layer.** Create a `Notes` folder, write short notes about what you decided or learned, and link each one to the conversation behind it.

---

## Your Chats, Connected to Your Thinking

Saving your AI conversations as files means they belong to you. Searching them means you can find them. Opening them in Obsidian means you can build on them, linking one answer to the next and turning scattered chats into notes you'll actually return to.

Open your Library folder in Obsidian, pick one conversation that mattered, and write a short note that links back to it. That's the whole habit.

If you haven't tried TotalRecalls yet, the Free Tier covers ChatGPT, Claude, and Perplexity on Windows 10 and 11. You can save your first conversations in minutes and open them in Obsidian the same day.

**Download free at totalrecalls.app.**
