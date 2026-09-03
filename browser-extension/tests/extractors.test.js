const test = require("node:test");
const assert = require("node:assert/strict");
const {
  HANDOFF_PROTOCOL,
  extractCurrentConversation,
  detectProvider
} = require("../extractors.js");

class FakeNode {
  constructor({ text = "", attrs = {}, children = [], tagName = "div" } = {}) {
    this.innerText = text;
    this.textContent = text;
    this.attrs = attrs;
    this.children = children;
    this.tagName = tagName;
    this.className = attrs.class || "";
  }
  getAttribute(name) {
    return this.attrs[name] || "";
  }
  querySelectorAll(selector) {
    if (selector === "a[href]") return this.children.filter((child) => child.getAttribute("href"));
    if (selector === "button, [aria-label*='copy' i], script, style") return [];
    return [];
  }
  querySelector(selector) {
    if (selector === "time[datetime]") return this.children.find((child) => child.getAttribute("datetime")) || null;
    return null;
  }
  cloneNode() {
    return new FakeNode({
      text: this.innerText,
      attrs: { ...this.attrs },
      children: this.children,
      tagName: this.tagName
    });
  }
}

class FakeDocument {
  constructor({ title, heading, nodes }) {
    this.title = title;
    this.heading = heading;
    this.nodes = nodes;
  }
  querySelector(selector) {
    if (selector === "h1") return this.heading;
    return null;
  }
  querySelectorAll(selector) {
    if (selector === '[data-message-author-role]' && this.nodes.author) return this.nodes.author;
    if (selector === '[data-testid="user-message"]' && this.nodes.user) return this.nodes.user;
    if (selector === '[data-testid="assistant-message"]' && this.nodes.assistant) return this.nodes.assistant;
    if (selector === "user-query" && this.nodes.userQuery) return this.nodes.userQuery;
    if (selector === "model-response" && this.nodes.modelResponse) return this.nodes.modelResponse;
    return [];
  }
}

function location(hostname, pathname) {
  return { hostname, pathname, href: `https://${hostname}${pathname}` };
}

test("detects only supported provider hosts", () => {
  assert.equal(detectProvider({ hostname: "chatgpt.com" }), "chatgpt");
  assert.equal(detectProvider({ hostname: "claude.ai" }), "claude");
  assert.equal(detectProvider({ hostname: "gemini.google.com" }), "gemini");
  assert.equal(detectProvider({ hostname: "example.com" }), "");
});

test("extracts ChatGPT role messages and metadata", () => {
  const nodes = [
    new FakeNode({ text: "What changed?", attrs: { "data-message-author-role": "user", "data-message-id": "u1" } }),
    new FakeNode({ text: "The handoff works.", attrs: { "data-message-author-role": "assistant", "data-model": "test-model" } })
  ];
  const result = extractCurrentConversation(
    new FakeDocument({ title: "Ignored", heading: new FakeNode({ text: "Current chat" }), nodes: { author: nodes } }),
    location("chatgpt.com", "/c/current")
  );
  assert.equal(result.protocol, HANDOFF_PROTOCOL);
  assert.equal(result.provider, "chatgpt");
  assert.equal(result.conversation.id, "current");
  assert.deepEqual(result.conversation.messages.map((message) => message.role), ["user", "assistant"]);
  assert.equal(result.conversation.messages[1].model, "test-model");
});

test("extracts Claude testid messages and removes duplicate text", () => {
  const user = new FakeNode({ text: "Question", attrs: { "data-testid": "user-message" } });
  const assistant = new FakeNode({ text: "Answer", attrs: { "data-testid": "assistant-message" } });
  const duplicate = new FakeNode({ text: "Answer", attrs: { "data-testid": "assistant-message" } });
  const result = extractCurrentConversation(
    new FakeDocument({ title: "Claude title", nodes: { user: [user], assistant: [assistant, duplicate] } }),
    location("claude.ai", "/chat/abc")
  );
  assert.equal(result.conversation.title, "Claude title");
  assert.equal(result.conversation.messages.length, 2);
});

test("extracts Gemini custom element roles", () => {
  const result = extractCurrentConversation(
    new FakeDocument({
      title: "Gemini title",
      nodes: {
        userQuery: [new FakeNode({ text: "Prompt", tagName: "user-query" })],
        modelResponse: [new FakeNode({ text: "Response", tagName: "model-response" })]
      }
    }),
    location("gemini.google.com", "/app/abc")
  );
  assert.deepEqual(result.conversation.messages.map((message) => message.role), ["user", "assistant"]);
  assert.equal(result.conversation.id, undefined);
});
