**Meta title:** How to Manage Your Saved AI Chats with PowerShell (Windows)

**Meta description:** Your saved AI conversations are plain files, so PowerShell can count, search, check, and index them. Here are safe, copy-and-paste commands for Windows 10 and 11.

---

# How to Manage Your Saved AI Chats with PowerShell

Over the last few posts, your Library folder has grown into something useful. You can search it, read it in Obsidian, work with it in VS Code, and back it up. As it grows, a new set of questions appears. How many chats have you saved? Which ones came from Claude last month? Is every Markdown file paired with its JSON file?

You could answer those by clicking through folders. PowerShell answers them in seconds.

PowerShell is a command tool that comes with Windows 10 and 11. You don't need to install anything, and you don't need to be a programmer. You type a command, press Enter, and read the result. Your saved chats are ordinary files, so PowerShell can work with them directly.

This post shows you how to manage your saved AI conversations with PowerShell on Windows. It takes about eight minutes to read. You'll learn:

- How to open PowerShell in your Library folder
- How to count, list, and find chats by provider or date
- How to search inside every conversation at once
- How to check your Library for missing or duplicate files
- How to build a simple index you can open in Excel, and refresh it on a schedule

---

## The Short Answer

The whole idea fits in three points:

- **PowerShell is already on your PC.** Open it, point it at your Library folder, and start with simple commands.
- **Most useful commands only read.** Counting, listing, searching, and checking don't change your files.
- **Save what you use often as a script.** A short script can build an index of every chat, and Task Scheduler can run it for you.

**Takeaway:** Start by typing one command at a time. Turn the ones you like into a script later.

---

## Which Tool for Which Job

PowerShell doesn't replace the tools from earlier posts. It fills a different gap.

| Task                           | **File Explorer** | **Obsidian** | **VS Code** | **PowerShell**           |
| ------------------------------ | ----------------- | ------------ | ----------- | ------------------------ |
| **Read one chat**              | Good              | Best         | Good        | Not ideal                |
| **Search for a phrase**        | Good              | Good         | Very good   | Very good                |
| **Link chats to notes**        | No                | Best         | Basic       | No                       |
| **Count chats by provider**    | Manual            | No           | No          | Best                     |
| **Check for missing files**    | Manual            | No           | No          | Best                     |
| **Build a list of every chat** | No                | No           | No          | Best                     |
| **Run on a schedule**          | No                | No           | No          | Yes, with Task Scheduler |

**Takeaway:** Use PowerShell for questions about your whole Library, not for reading individual chats.

---

## Before You Start

You need three things:

1. **Some saved conversations.** The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini, Grok, DeepSeek, Mistral, and Qwen.
2. **Windows PowerShell.** It's built into Windows 10 and 11. Every command in this post also works in PowerShell 7 if you've installed it.
3. **Your Library folder location.** By default, that's:

```
C:\TotalRecalls\Library\
```

If your Library lives somewhere else, swap in your own path wherever you see `C:\TotalRecalls\Library`.

### A Safe Habit Before You Begin

Make a backup first. If you followed Blog 8, you already have one. Almost every command here only reads files, but a fresh backup means you can experiment without worry.

**Takeaway:** Nothing to install. Just know your folder path and have a backup in place.

---

## Step 1: Open PowerShell in Your Library Folder

There are a few ways to open PowerShell. Pick whichever feels easiest.

| Method                     | How                                                                                             |
| -------------------------- | ----------------------------------------------------------------------------------------------- |
| **Start menu**             | Search for **PowerShell** and open **Windows PowerShell**                                       |
| **Windows 11 Terminal**    | Right-click the Start button and choose **Terminal**                                            |
| **From the folder itself** | Open the Library folder in File Explorer, type `powershell` in the address bar, and press Enter |
| **Windows 11 right-click** | Right-click inside the Library folder and choose **Open in Terminal**                           |

If you opened PowerShell from the Start menu, move into your Library folder with this command:

```
Set-Location "C:\TotalRecalls\Library"
```

The line before your cursor should now end with `C:\TotalRecalls\Library>`. That tells you where PowerShell is working.

You don't need to run PowerShell as an administrator for anything in this post. A normal window is safer.

**Takeaway:** Open PowerShell, move into your Library folder, and you're ready.

---

## Step 2: Count and List Your Saved Chats

Start with simple questions. Each command below only reads your files.

### How Many Chats Have You Saved?

Each conversation has one Markdown file, so counting `.md` files counts your chats:

```
(Get-ChildItem -Recurse -Filter *.md).Count
```

