# KT09 — Cross-platform public web test plan (BASIC)

## Goal

BASIC multi-OS compatibility testing of Sauce Demo on Windows desktop browsers and Android Chrome (real DOM WebDriver), plus teacher-required manual checklist.

## Environment (verified)

- Windows 10 + Chrome/Firefox (Selenium)
- Android 16 / API 36 emulator `emulator-5554` + Chrome 134.0.6998.135
- ChromeDriver 134.0.6998.165; Appium 3.8; capability `appium:chromedriverExecutable`

## Scope

In: TC09-W01…W10 DOM on Android; Windows login/inventory; screenshots; comparison.  
Out: iOS; load testing; ApiDemos for this BASIC web track (gestures kept separately).

## Entry / exit

Entry: emulator online, Appium ready, pinned ChromeDriver present.  
Exit: Android suite executed with reports; Windows evidence present; manual rows marked PASS or PENDING HUMAN VERIFICATION; DOCX updated.

## Automation vs manual

Automation supplements evidence. Teacher BASIC assignment still requires human OS checks — see checklist.
