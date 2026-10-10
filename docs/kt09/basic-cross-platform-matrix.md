# KT09 — BASIC OS×OS public web matrix (remediation)

Public app: https://www.saucedemo.com/

| OS | Browser | Method | Result | Evidence |
|---|---|---|---|---|
| Windows 10 | Chrome | Selenium Desktop | **PASS** | `windows_chrome_01_login.png`, `…_02_inventory.png` |
| Windows 10 | Firefox | Selenium Desktop | **PASS** | `windows_firefox_01_login.png`, `…_02_inventory.png` |
| Android (AVD API 36) | Chrome | adb VIEW intent + screencap | **PARTIAL** | `android_chrome_01_login.png`, `android_chrome_02_inventory.png`; ChromeDriver 134 missing for DOM login |
| iOS | Safari | — | **NOT RUN** | no simulator / XCUITest |

## Commands

```powershell
# Windows cells
.\.venv\Scripts\python.exe -m pytest selenium\tests\test_kt09_crossplatform_windows.py -v --page-load-strategy=eager

# Android cell (emulator-5554 + Appium optional; script uses adb)
.\.venv\Scripts\python.exe -m pytest mobile\tests\test_kt09_crossplatform_android.py -v
# or: .\.venv\Scripts\python.exe scripts\run_kt09_android_web_smoke.py
```

## Notes

- Historical Appium gesture suite (5 PASS) preserved.
- Android PARTIAL is intentional/honest: public page opened in Chrome on emulator with screenshots; full DOM automation blocked by ChromeDriver mismatch.
