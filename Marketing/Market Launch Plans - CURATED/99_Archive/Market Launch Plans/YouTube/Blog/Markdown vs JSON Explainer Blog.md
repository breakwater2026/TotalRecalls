**Meta title:** Markdown vs JSON: Which Saved Chat File to Use

**Meta description:** TotalRecalls saves every AI conversation as a .md and a .json file. Here's what each one is for, and which one most people should open first.

---

# Markdown vs JSON: Which Saved File Should You Use?

Every conversation you download with TotalRecalls arrives as two files with the same name. One ends in `.md`, and the other ends in `.json`. If you've opened your Library folder and wondered why there are two, or which one to use, this post explains it.

This Markdown vs JSON guide takes about five minutes to read. It covers what each format is, what it's good for, and where it falls short. It ends with a simple recommendation for most people.

---

## The Short Answer

If you only remember one thing, make it this:

- **Markdown (`.md`) is for people.** Open it when you want to read, copy, or share a conversation.
- **JSON (`.json`) is for software.** Use it when a tool, script, or app needs to work with your conversations.

Both files hold the same conversation. They store it in two different shapes, for two different jobs.

**Takeaway:** If you're reading, open the `.md` file. If a program is reading, give it the `.json` file.

---

## Why TotalRecalls Saves Two Files

People save AI conversations for different reasons. Some want to reread a useful answer next month. Others want to load hundreds of chats into a personal database. One format can't serve both jobs well.

Markdown is easy to read but loose in structure. JSON is precise in structure but tiring to read. Saving both means you don't have to choose up front. You can decide later, once you know how you'll use your files.

Both files sit side by side in your Library folder, inside each provider's subfolder:

```
claude
├── quarterly-report-draft.md
└── quarterly-report-draft.json
```

**Takeaway:** Two files means you keep your options open, at very little cost in disk space.

---

## What Markdown Is

Markdown is plain text with a few simple marks for structure. A `#` at the start of a line makes a heading. Two asterisks around a word make it **bold**. Everything else is ordinary writing.

It was designed to be readable even before any app formats it. You can open a Markdown file in Notepad and follow it without any trouble.

### What a Saved Markdown File Looks Like

Here's a simplified example of a saved conversation:

```
# Quarterly report draft

**Provider:** Claude
**Saved:** 2026-10-02

---

## You

Can you help me tighten the opening paragraph of my quarterly report?

## Claude

Here's a shorter version that leads with the main result:

Revenue grew 12% this quarter, driven by stronger renewals.
```

Your files may differ slightly in layout. The idea stays the same: each message is labeled, in order, as readable text.

### When to Use Markdown

**Rereading a conversation.** Open the file and scroll. Headings separate each message, so finding your place is easy.

**Copying part of a chat.** Select the text you want and paste it into an email, a document, or a message. There's no extra formatting to clean up.

**Keeping notes in a note-taking app.** Many note apps open or import Markdown files directly. Your AI conversations can sit right next to your other notes, in a format those apps already understand.

**Sharing with someone else.** Send a single `.md` file to a coworker. They can open it with Notepad or any text editor, without installing anything new.

### Where Markdown Falls Short

Markdown is loose by design. A program can't always tell where one message ends and the next begins, or which details describe the conversation itself. That's fine for reading, but it makes Markdown a weaker choice for automated work.

**Takeaway:** Markdown is the format to open when a person is doing the reading.

---

## What JSON Is

JSON stands for JavaScript Object Notation. Despite the name, it isn't tied to one programming language. It's a widely used format for storing structured data, and nearly every modern programming language and many apps can read it.

JSON organizes information into labeled fields. Each piece of information has a name and a value. Lists of items, like the messages in a conversation, sit inside square brackets.

### What a Saved JSON File Looks Like

Here's a simplified version of the same conversation:

```
{
  "title": "Quarterly report draft",
  "provider": "claude",
  "saved_at": "2026-10-02T09:14:00Z",
  "messages": [
    {
      "role": "user",
      "content": "Can you help me tighten the opening paragraph of my quarterly report?"
    },
    {
      "role": "assistant",
      "content": "Here's a shorter version that leads with the main result..."
    }
  ]
}
```

The exact fields in your files may vary. The shape is consistent, though: details about the conversation at the top, then each message in order, labeled by who sent it.

### When to Use JSON

