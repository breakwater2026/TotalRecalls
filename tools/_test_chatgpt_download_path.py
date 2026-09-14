"""Headless ChatGPT download-path test using the app's real code + saved session.

Runs the exact same calls the bridge makes:
  validate -> count_conversations -> list_conversations(deep) -> fetch_conversation
Prints timing per step. Never prints the credential.
"""
import os
import sys
import time

sys.path.insert(0, r"C:\Users\break\Projects\TotalRecalls")

from totalrecalls.core.paths import load_session  # noqa: E402
from totalrecalls.adapters.base import get_adapter  # noqa: E402

t0 = time.time()
try:
    sess = load_session()
except Exception as e:
    print(f"load_session FAILED: {e}")
    sys.exit(2)
if not sess or not sess.get("token"):
    print("no session token saved")
    sys.exit(2)
cred = sess["token"]
print(f"[{time.time()-t0:6.1f}s] session loaded; saved_at={sess.get('saved_at')}, email={sess.get('email')!r}, cred len={len(cred)}, starts {cred[:12]!r}")

a = get_adapter("chatgpt")
print(f"adapter: {a.id} / {a.display_name}")

# 1) validate (connect path, same fast retry budget)
t1 = time.time()
try:
    acct = a.validate(cred)
    print(f"[{time.time()-t1:6.1f}s] validate OK: email={acct.email!r} name={acct.display_name!r}")
except Exception as e:
    print(f"[{time.time()-t1:6.1f}s] validate FAILED: {type(e).__name__}: {e}")
    sys.exit(3)

# 2) count (fast badge path)
t2 = time.time()
try:
    n = a.count_conversations(cred)
    print(f"[{time.time()-t2:6.1f}s] count_conversations OK: {n}")
except Exception as e:
    print(f"[{time.time()-t2:6.1f}s] count_conversations FAILED: {type(e).__name__}: {e}")

# 3) deep list (what the export runs)
t3 = time.time()
try:
    items = a.list_conversations(cred, deep=True)
    print(f"[{time.time()-t3:6.1f}s] list_conversations(deep) OK: {len(items)} conversations")
    for it in items[:5]:
        print(f"    - {it.id} | {it.title[:60]}")
except Exception as e:
    print(f"[{time.time()-t3:6.1f}s] list_conversations FAILED: {type(e).__name__}: {e}")
    sys.exit(4)

# 4) fetch first conversation (what the download loop does)
if items:
    t4 = time.time()
    try:
        conv = a.fetch_conversation(cred, items[0].id)
        msgs = len(conv.messages)
        chars = sum(len(m.content_md or "") for m in conv.messages)
        print(f"[{time.time()-t4:6.1f}s] fetch_conversation OK: {msgs} messages, {chars} chars")
        print("    first user msg:", (conv.messages[0].content_md or "")[:80].replace("\n", " "))
    except Exception as e:
        print(f"[{time.time()-t4:6.1f}s] fetch_conversation FAILED: {type(e).__name__}: {e}")
        sys.exit(5)

print("ALL STEPS OK")
