# KT09 — Manual cross-platform checklist (teacher-required)

Teacher BASIC assignment requires **manual** testing of a public web app on different OS.  
Automation (Windows Selenium + Android Appium DOM) is **supplementary** and does **not** replace human checks.

Target: https://www.saucedemo.com/  
Demo credentials (public): `standard_user` / `secret_sauce`

Mark each row only after a human actually performs the step.  
Until then: **PENDING HUMAN VERIFICATION**. Do not invent tester names or timestamps.

---

## Windows 10 — Google Chrome

| ID | Preconditions | Steps | Expected | Actual | PASS/FAIL | Screenshot | Tester / date |
|---|---|---|---|---|---|---|---|
| M-W-C-01 | Chrome installed | Open https://www.saucedemo.com/ | Login page loads; URL correct | | PENDING HUMAN VERIFICATION | | |
| M-W-C-02 | On login page | Check username/password fields readable | Fields visible, usable | | PENDING HUMAN VERIFICATION | | |
| M-W-C-03 | Valid demo creds | Login standard_user / secret_sauce | Inventory page opens | | PENDING HUMAN VERIFICATION | | |
| M-W-C-04 | Logged in | Browse inventory cards | Names and prices visible | | PENDING HUMAN VERIFICATION | | |
| M-W-C-05 | Inventory | Open a product details page | Title/description/price shown | | PENDING HUMAN VERIFICATION | | |
| M-W-C-06 | Product or inventory | Add item to cart | Cart badge increments | | PENDING HUMAN VERIFICATION | | |
| M-W-C-07 | Item in cart | Open cart | Product details match | | PENDING HUMAN VERIFICATION | | |
| M-W-C-08 | Logged in | Open burger menu | Logout / All Items accessible | | PENDING HUMAN VERIFICATION | | |
| M-W-C-09 | Any page | Scroll page; check layout | No critical overflow; controls reachable | | PENDING HUMAN VERIFICATION | | |
| M-W-C-10 | Login or checkout fields | Type and clear text | Inputs usable | | PENDING HUMAN VERIFICATION | | |

## Windows 10 — Mozilla Firefox

| ID | Preconditions | Steps | Expected | Actual | PASS/FAIL | Screenshot | Tester / date |
|---|---|---|---|---|---|---|---|
| M-W-F-01 | Firefox installed | Open Sauce Demo | Login form visible | | PENDING HUMAN VERIFICATION | | |
| M-W-F-02 | On login | Login with demo credentials | Inventory loads | | PENDING HUMAN VERIFICATION | | |
| M-W-F-03 | Logged in | Add to cart → open cart | Item present | | PENDING HUMAN VERIFICATION | | |
| M-W-F-04 | Compare vs Chrome | Note functional/layout differences | Notes recorded | | PENDING HUMAN VERIFICATION | | |

## Android 16 — Chrome (emulator or device)

Device reference (verified automation env): `emulator-5554`, Chrome **134.0.6998.135**.

| ID | Preconditions | Steps | Expected | Actual | PASS/FAIL | Screenshot | Tester / date |
|---|---|---|---|---|---|---|---|
| M-A-01 | Chrome on Android | Open saucedemo.com | Login form visible | | PENDING HUMAN VERIFICATION | | |
| M-A-02 | On login | Verify form readability on mobile viewport | Fields readable | | PENDING HUMAN VERIFICATION | | |
| M-A-03 | Demo creds | Login | Inventory loads | | PENDING HUMAN VERIFICATION | | |
| M-A-04 | Logged in | Browse inventory | Cards visible | | PENDING HUMAN VERIFICATION | | |
| M-A-05 | Inventory | Open product details | Details visible | | PENDING HUMAN VERIFICATION | | |
| M-A-06 | Product | Add to cart | Cart state updates | | PENDING HUMAN VERIFICATION | | |
| M-A-07 | Cart | Open cart | Item details correct | | PENDING HUMAN VERIFICATION | | |
| M-A-08 | Logged in | Open menu | Important actions accessible | | PENDING HUMAN VERIFICATION | | |
| M-A-09 | Any page | Scroll; check layout / touch targets | Usable; note issues | | PENDING HUMAN VERIFICATION | | |
| M-A-10 | Inputs | Type in fields | Soft keyboard / input usable | | PENDING HUMAN VERIFICATION | | |

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
3. Save screenshots under `screenshots/kt09/manual/`.  
4. Ask the agent to integrate completed evidence into docs/DOCX.
