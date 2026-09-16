import asyncio, base64, json, os, sys, time
import urllib.request
import websockets

PORT = 9333
OUT = sys.argv[1]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 60
FPS = 30

def find_page():
    for _ in range(30):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json", timeout=2) as r:
                raw = json.loads(r.read())
            for t in raw:
                if t.get("type") == "page" and "logo_card" in t.get("url", ""):
                    return t.get("webSocketDebuggerUrl")
        except Exception:
            pass
        time.sleep(0.5)
    return None

async def main():
    ws_url = find_page()
    if not ws_url:
        print("FAIL: no page target"); sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    async with websockets.connect(ws_url, max_size=None) as ws:
        _id = 0
        async def send(method, **params):
            nonlocal _id
            _id += 1
            mid = _id
            await ws.send(json.dumps({"id": mid, "method": method, "params": params}))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get("id") == mid:
                    if "error" in msg:
                        raise RuntimeError(f"{method}: {msg['error']}")
                    return msg.get("result", {})
        await send("Page.enable")
        await send("Emulation.setDeviceMetricsOverride",
                   width=2292, height=1440, deviceScaleFactor=1, mobile=False)
        await asyncio.sleep(1.5)
        times = []
        got = 0
        for i in range(N):
            t0 = time.monotonic()
            r = await send("Page.captureScreenshot", format="jpeg", quality=93)
            path = os.path.join(OUT, f"f{i:04d}.jpg")
            with open(path, "wb") as f:
                f.write(base64.b64decode(r["data"]))
            times.append(time.monotonic() - t0)
            got = i + 1
        total = sum(times)
        times.sort()
        print(f"frames={got} total={total:.1f}s avg={total/got*1000:.0f}ms "
              f"med={times[len(times)//2]*1000:.0f}ms p90={times[int(len(times)*0.9)]*1000:.0f}ms")

asyncio.run(main())
