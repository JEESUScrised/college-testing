# KT03 — Тест-кейсы (публичный PO)

| ID | Тест | Page Objects |
|---|---|---|
| TC03-P01 | `test_po_login_page_opens_and_authenticates` | SauceLoginPage → SauceInventoryPage |
| TC03-P02 | `test_po_inventory_sort_and_open_product` | SauceInventoryPage → SauceProductPage |
| TC03-P03 | `test_po_product_add_and_cart` | SauceProductPage → SauceCartPage |
| TC03-P04 | `test_po_checkout_flow` | SauceCartPage → SauceCheckoutPage |
| TC03-P05 | `test_po_menu_logout` | SauceInventoryPage.logout → SauceLoginPage |

Исторические: `test_kt03_page_object.py` (4 PASS, WindowsMainPage / IframePage).
