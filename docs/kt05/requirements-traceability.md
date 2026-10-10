# Матрица трассируемости — КТ 05

| ID требования | Формулировка | Техника | Тест-кейс | Автотест | №1 | №2 | №3 (2026-10-11) |
|---|---|---|---|---|---|---|---|
| REQ-05-01 | Главная открывается | Black-box | TC-05-01 | `test_home_page_opens` | PASS | — | PASS |
| REQ-05-02 | Раздел новостей загружается | Black-box | TC-05-02 | `test_news_section_loads` | PASS | — | PASS |
| REQ-05-03 | Заголовок раздела виден | Black-box | TC-05-03 | `test_news_heading_visible` | PASS | — | PASS |
| REQ-05-04 | Карточки информативны | Black/Gray | TC-05-04 | `test_news_cards_have_meaningful_content` | PASS | — | PASS |
| REQ-05-05 | Карточки ведут на статьи | Gray-box | TC-05-05, TC-05-06 | links + open article | PASS | — | PASS |
| REQ-05-06 | Статья показывает заголовок | Black-box | TC-05-07 | `test_article_heading_and_details` | PASS | — | PASS |
| REQ-05-07 | Возврат к ленте | Black-box | TC-05-08 | `test_navigate_back_to_news_section` | PASS | — | PASS |
| REQ-05-08 | Доп. навигация / подгрузка | Black-box | TC-05-09, TC-05-10 | show_more + logo/menu | FAIL / PASS | PASS (TC-05-09) | PASS / PASS |

**White-box:** не применим к backend VDNH в рамках КТ 05 (закрытый исходный код сервера).

| Требование преподавателя | Документ / доказательство | Статус |
|---|---|---|
| Выбор сайта и обоснование | `website-selection.md`, test-plan §1–2 | PASS |
| Стратегия / black-gray-white | test-plan §5 | PASS (white-box N/A) |
| Планирование, entry/exit | test-plan §6 | PASS |
| Функциональные сценарии | test-cases.md (10 TC) | PASS |
| Фактическое исполнение | test-report.md прогоны №1–№3 | PASS |
| Дефекты | defect-analysis.md | PASS (баг сайта не подтверждён) |
| Анализ и рекомендации | recommendations.md | PASS |
| Итоговый отчёт | `reports/KT05.docx` | PASS |
