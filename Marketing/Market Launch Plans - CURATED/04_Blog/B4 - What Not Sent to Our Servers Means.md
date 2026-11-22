**Meta title:** What "Not Sent to Our Servers" Means in TotalRecalls

**Meta description:** TotalRecalls saves your AI conversations to your own PC. Here's exactly what connects to the internet, what doesn't, and where your chats actually go.

---

# What "Not Sent to Our Servers" Means in TotalRecalls

On our website, in our videos, and inside the app, you'll see one line again and again: **your conversations aren't sent to our servers.** It's the most important promise we make. It deserves more than a single sentence.

This post explains what that line covers and what it doesn't. You'll see which parts of TotalRecalls connect to the internet, where your conversations travel when you download them, and where they end up. It takes about six minutes to read. By the end, you should be able to explain how the app handles your chats in your own words.

---

## The Short Answer

Here's the whole idea in three points:

- **Your conversations travel from the AI provider straight to your PC.** TotalRecalls doesn't route them through our own servers along the way.
- **Your saved files stay on your computer.** They live in your Library folder, as Markdown and JSON files you control.
- **Some parts of the app still use the internet.** Downloading a conversation means connecting to the provider that holds it. A few other tasks connect too, and we list them below.

**Takeaway:** TotalRecalls is a direct line between you and your AI provider. We aren't standing in the middle of it.

---

## Why We Say It This Way

You might wonder why we don't simply call TotalRecalls "offline." The honest answer is that it wouldn't be true.

Your AI conversations are stored by the provider you used, such as ChatGPT or Claude. To make a copy, TotalRecalls has to reach that provider over the internet. No app can download your chat history without connecting to the place where it lives.

So we use a narrower, more precise promise. "Not sent to our servers" describes what actually happens. It tells you who handles your conversations, which is you and your provider, and who doesn't, which is us.

We'd rather make a smaller claim that holds up than a bigger one that doesn't.

**Takeaway:** The wording is careful on purpose. It describes the app as it really works.

---

## Where Your Conversations Actually Go

Here's the path a conversation takes when you download it, step by step.

1. **You open TotalRecalls on your Windows PC** and choose a provider, like Claude.
2. **You sign in to that provider inside the app.** The sign-in happens on your own computer, directly with the provider. You don't create a TotalRecalls account, and we never see your password.
3. **You pick the conversations you want.** The app requests them from the provider.
4. **The provider sends them to your PC.** They come straight from the provider to your computer.
5. **TotalRecalls saves them as files.** Each conversation becomes a Markdown file and a JSON file in your Library folder.

Here's the same path as a simple picture:

```
AI provider  ───────────────►  Your PC  ───────►  Library folder
(e.g. Claude)   direct download   (TotalRecalls)    .md + .json files

TotalRecalls servers:  not part of this path
```

### Gemini Works a Little Differently

On Pro, Gemini conversations come through a Google Takeout file. You request that file from Google and download it to your PC yourself. Then you bring it into TotalRecalls, which turns it into the same Markdown and JSON files as every other provider. The conversion happens on your computer, so the result is the same: your conversations aren't sent to our servers.

**Takeaway:** Your conversations make one trip, from the provider to your PC. Then they stay put.

---

## What Connects to the Internet

Being clear about this is the point of the whole post. These are the moments when TotalRecalls, or something related to it, uses the internet:

- **Signing in to a provider.** The sign-in window connects directly to that provider, the same way a browser would.
- **Downloading conversations.** The app connects to the provider to fetch the chats you selected.
- **Activating Pro.** When you enter a Pro license key, the app checks it so your license can work across up to three PCs. That check involves your license key, not your conversations.
- **Buying Pro.** Your purchase happens on our website, through a checkout process, before you ever enter a key in the app.
- **Getting the app.** You download TotalRecalls from totalrecalls.app, like any other Windows program.
- **Signing up for product updates.** If you choose to join our email list, we receive the email address you enter. That's the only thing the form collects.

## What Doesn't Need the Internet

Once your conversations are saved, a lot of what you'll do with them happens entirely on your PC:

- **Opening your saved files.** Markdown and JSON are standard formats. Notepad, VS Code, and many note-taking apps can open them without a connection.
- **Searching your saved chats.** Windows search looks through files on your own drive.
- **Organizing, copying, and backing up.** Moving files between folders or onto an external drive is ordinary file handling.

**Takeaway:** The internet is used to fetch your conversations and manage your license. Using your saved files doesn't require it.

---

## Connections at a Glance

