(function () {
  "use strict";

  var page = document.getElementById("page");
  var save = document.getElementById("save");
  var status = document.getElementById("status");

  function slug(value) {
    return String(value || "conversation").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 60) || "conversation";
  }

  function setStatus(message, isError) {
    status.textContent = message;
    status.style.color = isError ? "#b91c1c" : "#1d4ed8";
  }

  function activeTab() {
    return chrome.tabs.query({ active: true, currentWindow: true }).then(function (tabs) {
      return tabs[0];
    });
  }

  function extract(tab) {
    return chrome.tabs.sendMessage(tab.id, { type: "TOTALRECALLS_EXTRACT" }).catch(function () {
      return chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ["extractors.js", "content.js"]
      }).then(function () {
        return chrome.tabs.sendMessage(tab.id, { type: "TOTALRECALLS_EXTRACT" });
      });
    });
  }

  function download(handoff) {
    var title = handoff.conversation && handoff.conversation.title;
    var date = new Date().toISOString().slice(0, 10);
    var filename = "totalrecalls-" + handoff.provider + "-" + slug(title) + "-" + date + ".handoff.json";
    var json = JSON.stringify(handoff, null, 2) + "\n";
    return chrome.downloads.download({
      url: "data:application/json;charset=utf-8," + encodeURIComponent(json),
      filename: filename,
      saveAs: true,
      conflictAction: "uniquify"
    });
  }

  activeTab().then(function (tab) {
    var provider = globalThis.TotalRecallsExtractors.detectProvider(tab && tab.url ? new URL(tab.url) : {});
    page.textContent = provider ? "Ready to read this " + provider + " page." : "Open a ChatGPT, Claude, or Gemini conversation.";
    save.disabled = !provider;
  }).catch(function () {
    page.textContent = "Could not inspect the current page.";
    save.disabled = true;
  });

  save.addEventListener("click", function () {
    save.disabled = true;
    setStatus("Reading current conversation…");
    activeTab().then(extract).then(function (result) {
      if (!result || !result.ok) throw new Error(result && result.error || "Extraction failed.");
      return download(result.handoff).then(function () {
        setStatus("Downloaded. Import the JSON locally in TotalRecalls.");
      });
    }).catch(function (error) {
      setStatus(error.message || String(error), true);
    }).finally(function () {
      save.disabled = false;
    });
  });
})();
