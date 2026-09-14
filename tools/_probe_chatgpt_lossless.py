"""Prove removing the order=created pass is lossless.

Replicates list_conversations(deep=True) but lets us toggle pass #2
(order=created). Runs it BOTH ways, compares the unique conversation-ID
sets. If they're identical, the created pass is pure waste (broken +
redundant) and can be removed.
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from totalrecalls.core.paths import load_session
from totalrecalls.adapters import chatgpt as C
from totalrecalls.adapters.chatgpt import conversations as CV

tok = load_session()["token"]

def deep(with_created: bool) -> set:
    seen = {}
    CV._paginate(tok, seen, order="updated", stop_event=None)
    if with_created:
        CV._paginate(tok, seen, order="created", stop_event=None)
    CV._paginate_search(tok, seen, stop_event=None)
    CV._paginate(tok, seen, is_archived=True, is_starred=False, stop_event=None)
    CV._paginate(tok, seen, is_archived=True, is_starred=True, stop_event=None)
    CV._walk_gizmos(tok, seen, stop_event=None)
    CV._walk_projects(tok, seen, stop_event=None)
    return set(seen.keys())

t0 = time.time()
with_ids = deep(with_created=True)
t1 = time.time()
without_ids = deep(with_created=False)
t2 = time.time()

print(f"\nWITH  created pass: {len(with_ids)} unique convs   ({t1-t0:.1f}s)")
print(f"WITHOUT created pass: {len(without_ids)} unique convs   ({t2-t1:.1f}s)")
missing = with_ids - without_ids
extra = without_ids - with_ids
print(f"\nOnly-in-WITH (would be lost if removed): {len(missing)}")
print(f"Only-in-WITHOUT: {len(extra)}")
if not missing:
    print("\nRESULT: removing order=created is LOSSLESS. "
          f"Saved {t1-t0-(t2-t1):.1f}s per export.")
else:
    print("\nRESULT: removing order=created WOULD lose:", list(missing)[:20])