**Feeding conversations into other tools.** Some apps and personal databases accept JSON imports. Because every field is labeled, the tool can tell titles, dates, and messages apart.

**Working with scripts.** If you write code, even a short script, JSON is far easier to process than Markdown. A few lines can loop through a folder of conversations and pull out every message you sent, for example.

**Keeping a structured record.** JSON keeps each conversation's details in predictable places. That helps if you ever want to sort, filter, or count conversations by provider or date.

**Converting to other formats later.** Structured data is easier to reshape. If a new tool appears that needs a different format, starting from JSON usually makes the conversion simpler.

### Where JSON Falls Short

JSON is hard on the eyes. Quotes, brackets, and commas surround every value, and long messages can run across a single very long line. It's also strict. A missing comma or bracket can stop a program from reading the file at all.

If you want to look inside a JSON file, an editor like VS Code adds color and lets you fold sections. Microsoft Edge can also display JSON in a tidier layout.

**Takeaway:** JSON is the format to use when a program is doing the reading.

---

## Markdown vs JSON Side by Side

|                        | **Markdown (`.md`)**               | **JSON (`.json`)**                            |
| ---------------------- | ---------------------------------- | --------------------------------------------- |
| **Best for**           | People reading                     | Software processing                           |
| **Readability**        | Easy to read as is                 | Hard to read without a good editor            |
| **Structure**          | Loose, based on headings           | Strict, with labeled fields                   |
| **Copying text**       | Clean and quick                    | Awkward, with quotes and brackets around text |
| **Note-taking apps**   | Often opened or imported directly  | Rarely used directly                          |
| **Scripts and tools**  | Harder to process reliably         | Easy to process                               |
| **Editing by hand**    | Safe and simple                    | Easy to break by accident                     |
| **Opens with**         | Notepad, VS Code, note-taking apps | Notepad, VS Code, Microsoft Edge              |
| **Same conversation?** | Yes                                | Yes                                           |

---

## Which File to Use for Common Tasks

| What You Want to Do                      | Use This File |
| ---------------------------------------- | ------------- |
| Reread an old conversation               | `.md`         |
| Copy an answer into an email or document | `.md`         |
| Add a chat to your notes                 | `.md`         |
| Send one conversation to a coworker      | `.md`         |
| Import conversations into another tool   | `.json`       |
| Run a script across many conversations   | `.json`       |
| Sort or filter chats by date or provider | `.json`       |
| Back up your conversation history        | Both          |

**Takeaway:** Most everyday tasks point to Markdown. Most technical tasks point to JSON. Backups should include both.

---

## Common Questions

### Can I delete one of the two files?

You can, but there's little reason to. Both files are small, and keeping the pair means you won't need to download the conversation again if your needs change. If you want a tidier folder for reading, copy the `.md` files into a separate folder instead of deleting the originals.

### Is it safe to edit the files?

Editing a Markdown file is low risk, since it's just text. Editing JSON by hand is riskier, because one misplaced character can make the file unreadable to software. Either way, work on a copy and leave the originals in your Library folder as they are.

### Do I need TotalRecalls to open these files?

No. Both are standard formats. Once a conversation is saved, you can open either file with tools already on your PC, without TotalRecalls and without an internet connection.

### Does every provider save both formats?

Yes. Every supported provider saves the same pair of files, whether you're on the Free Tier or Pro. That includes Gemini on Pro, which works through a Google Takeout file and ends up as the same Markdown and JSON files as every other provider.

---

## The Recommendation for Most People

**Start with Markdown.** Open the `.md` file whenever you want to read, copy, or share a conversation. For most people, that covers nearly everything they'll do with their saved chats.

**Keep the JSON file anyway.** You may never open it, and that's fine. It takes up very little space, and it's there if you later want to import your conversations into a new tool or work with them in bulk.

**Back up both.** When you copy your Library folder to an external drive or another backup location, take the whole folder. That way you keep a readable version and a structured version of everything you've saved.

---

## Two Files, Two Jobs

Markdown and JSON aren't competing formats. They're two copies of the same conversation, each shaped for a different reader. Markdown suits you, and JSON suits your software.

For the next conversation you save, open the `.md` file first. If you ever need the structured version, the `.json` file will be right beside it.

If you haven't tried TotalRecalls yet, the Free Tier covers ChatGPT, Claude, and Perplexity. You can save your first conversation and open both files yourself in a few minutes.

**Download free at totalrecalls.app.**
