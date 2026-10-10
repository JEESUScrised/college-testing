# KT09 — BASIC OS×OS public web matrix

Public app: https://www.saucedemo.com/

| OS | Browser | Method | Result | Evidence |
|---|---|---|---|---|
| Windows 10 | Chrome | Selenium Desktop | **PASS** | `windows_chrome_*.png` |
| Windows 10 | Firefox | Selenium Desktop | **PASS** | `windows_firefox_*.png` |
| Android (AVD API 36) | Chrome 134.0.6998.135 | Appium + ChromeDriver 134.0.6998.165 DOM | **PASS** | `crossplatform/dom/dom_*.png` |
| iOS | Safari | — | **NOT RUN** | no simulator |
| Manual Windows/Android | any | Human checklist | **PENDING HUMAN VERIFICATION** | `mobile/docs/kt09-manual-checklist.md` |

## ChromeDriver pin

- Source: Chrome for Testing `https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.165/win64/chromedriver-win64.zip`
- Local: `mobile/drivers/chromedriver-134.exe` (gitignored binary)
- Download: `.\scripts\download_kt09_chromedriver.ps1`
- Capability: `appium:chromedriverExecutable`

## Commands

```powershell
.\.venv\Scripts\python.exe -m pytest selenium\tests\test_kt09_crossplatform_windows.py -v --page-load-strategy=eager
.\scripts\download_kt09_chromedriver.ps1
.\.venv\Scripts\python.exe -m pytest mobile\tests\test_kt09_android_chrome_dom.py -v --udid=emulator-5554
```
