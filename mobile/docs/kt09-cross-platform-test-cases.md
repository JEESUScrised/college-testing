# KT09 — Cross-platform test cases

## Android Chrome DOM (Appium + ChromeDriver 134.0.6998.165)

Suite: `mobile/tests/test_kt09_android_chrome_dom.py`  
Device: `emulator-5554` / Chrome 134.0.6998.135  
**Result 2026-10-11:** **11 passed in 36.91s** (DOM assertions)

Screenshot capability for future DOM re-runs: `appium:nativeWebScreenshot=false`  
(Previous `true` produced GPU-corrupted PNGs — removed from the tracked tree; not used as evidence.)

| ID | Case | Expected | Actual | Status |
|---|---|---|---|---|
| TC09-W01 | Website loading | saucedemo.com + logo | OK | **PASS** |
| TC09-W02 | Login form usable | inputs enabled | OK | **PASS** |
| TC09-W03 | Successful auth | inventory / Products | OK | **PASS** |
| TC09-W04 | Inventory listing | ≥6 names + $prices | OK | **PASS** |
| TC09-W05 | Product details | name/price match | OK | **PASS** |
| TC09-W06 | Add to cart | badge=1 | OK | **PASS** |
| TC09-W07 | Cart navigation | item in cart | OK | **PASS** |
| TC09-W08 | Checkout validation | First Name required | OK | **PASS** |
| TC09-W09 | Burger menu | inventory + logout links | OK | **PASS** |
| TC09-W10 | Mobile layout | no horizontal overflow | OK | **PASS** |
| journey | Compact regression | inventory ≥6 | OK | **PASS** |

## Canonical visual comparison (submission)

Eight matching scenarios — **AUTOMATED** only:

`screenshots/kt09/automated/windows/` ↔ `screenshots/kt09/automated/android/`  
See `mobile/docs/kt09-platform-comparison.md` and `reports/KT09.docx`.

## Windows desktop (Selenium)

| ID | Case | Chrome | Firefox | Visual evidence |
|---|---|---|---|---|
| XP-W-01/02 | Login + inventory | PASS | PASS | `automated/windows/*.png` |

## Gestures (historical ApiDemos)

5 PASS / 54.93s — preserved; not a substitute for BASIC public-web OS testing.  
Gesture PNGs remain under `screenshots/kt09/*.png` (Views/Gallery).

## Manual (teacher-required)

See `kt09-manual-checklist.md` → **PENDING HUMAN VERIFICATION**.
