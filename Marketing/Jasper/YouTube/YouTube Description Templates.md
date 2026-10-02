# YouTube Description Templates for the TotalRecalls Channel

A good YouTube description does two jobs. It tells viewers exactly what the video shows, and it gives them one clear next step. These templates handle both, so every upload sounds the same, links to the right page, and repeats the same accurate claims as the website.

There's one template for each video series on the channel:

- Proof Demos
- Provider Guides
- Workflow and File Videos
- Explainers
- Troubleshooting
- Product Updates

Each template uses the same structure. Only the opening line, the chapters, and a few series-specific lines change.

---

## How to Use These Templates

Copy the template for your video type. Then replace every bracketed note with real content. Delete the brackets and the guidance text before you publish.

A few things to know before you start:

- **The first two lines matter most.** YouTube shows roughly the first 150 characters above the "Show more" fold, and search results often show even less. The opening sentence and the download link belong there.
- **YouTube descriptions don't support bold or headings.** The templates use plain text and capital-letter labels so they look the same in the video page and in search.
- **Chapters need three things to work.** The first timestamp must be 0:00, there must be at least three chapters, and each chapter must last at least 10 seconds.
- **Every link gets a UTM tag.** This shows which videos send people to the website and which ones lead to downloads.

---

## Shared Building Blocks

These parts appear in every template. Keep them identical across the channel unless the website wording changes.

### UTM Tag Format

Use this pattern for every link in every description:

```
?utm_source=youtube&utm_medium=video&utm_campaign=[series]-[topic]
```

**Series codes:**

| Series                   | Code        |
| ------------------------ | ----------- |
| Proof Demos              | `proof`     |
| Provider Guides          | `guide`     |
| Workflow and File Videos | `workflow`  |
| Explainers               | `explainer` |
| Troubleshooting          | `fix`       |
| Product Updates          | `update`    |

**Topic codes** use lowercase words joined with hyphens, such as `chatgpt`, `library-folder`, or `markdown-vs-json`.

**Example:**

```
totalrecalls.app/?utm_source=youtube&utm_medium=video&utm_campaign=guide-claude
```

### About TotalRecalls Boilerplate

```
ABOUT TOTALRECALLS
TotalRecalls is a Windows app that saves your AI conversations to your PC as Markdown and JSON files. You sign in to each provider inside the app, on your own computer. Your conversations aren't sent to our servers, and there's no TotalRecalls account to create.

The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini (through Google Takeout), Grok, DeepSeek, Mistral, and Qwen, with unlimited downloads.
```

### Disclaimer Line

```
Real screen recording. Personal details are blurred. Loading time is trimmed.
```

\[If no loading time was cut, remove "Loading time is trimmed." If other waits were cut, such as email delivery, say so plainly: "Email delivery time is trimmed." Never let the video suggest faster speeds than users will see.]

### Platform Note

```
Windows 10 and 11.
```

