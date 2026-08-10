"""WinForms UI-thread dispatch helper."""

from __future__ import annotations


def dispatch_to_ui_thread(form, callback, begin_invoke=None):
    """Run callback on the form's UI thread when possible."""
    if getattr(form, "InvokeRequired", False):
        if begin_invoke is not None:
            begin_invoke(callback)
            return True
        try:
            from System import Action
            form.BeginInvoke(Action(callback))
            return True
        except Exception:
            pass
    callback()
    return True