`-Recurse` tells PowerShell to look inside every provider subfolder.

### How Many from Each Provider?

```
Get-ChildItem -Directory | ForEach-Object {
  [PSCustomObject]@{
    Provider = $_.Name
    Chats    = (Get-ChildItem $_.FullName -Filter *.md).Count
  }
}
```

You'll see a small table, something like this:

```
Provider   Chats
--------   -----
chatgpt       42
claude        27
perplexity    11
```

### Your Most Recent Chats

Filenames start with a date, so sorting by name puts them in date order:

```
Get-ChildItem -Recurse -Filter *.md |
  Sort-Object Name -Descending |
  Select-Object -First 10 Name, @{Name='Provider'; Expression={$_.Directory.Name}}
```

### Chats from a Specific Month

```
Get-ChildItem -Recurse -Filter "2026-09-*.md"
```

Change `2026-09` to any year and month you want.

### How Much Space Your Library Uses

```
"{0:N1} MB" -f ((Get-ChildItem -Recurse -File | Measure-Object Length -Sum).Sum / 1MB)
```

For most people, the answer is surprisingly small, because Markdown and JSON are plain text.

### Quick Reference

| Question                       | Command                                                                  |
| ------------------------------ | ------------------------------------------------------------------------ |
| Total chats                    | `(Get-ChildItem -Recurse -Filter *.md).Count`                            |
| Claude chats only              | `(Get-ChildItem .\claude -Filter *.md).Count`                            |
| Chats from one month           | `Get-ChildItem -Recurse -Filter "2026-09-*.md"`                          |
| Chats with a word in the title | `Get-ChildItem -Recurse -Filter "*pricing*.md"`                          |
| Library size                   | `(Get-ChildItem -Recurse -File \| Measure-Object Length -Sum).Sum / 1MB` |

**Takeaway:** A handful of short commands tells you more about your Library than an hour of clicking.

---

## Step 3: Search Inside Every Conversation

`Select-String` searches the text inside files. Think of it as Find for your whole Library.

### Search for a Word or Phrase

```
Get-ChildItem -Recurse -Filter *.md |
  Select-String -Pattern "renewal rate" -SimpleMatch
```

Each result shows the file, the line number, and the line itself. `-SimpleMatch` means PowerShell searches for exactly what you typed, so symbols like `.` or `?` don't cause surprises.

### List Each Matching Chat Once

A long chat might mention a word dozens of times. To see each file only once:

```
Get-ChildItem -Recurse -Filter *.md |
  Select-String -Pattern "budget" -SimpleMatch -List |
  Select-Object Filename, LineNumber
```

### Search One Provider

```
Select-String -Path ".\claude\*.md" -Pattern "budget" -SimpleMatch -List
```

### Open the Matches in Notepad

Once you've found what you need, open the matching chats directly:

```
Get-ChildItem -Recurse -Filter *.md |
  Select-String -Pattern "invoice template" -SimpleMatch -List |
  ForEach-Object { notepad $_.Path }
```

Use a specific phrase here. A common word could open dozens of Notepad windows at once.

### Search Options at a Glance

| What You Want                          | Add This                                           |
| -------------------------------------- | -------------------------------------------------- |
| Exact text, no pattern matching        | `-SimpleMatch`                                     |
| One result per file                    | `-List`                                            |
| Match exact capital letters            | `-CaseSensitive`                                   |
| Show lines around each match           | `-Context 1,2` (1 line before, 2 after)            |
| Find files that don't contain the word | `-NotMatch` (works line by line, so use with care) |

PowerShell ignores capital letters by default, so `Budget` and `budget` both match.

If accented letters or symbols look garbled in your results, add `-Encoding UTF8` to the `Select-String` command.

**Takeaway:** `Select-String` with `-SimpleMatch -List` is the fastest way to find which chats mention something.

---

## Step 4: Check Your Library for Problems

As your Library grows, small problems can creep in. A file gets moved, or a chat gets saved twice. These checks find them. None of them change anything.

### Find Markdown Files Without a JSON Partner

```
Get-ChildItem -Recurse -Filter *.md | Where-Object {
  -not (Test-Path ($_.FullName -replace '\.md$', '.json'))
} | Select-Object FullName
```

If nothing appears, every chat has both files. You can reverse the check by swapping `.md` and `.json`.

### Find Exact Duplicates

This compares file contents, not names, so it catches copies with different filenames:

