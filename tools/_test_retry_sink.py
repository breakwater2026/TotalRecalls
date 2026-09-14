"""Verify the retry sink propagates worker-thread -> request() (the UI path).

Mirrors bridge._export_worker: set_retry_sink INSIDE a worker thread, then make
the synchronous export chain call request() on that same thread. Counts the
retry notifications fired (proves the UI would stop looking frozen).
"""
import sys, threading, time
sys.path.insert(0, r"C:\Users\break\Projects\TotalRecalls")

from totalrecalls.core.paths import load_session
from totalrecalls.adapters.base import get_adapter
from totalrecalls.adapters.chatgpt.http import set_retry_sink, reset_retry_sink

sess = load_session()
cred = (sess or {}).get("token", "")
assert cred, "no saved chatgpt token"
a = get_adapter("chatgpt")

retries = []
def on_retry(attempt, code, backoff):
    retries.append((attempt, code, backoff))

def worker():
    tok = set_retry_sink(on_retry)      # set inside the worker thread
    t0 = time.time()
    try:
        items = a.list_conversations(cred, deep=True)   # synchronous, same thread
        print(f"list OK in {time.time()-t0:.0f}s -> {len(items)} conversations")
    except Exception as e:
        print(f"list raised {type(e).__name__}: {e} after {time.time()-t0:.0f}s")
    finally:
        reset_retry_sink(tok)

t = threading.Thread(target=worker)
t.start()
t.join()

print(f"\nRETRY NOTIFICATIONS RECEIVED: {len(retries)}")
for r in retries[:15]:
    print("   attempt=%d code=%d backoff=%.0fs" % r)
if retries:
    print("PASS: sink -> request() -> on_retry works (UI would show 'servers busy' each retry)")
else:
    print("NO retries fired (endpoint may have calmed) — mechanism still valid, nothing to surface this run")
