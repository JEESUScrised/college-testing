# Матрица трассируемости — КТ 05

| ID требования | Формулировка | Техника | Тест-кейс | Автотест | Прогон №1 | Прогон №2 |
|---|---|---|---|---|---|---|
| REQ-05-01 | Главная открывается | Black-box | TC-05-01 | `test_home_page_opens` | PASS | — |
| REQ-05-02 | Раздел новостей загружается | Black-box | TC-05-02 | `test_news_section_loads` | PASS | — |
| REQ-05-03 | Заголовок раздела виден | Black-box | TC-05-03 | `test_news_heading_visible` | PASS | — |
| REQ-05-04 | Карточки информативны | Black/Gray | TC-05-04 | `test_news_cards_have_meaningful_content` | PASS | — |
| REQ-05-05 | Карточки ведут на статьи | Gray-box | TC-05-05, TC-05-06 | links + open article | PASS | — |
| REQ-05-06 | Статья показывает заголовок | Black-box | TC-05-07 | `test_article_heading_and_details` | PASS | — |
| REQ-05-07 | Возврат к ленте | Black-box | TC-05-08 | `test_navigate_back_to_news_section` | PASS | — |
| REQ-05-08 | Доп. навигация / подгрузка | Black-box | TC-05-09, TC-05-10 | show_more + logo/menu | FAIL / PASS | PASS (только TC-05-09) |

**White-box:** не применим к backend VDNH в рамках КТ 05.
