# KT09 — Cross-platform test cases

## Automated

| ID | Case | OS/Browser | Expected | Actual | Status | Evidence |
|---|---|---|---|---|---|---|
| XP-W-01 | Login + inventory | Windows Chrome | ≥6 products | ≥6 | PASS | `windows_chrome_*.png` |
| XP-W-02 | Login + inventory | Windows Firefox | ≥6 products | ≥6 | PASS | `windows_firefox_*.png` |
| XP-A-01 | DOM login→cart→menu | Android Chrome 134 | cart=1, menu open | cart=1, menu open | **PASS** | `crossplatform/dom/dom_*.png` |
| XP-A-02 | Intent+screencap smoke | Android Chrome | activity Chrome | Chrome focused | PARTIAL (legacy) | `android_chrome_*.png` |

## Manual (teacher-required)

See `kt09-manual-checklist.md`. Rows without user confirmation = **PENDING HUMAN VERIFICATION**.
