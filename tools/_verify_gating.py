"""Verify free/Pro gating logic (no network): edition flag drives is_pro,
provider gating, and conversation limit."""
import sys
sys.path.insert(0, r"C:\Users\break\Projects\TotalRecalls")
import totalrecalls.licensing as L
from totalrecalls import edition

print("=== FREE edition (no stored key) ===")
edition.is_pro_edition = lambda: False
print("is_pro() =", L.is_pro(), "| tier =", L.tier_name())
for pid in ["perplexity", "chatgpt", "claude", "grok", "gemini", "deepseek", "mistral", "qwen"]:
    print(f"   {pid:12} pro_only={L.provider_is_pro_only(pid)}")
print("   FREE_CONVERSATION_LIMIT =", L.FREE_CONVERSATION_LIMIT)
print("   FREE_PROVIDER_IDS =", L.FREE_PROVIDER_IDS)

print("\n=== PRO edition (baked-in) ===")
edition.is_pro_edition = lambda: True
print("is_pro() =", L.is_pro(), "| tier =", L.tier_name())
print("   (all 8 providers + unlimited — is_pro() True bypasses gating)")

print("\n=== key-format validation ===")
for k in ["", "abc", "TR-1234-ABCD", "x" * 40]:
    print(f"   {k[:12]!r:14} valid_format={L.validate_license_key_format(k)}")