```
Get-ChildItem -Recurse -Filter *.md |
  Get-FileHash |
  Group-Object Hash |
  Where-Object Count -gt 1 |
  ForEach-Object { $_.Group.Path; "" }
```

Each group of paths is a set of identical files, with a blank line between groups.

### Find Empty or Very Small Files

```
Get-ChildItem -Recurse -File | Where-Object Length -lt 200 |
  Select-Object FullName, Length
```

A very small file may point to a download that didn't finish. Open it in Notepad to check, then save that conversation again in TotalRecalls if needed.

### Find Stray Files

```
Get-ChildItem -Recurse -File |
  Where-Object { $_.Extension -notin '.md', '.json' } |
  Select-Object FullName
```

This lists anything that isn't a saved chat, such as a note you dropped in by mistake. Obsidian's hidden `.obsidian` folder won't appear unless you add `-Force`.

### If You Decide to Remove Something

Delete files in File Explorer, so they go to the Recycle Bin. If you ever use `Remove-Item` in PowerShell, add `-WhatIf` first. It shows what would happen without doing it:

```
Remove-Item ".\chatgpt\2026-09-14-pricing-research-copy.md" -WhatIf
```

Files deleted with `Remove-Item` skip the Recycle Bin.

**Takeaway:** Run these checks every few months. They take seconds and keep your Library tidy.

---

## Step 5: Peek Inside a JSON File

The JSON file holds the same conversation as the Markdown file, in a structured format. PowerShell can read it as data.

```
$chat = Get-Content ".\chatgpt\2026-09-14-pricing-research.json" -Raw -Encoding UTF8 |
  ConvertFrom-Json
```

Nothing appears yet, because the result is stored in `$chat`. To see the top-level fields:

```
$chat | Get-Member -MemberType NoteProperty
```

To see the structure in a readable layout:

```
$chat | ConvertTo-Json -Depth 4 | more
```

Press the spacebar to page through, or **Q** to stop.

Take a few minutes to look at how the data is laid out before you write anything that depends on it. Field names may differ between providers, so check one file from each provider you use. If you only want lists, counts, and searches, the Markdown files are all you need.

**Takeaway:** `ConvertFrom-Json` turns a saved chat into data you can explore. Look before you build.

---

## Step 6: Build an Index of Every Chat

This is where PowerShell earns its place. A short script can create a spreadsheet listing every saved conversation, with its date, provider, and title.

### Create the Script

1. Create a folder for your scripts, such as `C:\Users\YourName\Documents\Scripts`.
2. Open **Notepad** and paste this:

```
$library = "C:\TotalRecalls\Library"
$output  = "$env:USERPROFILE\Documents\TotalRecalls-index.csv"

Get-ChildItem -Path $library -Recurse -Filter *.md |
  ForEach-Object {
    $date  = ""
    $title = $_.BaseName
    if ($_.BaseName -match '^(\d{4}-\d{2}-\d{2})-(.+)$') {
      $date  = $Matches[1]
      $title = $Matches[2] -replace '-', ' '
    }
    [PSCustomObject]@{
      Date     = $date
      Provider = $_.Directory.Name
      Title    = $title
      SizeKB   = [math]::Round($_.Length / 1KB, 1)
      Path     = $_.FullName
    }
  } |
  Sort-Object Date -Descending |
  Export-Csv -Path $output -NoTypeInformation -Encoding UTF8
```

3. Choose **File → Save As**.
4. Set **Save as type** to **All files**.
5. Name it `build-index.ps1` and save it in your Scripts folder.

The script saves the index in your Documents folder, not inside the Library. That keeps your Library holding only saved chats.

### What Each Part Does

| Part                                  | What It Does                                          |
| ------------------------------------- | ----------------------------------------------------- |
| `$library` and `$output`              | Where to read chats from, and where to save the index |
| `Get-ChildItem ... -Filter *.md`      | Finds every saved chat across all providers           |
| `-match '^(\d{4}-\d{2}-\d{2})-(.+)$'` | Splits a filename into its date and title             |
| `-replace '-', ' '`                   | Turns `pricing-research` into `pricing research`      |
| `[PSCustomObject]@{ ... }`            | Builds one row per chat                               |
| `Sort-Object Date -Descending`        | Puts the newest chats first                           |
| `Export-Csv ... -Encoding UTF8`       | Saves a file Excel can open, with characters intact   |

### Run the Script

Windows blocks scripts by default on most PCs. The simplest way to run this one without changing any settings:

```
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\Documents\Scripts\build-index.ps1"
```

This allows the script for this one run only.

If you plan to run your own scripts often, you can allow them for your user account instead:

