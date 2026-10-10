# КТ06 — Анализ дефектов

## Итог

**Подтверждённых дефектов приложения ApiDemos в исполненных сценариях нет.**

## Инцидент INC-06-01 (автоматизация)

| Поле | Значение |
|---|---|
| ID | INC-06-01 |
| Тип | Test implementation |
| Тест | `test_views_textfields_input` |
| Suite №1 | FAIL — пункт TextFields вне видимой области списка Views (API 36) |
| Suite №2 | PASS после `UiScrollable.scrollIntoView` в Page Object |
| Вывод | Не баг ApiDemos, а недостаточный scroll в тесте |

## Рекомендации (см. также kt06-recommendations.md)

- На API 36+ всегда учитывать необходимость scroll к пунктам списка.
- Для заявлений о качестве продукта использовать production/beta app + real device.
