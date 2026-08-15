# Debugging MT5 TF RiskManager script with Grok fixes

- **Provider:** claude
- **Account:** adenis258@gmail.com
- **Folder:** Home
- **ID:** 8e1f9b7a-ef09-4f1d-9330-0ec51a4d2906
- **Created:** 2026-03-02T21:35:04.709297Z
- **Updated:** 2026-03-06T17:39:07.451156Z

---

## Q1: Attached are two documents 1. a TF RiskManager script file for MetaTrader 5 (MT5). This is a script that allows to monit

Attached are two documents 1. a TF RiskManager script file for MetaTrader 5 (MT5). This is a script that allows to monitor the risks taken while trading for Trading Funds a $10K account. This account is under tight risk limitations and the breach of one risk parameter (DLL, TLL, TF Shield) results in the liquidation of the account. The current running script has bugs in it. 2. a Grok AI text file containing the fixes to the various bugs. These snippets have to be integrated into the main script and build v14.33.  I have no coding experience. So please read carefully Grok's corrective snippets and implement them.

Now let me read the key sections of the original script that need to be modified:

---

## Q2: Attached are two documents 1. a TF RiskManager script file for MetaTrader 5 (MT5). This is a script that allows to monit

Attached are two documents 1. a TF RiskManager script file for MetaTrader 5 (MT5). This is a script that allows to monitor the risks taken while trading for Trading Funds a $10K account. This account is under tight risk limitations and the breach of one risk parameter (DLL, TLL, TF Shield) results in the liquidation of the account. The current running script has bugs in it. 2. a Grok AI text file containing the fixes to the various bugs. These snippets have to be integrated into the main script and build v14.33.  I have no coding experience. So please read carefully Grok's corrective snippets and implement them.

Now I have a thorough understanding of both files. Let me implement all the changes precisely:
**Change 1 — Header: version + copyright + description**
**Change 2 — Forward declarations: add new panel helper function declarations**
**Change 3 — Fix `RecalculateBuffers()`: replace the DLL and TF Shield buffer calculations with the correct Grok version**
Now I need to find the end of `CreateTransparentPanel()` so I can replace the whole function. Let me find its exact boundaries:
Good. Now I'll replace the entire `CreateTransparentPanel()` body and, right after it, inject all the new helper functions plus `UpdateRiskPanel()`:
**Change 4 — OnTick: replace `CreateTransparentPanel()` call in the GUI throttle with `UpdateRiskPanel()`**
**Change 5 — OnInit: add `RecalculateBuffers()` call after `RecalculateLimits()`**
**Change 6 — OnInit: update the startup log messages to v14.33**
**Change 7 — OnDeinit: update version string**
Now let's do a final sanity check to make sure all critical pieces are in place:
Everything checks out. Let me copy the file to outputs:
**v14.33 is ready.** Here's a precise summary of every change applied from Grok's instructions:

---

### What was changed

**Bug Fix 1 — DLL Buffer calculation (the core fix)**
The old code computed `Buffer_DLL = equity - DLL_BreachLevel`, but `DLL_BreachLevel` could be pushed upward by the Profit Ratchet (when daily gains locked in). This caused the buffer to collapse even with a profitable day.

The fix: `Buffer_DLL = equity - (PriorDayClose - DLL_FixedAmount)` — always calculated from the true daily start point, regardless of ratchet activity.

**Bug Fix 2 — TF Shield buffer calculation**
Previously used *floating open-loss* against the shield limit (giving false warnings when positions are in profit). Now also uses the daily baseline: `Buffer_TF = equity - (PriorDayClose - tf_fixed)` — consistent with DLL logic.

**New — Professional GUI panel (`CreateTransparentPanel`)**
Completely replaced with a clean, consistent layout: semi-transparent dark background, uniform button heights/widths, Segoe UI fonts, proper 2-column label/value alignment, and section headers.

**New — `UpdateRiskPanel()` function**
A lightweight function called every tick that only updates text/colours on existing panel objects (instead of rebuilding everything). Values update dynamically with colour coding: green = safe, orange = warning (20–50%), red = critical (<20%).

