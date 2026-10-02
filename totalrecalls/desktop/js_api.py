"""Minimal JsApi facade exposed to pywebview (methods only)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from totalrecalls.desktop.bridge import Bridge


class JsApi:
    """Minimal surface exposed to JavaScript via pywebview.

    IMPORTANT: pywebview walks public attributes of the js_api object and
    recursively exposes nested objects (see webview.util.get_functions). Putting
    the Window, tokens, threads, etc. on the same object breaks JS bridge
    injection — symptoms: `connect is not a function`, `Main window failed to
    start`. Only public methods (and underscore-private attrs) belong here.
    """

    def __init__(self, bridge: "Bridge"):
        self._b = bridge

    def ping(self):
        return self._b.ping()

    def getState(self):
        return self._b.getState()

    def connect(self):
        return self._b.connect()

    def cancelLogin(self):
        return self._b.cancelLogin()

    def pasteCookie(self, token: str = ""):
        return self._b.pasteCookie(token)

    def chooseFolder(self):
        return self._b.chooseFolder()

    def startExport(self, refresh: bool = False):
        return self._b.startExport(refresh)

    def startLatestExport(self):
        return self._b.startLatestExport()

    def openFolder(self):
        return self._b.openFolder()

    def copyLatestMarkdown(self):
        return self._b.copyLatestMarkdown()

    def exportLatestPdf(self):
        return self._b.exportLatestPdf()

    def listExportedConversations(self):
        return self._b.listExportedConversations()

    def getExportedConversation(self, relative_path: str = ""):
        return self._b.getExportedConversation(relative_path)

    def exportSelectedMessages(self, relative_path: str = "", message_indexes=None):
        return self._b.exportSelectedMessages(relative_path, message_indexes)

    def disconnect(self):
        return self._b.disconnect()

    def quitApp(self):
        return self._b.quitApp()

    def listProviders(self):
        return self._b.listProviders()

    def setProvider(self, provider_id: str = "perplexity"):
        return self._b.setProvider(provider_id)

    def chooseTakeoutPath(self):
        return self._b.chooseTakeoutPath()

    # --- licensing -------------------------------------------------------
    # These two live on Bridge but were missing from this facade, so the UI's
    # `a.activateLicense(key)` / `a.openBuyPage()` threw "not a function" in the
    # webview: the Activate button sat on "Activating…" forever without ever
    # calling Python, and the Buy button did nothing (reported 2026-09-26).
    # Every method the UI calls must be delegated here — see
    # tools/_check_ui_bridge_contract.py, which fails the build otherwise.
    def activateLicense(self, key: str = ""):
        return self._b.activateLicense(key)

    def resetLicense(self):
        return self._b.resetLicense()

    def openBuyPage(self):
        return self._b.openBuyPage()
