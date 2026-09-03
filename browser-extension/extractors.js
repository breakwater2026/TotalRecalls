(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.TotalRecallsExtractors = factory();
  }
})(typeof globalThis === "object" ? globalThis : this, function () {
  "use strict";

  var HANDOFF_PROTOCOL = "totalrecalls-browser-handoff";
  var HANDOFF_VERSION = 1;
  var SUPPORTED_PROVIDERS = ["chatgpt", "claude", "gemini"];

  function textOf(node) {
    if (!node) return "";
    var value = typeof node.innerText === "string" ? node.innerText : node.textContent || "";
    return value.replace(/\u00a0/g, " ").replace(/[ \t]+\n/g, "\n").replace(/\n{3,}/g, "\n\n").trim();
  }

  function attr(node, names) {
    for (var i = 0; i < names.length; i += 1) {
      var value = node && node.getAttribute && node.getAttribute(names[i]);
      if (value) return value;
    }
    return "";
  }

  function providerFromHost(host) {
    host = String(host || "").toLowerCase().split(":")[0];
    if (host === "chatgpt.com" || host.endsWith(".chatgpt.com") || host === "chat.openai.com") {
      return "chatgpt";
    }
    if (host === "claude.ai" || host.endsWith(".claude.ai")) return "claude";
    if (host === "gemini.google.com" || host.endsWith(".gemini.google.com")) return "gemini";
    return "";
  }

  function detectProvider(locationLike) {
    return providerFromHost(locationLike && locationLike.hostname);
  }

  function roleOf(node, provider) {
    var value = attr(node, ["data-message-author-role", "data-role", "role", "aria-label"]);
    var testid = attr(node, ["data-testid"]);
    var tag = String(node && node.tagName || "").toLowerCase();
    var classes = String(node && node.className || "").toLowerCase();
    var combined = (value + " " + testid + " " + tag + " " + classes).toLowerCase();
    if (/\b(user|human|you|user-message|user_query)\b/.test(combined)) return "user";
    if (/\b(assistant|ai|model|claude|gemini|chatgpt|assistant-message|model-response)\b/.test(combined)) {
      return "assistant";
    }
    if (/\bsystem\b/.test(combined)) return "system";
    if (provider === "gemini" && /user-query/.test(combined)) return "user";
    if (provider === "gemini" && /model-response/.test(combined)) return "assistant";
    return "";
  }

  function uniqueNodes(nodes) {
    var result = [];
    nodes.forEach(function (node) {
      if (result.indexOf(node) === -1) result.push(node);
    });
    return result;
  }

  function candidatesFor(documentLike, provider) {
    var selectors = {
      chatgpt: [
        '[data-message-author-role]',
        '[data-testid^="conversation-turn-"]',
        'article[data-testid*="conversation"]'
      ],
      claude: [
        '[data-testid="user-message"]',
        '[data-testid="assistant-message"]',
        '[data-message-author-role]',
        '[data-testid*="message"]'
      ],
      gemini: [
        'user-query',
        'model-response',
        '[data-message-author-role]',
        '[data-testid*="message"]'
      ]
    }[provider] || [];
    var nodes = [];
    selectors.forEach(function (selector) {
      var found = Array.prototype.slice.call(documentLike.querySelectorAll(selector) || []);
      nodes = uniqueNodes(nodes.concat(found));
    });
    return nodes;
  }

  function citationsOf(node) {
    if (!node || !node.querySelectorAll) return [];
    var links = Array.prototype.slice.call(node.querySelectorAll("a[href]") || []);
    return links.map(function (link) {
      var url = link.href || attr(link, ["href"]);
      if (!/^https?:\/\//i.test(url || "")) return null;
      return { title: textOf(link), url: url, snippet: "" };
    }).filter(function (citation, index, all) {
      return citation && all.findIndex(function (item) { return item.url === citation.url; }) === index;
    });
  }

  function messageFromNode(node, provider) {
    var role = roleOf(node, provider);
    if (!role) return null;
    var copy = node.cloneNode ? node.cloneNode(true) : node;
    if (copy.querySelectorAll) {
      Array.prototype.slice.call(copy.querySelectorAll("button, [aria-label*='copy' i], script, style")).forEach(function (element) {
        if (element.remove) element.remove();
      });
    }
    var content = textOf(copy);
    if (!content) return null;
    var timestampNode = copy.querySelector && copy.querySelector("time[datetime]");
    var createdAt = timestampNode ? attr(timestampNode, ["datetime"]) : "";
    return {
      role: role,
      content_md: content,
      created_at: createdAt,
      model: attr(node, ["data-model", "data-message-model", "data-model-name"]),
      citations: citationsOf(node),
      external_id: attr(node, ["data-message-id", "data-id"])
    };
  }

  function titleOf(documentLike, provider) {
    var heading = documentLike.querySelector && documentLike.querySelector("h1");
    var title = textOf(heading);
    if (!title && documentLike.querySelector) {
      var meta = documentLike.querySelector('meta[property="og:title"], meta[name="title"]');
      title = meta && attr(meta, ["content"]);
    }
    if (!title && documentLike.title) title = String(documentLike.title).replace(/\s*[|·-]\s*(ChatGPT|Claude|Gemini).*$/i, "");
    return title.trim() || ("Untitled " + provider + " conversation");
  }

  function conversationId(locationLike) {
    var path = String(locationLike && locationLike.pathname || "");
    var match = path.match(/\/(?:c|chat|conversation|conversations)\/([^/?#]+)/i);
    return match ? decodeURIComponent(match[1]) : "";
  }

  function extractCurrentConversation(documentLike, locationLike) {
    var provider = detectProvider(locationLike);
    if (!provider) throw new Error("This page is not a supported ChatGPT, Claude, or Gemini conversation.");
    var messages = candidatesFor(documentLike, provider).map(function (node) {
      return messageFromNode(node, provider);
    }).filter(Boolean);
    var deduped = [];
    messages.forEach(function (message) {
      var key = message.role + "\n" + message.content_md;
      if (!deduped.some(function (item) { return item.role + "\n" + item.content_md === key; })) deduped.push(message);
    });
    if (!deduped.length) {
      throw new Error("No conversation messages were found. Open a conversation and try again.");
    }
    var now = new Date().toISOString();
    var url = String(locationLike && locationLike.href || "");
    var conversation = {
      id: conversationId(locationLike),
      title: titleOf(documentLike, provider),
      created_at: deduped[0].created_at || "",
      updated_at: now,
      messages: deduped
    };
    if (!conversation.id) delete conversation.id;
    return {
      protocol: HANDOFF_PROTOCOL,
      version: HANDOFF_VERSION,
      schema_version: 1,
      provider: provider,
      source: { url: url, provider: provider },
      conversation: conversation
    };
  }

  return {
    HANDOFF_PROTOCOL: HANDOFF_PROTOCOL,
    HANDOFF_VERSION: HANDOFF_VERSION,
    SUPPORTED_PROVIDERS: SUPPORTED_PROVIDERS,
    detectProvider: detectProvider,
    extractCurrentConversation: extractCurrentConversation,
    providerFromHost: providerFromHost
  };
});
