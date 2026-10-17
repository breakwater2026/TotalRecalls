**Meta title:** How to Back Up Your Saved AI Chats on Windows 10 and 11

**Meta description:** Your saved AI conversations are files on your PC, so you can back them up like any other files. Here are four simple ways to keep them safe on Windows.

---

# How to Back Up Your Saved AI Conversations on Windows

Over the last few posts, your Library folder has become more useful. You can search it, open it in Obsidian, and link chats to your own notes. That also makes it worth protecting.

Saving conversations to your PC means they belong to you. It also means your drive is now the only place they live. If that drive fails, or a folder gets deleted by mistake, those chats go with it. A good backup fixes that.

The good news is that your saved chats are ordinary Markdown and JSON files. You don't need special software to protect them. Windows already has everything you need.

This post shows you how to back up your saved AI conversations on Windows 10 and 11. It takes about seven minutes to read. You'll learn:

- What to back up, and where it lives
- Four backup methods, from a one-time copy to a fully automatic schedule
- How to restore a chat when you need it
- How to choose the right method for how you work

---

## The Short Answer

The whole idea fits in three points:

- **Back up the whole Library folder.** It holds every saved conversation, from every provider, in one place.
- **Keep at least one copy off your PC.** An external drive is the simplest choice. A cloud folder works too.
- **Make it automatic.** File History or a scheduled copy means you never have to remember.

**Takeaway:** Turn on File History with an external drive, include your Library folder, and let Windows handle the rest.

---

## What to Back Up

Everything you need is in one folder. By default, that's:

```
C:\TotalRecalls\Library\
```

Inside, each provider has its own subfolder, and each conversation is saved as a Markdown file and a JSON file:

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

On the Free Tier, you'll see folders for ChatGPT, Claude, and Perplexity. Pro adds Gemini, Grok, DeepSeek, Mistral, and Qwen. However many providers you use, backing up the Library folder covers all of them.

### Keep Both File Types

It's tempting to back up only the Markdown files, since those are the ones you read. Keep the JSON files too. They hold the same conversation in a structured format that's useful for scripts and other tools. They're small, so including them costs almost nothing.

### Don't Forget Your Own Notes

If you followed Blog 7 and keep notes in an Obsidian vault, back up the vault folder as well. If your Library folder sits inside that vault, one backup covers both.

**Takeaway:** Back up the full Library folder, both file types, and any notes folder that links to it.

---

## Method 1: Copy the Folder to an External Drive

This is the quickest way to make your first backup. It takes a few minutes and needs nothing but a USB drive.

