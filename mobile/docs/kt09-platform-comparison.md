# KT09 — Windows vs Android comparison (automated evidence)

App: https://www.saucedemo.com/  
Evidence type: **AUTOMATED** (not manual)

| Scenario | Windows Firefox | Android Chrome | Screenshots | Conclusion |
|---|---|---|---|---|
| Login | PASS | PASS | `automated/windows/01_login.png` / `automated/android/01_login.png` | Compatible |
| Inventory | PASS | PASS | `02_inventory.png` | Desktop grid vs mobile column |
| Product details | PASS | PASS | `03_product_details.png` | Compatible |
| Added to cart | PASS | PASS | `04_added_to_cart.png` | Compatible |
| Cart | PASS | PASS | `05_cart.png` | Compatible |
| Menu | PASS | PASS | `06_menu.png` | Compatible |
| Checkout form | PASS | PASS | `07_checkout_form.png` | Compatible |
| Order confirmation | PASS | PASS | `08_order_confirmation.png` | Compatible |

**Environments**

- Windows 10 + Firefox (Selenium), 1280×900  
- Android 16 / API 36 / emulator-5554 / Chrome 134.0.6998.135 / ChromeDriver 134 / Appium 3.8  

**Preserved suite results:** Android DOM **11 PASS / 36.91s**; Windows web history **2 PASS**; gestures **5 PASS**.  

**Manual human comparison:** PENDING HUMAN VERIFICATION  
**Functional defects:** none confirmed.  
**Env notes:** Android may show Google Password Manager dialogs / occasional emulator GPU artifacts on some frames.