**New — 6 panel helper functions**
`CreatePanelLabel`, `CreatePanelButton`, `CreatePanelEdit`, `CreatePanelHeader`, `CreatePanelInfo`, `CreatePanelPosLine` — clean, reusable building blocks used by the new panel.

**All original features untouched** — ZigZag, news filter, partial TP, smart entry, settings panel, position monitoring, ratchet, tilt protection, etc.

### How to install
1. In MT5, open **MetaEditor** (F4)
2. Open `TF-RiskManager-v14_33.mq5`
3. Press **Compile** (F7) — should compile with 0 errors
4. Drag the EA onto your chart (or re-attach if already running)

---

## Q3: see attached compilation errors log

see attached compilation errors log

The error is clear — all `ObjectSetString` calls in `UpdateRiskPanel` are missing the required `OBJPROP_TEXT` property parameter. MQL5 requires 4 arguments: `ObjectSetString(chart_id, name, OBJPROP_TEXT, value)`.
All remaining `ObjectSetString` calls without `OBJPROP_TEXT` are correctly using `OBJPROP_FONT` — those are fine. Let me verify the fix looks correct:
All correct. Let me copy the fixed file to outputs:
**Fixed.** All 35 errors were caused by the same single mistake: `ObjectSetString` in MQL5 requires **4 parameters**, not 3:

```
// ❌ Wrong (3 params — what was generating all the errors)
ObjectSetString(0, "ACC_EQUITY_VAL", "$10,334.36");

// ✅ Fixed (4 params — OBJPROP_TEXT inserted as 3rd argument)
ObjectSetString(0, "ACC_EQUITY_VAL", OBJPROP_TEXT, "$10,334.36");
```

All 33 affected calls in `UpdateRiskPanel()` have been corrected. The `ObjectSetString` calls using `OBJPROP_FONT` elsewhere in the file were already correct and were left untouched. Recompile and it should be 0 errors, 0 warnings.

---

## Q4: see attached remaining compilation errors log

see attached remaining compilation errors log

The issue is that `OBJPROP_TRANSPARENCY` is not supported for `OBJ_RECTANGLE_LABEL` in MQL5. The dark background color `C'25,25,35'` already achieves the visual intent. Simple fix — remove that one line.
**Fixed.** The 3 errors were all caused by one line:

```mql5
// ❌ Removed — OBJPROP_TRANSPARENCY is not supported for OBJ_RECTANGLE_LABEL
ObjectSetInteger(0, bg, OBJPROP_TRANSPARENCY, 85);
```

`OBJ_RECTANGLE_LABEL` in MQL5 doesn't support transparency via a property — it's controlled purely through the background color. The panel background `C'25,25,35'` (a very dark navy) combined with `OBJPROP_BACK = true` already renders it as a clean, dark, unobtrusive overlay on the chart. Recompile — should be 0 errors, 0 warnings.

---

## Q5: We are getting closer. A few more cosmetic changes: 1. directly underneath the Buy/Sell/Market  line you have Size/SL Pi

We are getting closer. A few more cosmetic changes: 1. directly underneath the Buy/Sell/Market  line you have Size/SL Pips and underneath that line you have TP pips. I suggest having a line for size (with the box) but a bit lower so that it is not overaken by the Buy/Sell/Market buttons line. Right underneath we should have SL  (pips) and TP (pips).  2. At this point we do not have the 2 required pips levels for the Trailing order. They should be underneath the SL and TP line, the two of them on the same line. The two Trailing Order variables a new and need to be connected to the script. 3. Visually, the Output GUI characters are too small. Adjusting manually the GUI size in the parameter input panels does not change the size of those parameters.

Now I have a complete picture. Let me implement all three fixes at once:
1. Layout: Size → SL → TP → Trailing (each on own lines)  
2. Trailing Distance + Activation edit boxes connected to `Runtime_TrailingDistance`/`Runtime_TrailingActivation`
3. Font scaling: all text scales with `Runtime_GuiScale`
Now add the trailing edit box event handlers to `OnChartEvent`:
Now add `BTN_SmartBuy` / `BTN_SmartSell` forward declaration if needed, and also update the forward declarations to include the new `CreatePanelButton` signature with fsize:
The forward declarations need updating to match the new signatures:
Now verify no leftover references to the old "BTN_BUY"/"BTN_SELL" button names that aren't handled, and confirm the complete handler chain is clean:
All connections are clean. Let's do a final check for any remaining `ObjectSetString` calls still missing `OBJPROP_TEXT`:
Zero violations. All good.
Here's everything that was changed:

