# KT09 — Cross-platform public web test plan (BASIC)

## Goal

Perform BASIC cross-platform compatibility testing of a public web application on different operating systems, with genuine screenshots and documented findings.

## Selected application

https://www.saucedemo.com/ (Sauce Demo / Swag Labs)

Justification: stable demo storefront, deterministic credentials, known DOM, suitable for Windows desktop browsers and Android Chrome.

## Scope

**In scope**
- Windows 10: Chrome, Firefox (Selenium Desktop)
- Android emulator API 36: Chrome (Appium + pinned ChromeDriver 134)
- Login, inventory, product details, cart, menu visibility
- Horizontal overflow / critical visibility checks (DOM viewport metrics on Android)

**Out of scope**
- iOS / Safari (NOT RUN — no simulator)
- Load/stress testing of the public site
- Visual pixel-perfect diffs across OS

## Entry criteria

- Emulator `emulator-5554` online OR Windows browsers available
- Appium 3.8 ready for Android DOM tests
- Pinned ChromeDriver via `scripts/download_kt09_chromedriver.ps1`

## Exit criteria

- Automated Windows cells executed with PASS/FAIL
- Automated Android DOM journey executed OR blocker documented
- Manual checklist present (PENDING HUMAN VERIFICATION if unconfirmed)
- Screenshots under `screenshots/kt09/crossplatform/`
- Comparison document written

## Test types

| Type | How applied |
|---|---|
| Functional | Login, cart, navigation |
| Compatibility | Windows vs Android browsers |
| Visual/usability | Screenshots + overflow metrics |
| Manual (teacher-required) | Checklist — human confirmation required |

## Automation vs manual

- Automation = supplementary evidence
- Teacher BASIC assignment requires **manual** OS testing — see `kt09-manual-checklist.md`
