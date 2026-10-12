# KT09 — BASIC OS×OS public web matrix

Public app: https://www.saucedemo.com/

| OS | Browser | Method | Result | Evidence |
|---|---|---|---|---|
| Windows 10 | Firefox | Selenium Desktop visual | **PASS** | `screenshots/kt09/automated/windows/*.png` (8) |
| Windows 10 | Chrome | Selenium Desktop | **PASS** (functional history) | logs; visual — use Firefox set above |
| Android (AVD API 36) | Chrome 134.0.6998.135 | Appium + ChromeDriver 134 DOM assertions | **PASS** | suite **11 PASS / 36.91s** |
| Android (AVD API 36) | Chrome 134 | ChromeDriver web screenshot (`nativeWebScreenshot=false`) | **PASS** (visual) | `screenshots/kt09/automated/android/*.png` (8) |
| iOS | Safari | — | **NOT RUN** | no simulator |
| Manual Windows/Android | any | Human checklist | **PENDING HUMAN VERIFICATION** | `mobile/docs/kt09-manual-checklist.md` |

## Capture note

Do **not** use `screenshots/kt09/crossplatform/` or `crossplatform/dom/` for submission visuals.
Those frames were produced with `nativeWebScreenshot=true` (GPU corruption) or Chrome dialogs / partial loads.
Archived under `screenshots/kt09/archive/unusable-visual/`.

## ChromeDriver pin

- Source: Chrome for Testing `https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.165/win64/chromedriver-win64.zip`
- Local: `mobile/drivers/chromedriver-134.exe` (gitignored binary)
- Download: `.\scripts\download_kt09_chromedriver.ps1`
- Capability: `appium:chromedriverExecutable`
- Screenshots: `appium:nativeWebScreenshot=false`

## Commands

```powershell
.\.venv\Scripts\python.exe -m pytest selenium\tests\test_kt09_crossplatform_windows.py -v --page-load-strategy=eager
.\scripts\download_kt09_chromedriver.ps1
.\.venv\Scripts\python.exe -m pytest mobile\tests\test_kt09_android_chrome_dom.py -v --udid=emulator-5554
.\.venv\Scripts\python.exe scripts\capture_kt09_android_visual.py
.\.venv\Scripts\python.exe scripts\organize_kt09_automated_shots.py
```
