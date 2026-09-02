"""Build edition — baked in at packaging time.

TotalRecalls ships in two builds:

  * ``free`` — the Free Tier. 3 providers, 5 conversations per download,
    until a license key is activated.
  * ``pro``  — the buyer build. Permanently unlocked: all 8 providers,
    unlimited conversations. No license key needed.

PyInstaller freezes the source at build time, so this constant is what the
packaged EXE ships with. ``tools/build_exe.py --edition pro|free`` rewrites
the flag before invoking PyInstaller and restores it afterwards — the source
tree always stays on the ``free`` default.
"""

EDITION = "free"  # "free" | "pro"


def is_pro_edition() -> bool:
    """True when this build is the unlocked buyer (Pro) edition."""
    return EDITION == "pro"
