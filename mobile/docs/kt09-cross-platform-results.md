# KT09 — Cross-platform results

## Windows (2026-10-10, historical remediation)

```
======================= 2 passed in 12.43s ========================
```

Command:

```powershell
.\.venv\Scripts\python.exe -m pytest selenium\tests\test_kt09_crossplatform_windows.py -v --page-load-strategy=eager
```

## Android DOM (2026-10-10, ChromeDriver 134.0.6998.165)

```
============================= 1 passed in 16.71s ==============================
```

| Item | Value |
|---|---|
| Emulator Chrome | 134.0.6998.135 |
| Host ChromeDriver | 134.0.6998.165 (Chrome for Testing) |
| Path | `mobile/drivers/chromedriver-134.exe` |
| Capability | `appium:chromedriverExecutable` |
| Viewport | 411×810 CSS px, DPR 2.625 |
| Overflow | none (login/inventory) |
| Product | Sauce Labs Backpack → cart=1 |

Command:

```powershell
.\scripts\download_kt09_chromedriver.ps1   # once
.\.venv\Scripts\python.exe -m pytest mobile\tests\test_kt09_android_chrome_dom.py -v --udid=emulator-5554
```

## Gesture suite (historical, preserved)

```
============================= 5 passed in 54.93s ==============================
```

ApiDemos swipe/scroll — supplementary, not a substitute for BASIC public-web OS testing.