```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

After that, you can run the script by typing its path. `RemoteSigned` still blocks unsigned scripts downloaded from the internet, which is a sensible middle ground.

### Open the Index

Double-click `TotalRecalls-index.csv` in your Documents folder. It opens in Excel, or in any spreadsheet app. You can sort by provider, filter by month, or search titles. Copy a path from the **Path** column into File Explorer's address bar to open that chat.

**Takeaway:** One short script gives you a sortable list of every conversation you've saved.

---

## Step 7: Refresh the Index on a Schedule

Your index only knows about chats that existed when it ran. Task Scheduler can rerun it for you.

1. Search for **Task Scheduler** in the Start menu and open it.
2. Click **Create Basic Task**.
3. Name it `Refresh TotalRecalls index` and click **Next**.
4. Choose how often to run it, such as **Weekly**, and pick a day and time.
5. Choose **Start a program** and click **Next**.
6. In **Program/script**, type:

```
powershell.exe
```

7. In **Add arguments**, type this, with your own username:

```
-NoProfile -ExecutionPolicy Bypass -File "C:\Users\YourName\Documents\Scripts\build-index.ps1"
```

8. Click **Next**, then **Finish**.

To test it, find the task in the Task Scheduler Library, right-click it, and choose **Run**. Check that the date on `TotalRecalls-index.csv` has updated.

If the CSV is open in Excel when the task runs, the update will fail. Close it first, or schedule the task for a time you're usually away.

**Takeaway:** Schedule the index once, and it stays current without you thinking about it.

---

## Common Mistakes to Avoid

- **Running PowerShell as administrator when you don't need to.** A normal window is enough for everything here, and it's safer.
- **Using `Remove-Item` without `-WhatIf`.** Deleted files skip the Recycle Bin. Delete in File Explorer instead.
- **Saving scripts or the index inside the Library folder.** Keep them in Documents, so your Library holds only saved chats.
- **Forgetting to save as "All files" in Notepad.** Otherwise your script becomes `build-index.ps1.txt` and won't run.
- **Assuming every JSON file looks the same.** Check one from each provider before building anything on top of them.
- **Copying scripts from the internet without reading them.** Only run commands you understand, especially ones that move or delete files.

---

## Common Questions

### Do I need to install anything?

No. Windows PowerShell comes with Windows 10 and 11. Every command here also works in PowerShell 7 if you prefer it.

### Will these commands change my saved chats?

The counting, listing, searching, checking, and JSON commands only read files. The index script creates one new file in your Documents folder and leaves your Library unchanged.

### Do I need TotalRecalls open?

No. Your saved conversations are standard files. PowerShell works with them whether TotalRecalls is open or not.

### What is the execution policy?

It's a Windows setting that controls whether scripts can run. It's there to prevent scripts from running by accident. Typing commands one at a time isn't affected. Only saved `.ps1` files are.

### Does PowerShell send my chats anywhere?

The commands in this post work entirely on your PC. Your saved conversations aren't sent to our servers, and nothing here uploads them anywhere.

### Is this hard if I've never used a command line?

Not for these tasks. Copy a command, paste it with a right-click or **Ctrl + V**, press Enter, and read the result. If something goes wrong, PowerShell shows a red error message and your files stay as they were.

### Does this work on Mac or Linux?

TotalRecalls runs on Windows 10 and 11. macOS and Linux versions are in development.

---

## The Recommendation for Most People

**Try three commands today.** Count your chats, count them by provider, and search for one phrase with `Select-String`. That's enough to see what PowerShell can do.

**Run the checks every few months.** Missing pairs, duplicates, and tiny files take seconds to find.

**Build the index once, then schedule it.** A weekly refresh gives you a current list of every conversation, ready to sort and filter in Excel.

---

## Your Library, Seen All at Once

Saving your AI conversations as files means they belong to you. Searching, linking, reusing, and backing them up keeps them useful and safe. PowerShell adds one more thing: a clear view of everything you've saved, in a few lines of text.

Open PowerShell in your Library folder, type `(Get-ChildItem -Recurse -Filter *.md).Count`, and press Enter. The number you see is your personal archive of AI answers, kept on your own drive.

If you haven't tried TotalRecalls yet, the Free Tier covers ChatGPT, Claude, and Perplexity on Windows 10 and 11. Pro adds Gemini, Grok, DeepSeek, Mistral, and Qwen. You can save your first conversations in minutes and start organizing them with PowerShell the same day.

**Download free at totalrecalls.app.**
