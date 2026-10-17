**Meta title:** How to Back Up Your AI Conversation Library

**Meta description:** Your saved AI chats are only as safe as the PC they're on. Here's how to back up your TotalRecalls Library folder, step by step.

---

# How to Back Up Your AI Conversation Library

When you save a conversation with TotalRecalls, it lands in your Library folder as a Markdown file and a JSON file. Those files live on your PC, which means you control them. It also means they're only as safe as that one computer.

A hard drive can fail. A laptop can be lost or replaced. A backup means none of that costs you the conversations you chose to keep.

This post shows you how to back up your AI conversation library in plain steps. It takes about six minutes to read. You'll learn:

- What to back up, and what you can skip
- Four simple backup methods, with the tradeoffs of each
- How often to back up, and how to check that it worked

---

## The Short Answer

The whole idea fits in three points:

- **Back up the entire Library folder.** It holds every saved conversation, in both formats, organized by provider.
- **Keep at least one copy off your PC.** An external drive is the simplest choice. A cloud folder works too, if you're comfortable storing your chats with that service.
- **Repeat it regularly.** Back up after a big download session, and on a set schedule, such as once a month.

**Takeaway:** Copy the whole Library folder to a second place, and do it on a schedule you'll actually keep.

---

## What to Back Up

Your Library folder is the only thing you need to protect. Inside it, each provider has its own subfolder:

```
Library
├── chatgpt
├── claude
└── perplexity
```

Every conversation sits inside as a pair of files, one `.md` and one `.json`. Back up both. The Markdown file is what you'll read later. The JSON file is what you'll need if you ever import your chats into another tool.

### A Few Extras Worth Keeping

**Your Pro license details.** If you use Pro, store your license key and order email somewhere safe, such as a password manager. Pro activates on up to three PCs, so you'll want the key handy when you set up a new computer.

**Gemini Takeout files.** On Pro, Gemini conversations come through a Google Takeout file. TotalRecalls converts it into Markdown and JSON files in your Library folder. Keeping the original Takeout file is optional, but it gives you a second source if you ever want to convert it again.

### What You Can Skip

You don't need to back up the TotalRecalls app itself. You can download it again from totalrecalls.app at any time. Your conversations are what matter, and they're all in the Library folder.

**Takeaway:** Back up the Library folder. Keep your license key safe. Everything else can be replaced.

---

## Four Ways to Back Up Your Library Folder

There's no single right method. The best one is the one that fits how you already use your PC. Here are four options, from most hands-on to most automatic.

### 1. Copy It to an External Drive

This is the simplest backup and the easiest to understand.

1. Plug in a USB flash drive or external hard drive.
2. Open File Explorer and find your Library folder.
3. Copy the whole folder onto the drive.
4. When the copy finishes, safely eject the drive.

For example, you might keep a small USB drive in a desk drawer. Once a month, you plug it in, copy the Library folder over the old copy, and put the drive away.

**Tradeoff:** It only happens when you remember to do it.

### 2. Use Windows File History

Windows 10 and 11 both include File History, a built-in tool that backs up files to an external drive on a schedule.

1. Connect an external drive.
2. Search for "File History" in the Start menu and open it.
3. Turn it on and choose your drive.
4. Check which folders it covers.

File History focuses on standard folders, such as Documents. If your Library folder sits somewhere else, make sure it's included, or it won't be backed up.

**Tradeoff:** It runs automatically, but only while the drive is connected.

### 3. Keep a Copy in a Cloud Folder

You can copy your Library folder into OneDrive, Dropbox, Google Drive, or a similar service. Your files then live on that service's servers as well as your PC.

This protects your chats if your computer and drive are both lost. Before you do it, though, make a deliberate choice. Your conversations aren't sent to our servers, but a cloud service will store whatever you place in its folder, under its own policies.

**Tradeoff:** Strong protection against losing your PC, but your files no longer stay only on your computer.

### 4. Make a Dated Zip Archive

A zip file bundles your whole Library folder into one compressed file.

1. Right-click your Library folder in File Explorer.
2. Choose the option to compress it to a zip file.
3. Rename it with the date, such as `library-backup-2026-10.zip`.
4. Move the zip file to an external drive or another safe location.

Dated archives give you snapshots over time. If you delete or edit a file by mistake, you can open an older archive and recover it.

**Tradeoff:** Tidy and easy to store, but each archive is a manual step.

