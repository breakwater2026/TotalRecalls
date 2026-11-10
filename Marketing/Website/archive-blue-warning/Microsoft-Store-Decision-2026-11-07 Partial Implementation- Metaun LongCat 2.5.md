Microsoft Store Strategy Implmentation-Metaun-LongCat 2.5


Done — both changes are in the repo and verified by real builds.

What changed
File
Change
TotalRecalls.spec	Reads TR_BUILD_MODE (onefile default / onedir) and emits either the single EXE or a COLLECT folder. Default behaviour unchanged.
tools/build_exe.py	New --mode {onefile,onedir} flag, correct output path per mode, edition flag still restored after build.
tools/generate_msix_assets.py	New — extracts the square app icon from logo_Final.png and generates the full Store asset set.
msix/Package.appxmanifest	New — desktop-app manifest with runFullTrust, tile/splash references, placeholders marked for your Partner Center publisher CN.
msix/Assets/	New — 11 PNGs (square 44→310, StoreLogo, Wide310x150, Splash 620x300), navy #263343.
msix/README.md	New — build, package, test and submit steps.
Verified
--mode onedir   → dist\TotalRecalls\TotalRecalls.exe  (7.2 MB) + _internal\  (26 MB total)
--mode onefile  → dist\TotalRecalls.exe               (21 MB)   ← unchanged default
Both succeeded, and edition.py was correctly restored to "free" afterwards. I restored the tracked dist/TotalRecalls.exe that my test build overwrote.

One environment problem you should know about
Your .venv is Python 3.15.2 but contains 169 cp311 native binaries — it was upgraded in place, so most C extensions no longer load. The build only worked after I reinstalled numpy (2.3.5 → 2.5.4); the failure was PyInstaller's isolated subprocess dying on numpy.

Other stale packages remain (aiohttp, pydantic_core, regex, markupsafe, PIL, curl_cffi, and more). The build succeeded because PyInstaller excludes most of them, but any future build or test run may hit the next broken one.

There is no requirements.txt in the repo, so a clean venv rebuild isn't a one-liner. Worth doing properly at some point — and worth adding a requirements.txt so the build environment is reproducible.

Next steps
Replace the publisher placeholders in msix/Package.appxmanifest once Partner Center issues your CN.
Build with --mode onedir.
Package via Visual Studio's MSIX project (the README walks through it).
Submit — the app is listed free, so Paddle/Worker/Resend stay exactly as they are.
Want me to add a requirements.txt and rebuild the venv