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

    def openFolder(self):
        return self._b.openFolder()

    def disconnect(self):
        return self._b.disconnect()

    def quitApp(self):
        return self._b.quitApp()

    def listProviders(self):
        return self._b.listProviders()

