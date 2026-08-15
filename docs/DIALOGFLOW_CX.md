# Dialogflow CX Integration Plan — TotalRecalls

> **Objective:** Utilize your $845 in Dialogflow CX promotional credits to embed an AI customer support & pre-sale assistant on `totalrecalls.app`.

## 1. What Dialogflow CX Does for TotalRecalls
- **24/7 Pre-Sale Assistant:** Answers visitor questions about supported AI providers (ChatGPT, Claude, Perplexity, Gemini, Grok), pricing ($24 one-time), local-first privacy guarantees, and Windows SmartScreen instructions.
- **In-App Troubleshooting Help:** Assists users with common local export setup questions.
- **Credit Compliance:** 100% covered by your Dialogflow CX promotional credits.

## 2. Integration Blueprint
1. **Agent Setup:** Create a new Agent in the Dialogflow CX Console (`us-central1`).
2. **Knowledge Base / FAQ Grounding:** Import your site documentation (`site/src/pages/faq/index.astro`, `site/src/pages/how-it-works/index.astro`) into Dialogflow CX Data Stores so the bot automatically answers from your official site copy.
3. **Web Widget Embedding:** Add the Dialogflow CX Messenger web component (`df-messenger`) to `site/src/layouts/BaseLayout.astro`:
   ```html
   <script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>
   <df-messenger
     intent="WELCOME"
     chat-title="TotalRecalls Support"
     agent-id="YOUR-DIALOGFLOW-AGENT-ID"
     language-code="en"
     location-region="us-central1">
   </df-messenger>
   ```
4. **Deploy:** Commit and push to `RedesignV5` → Cloud Run updates the preview and production site with the chat widget.