---

### Fix 1 — Input field layout (4 clean rows)
Each field now has its own dedicated row, in this order:
- **Size (lots)** — edit box
- **SL (pips)** — edit box
- **TP (pips)** — edit box
- **Trail Dist: ___ pips | Act: ___ pips** — both on the same row

---

### Fix 2 — Trailing order fields connected to the script
- `EDIT_TRAIL_D` reads/writes `Runtime_TrailingDistance` (used by `MonitorPositions` trailing logic)
- `EDIT_TRAIL_A` reads/writes `Runtime_TrailingActivation` (the activation threshold)
- Both fire on `CHARTEVENT_OBJECT_ENDEDIT` — type a value, press Enter, it takes effect immediately for all monitored positions

---

### Fix 3 — Font scaling now works
Three root causes were fixed:
1. Font sizes are now computed as `(int)(9 * Runtime_GuiScale)` before being passed to helpers — so changing GuiScale from 1.0 to 1.5 scales all text proportionally
2. All property updates (`FONTSIZE`, `XDISTANCE`, `YDISTANCE`) are now applied **every call**, not just on object creation — so a scale change takes effect immediately when the panel rebuilds
3. The panel background also deletes and recreates itself on each `CreateTransparentPanel()` call so dimensions rescale correctly

---

## Q6: 3 issues to resolve. 1. See attached error log. 2. Also could you rename the script "TF RiskManager v.14.34" and 3. the 

3 issues to resolve. 1. See attached error log. 2. Also could you rename the script "TF RiskManager v.14.34" and 3. the attached image shows a slightly lighter dark background color de show that it is a GUI panel. Adjust that box to cover all the GUI outputs lower.

Found the root cause. MQL5 forbids default parameter values in forward declarations — they belong only on the actual definition. Now fixing all three issues at once:
All clean. Delivering the file:
Here's exactly what was fixed:

---

### Fix 1 — "event handling function not found" compilation error
**Root cause:** MQL5 strictly forbids default parameter values (`= 9`, `= true`, `= 118`, etc.) in forward declarations — they are only allowed on the actual function definition. The 5 affected declarations were:
```
// ❌ MQL5 won't accept this in a forward declaration:
void CreatePanelLabel(..., int fsize=9, bool bold=false);

// ✅ Fixed — defaults removed from declaration, kept only on definition:
void CreatePanelLabel(..., int fsize, bool bold);
```

---

### Fix 2 — Renamed to v14.34
All 7 version references updated: header comment, `#property version`, title label, startup log, shutdown log, and internal print messages.

---

### Fix 3 — Lighter background + full coverage
- Background color changed from `C'25,25,35'` (near-black) to `C'45,45,62'` (visible dark slate — matches the style shown in your reference image)
- Initial panel height set to `900 × GuiScale` so it never clips during the first render frame
- Final auto-resize margin increased from 60px to 80px so the open positions list never gets cut off at the bottom

---

## Q7: You strayed away from the Grok GUI formatting (which was nearly perfect, all columns well line up, clean and equal dista

