# Compliance Remediation Baseline

Date: 2026-10-10  
HEAD verified: `f2ed436` (KT08 Allure remediation, 9 PASS)  
Branch: `main` (ahead of origin; no push)  
Untracked left untouched: `KT01-KT12_reports.zip`

## Environment

| Item | Status |
|---|---|
| Python 3.13.2 / Selenium 4.50.0 | OK |
| Chrome / Firefox | Installed |
| Java 21 | OK |
| AVD `Medium_Phone_API_36.1` | Running (`emulator-5554`) |
| Sauce Demo | HTTP 200 |
| Selenium Grid JAR | Present via existing scripts (Grid 4.50) |

## Historical results (preserve; not new compliance)

| KT | Historical | Gap vs original presentation |
|---|---|---|
| KT02 | 6 PASS local windows/iframe | Missing public app + pos/neg/boundary + cookies |
| KT03 | 4 PASS local PO | Missing public website Page Objects |
| KT07 | 5 Standalone + Hub/1 Node | Missing multi-node + parallel overlap |
| KT09 | 5 Android gestures | Missing BASIC OS×OS public web manual matrix |
| KT10 | 10 Chrome×Firefox @ one viewport | Missing responsive viewports / public responsive app |

## Planned phases

1. KT10 responsive matrix (Sauce Demo × Chrome/Firefox × Desktop/Tablet/Phone)
2. KT02 public functional techniques
3. KT03 public Page Object (shared sauce pages)
4. KT07 Hub + Chrome Node + Firefox Node + parallel evidence
5. KT09 basic cross-platform Windows vs Android (manual checklist; human verification if needed)
6. Final compliance audit
