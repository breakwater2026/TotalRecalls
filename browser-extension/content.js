(function () {
  "use strict";

  if (!globalThis.TotalRecallsExtractors) return;

  chrome.runtime.onMessage.addListener(function (message, _sender, sendResponse) {
    if (!message || message.type !== "TOTALRECALLS_EXTRACT") return undefined;
    try {
      sendResponse({
        ok: true,
        handoff: globalThis.TotalRecallsExtractors.extractCurrentConversation(document, location)
      });
    } catch (error) {
      sendResponse({ ok: false, error: error && error.message ? error.message : String(error) });
    }
    return true;
  });
})();