You strayed away from the Grok GUI formatting (which was nearly perfect, all columns well line up, clean and equal distance between the lines, crisp (but to small) letters to the attached. Please go back to the method used by Grok (see Grok modifications v14.32) as the perfect coding for laying out the GUI. Also, please change the name of the file in the header on top of the output GUI box to TF RiskManager v14.34.

Now I have Grok's exact approach. Let me read the current file's panel+helpers block to replace it cleanly.

All 15 checks pass, zero errors. The file from the previous step was already correct — the response got cut off before I could present it. Here it is:
Here's what was restored to Grok's exact methodology:

**Layout engine — back to Grok's approach:**
- Single `lbl_w = (int)(135 * s)` constant → `val_x = x + lbl_w + pad` → every value label on the **exact same column X**, no exceptions. This is what gave Grok's version its clean aligned look.
- `row = (int)(22 * s)` uniform row height — every `y += row` advances identically, giving equal spacing throughout.
- All section spacers are `y += 6` or `y += 8`, matching Grok's tight, consistent gaps.

**Title:** Changed to `TF RiskManager v14.34` as requested.

**Background:** `C'32,32,48'` — visibly dark slate (distinct from the chart) with a `clrSlateGray` border outline.

**Font scaling:** Font sizes computed as `(int)MathRound(9 * s)` before being passed in, so increasing `GuiScale` in the input parameters enlarges all text proportionally.

**All new fields preserved:** Size / SL / TP each on their own row, Trailing Dist + Trailing Act on one shared row, all wired to their runtime variables.

---

## Q8: Did not work. See image

Did not work. See image

Found the root cause — when `CreateTransparentPanel()` is called, it only deletes the background rect but **not the old label/button/edit objects**. Old objects persist from previous versions loaded on the chart, and since `ObjectFind()` finds them still existing, only position/size updates run — but the old text/sizing from a different scale remains. The fix: **delete all panel objects before rebuilding**.
**Root cause identified and fixed.** The issue was a classic MT5 rendering trap:

**The real problem:** `CreateTransparentPanel()` only deleted the background rectangle (`TF_MAIN_BG`) on each call, but left all old label, button, and edit objects alive from the previously loaded version. When `ObjectFind()` found them still existing, only `XDISTANCE`/`YDISTANCE`/`XSIZE` were updated — but the objects kept their OLD text content, old font sizes, and old visual properties from whatever version was previously on the chart. This caused the garbled/truncated appearance.

**The fix:** A full teardown at the top of `CreateTransparentPanel()` — `ObjectsDeleteAll()` on every prefix (`TF_`, `BTN_`, `LBL_`, `HDR_`, `ACC_`, `LIM_`, `RISK_`, `GUI_EDIT_`, `EDIT_TRAIL_`, `MON_PL_`) — then every object is recreated from scratch with the correct current values. This also means **GuiScale changes now take full effect immediately** after reattaching the EA.

**Also widened** the panel (`310×s`) and buttons (`big_w=130`, `mkt_w=80`) to ensure no text is ever truncated regardless of scale or display DPI.

---

## Q9: his is the continuity of an aborted session. We are dealing with an identified but persistent problem on this Meta Trade

his is the continuity of an aborted session. We are dealing with an identified but persistent problem on this Meta Trader 5 (MT5) .mq5 script. To better understand what stage we are at, attached are three documents: 1. A copy of the preceding conversation on the topic as contextual information, 2. the TF RiskManager v14.12 script and the TF RiskManager v15.2 script.

Let me read all three files carefully before touching any code.

Let me read both source files thoroughly before writing a single line of code.

I have the full context. Let me read v14.12's GUI helpers before writing a single line of code.
Good. I have a complete picture. Now I'll build the fix in one deterministic pass.

**Root cause confirmed:** v15.2's data-driven settings architecture (`ENUM_INPUT_VARS`, `SetInputVarFromString`, `g_input_settings[]` loop) does not correctly propagate typed values back to runtime variables. v14.12's direct per-field ENDEDIT handlers are proven to work. My job is to transplant the entire v14.12 settings engine into v15.2 cleanly, with zero brace imbalance.
I have all the data I need. Now I'll build the replacement script — bottom-to-top so line numbers stay valid.

Let me read both files thoroughly before writing a single line of code.
Now let me read the v14.12 version to understand its architecture:
Now let me read the critical `UpdateRiskPanel()` function to find the overwrite bug:
Now let me look at `OnTick` to find the overwrite path:
Now I have a complete picture. The root cause is clear. Let me implement the precise fixes:
**Fix 1 — Core bug: toggle click calls `CreateSettingsPanelObjects()` which destroys unsaved user input:**
**Fix 2 — UpdateSettingsPanel becomes buttons-only (eliminates the race condition permanently):**
**Fix 3 — Version banner references in OnInit still say "15.0":**
**Fix 4 — ENDEDIT handler: after updating a SET_EDIT_ field via SetInputVarFromString, call UpdateSettingsPanel (buttons-only) to refresh button states without nuking edit boxes:**

**Fix 5 — Add ENDEDIT handler for the EDIT_TRAIL_D and EDIT_TRAIL_A edit boxes (from the v14.34 panel):**
Good — v15.2 doesn't use those boxes. Now verify the final state of all fixes:
11/11. Copy to output:
**11/11 checks pass.** Here is exactly what was wrong and what was fixed:

---

**Root cause — one function doing two incompatible jobs**

The `UpdateSettingsPanel()` function was being called from two contexts:
1. **Toggle button clicks** — to refresh ON/OFF button colours
2. **Per-tick OnTick** — to sync edit boxes to runtime values

The problem: every call re-ran a data-driven loop that deleted and re-created every `SET_EDIT_*` box — overwriting whatever the user had typed with the stale `Runtime_*` value. This is why you could type a number and it would immediately revert.

---

**Fix 1 — Toggle handler** (`OnChartEvent`, BTN_ block)
The toggle button handler was calling `CreateSettingsPanelObjects()`, which rebuilds the entire settings panel from scratch including all edit boxes, discarding any typed-but-unsaved values. Changed to call `UpdateSettingsPanel()` (buttons-only) instead.

**Fix 2 — `UpdateSettingsPanel()` made buttons-only**
Replaced the data-driven edit-box loop with a loop that only updates the `BTN_MON`, `BTN_TRL`, etc. ON/OFF text and colour. Edit boxes are now written exactly once (when the panel opens) and kept alive until the user either commits via Enter (`CHARTEVENT_OBJECT_ENDEDIT`) or closes the panel (`SaveSettingsFromPanel`). No more race condition.

**Fix 3 — Version banner**
Print statement in `OnInit` corrected from `v15.0` to `v15.2`.

---

## Q10: Did not work, the numerical  variables inputs are still inactive.  For troubleshooting purpose, I ran v14.12 (numerical 

Did not work, the numerical  variables inputs are still inactive.  For troubleshooting purpose, I ran v14.12 (numerical input parameters active) and created a breach condition that forces the liquidation and block the account from trading. Despite this most punitive condition, I was able to change the numerical input variables. Since v14.12 works, I suggest you redo your comparative analysis and determine what makes the input numerical variables to be inactive.

Let me do a surgical, line-by-line comparison of exactly how v14.12 handles edit boxes vs v15.2.

Let me do this properly. I'll read both files completely fresh, side by side, focusing only on the exact mechanisms that control edit box interactivity.

Let me read both files completely fresh — OnTick, OnChartEvent, and the full settings panel flow, side by side.
Let me look at OnInit in both files, and then carefully read the full AddSettingsRow and CreateField functions.
Let me look at the actual var_id mapping in SetInputVarFromString:
Let me look at the g_input_settings and g_toggle_settings arrays to understand what fields exist in the settings panel:
Let me read v14.12's UpdateSettingsPanel and ToggleSettingsPanel completely:
Found it. Now I have a clear picture. Let me document the complete diagnosis before writing any code:
Now I have the definitive root cause. It's **three distinct bugs**, not one:

**Bug 1 — `RecalculateLimits()` overwrites user values (lines 1504-1505):**
Every call to `RecalculateLimits()` forces `Runtime_DailyLossLimitPct = 5.0` and `Runtime_MaxTrailingDDPct = 8.0`. `SetInputVarFromString` saves the user's typed value, then immediately calls `RecalculateLimits()` which wipes it. The user's input is destroyed before the settings panel even redraws.

**Bug 2 — `DLL_BreachLevel` is calculated from user value then silently overwritten:** Lines 1470-1473 calculate `DLL_BreachLevel` using `Runtime_DailyLossLimitPct` (user value), but line 1507 then overwrites `DLL_FixedAmount` with the TF value without recalculating `DLL_BreachLevel`. The actual breach level is frozen at whatever the input parameter was.

**Bug 3 — Original race condition (my previous fix):** Toggle buttons call `CreateSettingsPanelObjects()` which deletes/rebuilds all edit boxes. Already fixed.
Now remove the `g_active_edit_object != ""` early return from OnTick — it's unnecessary (UpdateRiskPanel never touches edit boxes) and could mask future issues:
Now verify all fixes are in place and brace balance is intact:
Good — ordering is correct. Let me do the full clean verification:
