# KT09 — Cross-platform test cases

## Android Chrome DOM (Appium + ChromeDriver 134.0.6998.165)

Suite: `mobile/tests/test_kt09_android_chrome_dom.py`  
Device: `emulator-5554` / Chrome 134.0.6998.135  
**Result 2026-10-11:** **11 passed in 36.91s**

| ID | Case | Expected | Actual | Status | Evidence |
|---|---|---|---|---|---|
| TC09-W01 | Website loading | saucedemo.com + logo | OK | **PASS** | `dom/tc09_w01_loading.png` |
| TC09-W02 | Login form usable | inputs enabled | OK | **PASS** | `dom/tc09_w02_login_form.png` |
| TC09-W03 | Successful auth | inventory / Products | OK | **PASS** | `dom/tc09_w03_authenticated.png` |
| TC09-W04 | Inventory listing | ≥6 names + $prices | OK | **PASS** | `dom/tc09_w04_inventory.png` |
| TC09-W05 | Product details | name/price match | OK | **PASS** | `dom/tc09_w05_product.png` |
| TC09-W06 | Add to cart | badge=1 | OK | **PASS** | `dom/tc09_w06_add_cart.png` |
| TC09-W07 | Cart navigation | item in cart | OK | **PASS** | `dom/tc09_w07_cart.png` |
| TC09-W08 | Checkout validation | First Name required | OK | **PASS** | `dom/tc09_w08_checkout_validation.png` |
| TC09-W09 | Burger menu | inventory + logout links | OK | **PASS** | `dom/tc09_w09_menu.png` |
| TC09-W10 | Mobile layout | no horizontal overflow | OK | **PASS** | `dom/tc09_w10_layout.png` |
| journey | Compact regression | inventory ≥6 | OK | **PASS** | `dom/dom_journey_regression.png` |

## Windows desktop (Selenium)

| ID | Case | Chrome | Firefox | Evidence |
|---|---|---|---|---|
| XP-W-01/02 | Login + inventory | PASS | PASS | `windows_*_*.png` |

## Gestures (historical ApiDemos)

5 PASS / 54.93s — preserved; not a substitute for BASIC public-web OS testing.

## Manual (teacher-required)

See `kt09-manual-checklist.md` → **PENDING HUMAN VERIFICATION**.
