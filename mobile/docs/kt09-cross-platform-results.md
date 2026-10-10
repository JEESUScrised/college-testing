# KT09 — Cross-platform results

## Android Chrome DOM suite (2026-10-11)

```
collected 11 items
============================= 11 passed in 36.91s =============================
```

| Item | Value |
|---|---|
| Emulator | emulator-5554, Android 16 / API 36 |
| Chrome | 134.0.6998.135 |
| ChromeDriver | 134.0.6998.165 (`mobile/drivers/chromedriver-134.exe`) |
| Appium | 3.8.0 |
| Reports | `mobile/artifacts/kt09/report_android_dom_20261011_011509.html` |
| JUnit | `mobile/artifacts/kt09/junit_android_dom_20261011_011509.xml` |

```powershell
.\.venv\Scripts\python.exe -m pytest mobile\tests\test_kt09_android_chrome_dom.py -v --udid=emulator-5554
```

## Windows (prior remediation)

```
======================= 2 passed in 12.43s ========================
```

## Gestures (historical)

```
============================= 5 passed in 54.93s ==============================
```

## Manual (human UI only)

**PENDING HUMAN VERIFICATION**

- Guide: `kt09-manual-execution-guide.md`
- Checklist: `kt09-manual-checklist.md`
- Screenshot dirs (empty until human): `screenshots/kt09/manual/windows/`, `screenshots/kt09/manual/android/`

Automated results above are **not** a substitute for manual rows.
