Technical Note: Gemini Live API Reverse-Engineering Attempt
Goal
Enable authenticated export of Gemini conversations via clients6.google.com/feeds/ RPC endpoint using cookies captured from the embedded WebView2 login flow.

What We Tried
1. URL Construction

Bug: URL path missing / separator (clients6.google.comfeeds/ instead of clients6.google.com/feeds/)
Fix: Ensure rpc_path starts with /, base_url doesn't end with /
Status: ✅ Resolved
2. RPC Body Format

Attempt 1: Raw JSON array body ["gemini.conversation.list", {"page_size": 100}] with Content-Type: application/json
Result: HTTP 400
Attempt 2: f.req=[[""]] form-encoded with Content-Type: application/x-www-form-urlencoded
Result: HTTP 400
Attempt 3: f.req=[[""]] with X-Goog-Visitor-Id, X-Goog-AuthUser, X-Goog-AuthServer, X-Goog-AuthMethod headers
Result: HTTP 400
Status: ❌ Unresolved — body format is wrong
3. Cookie Completeness

Bug: WebView2 CookieManager.GetCookies() only returned cookies scoped to gemini.google.com — missing .google.com parent-domain cookies needed for clients6.google.com
Fix: Added explicit GetCookies("https://www.google.com/") and GetCookies("https://accounts.google.com/") calls
Status: ✅ Implemented (untested)
4. Consent Cookies

Missing: CONSENT and SOCS cookies not found in user's cookie export
Fix: Auto-inject CONSENT=YES+placeholder and SOCS=0 in _make_rpc_request()
Status: ✅ Implemented but untested (Google may reject placeholder values)
Known Unknowns
at_token: The thykhd config key from page HTML should provide an at= auth token for the RPC URL, but extraction success is unverified
Google RPC protocol: The clients6.google.com/feeds/<hash> endpoints may require a completely different wire format (protobuf, gzipped, etc.) that can't be determined without observing actual browser traffic
Error 400: Google returns "Bad Request" for all body format attempts — this could mean missing required headers, wrong compression, or truly wrong body structure
Environment
API endpoint: https://geminiweb-pa.clients6.google.com/feeds/mcudyrk2a4khkz?key=AIza...
Auth method: Session cookies from gemini.google.com/app login via WebView2
UA: Chrome 131 (via curl_cffi impersonation)
Response: HTTP 400 "Bad Request" (Google's standard error page, no JSON body)

Latest Build: 42,883,328 bytes (commit 2279e0d at 19:05)
What we now know (from the user's cookie dump):
The cookies include __Secure-1PSID, SID, SAPISID, HSID, APISID, NID, SIDCC, OTZ — but no CONSENT or SOCS cookies. These are set on .google.com domain.

What we've tried (15+ iterations):
URL construction (fixed / separator) ✅
Config key extraction (HUGNlb, qKIAYe, thykhd/SNlM0e) ✅
Multi-domain cookie capture (www.google.com + accounts.google.com) ✅
SAPISIDHASH auth header ✅
Multiple RPC body formats:
f.req=[[""]] (batchexecute format) → 400
f.req=[["", params, null, "generic"]] (data-4 format) → 400
Raw JSON [[["", params]]] (ProtoRPC format) → 400
Binary protobuf → not tested
Content-Type: application/x-protobuf, application/x-www-form-urlencoded;charset=UTF-8 → both 400
Headers: X-Same-Domain, X-Goog-BatchExecute-Path, `Authorization: *** → 400
CONSENT/SOCS: Auto-injected, manually injected, removed → all 400

The 400 error is Google's standard "Bad Request" HTML page (Error 400 (Bad Request)!!1)
Root cause analysis (per Perplexity + Grok 4.5):
The /feeds/<hash> endpoint at clients6.google.com requires a specific binary protobuf format that cannot be reliably guessed. The format varies by endpoint and changes when Google updates their internal APIs.

What's needed for success:
Capture the actual browser request as cURL from Chrome DevTools Network tab when loading the conversation list on gemini.google.com/app. The exact Content-Type, body format, and headers must be replicated byte-for-byte.

Grok 4.6 Review (interrupted)

I'll start by loading the workspace skill, reading your Gemini login-hurdle note, and inspecting the current Gemini adapter so we can see where auto-download still fails.
The note is clear: Gemini still 400s on the Live API while the other four providers work. I’ll load the workspace skill, then inspect the Gemini adapter, current diffs, and how the working providers authenticate.
The 400s match a guessed RPC body, not a cookie problem. Next I’ll compare the working providers, the WebView2 login path, and current Gemini research so we can copy a real request instead of guessing.
The 400s look like a malformed RPC, not a login failure. I’ll inspect the login capture path, the current Gemini diff, and public clients that already talk to the same Gemini web endpoints.
Cookie capture is likely fine; the live Gemini path still invents an RPC body. I’ll inspect the CDP login pattern we already use and public Gemini web clients so we can replay a real request instead of guessing.
gemini-webapi already implements list_chats and read_chat with the same cookies we capture. I’ll pull that source and wire the same working request path into our adapter instead of guessing /feeds/ protobuf.
The working clients use BardChatUi batchexecute, not clients6.google.com/feeds/. I’ll pull the public RPC IDs and chat-list flow so we can call the same endpoint the Gemini page already uses.
The 400s came from posting RPC bodies to a push-feed id (qKIAYe = feeds/mcudyrk2a4khkz), not the conversation API. I’ll switch the live path to BardChatUi batchexecute and fix Gemini cookie capture so we actually send a complete session.

