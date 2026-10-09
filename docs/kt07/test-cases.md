# Тест-кейсы — КТ 07

| ID | Автотест | Предусловие | Шаги | Ожидание |
|---|---|---|---|---|
| TC-07-01 | `test_remote_session_created` | Grid ready | Создать `webdriver.Remote` | `RemoteWebDriver`, непустой `session_id`, `browserName=chrome`, executor `127.0.0.1:4444` |
| TC-07-02 | `test_navigate_and_title` | Grid + HTTP fixtures | Открыть `/kt07/index.html` | Title `KT07 Grid Landing`, заголовок виден |
| TC-07-03 | `test_dom_element_interaction` | то же | Ввод имени, Submit | Статус содержит «принято — KT07 Remote» |
| TC-07-04 | `test_window_open_and_switch` | то же | Открыть второе окно, switch, close | Handles корректны, возврат на main |
| TC-07-05 | `test_iframe_interaction_and_context_switch` | то же | frame → input → default_content | Результат iframe и контекст host |

Локаторы: стабильные `id` на локальных HTML-фикстурах. Ожидания: explicit waits (Selenium `EC`).
