# KT09 — Manual cross-platform checklist (teacher-required)

Teacher BASIC assignment requires **manual** testing on different OS. Automation is supplementary.

Mark each row after a human actually performs the step. Until then status = **PENDING HUMAN VERIFICATION**.

## Windows desktop

| Step | Action | Expected | Status | Tester / date |
|---|---|---|---|---|
| M-W-01 | Open Chrome → saucedemo.com | Login form visible | PENDING HUMAN VERIFICATION | |
| M-W-02 | Login `standard_user` / `secret_sauce` | Inventory loads | PENDING HUMAN VERIFICATION | |
| M-W-03 | Open product, add to cart | Cart badge = 1 | PENDING HUMAN VERIFICATION | |
| M-W-04 | Open Firefox → same journey | Same functional result | PENDING HUMAN VERIFICATION | |
| M-W-05 | Note layout / usability differences | Notes recorded | PENDING HUMAN VERIFICATION | |

## Android

| Step | Action | Expected | Status | Tester / date |
|---|---|---|---|---|
| M-A-01 | Open Chrome on emulator/device → saucedemo.com | Login form visible | PENDING HUMAN VERIFICATION | |
| M-A-02 | Login with demo credentials | Inventory loads | PENDING HUMAN VERIFICATION | |
| M-A-03 | Add product to cart | Cart shows item | PENDING HUMAN VERIFICATION | |
| M-A-04 | Check readability / touch targets | Notes recorded | PENDING HUMAN VERIFICATION | |
| M-A-05 | Compare with Windows notes | Differences documented | PENDING HUMAN VERIFICATION | |

## Automated evidence already available (not a substitute for manual)

- Windows Selenium: PASS (2 tests)
- Android DOM Appium: PASS (1 journey, 16.71s)
