# Отчёт о тестировании — КТ 08

Дата: **2026-10-09**.

## Среда

| Параметр | Значение |
|---|---|
| Python / Selenium / Pillow | 3.13.2 / 4.50.0 / 11.3.0 |
| Chrome | локальный headed |
| Baseline | `selenium/baselines/kt08/home_baseline.png` (1384×849) |
| Window | 1400×1000 |

## Прогоны

- Диагностика TC-08-01: **PASS** (2.89 с)  
- Полный suite: **5 passed in 13.71s**, exit 0  

## Метрики suite

| ID | Status | Diff% | Changed px | Notes |
|---|---|---:|---:|---|
| TC-08-01 | PASS | 0.0000 | 0 | MATCH |
| TC-08-02 | PASS | 1.1082 | 13021 | text/color |
| TC-08-03 | PASS | 5.0647 | 59511 | layout shift |
| TC-08-04 | PASS | 99.8457 | 1173203 | significant |
| TC-08-05 | PASS | n/a | — | DIMENSION_MISMATCH 1384×849 vs 884×549 |

## Артефакты

- Screenshots: `screenshots/kt08/01_…` … `05_…`
- Diff/overlay: `selenium/artifacts/kt08/*_diff_mask.png`, `*_overlay.png`
- Summary: `selenium/artifacts/kt08/comparison_summary.jsonl`
- Отчёт DOCX: `reports/KT08.docx`
