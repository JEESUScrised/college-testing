# Unusable KT09 visual evidence (archived)

These PNG files are **not** valid visual proof of SauceDemo UI for submission.

## Why archived

| Issue | Examples |
|---|---|
| Android GPU compositor corruption (`nativeWebScreenshot=true`) | `crossplatform/dom/tc09_w*.png`, many `dom_*.png` |
| Chrome onboarding / Password Manager overlays | `android_chrome_01_login.png`, several `dom_*.png` |
| Partially loaded Windows Chrome (fonts/text missing) | `windows_chrome_01_login.png`, `windows_chrome_02_inventory.png` |
| Misleading rename (page copied as “inventory”) | `android_chrome_02_inventory.png` ← copy of `android_chrome_02_page.png` |
| Android home/launcher or non-browser frames | `manual/01_login_screen.png` (if present) |

## Canonical evidence (use these)

- `screenshots/kt09/automated/windows/` — 8 Firefox Selenium captures
- `screenshots/kt09/automated/android/` — 8 ChromeDriver web screenshots (`nativeWebScreenshot=false`)

## Preserved separately

- Historical **test logs / PASS counts** for the Android DOM suite remain valid (assertions passed even when native screenshots were glitched).
- Appium **gesture** screenshots under `screenshots/kt09/*.png` (Views/Gallery) are unrelated and kept in place.

Do not reintroduce these files into `reports/KT09.docx` or the submission ZIP as successful UI evidence.