| What You're Doing                | Connects To            | What's Shared                                    | Includes Your Conversations?           |
| -------------------------------- | ---------------------- | ------------------------------------------------ | -------------------------------------- |
| Signing in to a provider         | That AI provider       | Your sign-in, entered directly with the provider | No                                     |
| Downloading conversations        | That AI provider       | A request for your chats, sent from your PC      | Yes, from the provider to your PC only |
| Importing a Gemini Takeout file  | Nothing                | The file is converted on your PC                 | No                                     |
| Activating Pro                   | TotalRecalls licensing | Your license key                                 | No                                     |
| Buying Pro                       | Our website checkout   | Your purchase details                            | No                                     |
| Joining the email list           | Our email service      | Your email address                               | No                                     |
| Opening or searching saved files | Nothing                | Nothing                                          | No                                     |
| Backing up your Library folder   | Wherever you choose    | Whatever you choose to copy                      | Only if you copy them                  |

**Takeaway:** The only connection that carries your conversations is the one between you and the provider that already holds them.

---

## Where Your Files Live on Your PC

Every saved conversation goes into your Library folder, organized by provider:

```
Library
├── chatgpt
├── claude
└── perplexity
```

These are normal files on your drive. They sit alongside your documents and photos, and they follow the same rules.

That has one practical consequence worth knowing. If you place your Library folder inside a folder that syncs to the cloud, such as OneDrive, Dropbox, or Google Drive, that service will copy your files to its own servers. That's your choice to make, and it can be a useful backup. It just means "on my PC only" stops being true for those files.

The same goes for backups. If you copy your Library folder to an external drive, it lives there too. If you copy it to a cloud backup, it lives with that service.

**Takeaway:** Your files go wherever you put them. If you want them to stay only on your PC, keep the Library folder outside any synced folder.

---

## What "Not Sent to Our Servers" Doesn't Mean

A clear promise also needs clear limits. Here's what this line doesn't cover.

**It doesn't remove conversations from your provider.** TotalRecalls makes a copy. Your original conversations stay with ChatGPT, Claude, or whichever provider you used, under that provider's own policies.

**It doesn't make your PC more secure.** Your saved files are as safe as the computer they're on. A strong Windows password, current updates, and regular backups protect them better than any app can.

**It doesn't cover other apps you use.** If you open a saved chat in a note-taking app that syncs online, that app's rules apply.

**It doesn't mean the app never connects.** As covered above, downloads and license checks need the internet.

**Takeaway:** We control what TotalRecalls does with your conversations. We don't control your provider, your other apps, or your cloud settings.

---

## Common Questions

### Do you ever see my AI conversations?

No. Your conversations aren't sent to our servers. They move from your provider to your PC, and TotalRecalls saves them in your Library folder.

### Do I need a TotalRecalls account?

No. There's no TotalRecalls account to create. You sign in to each AI provider inside the app, directly with that provider.

### Do you see my provider password?

No. You enter it in the provider's own sign-in window, on your computer. That sign-in goes to the provider, not to us.

### What does the Pro license check send?

It sends your license key, so the app can confirm it's valid and track activations across your PCs. Pro activates on up to three PCs. Your conversations aren't part of that check.

### Can I use my saved files without an internet connection?

Yes. Once a conversation is saved, you can open, read, search, and copy it without a connection. You'll only need the internet again to download new conversations.

### Does deleting a file in TotalRecalls delete it from ChatGPT or Claude?

No. Your Library folder holds copies. Deleting a file there has no effect on the original conversation stored by your provider.

### Which versions of Windows does this apply to?

TotalRecalls runs on Windows 10 and 11, and it handles your conversations the same way on both. macOS and Linux versions are in development.

---

## The Recommendation for Most People

**Trust the promise, and understand its edges.** Your conversations aren't sent to our servers. They travel from your provider straight to your PC.

**Decide where your Library folder lives.** If you want your files only on your computer, keep the folder outside OneDrive or any other synced location. If you'd like a cloud backup, place it there on purpose.

**Back up the whole folder.** Your saved chats are only as safe as your PC. Copy your Library folder to an external drive now and then, so one hardware problem doesn't cost you everything.

---

## A Smaller Promise You Can Check

"Not sent to our servers" isn't a slogan. It's a plain description of how TotalRecalls works. Your conversations come from your provider, land on your PC, and stay in a folder you control.

You don't have to take our word for it. Save a conversation, open your Library folder, and look at the files yourself. Everything we've described here is right there on your screen.

The Free Tier covers ChatGPT, Claude, and Perplexity, on Windows 10 and 11. You can save your first conversation in a few minutes and see exactly where it goes.

**Download free at totalrecalls.app.**
