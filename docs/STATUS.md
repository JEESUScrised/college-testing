# Статус контрольных точек

Дата начала: 2026-10-09. Финальная синхронизация: **2026-10-12**.

| КТ | Статус | Тесты | Отчёт | Примечания |
|---|---|---|---|---|
| 01 | DONE | PASS | DONE | `reports/KT01.docx` |
| 02 | DONE | PASS | DONE | Local windows/iframe 6 PASS + public Sauce **11 PASS** (49.34 с); скриншоты public пересняты 2026-10-12; `reports/KT02.docx` |
| 03 | DONE | PASS | DONE | Local PO 4 PASS + public Sauce PO **5 PASS** (21.11 с); public screenshots пересняты; `reports/KT03.docx` |
| 04 | DONE | MIXED | DONE | seeded 2P/3F; lifecycle **3 PASS / 8.74s**; Jira **KAN-4/5/6 Done**; Components UNAVAILABLE (405); dashboard charts configured; `reports/KT04.docx` |
| 05 | DONE | PASS | DONE | VDNH; история 9P/1F + follow-up; remediation **10 PASS / 50.63 с**; media screenshots пересняты с images on; `reports/KT05.docx` |
| 06 | DONE | PASS | DONE | AVD API 36; история **7 PASS / 44.63 с**; remediation **10 PASS / 67.70 с**; `reports/KT06.docx` |
| 07 | DONE | PASS | DONE | Standalone 5 PASS + Hub+**2 Nodes** Chrome/Firefox **4 PASS** (7.72 с) + parallel overlap; один хост; `reports/KT07.docx` |
| 08 | DONE | PASS | DONE | Public Sauce + Allure HTML (HTTP capture); Full **9 PASS** (34.64 с); Pillow history 5/13.71с; `reports/KT08.docx` |
| 09 | DONE | MIXED | DONE | Gestures 5 PASS + Android DOM **11 PASS**; visual **automated/** 8×2; corrupt archive удалён из дерева; manual PENDING; iOS NOT RUN; `reports/KT09.docx` |
| 10 | DONE | PASS | DONE | Functional 10/52.92с + responsive Sauce **6 PASS** (42.73 с, 36 rows); responsive screenshots пересняты; `reports/KT10.docx` |
| 11 | DONE | PASS | DONE | Robot Framework 7.5 + SeleniumLibrary; **10 PASS** (28.39 с); `reports/KT11.docx` |
| 12 | DONE | PASS | DONE | Inventory gRPC; **10 PASS** (2.34 с); `reports/KT12.docx` |

Значения: TODO / IN PROGRESS / DONE / BLOCKED. Тесты: PASS / FAIL / SKIP / NOT RUN / MIXED.

## Итог проекта (КТ 01–12)

Все 12 контрольных точек реализованы; отчёты `reports/KT01.docx` … `reports/KT12.docx` присутствуют.

Персональные поля DOCX заполнены: **Прилепов Никита Алексеевич**, группа **4P1.23** (`reports/report_metadata.json`). Поле преподавателя отсутствует.

Известные ограничения (сохранены):
- **КТ04** — seeded FAIL сохранены; Jira **DONE** (KAN-4/5/6); Components **UNAVAILABLE** on team-managed (labels); dashboard **configured**.
- **КТ05** — исторически 9P/1F + follow-up; текущий remediation suite **10/10 PASS** (прогоны не склеивать).
- **КТ07** — multi-node Grid на **одном компьютере** (не кросс-машинный).
- **КТ09** — manual **PENDING HUMAN VERIFICATION**; iOS **NOT RUN**; удалённые GPU-corrupt PNG не входят в сдачу.
- Презентации cloud.ithub.ru без логина недоступны — полное соответствие скрытым слайдам не утверждается.

Скриншотный аудит: `docs/compliance/SCREENSHOT_VISUAL_AUDIT.md` (excl. KT09: 170 GOOD + 3 intentional blank).  
Архив сдачи: `submission/KT01-KT12_READY_FOR_SUBMISSION.zip`. Push — только по явному запросу.

## КТ 12 — gRPC InventoryService (финальная)

- grpcio/grpcio-tools **1.84.0**, protobuf **7.36.2**; proto3 `inventory.proto` + generated stubs.
- Suite: **10 passed in 2.34s**; unary + server/client/bidi streaming + DEADLINE_EXCEEDED.
- Код: `grpc/server/`, `grpc/client/cli.py`, `grpc/tests/test_kt12_grpc.py`, `grpc/conftest.py`.
- Артефакты: `grpc/artifacts/kt12/` (gitignore); скриншот `screenshots/kt12/`; отчёт `reports/KT12.docx`.

## КТ 11 — Robot Framework

- Robot Framework **7.5** + SeleniumLibrary **6.9.0**; Selenium 4.50.0 сохранён.
- Suite: **10 passed / 0 failed**, elapsed **28.39 с** (`output.xml`).
- Код: `robot/tests/kt11.robot`, `robot/resources/*.resource`, `robot/fixtures/`, `robot/lib/FixtureServer.py`.
- Артефакты: `robot/artifacts/kt11/` (gitignore); скриншоты `screenshots/kt11/`; отчёт `reports/KT11.docx`.

## КТ 10 — Кроссбраузерность + responsive

- Исторический functional: Chrome×Firefox 5×2 = **10 PASS / 52.92 с** + listener (сохранён).
- Responsive Sauce Demo **6 PASS / 42.73 с** (36 matrix rows; overflow не найден).
- CDP Chrome tablet/phone; Firefox = window resize (не Android/iOS).
- `screenshots/kt10/responsive/`; `reports/KT10.docx`.

## КТ 09 — Жесты + BASIC cross-platform

- Жесты Android: **5 PASS / 54.93 с** (скрины `screenshots/kt09/*.png` сохранены).
- BASIC public web auto: Windows **2 PASS**; Android Chrome DOM TC09-W01…W10 **11 PASS / 36.91 с**.
- Visual evidence: `screenshots/kt09/automated/windows|android` (8×2).
- Manual checklist: **PENDING HUMAN VERIFICATION**.
- iOS: **NOT RUN**. Отчёт: `reports/KT09.docx`.

## КТ 08 — Скриншоты + Allure

- Публичный сайт: https://www.saucedemo.com/; Allure HTML со скриншотами (overview/suites пересняты через HTTP).
- Full suite: **9 passed in 34.64s**; исторический Pillow: **5 passed in 13.71s**.
- Отчёт: `reports/KT08.docx`.

## КТ 07 — Selenium Grid 4

- Hub + Node A(:5556) + Node B(:5557); status **nodes=2** на одном хосте.
- Multi-browser: Chrome+Firefox **4 PASS / 7.72 с**; parallel overlap **true**.
- Отчёт: `reports/KT07.docx`.

## КТ 06 — Appium Android

- AVD **`Medium_Phone_API_36.1`** (API 36); remediation **10 PASS / 67.70 с**.
- Скриншоты: `screenshots/kt06/`; `reports/KT06.docx`.

## КТ 05 — VDNH

- Remediation **10 passed in 50.63s**; исторические 9P/1F сохранены отдельно.
- Отчёт: `reports/KT05.docx`.

## КТ 04

Campus Portal Demo; seeded **2 PASS / 3 FAIL** (сохранён).  
Lifecycle retest **3 PASS / 8.74 с**.  
Jira: https://collegeqakt04.atlassian.net — **KAN-4 / KAN-5 / KAN-6** → **Done**.  
Components: **UNAVAILABLE** (POST 405); labels substitute.  
Отчёт: `reports/KT04.docx`.

## КТ 02 / КТ 03

- KT02 public Sauce **11 PASS / 49.34 с**; KT03 public PO **5 PASS / 21.11 с**.
- Отчёты: `reports/KT02.docx`, `reports/KT03.docx`.

## КТ 01

См. `reports/KT01.docx`.
