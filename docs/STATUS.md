# Статус контрольных точек

Дата начала: 2026-10-09.

| КТ | Статус | Тесты | Отчёт | Примечания |
|---|---|---|---|---|
| 01 | DONE | PASS | DONE | Регрессия при КТ 04: PASS; `reports/KT01.docx` |
| 02 | DONE | PASS | DONE | Регрессия при КТ 04: PASS; `reports/KT02.docx` |
| 03 | DONE | PASS | DONE | Регрессия при КТ 04: PASS; `reports/KT03.docx` |
| 04 | DONE | MIXED | DONE | Campus Portal Demo; `2 passed, 3 failed` (seeded); Issues #1–#3 Open; `reports/KT04.docx` |
| 05 | TODO | NOT RUN | TODO | Функциональные тесты |
| 06 | TODO | NOT RUN | TODO | Appium |
| 07 | TODO | NOT RUN | TODO | Grid |
| 08 | TODO | NOT RUN | TODO | Визуальное сравнение |
| 09 | TODO | NOT RUN | TODO | Свайпы |
| 10 | TODO | NOT RUN | TODO | Браузеры + отчеты |
| 11 | TODO | NOT RUN | TODO | 10 Robot тестов |
| 12 | TODO | NOT RUN | TODO | 10 gRPC тестов |

Значения: TODO — не начато, IN PROGRESS — в процессе, DONE — выполнено с реальными доказательствами, BLOCKED — есть препятствие. Тесты: PASS / FAIL / SKIP / NOT RUN / MIXED.

## КТ 04 — факт прогона

- Приложение: `selenium/fixtures/kt04/` (Campus Portal Demo, учебные seeded-баги).
- Команда: `pytest selenium\tests\test_kt04_defects.py -v --browser=chrome`
- Результат: `3 failed, 2 passed in 18.08s`, exit code: 1, warnings: нет (после регистрации маркера kt04).
  - TC-01 valid login — PASS
  - TC-02 empty password — FAIL (SEED-001)
  - TC-03 invalid email — FAIL (SEED-002)
  - TC-04 zero quantity — FAIL (SEED-003)
  - TC-05 valid order — PASS
- Регрессия КТ 01–03: `11 passed in 53.55s`, exit code: 0.
- Скриншоты: `screenshots/kt04/tc01_*.png` … `tc05_*.png`
- Документы: `bug-reports/test-plan.md`, `test-cases.md`, `bug-reports.md`, `defect-summary.md`
- GitHub Issues (Open):
  - https://github.com/JEESUScrised/college-testing/issues/1
  - https://github.com/JEESUScrised/college-testing/issues/2
  - https://github.com/JEESUScrised/college-testing/issues/3
- Отчёт: `reports/KT04.docx`

## КТ 01–03 (кратко)

См. предыдущие разделы и отчёты `reports/KT01.docx` … `KT03.docx`. Регрессия при сдаче КТ 04 подтверждена.
