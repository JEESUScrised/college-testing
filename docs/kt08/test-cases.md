# Тест-кейсы — КТ 08

## A. Публичный сайт (Sauce Demo) + Allure

| ID | Тест | UI | Allure |
|---|---|---|---|
| TC-08-P01 | `test_public_login_page_and_branding` | Login / branding / form | screenshot + steps |
| TC-08-P02 | `test_public_inventory_after_login` | Products inventory | screenshot + steps |
| TC-08-P03 | `test_public_sort_dropdown` | Sort dropdown | screenshot + steps |
| TC-08-P04 | `test_public_add_to_cart` | Add to cart / badge | screenshot + steps |

## B. Локальная Pillow visual regression (сохранено)

| ID | Тест | Ожидание |
|---|---|---|
| TC-08-01 | match baseline | MATCH / 0% |
| TC-08-02 | text/color change | DIFF ≥ 0.3% |
| TC-08-03 | layout shift | DIFF ≥ 1% |
| TC-08-04 | significant | DIFF ≥ 10% |
| TC-08-05 | dimension mismatch | DIMENSION_MISMATCH |

Исторический прогон Pillow: **5 passed in 13.71s** (2026-10-09).
