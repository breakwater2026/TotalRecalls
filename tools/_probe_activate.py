"""Reproduce the app's activation call with the SAME stack the app uses.

The app posts {"license_key", "instance_name"} to LICENSE_VERIFY_ENDPOINT via
urllib.request with a 12s timeout. curl to the same endpoint works, so if this
hangs, the difference is the HTTP client (IPv6 route, TLS, proxy env) — not the
endpoint.
"""
import json
import socket
import sys
import time
import urllib.request

URL = "https://totalrecalls.app/api/licenses/verify"
KEY = sys.argv[1] if len(sys.argv) > 1 else "TR-TKAEDYFC-RDUZ-EZFG"

print("resolving host...")
t0 = time.time()
try:
    infos = socket.getaddrinfo("totalrecalls.app", 443, proto=socket.IPPROTO_TCP)
    fams = sorted({("IPv6" if i[0] == socket.AF_INET6 else "IPv4", i[4][0]) for i in infos})
    print(f"  {time.time() - t0:.2f}s -> {fams}")
except Exception as exc:                     # noqa: BLE001
    print("  DNS FAILED:", exc)

print("\nPOST via urllib (timeout=12) ...")
payload = json.dumps({"license_key": KEY, "instance_name": "TR-PROBE00001"}).encode()
req = urllib.request.Request(
    URL, data=payload, method="POST",
    headers={"Content-Type": "application/json", "Accept": "application/json"},
)
t0 = time.time()
try:
    with urllib.request.urlopen(req, timeout=12) as resp:
        body = resp.read().decode("utf-8", "replace")
    print(f"  returned in {time.time() - t0:.2f}s  HTTP {resp.status}")
    print("  body:", body[:300])
except Exception as exc:                     # noqa: BLE001
    print(f"  FAILED after {time.time() - t0:.2f}s: {type(exc).__name__}: {exc}")
