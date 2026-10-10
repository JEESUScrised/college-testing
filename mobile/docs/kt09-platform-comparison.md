# KT09 — Windows vs Android comparison

Public app: https://www.saucedemo.com/

| Aspect | Windows Chrome | Windows Firefox | Android Chrome (AVD API 36) |
|---|---|---|---|
| OS | Windows 10.0.19045 | Windows 10.0.19045 | Android 16 / API 36 emulator |
| Browser | Chrome (desktop) | Firefox (desktop) | Chrome 134.0.6998.135 |
| Automation | Selenium 4 Desktop | Selenium 4 Desktop | Appium 3.8 + ChromeDriver 134.0.6998.165 |
| Viewport | ~1280×900 window | ~1280×900 window | 411×810 CSS px (DPR 2.625) |
| Login form | Usable | Usable | Usable (DOM) |
| Inventory | ≥6 cards | ≥6 cards | 6 cards |
| Product→cart | Covered in KT02/03 | Covered in KT02/03 | Covered in DOM journey PASS |
| Horizontal overflow | Not observed (KT10 desktop) | Not observed | **none** (`scrollWidth==clientWidth`) |
| Layout differences | Multi-column product grid | Multi-column product grid | Single-column stacked cards; burger menu |
| Functional defects | **None confirmed** | **None confirmed** | **None confirmed** in executed DOM journey |
| Usability | Desktop mouse/keyboard | Desktop mouse/keyboard | Touch; Chrome onboarding/promo dialogs may appear before page |

## Recommendations

1. Keep pinned ChromeDriver in sync when emulator Chrome updates (`download_kt09_chromedriver.ps1`).
2. Complete human manual checklist on a physical Android device if available (emulator ≠ real device).
3. iOS Safari remains NOT RUN — add when simulator exists.
4. No website defect filing required from this comparison.

## Screenshots

- Windows: `screenshots/kt09/crossplatform/windows_*`
- Android DOM: `screenshots/kt09/crossplatform/dom/dom_*.png`