**Takeaway:** Pick one method to start. You can always add a second one later.

---

## Backup Methods Side by Side

|                                                   | **External Drive Copy** | **File History**              | **Cloud Folder**         | **Zip Archive**           |
| ------------------------------------------------- | ----------------------- | ----------------------------- | ------------------------ | ------------------------- |
| **Effort**                                        | Low, but manual         | Set once, then automatic      | Set once, then automatic | Low, but manual           |
| **Runs on its own?**                              | No                      | Yes, with the drive connected | Yes                      | No                        |
| **Files stay off the cloud?**                     | Yes                     | Yes                           | No                       | Yes, if stored locally    |
| **Protects against PC failure**                   | Yes                     | Yes                           | Yes                      | Yes, if stored off the PC |
| **Protects against losing PC and drive together** | No                      | No                            | Yes                      | Only if stored elsewhere  |
| **Keeps older versions**                          | No                      | Yes                           | Depends on the service   | Yes, one per archive      |
| **Built into Windows**                            | Yes                     | Yes                           | No                       | Yes                       |

**Takeaway:** For most people, an external drive covers the basics. Add a cloud folder or a second drive if you want protection beyond your home or office.

---

## How Often to Back Up

The right schedule depends on how often you save new conversations. Here's a simple guide:

| How You Use TotalRecalls                 | Suggested Backup Schedule       |
| ---------------------------------------- | ------------------------------- |
| You save a few chats now and then        | Once a month                    |
| You save conversations every week        | Every week or two               |
| You just finished a large download       | Right away                      |
| You're about to replace or reset your PC | Right away, then check the copy |

A good rule of thumb is this: back up whenever losing your new conversations would bother you. If you just saved six months of project chats, that's a good moment.

**Takeaway:** Match your backup schedule to how much you'd lose if your PC failed today.

---

## How to Check That Your Backup Worked

A backup you've never opened is a guess. Checking takes two minutes.

1. Open your backup location, whether it's a drive, cloud folder, or zip file.
2. Confirm each provider subfolder is there.
3. Open two or three `.md` files and read a few lines.
4. Open one `.json` file to make sure it isn't empty.

Because both formats are standard, you don't need TotalRecalls to open them. Notepad works for both.

**Takeaway:** Open a few files from every new backup. If you can read them, your backup works.

---

## Common Questions

### Does TotalRecalls back up my files automatically?

TotalRecalls saves your conversations into your Library folder. Backing up that folder is up to you, using any of the methods above.

### Can I restore my conversations on a new PC?

Yes. Copy your Library folder from the backup onto the new computer. The files open in Notepad, VS Code, or note-taking apps right away. If you use Pro, install TotalRecalls and enter your license key. Pro activates on up to three PCs.

### Isn't my provider already storing my chats?

Your original conversations stay with your provider, under that provider's own policies. Your Library folder holds your own copy. A backup protects that copy if something happens to your PC.

### Should I back up both the Markdown and JSON files?

Yes. They're small, and each serves a different purpose. Backing up the whole folder keeps both without any extra effort.

### Is it safe to keep backups on a USB drive?

It's as safe as the drive itself. If the drive could be lost, consider an encrypted one. Some editions of Windows include BitLocker To Go for encrypting removable drives.

### Does this work on Mac or Linux?

TotalRecalls runs on Windows 10 and 11. macOS and Linux versions are in development.

---

## The Recommendation for Most People

**Start with an external drive.** Copy your whole Library folder onto it today. It takes a few minutes and covers the most common risk, which is a failing or replaced PC.

**Put it on a schedule.** Set a monthly reminder, or turn on File History so it happens automatically. Back up right away after any big download session.

**Add a second location if your chats matter a lot.** A second drive kept somewhere else, or a cloud folder you've chosen on purpose, protects you if your PC and first drive are lost together.

---

## Your Chats, Kept Twice

Saving your AI conversations as files gives you control. Backing them up makes that control last. One copy on your PC and one somewhere else is all it takes.

Choose a method, copy your Library folder, and open a few files to check it worked. Then repeat it on a schedule you'll keep.

If you haven't tried TotalRecalls yet, the Free Tier covers ChatGPT, Claude, and Perplexity on Windows 10 and 11. You can save your first conversation in a few minutes, then back it up the same day.

**Download free at totalrecalls.app.**
