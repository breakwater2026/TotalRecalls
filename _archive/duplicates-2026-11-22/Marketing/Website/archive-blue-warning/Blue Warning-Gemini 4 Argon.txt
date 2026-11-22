The "blue warning" is Windows Defender SmartScreen, and for a new direct-download .exe, it is a brutal conversion killer—typically causing a 40% to 70% drop-off between download and launch.

However, your premise about the Microsoft Store taking a 15% cut is actually outdated in a way that works heavily in your favor, and there is a trick with Azure Trusted Signing to bypass the "volume catch-22."

Here is the exact breakdown of your options and the realities of each as of Microsoft's current policies.

1. The Microsoft Store Reality Check (It’s 0% Fee, Not 15%)
Microsoft overhauled its Store policies for traditional desktop apps (Win32 / .exe / .msi):

0% Revenue Share: For non-gaming apps, Microsoft allows you to use your own commerce/payment system (Lemon Squeezy, Stripe, etc.) and keep 100% of the revenue. The 15% fee only applies if you choose to use Microsoft’s built-in checkout API.
Direct Hosting: You don't even have to repackage TotalRecalls as an MSIX container if you don't want to. You can submit your existing installer URL (totalrecalls.app/.../TotalRecalls-Setup.exe), and the Store acts as a trusted catalog wrapper that downloads and installs your .exe with zero SmartScreen warnings.
One-Time Cost: An Individual Microsoft Partner Center account is $0 (Microsoft recently eliminated the $19 individual developer registration fee in most markets, including US/Canada).
Wait—what's the catch with the Store for TotalRecalls specifically?
Policy 10.8.4 and Windows Store sandboxing/review rules. Because TotalRecalls launches Playwright/Chromium (--remote-debugging-port) and extracts user conversation histories across third-party domains, a strict manual Store reviewer might flag it or ask for clarification on why it controls an external browser instance. However, because unpacked Win32 apps run with full user privileges (unsandboxed), if it passes initial certification, it works identically to your direct download.

2. The 4 Options Compared
Option
Upfront Cost
Ongoing Cut
SmartScreen Behavior
Friction / Catch
1. Unsigned .exe	$0	0%	Permanent Red/Blue Block ("Unknown Publisher"). Reset to zero on every single version update.	Kills 50%+ of trial installs. Antivirus false-positives are frequent with PyInstaller EXEs.
2. Azure Trusted Signing	$9.99 / mo	0%	Reputation carries across updates (tied to your Identity/Publisher, not the file hash).	Requires 3+ years business history for Organization validation, OR Individual validation (ID check). Still shows SmartScreen briefly until you get ~50–200 clean installs—unless you seed it (see below).
3. EV Code Signing (Hardware Token)	$350 – $600 / yr	0%	No longer gives instant bypass. Microsoft revoked instant EV SmartScreen reputation in 2024 due to malware abuse.	Expensive, annoying physical USB dongle, and still requires building reputation just like Azure/OV certs. Skip this completely.
4. Microsoft Store (BYO Commerce)	$0 (Individual)	0% (using Lemon Squeezy)	Instant 100% Bypass. Installed via Store UI or web badge with zero warnings.	Store review takes 1–3 days per release; user goes through the MS Store window to click "Install".
3. How to Beat the "Volume Catch-22" on Direct Downloads
You noted correctly that signing via Azure Trusted Signing ($9.99/mo) doesn't give instant reputation on Day 1. However, you do not need to wait for organic sales to clear the warning:

Microsoft Defender Sample Submission (The Secret Weapon):
Before you announce or run ads, you sign your PyInstaller executable + installer with Azure Trusted Signing ($9.99/mo). Then you submit the signed .exe directly to the Microsoft Security Intelligence Developer Portal (Submit a file for malware analysis → Software developer → Incorrectly detected by SmartScreen).
A Microsoft analyst/automated sandbox scans the signed binary.
Within 24 to 72 hours, Microsoft often whitelists the signed binary + publisher certificate directly in SmartScreen—bypassing the organic download threshold entirely.
Sign Both Inner .exe and Outer Installer:
Because TotalRecalls is built with PyInstaller, you must sign TotalRecalls.exe before wrapping it in your installer (Inno Setup / NSIS), and then sign TotalRecalls-Setup.exe. Because your signing identity in Azure stays constant, when you ship v1.0.1, your reputation carries over instead of resetting to zero.
4. Proposed Course of Action
Do not rely on a single channel, and do not pay 15%. Run a dual-track distribution that costs $9.99/month total and 0% commission:

Step 1: Set up Azure Trusted Signing ($9.99/mo) — Do this now
Register under Individual Validation (requires a quick mobile ID verification—driver's license/passport) or Organization Validation (if your business entity is 3+ years old).
Integrate signtool.exe with the Azure Trusted Signing dlib into your build script so both TotalRecalls.exe and the setup installer are signed automatically on every build.
Why: Even if a user downloads directly from totalrecalls.app, seeing Verified Publisher: [Your Name / Breakwater] instead of Publisher: Unknown cuts abandonment in half immediately, and allows reputation to accumulate across versions.
Step 2: Pre-Clear the Signed Binary with Microsoft Security Intelligence
As soon as your production release candidate is signed, submit it to microsoft.com/en-us/wdsi/filesubmission as the software vendor requesting SmartScreen verification.
Have 5–10 friends/devices download the signed installer from totalrecalls.app via Microsoft Edge (SmartScreen reputation only counts downloads through Edge/Windows shell) and click "Run anyway". Combined with the developer submission, this frequently clears the blue popup before your first real customer arrives.
Step 3: List on the Microsoft Store as "Free Trial" (0% Fee, Bring Your Own Licensing)
Open a free Individual account at partner.microsoft.com.
Submit TotalRecalls as a Win32 .exe app classified as "Free" (since your app runs in Free/Trial mode out of the box and unlocks via your Lemon Squeezy license key).
Because the transaction happens on totalrecalls.app via Lemon Squeezy and the user just pastes their license key into the app, Microsoft takes $0 (0%).
Put two buttons on totalrecalls.app:
[Get it from Microsoft Store] (Recommended — 1-click install, zero warnings)
[Direct Download (.exe)] (Signed with Azure Trusted Signing)
Summary Verdict
Never ship unsigned (PyInstaller .exe files without a signature get flagged by both SmartScreen and Windows Defender heuristics).
Skip $500 EV certificates (they no longer buy instant SmartScreen bypass).
Use Azure Trusted Signing ($9.99/mo) + WDSI Developer Pre-Submission for your direct .exe download.
List on the Microsoft Store with your existing Lemon Squeezy license key flow to get a 100% warning-free install channel at 0% commission.