1. Plug in an external drive or USB stick.
2. Open File Explorer and go to `C:\TotalRecalls\`.
3. Right-click the **Library** folder and choose **Copy**.
4. Open your external drive.
5. Create a folder with a clear name, such as `TotalRecalls Backup 2026-10-02`.
6. Open that folder, right-click, and choose **Paste**.

Putting the date in the folder name makes it easy to tell backups apart later.

### Make a Zip Archive Instead

If you'd rather keep a single file, compress the folder first:

- **Windows 11:** Right-click the Library folder and choose **Compress to ZIP file**.
- **Windows 10:** Right-click the Library folder and choose **Send to → Compressed (zipped) folder**.

Then copy the zip file to your external drive. Remember that Windows can't reliably search inside zip files, so you'll need to extract one before searching it.

**Takeaway:** A manual copy is perfect for a first backup. The downside is that it only protects what you've saved so far.

---

## Method 2: Turn On File History

File History is built into Windows 10 and 11. It copies your files to an external drive on a schedule and keeps older versions, so you can go back to an earlier copy of a file. For most people, this is the best long-term option.

### On Windows 10

1. Plug in your external drive.
2. Open **Settings → Update & Security → Backup**.
3. Under **Back up using File History**, click **Add a drive** and choose your external drive.
4. Click **More options**.
5. Under **Back up these folders**, click **Add a folder**.
6. Select `C:\TotalRecalls\Library` and click **Choose this folder**.
7. Set **Back up my files** to a schedule that suits you, such as every hour or daily.

### On Windows 11

File History in Windows 11 lives in Control Panel, and it backs up your Windows libraries rather than any folder you pick. You add your Library folder to a Windows library first, then turn File History on.

**Add your Library folder to a Windows library:**

1. Open File Explorer.
2. In the left-hand panel, right-click an empty area and choose **Show libraries**.
3. Find `C:\TotalRecalls\Library`, right-click it, and choose **Include in library → Documents**.

**Turn on File History:**

1. Plug in your external drive.
2. Search for **File History** in the Start menu and open it.
3. Choose your external drive if it isn't already selected.
4. Click **Turn on**.
5. Open **Advanced settings** to choose how often it saves copies and how long it keeps them.

Your files stay where they are. Including the folder in a library only tells Windows to back it up.

### A Note on "Windows Backup" in Windows 11

Windows 11 also has an app called **Windows Backup**. It mainly backs up folders like Desktop, Documents, and Pictures to OneDrive. It doesn't cover `C:\TotalRecalls\Library` on its own, so don't rely on it for your saved chats unless you move them into one of those folders.

**Takeaway:** File History runs in the background and keeps older versions. Set it up once and it keeps working.

---

## Method 3: Use a Cloud-Synced Folder

If you already use OneDrive, Dropbox, or Google Drive on your PC, you can keep a copy of your Library folder inside it. The sync app then uploads it for you.

1. Open your cloud folder in File Explorer, such as `C:\Users\YourName\OneDrive`.
2. Create a folder called `TotalRecalls Backup`.
3. Copy your Library folder into it.

You could also move the Library folder into your cloud folder completely. If you do, check whether TotalRecalls lets you choose a save location, and point it at the new path. Otherwise, new chats keep going to the old folder.

### Think About Privacy First

Your conversations aren't sent to our servers when you save them. A cloud folder is different. Once your chats are inside one, that service stores a copy under its own policies. If some conversations are sensitive, an external drive may be the better choice.

### Sync Isn't Quite a Backup

Sync copies changes in both directions. If you delete a file on your PC, the sync service usually deletes it in the cloud too. Most services keep deleted files for a limited time, but a separate copy on an external drive gives you a safer fallback.

**Takeaway:** Cloud folders are convenient and protect you if your PC is lost. Weigh the privacy trade-off, and don't treat sync as your only backup.

---

## Method 4: Schedule a Copy with Robocopy

Robocopy is a copy tool built into Windows. It only copies new or changed files, so repeat backups are fast. Pair it with Task Scheduler and it runs automatically. This method suits people who are comfortable with a short command.

### Create the Backup File

1. Open **Notepad**.
2. Paste this line, changing `E:` to your external drive's letter:

```
robocopy "C:\TotalRecalls\Library" "E:\TotalRecalls Backup\Library" /E /XO /R:1 /W:1
```

3. Choose **File → Save As**.
4. Set **Save as type** to **All files**.
5. Name the file `backup-library.bat` and save it somewhere easy to find, such as `C:\TotalRecalls\`.

Here's what each part does:

| Part                               | What It Does                                                               |
| ---------------------------------- | -------------------------------------------------------------------------- |
| `"C:\TotalRecalls\Library"`        | The folder to copy from                                                    |
| `"E:\TotalRecalls Backup\Library"` | The folder to copy to                                                      |
| `/E`                               | Includes every subfolder, so all providers are covered                     |
| `/XO`                              | Skips files that are already up to date in the backup                      |
| `/R:1 /W:1`                        | Retries a busy file once, after one second, instead of waiting a long time |

Double-click the file to test it. A window opens, lists the copied files, and closes when it's done.

### Avoid /MIR Unless You Mean It

You may see guides that use `/MIR`. It makes the backup an exact mirror, which means files you delete on your PC are also deleted from the backup. For saved conversations, the safer choice is `/E`, which only adds and updates.

### Run It on a Schedule

1. Search for **Task Scheduler** in the Start menu and open it.
2. Click **Create Basic Task**.
3. Name it `Back up TotalRecalls Library` and click **Next**.
4. Choose how often to run it, such as **Weekly**, and pick a day and time.
5. Choose **Start a program**.
6. Click **Browse**, select `backup-library.bat`, and click **Finish**.

Make sure the external drive is plugged in at the scheduled time, and that Windows gives it the same drive letter each time.

**Takeaway:** Robocopy plus Task Scheduler gives you a fast, automatic copy with full control over where it goes.

---

## Backup Methods Side by Side

|                                           | **Manual Copy**                        | **File History**                       | **Cloud Folder**                   | **Robocopy + Task Scheduler**          |
| ----------------------------------------- | -------------------------------------- | -------------------------------------- | ---------------------------------- | -------------------------------------- |
| **Setup effort**                          | Lowest                                 | Low                                    | Low                                | Medium                                 |
| **Runs automatically?**                   | No                                     | Yes                                    | Yes                                | Yes                                    |
| **Keeps older versions?**                 | Only if you make dated copies          | Yes                                    | Limited, depends on the service    | No                                     |
| **Protects against a lost or stolen PC?** | Yes, if the drive is stored separately | Yes, if the drive is stored separately | Yes                                | Yes, if the drive is stored separately |
| **Copy stays off the internet?**          | Yes                                    | Yes, with an external drive            | No                                 | Yes, with an external drive            |
| **Needs a drive plugged in?**             | Only while copying                     | Yes, for each backup                   | No                                 | Yes, at the scheduled time             |
| **Best for**                              | A quick first backup                   | Most people                            | People already using cloud storage | People who like control                |

You don't have to pick just one. A strong setup for many people is File History to an external drive, plus an occasional dated zip stored somewhere else.

**Takeaway:** File History is the best default. Add a second copy in a different place if your chats really matter to you.

---

## How to Restore a Saved Chat

A backup is only useful if you can get files back. Try a restore once, so you know it works before you need it.

### From a Manual Copy or Robocopy Backup

1. Open the backup folder on your external drive.
2. Find the provider subfolder, such as `claude`.
3. Copy the `.md` and `.json` files you need.
4. Paste them back into the same subfolder in `C:\TotalRecalls\Library\`.

### From File History

1. Plug in the drive File History uses.
2. Open File Explorer and go to `C:\TotalRecalls\Library\`.
3. Right-click the provider subfolder and choose **Properties**.
4. Open the **Previous Versions** tab.
5. Pick a date, then click **Restore** or **Open** to choose specific files.

You can also search for **Restore your files with File History** in the Start menu. It opens a window where you can browse back through dates using the arrow buttons.

### From a Cloud Folder

Copy the files from your cloud folder back into your Library folder. If a file was deleted, check your cloud service's recycle bin or deleted files page.

**Takeaway:** Restoring is just copying files back to the right provider subfolder. Test it once so you're confident.

---

## Common Mistakes to Avoid

- **Backing up to the same drive.** A copy on `C:` doesn't help if `C:` fails. Use an external drive or the cloud.
- **Leaving the backup drive plugged in all the time.** Unplug it between backups, or at least store it away from your PC, so one problem can't affect both.
- **Using /MIR without thinking.** It deletes backup files when you delete originals.
- **Moving the Library folder without updating the save path.** New chats keep going to the old location and miss the backup.
- **Never testing a restore.** Check once that you can open a backed-up chat.

---

## Common Questions

### How often should I back up my saved chats?

It depends on how often you save new conversations. If you save chats most days, a daily or hourly File History schedule makes sense. If you save a few a month, a weekly backup is plenty.

### How much space do I need?

Not much. Markdown and JSON are plain text, so even hundreds of conversations usually take up very little room. A small USB stick is often enough.

### Do I need TotalRecalls open to back up my chats?

No. Your saved conversations are standard files. Windows can copy and back them up whether TotalRecalls is open or not.

### Can I open my backups on another PC?

Yes. The files open in Notepad, VS Code, Obsidian, or any text editor. You don't need TotalRecalls installed to read them.

### Should I encrypt my backup drive?

If your chats contain sensitive information, it's a good idea. BitLocker To Go is built into Windows 10 and 11 Pro, Enterprise, and Education editions. Right-click the drive in File Explorer and look for **Turn on BitLocker**. Windows Home doesn't include it, so you'd need a drive with its own encryption or a third-party tool.

### Does backing up send my conversations anywhere?

Backing up to an external drive keeps everything on hardware you own. Your conversations aren't sent to our servers when you save them. If you back up to a cloud folder, that service stores a copy under its own policies.

### Does this work on Mac or Linux?

TotalRecalls runs on Windows 10 and 11. macOS and Linux versions are in development.

---

## The Recommendation for Most People

**Make one copy today.** Copy your Library folder to a USB drive, with the date in the folder name. It takes five minutes.

**Set up File History this week.** Point it at an external drive and include your Library folder. After that, backups happen without you thinking about them.

**Keep a second copy somewhere else.** Every few months, make a dated zip and store it on a different drive or in the cloud.

---

## Your Chats, Kept Safe

Saving your AI conversations as files gives you ownership. Searching and linking them makes them useful. Backing them up makes sure all that work is still there next year, whatever happens to your PC.

Start small. Plug in a drive, copy your Library folder, and open one backed-up chat to check it's readable. Then turn on File History and let Windows do the rest.

If you haven't tried TotalRecalls yet, the Free Tier covers ChatGPT, Claude, and Perplexity on Windows 10 and 11. Pro adds Gemini, Grok, DeepSeek, Mistral, and Qwen. You can save your first conversations in minutes and back them up the same day.

**Download free at totalrecalls.app.**
