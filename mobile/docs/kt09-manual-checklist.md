# KT09 — Manual cross-platform checklist (teacher-required)

Teacher BASIC assignment requires **manual** testing of a public web app on different OS.  
Automation (Windows Selenium + Android Appium DOM) is **supplementary** and does **not** replace human checks.

Target: https://www.saucedemo.com/  
Demo credentials (public): `standard_user` / `secret_sauce`

Short guide: `mobile/docs/kt09-manual-execution-guide.md`

Mark each row only after a human actually performs the step.  
Until then: **PENDING HUMAN VERIFICATION**. Do not invent tester names or timestamps.

Screenshot folders (empty until human captures):

- `screenshots/kt09/manual/windows/`
- `screenshots/kt09/manual/android/`

---

## Windows 10 — Google Chrome

| ID | Steps | Expected | Actual | PASS/FAIL | Screenshot | Tester / date |
|---|---|---|---|---|---|---|
| M-W-C-01 | Open https://www.saucedemo.com/ | Login page loads; URL correct | | PENDING HUMAN VERIFICATION | | |
| M-W-C-02 | Check username/password readability | Fields visible, usable | | PENDING HUMAN VERIFICATION | | |
| M-W-C-03 | Login `standard_user` / `secret_sauce` | Inventory page opens | | PENDING HUMAN VERIFICATION | | |
| M-W-C-04 | Browse inventory cards | Names and prices visible | | PENDING HUMAN VERIFICATION | | |
| M-W-C-05 | Open a product details page | Title/description/price shown | | PENDING HUMAN VERIFICATION | | |
| M-W-C-06 | Add item to cart | Cart badge increments | | PENDING HUMAN VERIFICATION | | |
| M-W-C-07 | Open cart | Product details match | | PENDING HUMAN VERIFICATION | | |
| M-W-C-08 | Open burger menu | Logout / All Items accessible | | PENDING HUMAN VERIFICATION | | |
| M-W-C-09 | Scroll; check layout / overflow | No critical overflow; controls reachable | | PENDING HUMAN VERIFICATION | | |
| M-W-C-10 | Type and clear checkout/login fields | Inputs usable | | PENDING HUMAN VERIFICATION | | |

## Android 16 — Chrome (emulator or device)

Device reference (automation env only): `emulator-5554`, Chrome **134.0.6998.135**.  
Manual run must use the Chrome UI directly (not Appium).

| ID | Steps | Expected | Actual | PASS/FAIL | Screenshot | Tester / date |
|---|---|---|---|---|---|---|
| M-A-01 | Open saucedemo.com in Chrome | Login form visible | | PENDING HUMAN VERIFICATION | | |
| M-A-02 | Verify form readability on mobile viewport | Fields readable | | PENDING HUMAN VERIFICATION | | |
| M-A-03 | Login with demo credentials | Inventory loads | | PENDING HUMAN VERIFICATION | | |
| M-A-04 | Browse inventory | Cards visible | | PENDING HUMAN VERIFICATION | | |
| M-A-05 | Open product details | Details visible | | PENDING HUMAN VERIFICATION | | |
| M-A-06 | Add to cart | Cart state updates | | PENDING HUMAN VERIFICATION | | |
| M-A-07 | Open cart | Item details correct | | PENDING HUMAN VERIFICATION | | |
| M-A-08 | Open menu | Important actions accessible | | PENDING HUMAN VERIFICATION | | |
| M-A-09 | Scroll; check layout / touch targets | Usable; note issues | | PENDING HUMAN VERIFICATION | | |
| M-A-10 | Type in checkout/login fields | Soft keyboard / input usable | | PENDING HUMAN VERIFICATION | | |

## Comparison notes (human)

| Topic | Windows observation | Android observation | Compatibility conclusion |
|---|---|---|---|
| Login | PENDING HUMAN VERIFICATION | PENDING HUMAN VERIFICATION | |
| Cart | PENDING HUMAN VERIFICATION | PENDING HUMAN VERIFICATION | |
| Menu / layout | PENDING HUMAN VERIFICATION | PENDING HUMAN VERIFICATION | |

## Automated evidence already available (not a substitute)

| Layer | Result | Note |
|---|---|---|
| Windows Chrome/Firefox Selenium | 2 PASS | Cross-platform automation |
| Android Chrome DOM Appium | **11 PASS / 36.91s** | TC09-W01…W10 |
| Android gestures | 5 PASS / 54.93s | Supplementary |
| iOS | NOT RUN | — |

## How to complete

1. Perform each step personally on the stated platform/browser.  
2. Fill Actual / PASS/FAIL / Screenshot / Tester+date.  
3. Save screenshots under `screenshots/kt09/manual/windows/` and `.../android/`.  
4. Ask the agent to integrate completed evidence into docs/DOCX.
