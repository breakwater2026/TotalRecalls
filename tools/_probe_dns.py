"""Byte-exact DNS check for the Resend records.

Prints the RAW TXT string list (no quote stripping — stripping quotes is exactly
how a quoting bug hides) and compares the DKIM value byte-for-byte with what
Resend expects. Queries the authoritative Cloudflare nameservers directly, plus
two public resolvers, and repeats to expose flapping.
"""
import json
import re
import os
import subprocess
import sys

import dns.resolver

DKIM = "resend._domainkey.totalrecalls.app"
AUTH_NS = ["collins.ns.cloudflare.com", "walt.ns.cloudflare.com"]
PUBLIC = ["1.1.1.1", "8.8.8.8"]
NEW_ID = "17ddfee6-8be0-4140-b25d-e082393cf841"

# dnspython wants nameserver IPs, so resolve the Cloudflare NS hostnames first.
auth_ips = []
for host in AUTH_NS:
    try:
        auth_ips += [(host, str(rr)) for rr in dns.resolver.resolve(host, "A")]
    except Exception as exc:                                      # noqa: BLE001
        print("could not resolve %s: %s" % (host, exc))

KEY = None
env_path = os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes", ".env")
for line in open(env_path, encoding="utf-8", errors="replace"):
    if re.match(r"\s*RESEND", line, re.I):
        KEY = line.split("=", 1)[1].strip().strip('"').strip("'")

# What Resend generated for the freshly re-added domain.
r = subprocess.run(["curl", "-sS", "-m", "30", f"https://api.resend.com/domains/{NEW_ID}",
                    "-H", f"Authorization: Bearer {KEY}"], capture_output=True, text=True)
expected = ""
try:
    dom = json.loads(r.stdout)
    expected = next((x.get("value") for x in dom.get("records", []) if x.get("record") == "DKIM"), "") or ""
except Exception as exc:                                          # noqa: BLE001
    print("resend fetch failed:", r.stdout[:120], exc)
print("Resend expects DKIM (%d chars): %s..." % (len(expected), expected[:40]))


def query(name, rtype, server=None, repeat=2):
    res = dns.resolver.Resolver(configure=False)
    res.nameservers = [server] if server else dns.resolver.Resolver().nameservers
    res.timeout = 8
    res.lifetime = 12
    out = []
    for _ in range(repeat):
        try:
            ans = res.resolve(name, rtype)
            vals = []
            for rr in ans:
                if getattr(rr, "strings", None):
                    vals.append(("".join(s.decode("utf-8", "replace") for s in rr.strings),
                                 len(rr.strings)))
                else:
                    vals.append((rr.to_text().strip('"'), 1))
            out.append(vals)
        except dns.resolver.NXDOMAIN:
            out.append("NXDOMAIN")
        except dns.resolver.NoAnswer:
            out.append("NOANSWER")
        except Exception as exc:                                  # noqa: BLE001
            out.append(type(exc).__name__)
    return out


print("\n=== DKIM TXT, raw strings, from each server (x2 to expose flapping) ===")
clean_ok = 0
total = 0
targets = [(f"{h} ({ip})", ip) for h, ip in auth_ips] + [(ip, ip) for ip in PUBLIC]
for label, srv in targets:
    for g in query(DKIM, "TXT", srv):
        total += 1
        if isinstance(g, list) and g:
            for val, n_strings in g:
                exact = val == expected
                clean_ok += 1 if exact else 0
                print(f"  {label:28} charstrings={n_strings} len={len(val)} exact={exact}")
        else:
            print(f"  {label:28} -> {g}")

print("\n=== other records (authoritative) ===")
for name, typ in (("send.totalrecalls.app", "TXT"), ("send.totalrecalls.app", "MX"),
                  ("rsend.totalrecalls.app", "CNAME"), ("_dmarc.totalrecalls.app", "TXT"),
                  ("totalrecalls.app", "TXT")):
    got = query(name, typ, auth_ips[0][1] if auth_ips else None, repeat=1)[0]
    print(f"  {typ:5} {name:32} {got}")

print("\nVERDICT: DKIM exact-and-clean at %d/%d answers." % (clean_ok, total))
sys.exit(0 if clean_ok else 1)