\[Don't add macOS or Linux release dates. If you mention them at all, describe them as "in development."]

---

## Template 1: Proof Demos

Use this for short, literal recordings of one download from start to finish. These videos are 45–90 seconds and end with files open on screen.

```
[Opening sentence: Say exactly what the video shows, in one plain sentence. Name the provider and the result. Example: "One real ChatGPT download with TotalRecalls, from opening the app to opening the saved Markdown and JSON files."]

Download TotalRecalls free: totalrecalls.app/?utm_source=youtube&utm_medium=video&utm_campaign=proof-[provider]
[For Pro-only providers (Gemini, Grok, DeepSeek, Mistral, Qwen), keep the free download link first. Add one line below it: "This provider is included in Pro." Don't push the upgrade harder than that.]

See it work: [See It Work page URL]?utm_source=youtube&utm_medium=video&utm_campaign=proof-[provider]
Full written guide: [Matching Guides page URL for this provider]?utm_source=youtube&utm_medium=video&utm_campaign=proof-[provider]

CHAPTERS
0:00 Open the app
[0:00] Choose [provider]
[0:00] Sign in
[0:00] Pick a conversation
[0:00] Download
[0:00] Open your files
[Match each timestamp to the final cut. Use the same step names as the on-screen captions. For the ChatGPT demo, the timestamps should match the See It Work page exactly.]

ABOUT TOTALRECALLS
TotalRecalls is a Windows app that saves your AI conversations to your PC as Markdown and JSON files. You sign in to each provider inside the app, on your own computer. Your conversations aren't sent to our servers, and there's no TotalRecalls account to create.

The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini (through Google Takeout), Grok, DeepSeek, Mistral, and Qwen, with unlimited downloads.

Real screen recording. Personal details are blurred. Loading time is trimmed.

Windows 10 and 11.
```

---

## Template 2: Provider Guides

Use this for full walkthroughs of one provider, usually 3–6 minutes. These videos target people searching for a specific fix, so the opening line should use the words they type.

```
[Opening sentence: Start with the search phrase, then the outcome. Example: "How to save your Claude conversations to your PC as Markdown and JSON files, step by step, using TotalRecalls on Windows."]

[Optional second sentence: Add one detail that sets expectations. Example: "This guide covers signing in, choosing conversations, downloading, and finding your files."]

Download TotalRecalls free: totalrecalls.app/?utm_source=youtube&utm_medium=video&utm_campaign=guide-[provider]
[For Pro providers, add: "This provider is included in Pro. Compare Free and Pro: totalrecalls.app/pricing/?utm_source=youtube&utm_medium=video&utm_campaign=guide-[provider]"]

See it work: [See It Work page URL]?utm_source=youtube&utm_medium=video&utm_campaign=guide-[provider]
Full written guide with screenshots: [Matching Guides page URL]?utm_source=youtube&utm_medium=video&utm_campaign=guide-[provider]

CHAPTERS
0:00 What this guide covers
[0:00] Open TotalRecalls and choose [provider]
[0:00] Sign in to [provider] inside the app
[0:00] Choose the conversations to save
[0:00] Download
[0:00] Where your files are saved
[0:00] Common problems and fixes
[Rename or add chapters to match the video. Keep names short and literal.]

[GEMINI ONLY: Replace the sign-in and choose chapters with Takeout steps, such as "Request your Google Takeout file," "Download the Takeout file," and "Import it into TotalRecalls." Add this line above CHAPTERS: "Gemini conversations come in through a Google Takeout file. This isn't a one-click download, and this guide shows each step." Never imply Gemini works like the other providers.]

ABOUT TOTALRECALLS
TotalRecalls is a Windows app that saves your AI conversations to your PC as Markdown and JSON files. You sign in to each provider inside the app, on your own computer. Your conversations aren't sent to our servers, and there's no TotalRecalls account to create.

The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini (through Google Takeout), Grok, DeepSeek, Mistral, and Qwen, with unlimited downloads.

Real screen recording. Personal details are blurred. Loading time is trimmed.

Windows 10 and 11.

[Recorded with TotalRecalls version [X.X] on [Month Year]. Add this line so viewers can tell whether the guide is current. Update it when you re-record.]
```

---

## Template 3: Workflow and File Videos

Use this for videos about what people can do with their saved files, such as organizing, searching, backing up, or opening chats in other apps.

```
[Opening sentence: Describe the task and the result. Example: "How to search across all your saved AI conversations using Windows search, so you can find any chat in seconds."]

[Optional second sentence: Name the tools shown, plainly. Example: "This video uses File Explorer and Notepad. Both come with Windows." If you show a third-party app, such as VS Code or a note-taking app, name it as text only. Don't imply any partnership or endorsement.]

Download TotalRecalls free: totalrecalls.app/?utm_source=youtube&utm_medium=video&utm_campaign=workflow-[topic]

See it work: [See It Work page URL]?utm_source=youtube&utm_medium=video&utm_campaign=workflow-[topic]
Full written guide: [Matching Guides page URL]?utm_source=youtube&utm_medium=video&utm_campaign=workflow-[topic]
[If no written guide exists for this topic yet, link to the main Guides page instead.]

CHAPTERS
0:00 [What you'll do in this video]
[0:00] [First step, such as "Open your Library folder"]
[0:00] [Second step, such as "Search by keyword"]
[0:00] [Third step, such as "Filter by date"]
[0:00] [Result, such as "Open the chat you found"]
[Use action verbs. Each chapter should describe one thing the viewer does.]

ABOUT TOTALRECALLS
TotalRecalls is a Windows app that saves your AI conversations to your PC as Markdown and JSON files. You sign in to each provider inside the app, on your own computer. Your conversations aren't sent to our servers, and there's no TotalRecalls account to create.

The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini (through Google Takeout), Grok, DeepSeek, Mistral, and Qwen, with unlimited downloads.

Real screen recording. Personal details are blurred. Loading time is trimmed.

Windows 10 and 11.
```

---

## Template 4: Explainers

Use this for short videos that explain the "why" behind the product, such as Markdown vs JSON, Free vs Pro, or what "local" means. These may mix screen recording with a spoken explanation.

```
[Opening sentence: State the question the video answers, then the short answer. Example: "Markdown or JSON? TotalRecalls saves every conversation in both formats, and this video explains what each one is good for."]

Download TotalRecalls free: totalrecalls.app/?utm_source=youtube&utm_medium=video&utm_campaign=explainer-[topic]
[FREE VS PRO ONLY: Add this line below the download link: "Compare Free and Pro: totalrecalls.app/pricing/?utm_source=youtube&utm_medium=video&utm_campaign=explainer-free-vs-pro". If the price is mentioned, write "Pro is $24 one-time (launch price)." Always keep "launch price" beside $24. Don't add discounts or end dates unless they're published and real.]

See it work: [See It Work page URL]?utm_source=youtube&utm_medium=video&utm_campaign=explainer-[topic]
Read more: [Matching Guides page URL]?utm_source=youtube&utm_medium=video&utm_campaign=explainer-[topic]

CHAPTERS
0:00 [The question]
[0:00] [First point]
[0:00] [Second point]
[0:00] [Example on screen]
[0:00] [Short answer and recap]

[PRIVACY EXPLAINER ONLY: Add this line above CHAPTERS: "Downloads connect directly from your PC to each AI provider. Your conversations aren't sent to our servers." Never describe the app as "fully offline" or say it "never touches the internet."]

ABOUT TOTALRECALLS
TotalRecalls is a Windows app that saves your AI conversations to your PC as Markdown and JSON files. You sign in to each provider inside the app, on your own computer. Your conversations aren't sent to our servers, and there's no TotalRecalls account to create.

The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini (through Google Takeout), Grok, DeepSeek, Mistral, and Qwen, with unlimited downloads.

Real screen recording. Personal details are blurred. Loading time is trimmed.
[If the explainer includes non-recorded visuals, such as a simple diagram, adjust the line: "Screen recordings are real. Personal details are blurred. Loading time is trimmed."]

Windows 10 and 11.
```

---

## Template 5: Troubleshooting

Use this for short, specific fixes based on real support questions. People find these videos when something isn't working, so get to the answer fast.

```
[Opening sentence: Name the problem in the words a user would search for, then promise the fix. Example: "If the sign-in window won't load in TotalRecalls, this short video shows how to fix it."]

PROBLEM: [Describe the symptom in one sentence. Example: "The provider's sign-in window stays blank after you choose it."]
FIX: [Summarize the fix in one or two sentences, so people can solve it without watching. Example: "Close TotalRecalls, check your internet connection, and reopen the app from its folder."]

Download TotalRecalls free: totalrecalls.app/?utm_source=youtube&utm_medium=video&utm_campaign=fix-[topic]

See it work: [See It Work page URL]?utm_source=youtube&utm_medium=video&utm_campaign=fix-[topic]
Full written guide: [Matching Guides or help page URL]?utm_source=youtube&utm_medium=video&utm_campaign=fix-[topic]

Still stuck? Contact us: [support email or contact page URL]

CHAPTERS
0:00 The problem
[0:00] Why it happens
[0:00] Step 1: [first fix step]
[0:00] Step 2: [second fix step]
[0:00] Check that it worked
[Short videos under about a minute can skip chapters if they can't meet the three-chapter, 10-second minimum.]

[LICENSE OR DEVICE VIDEOS ONLY: Use exact wording. "Pro activates on up to 3 PCs." Never say "unlimited devices." Blur the license key in the video and never include it in the description.]

ABOUT TOTALRECALLS
TotalRecalls is a Windows app that saves your AI conversations to your PC as Markdown and JSON files. You sign in to each provider inside the app, on your own computer. Your conversations aren't sent to our servers, and there's no TotalRecalls account to create.

The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini (through Google Takeout), Grok, DeepSeek, Mistral, and Qwen, with unlimited downloads.

Real screen recording. Personal details are blurred. Loading time is trimmed.

Windows 10 and 11.

[Recorded with TotalRecalls version [X.X] on [Month Year].]
```

---

## Template 6: Product Updates

Use this for brief, honest notes on what changed. These videos show the product is cared for, so keep the summary factual and specific.

```
[Opening sentence: Name the update and its main change. Example: "What's new in TotalRecalls for [Month Year]: faster Claude downloads, a clearer Library folder, and two bug fixes."]

NEW
- [New feature or provider, in one plain line]
- [Another new item, if any]

FIXED
- [Bug fix, described by what users will notice. Example: "Long Perplexity threads now save completely."]

IN PROGRESS
- [Work underway, with no dates. Example: "macOS and Linux versions are in development."]
[Never give release dates for macOS, Linux, or new providers until they're real and published. If updates come up, say "for the life of the product." Never say "forever" or "lifetime updates."]

Download TotalRecalls free: totalrecalls.app/?utm_source=youtube&utm_medium=video&utm_campaign=update-[month-year]

Get product updates by email: totalrecalls.app/?utm_source=youtube&utm_medium=video&utm_campaign=update-[month-year]#[footer signup anchor]
[Product Update videos are the right place for the email signup. Link straight to the footer form if it has an anchor. Keep this line below the download link.]

See it work: [See It Work page URL]?utm_source=youtube&utm_medium=video&utm_campaign=update-[month-year]
Full changelog: [Changelog or Guides page URL]?utm_source=youtube&utm_medium=video&utm_campaign=update-[month-year]

CHAPTERS
0:00 What's in this update
[0:00] [First new item]
[0:00] [Second new item]
[0:00] Fixes
[0:00] What we're working on

ABOUT TOTALRECALLS
TotalRecalls is a Windows app that saves your AI conversations to your PC as Markdown and JSON files. You sign in to each provider inside the app, on your own computer. Your conversations aren't sent to our servers, and there's no TotalRecalls account to create.

The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini (through Google Takeout), Grok, DeepSeek, Mistral, and Qwen, with unlimited downloads.

Real screen recording. Personal details are blurred. Loading time is trimmed.
[If the update includes on-camera segments, adjust: "Screen recordings are real. Personal details are blurred. Loading time is trimmed."]

Windows 10 and 11.
```

---

## Common Mistakes to Avoid

Small wording slips can undo the trust these videos build. Watch for these before you publish:

- **Don't** stack calls to action. Keep "Download free" first and skip extra asks to like, subscribe, and buy in the description.
- **Don't** use hype words like "secret," "insane," or "game-changing." Plain descriptions match the product.
- **Don't** paste provider logos or trademark symbols into descriptions. Write provider names as text.
- **Don't** leave bracketed guidance in a published description. Search the text for "\[" before you hit publish.
- **Do** match every chapter name to what's actually on screen.
- **Do** confirm the Free Tier limit wording ("per provider" or "per download") matches the live site before mentioning it anywhere.
- **Do** keep "launch price" beside every mention of $24.

---

## Before You Publish

Run through this short checklist on every upload:

1
