# Тест-кейсы — КТ 08

| ID | Автотест | Fixture / действие | Ожидание |
|---|---|---|---|
| TC-08-01 | `test_unchanged_page_matches_baseline` | `home.html` vs `home_baseline.png` | `matched=True`, diff≈0% |
| TC-08-02 | `test_text_or_color_change_detected` | `home_text_color.html` | `matched=False`, diff≥0.3%, mask+overlay |
| TC-08-03 | `test_layout_shift_detected` | `home_layout_shift.html` | `matched=False`, diff≥1% |
| TC-08-04 | `test_significant_difference_reported_with_metrics` | `home_significant.html` | `matched=False`, diff≥10%, метрики в message |
| TC-08-05 | `test_dimension_mismatch_detected` | `home.html` @ 900×700 | `dimension_mismatch=True`, без resize |

Параметры сравнения: `color_tolerance=12`, порог совпадения `0.75%`.
