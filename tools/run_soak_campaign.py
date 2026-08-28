"""Launch the full 50-run soak campaign for all ready providers, sequentially.

Providers are soaked in rate-limit-safety order: perplexity -> claude -> grok.
ChatGPT and Gemini join after fresh app connects (their stored credentials are
stale / app-bound).

Each provider: 50 runs x (up to 10 conversations) with 30s cooldown between runs.
Results append to %APPDATA%/PerplexityExporter/soak_results.json
Progress log: C:/Users/break/Videos/TR-demo-shoot/soak_log.txt
"""

import json
import os
import subprocess
import sys
import time

APPD = os.path.expandvars(r"%APPDATA%\PerplexityExporter")
SOAK = r"C:\Users\break\Projects\TotalRecalls\tools\soak_test.py"
LOG = r"C:\Users\break\Videos\TR-demo-shoot\soak_log.txt"
ENVF = os.path.expandvars(r"%TEMP%\soak_env.json")

RUNS = 50
LIMIT = 10
COOLDOWN = 30

def main() -> int:
    env = os.environ.copy()
    if os.path.exists(ENVF):
        env.update(json.load(open(ENVF, encoding="utf-8")))

    # skip providers without creds
    needed = {"TR_SOAK_TOKEN_PERPLEXITY", "TR_SOAK_TOKEN_CLAUDE", "TR_SOAK_TOKEN_GROK"}
    missing = needed - set(env)
    if missing:
        print("missing creds:", missing)
        return 1

    for provider in ("perplexity", "claude", "grok"):
        print(f"=== starting {provider} soak ({RUNS} runs) ===", flush=True)
        cmd = [sys.executable, SOAK,
               "--provider", provider,
               "--runs", str(RUNS),
               "--limit", str(LIMIT),
               "--cooldown", str(COOLDOWN)]
        with open(LOG, "a") as lf:
            rc = subprocess.call(cmd, stdout=lf, stderr=subprocess.STDOUT, env=env)
        print(f"=== {provider} finished rc={rc} ===", flush=True)
        time.sleep(60)  # breather between providers

    print("ALL SOAK RUNS COMPLETE")
    return 0

if __name__ == "__main__":
    sys.exit(main())
