"""Run the app's exact activation path in-process, with a watchdog.

If the call hangs, faulthandler dumps the Python stack after 20s and exits --
that shows precisely where it blocks, which the app's own log cannot.
"""
import faulthandler
import json
import sys
import time

sys.path.insert(0, r"C:\Users\break\Projects\TotalRecalls")

faulthandler.dump_traceback_later(20, exit=True)   # hang -> stack dump, then exit

import totalrecalls.licensing as L                 # noqa: E402

print("endpoint      :", L.LICENSE_VERIFY_ENDPOINT)
print("User-Agent    :", L.USER_AGENT)
t0 = time.time()
print("machine_id    :", L.machine_identity(), "(%.2fs)" % (time.time() - t0))

t0 = time.time()
try:
    res = L.activate_license("TR-TKAEDYFC-RDUZ-EZFG")
    print("activate_license: %.2fs" % (time.time() - t0), json.dumps(res))
except Exception as exc:                            # noqa: BLE001
    print("activate_license RAISED after %.2fs: %s: %s" % (time.time() - t0, type(exc).__name__, exc))

faulthandler.cancel_dump_traceback_later()
print("is_pro now    :", L.is_pro(), "| tier:", L.tier_name())
