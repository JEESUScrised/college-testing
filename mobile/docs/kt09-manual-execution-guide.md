# KT09 — Manual testing guide (human only)

Automation does **not** count. You must use the real browser UI yourself.

## Target

https://www.saucedemo.com/  
Credentials (public demo): `standard_user` / `secret_sauce`

## Platforms

1. **Windows 10 + Google Chrome** (desktop)
2. **Android 16 + Chrome** inside emulator `emulator-5554` (or a real device)

## Before you start

1. Open Chrome normally (not via Appium/Selenium).
2. Prepare folders for your screenshots:
   - `screenshots/kt09/manual/windows/`
   - `screenshots/kt09/manual/android/`
3. Open the checklist: `mobile/docs/kt09-manual-checklist.md`
4. Fill **Actual / PASS-FAIL / Screenshot path / Tester+date** only after you personally do the step.

## Scenarios (do on BOTH platforms)

| # | What to do | Expected |
|---|---|---|
| 1 | Open SauceDemo | Login page loads |
| 2 | Check login form readability | Username/password fields usable |
| 3 | Log in with demo credentials | Inventory opens |
| 4 | Verify inventory listing | Names and prices visible |
| 5 | Open a product details page | Title / description / price shown |
| 6 | Add an item to the cart | Cart badge increments |
| 7 | Open cart | Contents match added item |
| 8 | Open and close the burger menu | Menu actions accessible |
| 9 | Scroll; check clipping / horizontal overflow | No critical layout breakage |
| 10 | Try checkout name fields (type/clear) | Inputs usable |

## After completion

Tell the agent: which rows are PASS/FAIL, screenshot paths, browser versions, and your name/date.  
Until then status remains: **PENDING HUMAN VERIFICATION**.
