"""Verify the Paddle licensing path is really inside the freshly built EXE.

Size and mtime prove nothing about WHICH code shipped: the PYZ is a custom zlib
archive, so plain string scans miss it. This walks the archive properly and
compares the licensing module's string constants against the source.

Run with the build venv:
  "C:/Users/break/AppData/Local/tr-build-venv/Scripts/python.exe" tools/_verify_paddle_build.py
"""
import os
import sys
import tempfile

EXE = os.path.join("dist", "TotalRecalls.exe")
MODULES = ("totalrecalls.licensing", "totalrecalls.edition", "totalrecalls.desktop.bridge",
           "totalrecalls.desktop.js_api")

WANT = "https://totalrecalls.app/api/licenses/verify"
MUST_NOT = ("api.lemonsqueezy.com", "paddle-fulfillment-worker.sparkling-paradox.workers.dev")
# The in-app Buy button must reach the live site page, not a dead checkout URL.
BRIDGE_WANT = "https://totalrecalls.app/buy"
BRIDGE_MUST_NOT = ("pay.paddle.io/checkout/hsc_", "lemonsqueezy", "onfastspring", "orderprocessor")
# Cloudflare 403s (error 1010) urllib's default UA, so the app MUST send its own.
UA_WANT = "TotalRecalls/1.0 (+https://totalrecalls.app)"
UA_MUST_NOT = ("Python-urllib",)


def collect_consts(code, out):
    """Recursively gather string/number constants, descending into code objects."""
    for c in getattr(code, "co_consts", ()):
        if isinstance(c, str):
            out.add(c)
        elif isinstance(c, (int, float)) and not isinstance(c, bool):
            out.add(c)
        elif hasattr(c, "co_consts"):
            collect_consts(c, out)
    return out


def collect_names(code, out):
    """Recursively gather identifier names (co_names / co_varnames).

    Class-body method names never appear in co_consts — they are STORE_NAME'd,
    so they live in co_names. Checking a facade for exposed methods therefore
    has to look here, not at the constants.
    """
    for n in getattr(code, "co_names", ()):
        out.add(n)
    for n in getattr(code, "co_varnames", ()):
        out.add(n)
    for c in getattr(code, "co_consts", ()):
        if hasattr(c, "co_consts"):
            collect_names(c, out)
    return out


def short_strings(consts):
    """String consts that could be a live URL/identifier rather than prose.

    Docstrings and comments legitimately MENTION retired endpoints (and should —
    that history is useful). A reference that can actually be used is a short
    literal, so only those are checked for staleness.
    """
    return [c for c in consts if isinstance(c, str) and len(c) < 120]


def main():
    from PyInstaller.archive.readers import CArchiveReader, ZlibArchiveReader

    if not os.path.exists(EXE):
        print("FAIL: %s not found" % EXE)
        return 1

    ca = CArchiveReader(EXE)
    toc = getattr(ca, "toc", None)
    if toc is None:
        print("FAIL: could not read CArchive toc")
        return 1
    print("CArchive entries: %d" % len(toc))

    pyz_bytes = ca.extract("PYZ.pyz")
    tmp = os.path.join(tempfile.mkdtemp(), "pyz.pyz")
    with open(tmp, "wb") as fh:
        fh.write(pyz_bytes)
    zr = ZlibArchiveReader(tmp)
    print("PYZ modules: %d" % len(zr.toc))

    problems = []
    # Per-module floor: a real module has many consts, but the tiny ones
    # (edition.py) legitimately have a handful. The floor exists only to catch
    # a broken collector reporting an empty set as a "match".
    min_consts = {"totalrecalls.licensing": 20, "totalrecalls.edition": 2}
    for mod in MODULES:
        try:
            code = zr.extract(mod)
        except Exception as exc:                     # noqa: BLE001
            problems.append("%s: extract failed: %s" % (mod, exc))
            continue
        consts = collect_consts(code, set())
        n_str = sum(1 for c in consts if isinstance(c, str))
        print("\n%s: %d consts (%d strings)" % (mod, len(consts), n_str))
        if len(consts) < min_consts.get(mod, 2):
            problems.append("%s: suspiciously few consts (%d) — collector bug?" % (mod, len(consts)))
            continue

        if mod == "totalrecalls.licensing":
            print("   endpoint present :", WANT in consts)
            if WANT not in consts:
                problems.append("licensing: %s NOT in consts" % WANT)
            for bad in MUST_NOT:
                hit = [c for c in short_strings(consts) if bad in c][:2]
                if hit:
                    print("   STALE ref        :", hit)
                    problems.append("licensing: stale reference %r" % hit)
            for probe in ("TR_LICENSE_VERIFY_ENDPOINT", "instance_name", "valid",
                          "Could not reach the license server"):
                print("   %-34s %s" % (probe, probe in consts))
            print("   %-34s %s" % ("User-Agent override", UA_WANT in consts))
            if UA_WANT not in consts:
                problems.append("licensing: User-Agent override missing (%s)" % UA_WANT)
        if mod == "totalrecalls.edition":
            top = getattr(code, "co_consts", ())
            edition = "pro" if "pro" in top else ("free" if "free" in top else "?")
            print("   top-level edition const:", edition)
            if edition != "free":
                problems.append("edition is %r, expected 'free' for the shipping build" % edition)
            bundled = None
            try:
                bundled = ca.extract("app_ui.html")
            except Exception:                        # noqa: BLE001
                pass
            print("   app_ui.html bundled:", bool(bundled), "(%s bytes)" % (len(bundled) if bundled else 0))
        if mod == "totalrecalls.desktop.bridge":
            print("   buy URL present :", BRIDGE_WANT in consts)
            if BRIDGE_WANT not in consts:
                problems.append("bridge: %s NOT in consts" % BRIDGE_WANT)
            for bad in BRIDGE_MUST_NOT:
                hit = [c for c in short_strings(consts) if bad in c][:2]
                if hit:
                    print("   STALE ref       :", hit)
                    problems.append("bridge: stale buy reference %r" % hit)
        if mod == "totalrecalls.desktop.js_api":
            # The facade must delegate the licensing calls the UI makes;
            # without them the buttons throw "not a function" in the webview.
            # Method names live in co_names (see collect_names).
            names = collect_names(code, set())
            print("   names collected  :", len(names))
            for need in ("activateLicense", "openBuyPage"):
                print("   %-16s %s" % (need, need in names))
                if need not in names:
                    problems.append("js_api: %s not exposed to the UI" % need)

    # keep `tmp` alive until here: ZlibArchiveReader guards the file
    print("\n" + ("=" * 58))
    if problems:
        print("VERIFY FAILED:")
        for p in problems:
            print("  -", p)
        return 2
    print("VERIFY OK — Paddle endpoint present, no Lemon Squeezy leftovers, edition=free")
    return 0


if __name__ == "__main__":
    sys.exit(main())
