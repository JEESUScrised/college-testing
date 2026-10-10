# KT02 — Тест-кейсы (публичный Sauce Demo)

| ID | Тест | Техника | Ожидание |
|---|---|---|---|
| TC02-P01 | `test_kt02_positive_login_inventory` | Positive | Login → ≥6 товаров |
| TC02-P02 | `test_kt02_positive_product_details_and_cart` | Positive | Карточка → cart = 1 |
| TC02-P03 | `test_kt02_positive_remove_and_checkout` | Positive | Remove → re-add → Thank you |
| TC02-N01 | `test_kt02_negative_empty_username` | Negative | Username is required |
| TC02-N02 | `test_kt02_negative_empty_password` | Negative | Password is required |
| TC02-N03 | `test_kt02_negative_bad_credentials` | Negative | Epic sadface / mismatch |
| TC02-N04 | `test_kt02_negative_checkout_missing_fields` | Negative | First Name required |
| TC02-B01 | `test_kt02_boundary_checkout_zip_values` | Boundary | empty zip reject; `1` accept |
| TC02-T01 | `test_kt02_locators_strategies` | Locators | ID / CSS / Name / XPath |
| TC02-T02 | `test_kt02_cookie_management` | Cookies | add/get/delete + session-username |
| TC02-T03 | `test_kt02_window_handles_public` | Windows | secondary tab + return |

Исторические TC окон/iframe: `test_kt02_windows.py`, `test_kt02_iframe.py` (6 PASS, сохранены).
