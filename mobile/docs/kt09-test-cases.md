# Тест-кейсы — КТ 09

| ID | Автотест | Действие | Ожидание |
|---|---|---|---|
| TC-09-01 | `test_vertical_swipe_up_reveals_lower_menu_items` | Swipe up в Views | Появляются нижние пункты (напр. TextFields/WebView) |
| TC-09-02 | `test_vertical_swipe_down_restores_upper_items` | Swipe down после прокрутки | Снова видны верхние пункты (Animation/…) |
| TC-09-03 | `test_scroll_until_target_and_open` | Scroll until TextFields → open | Экран TextFields открыт, ввод текста OK |
| TC-09-04 | `test_horizontal_swipe_left_moves_gallery` | Swipe left в Gallery | Сигнатура позиций ImageView изменилась |
| TC-09-05 | `test_horizontal_swipe_right_reverses_gallery` | Swipe right после left | Позиции снова изменились |

Все assertions проверяют состояние UI, не только отсутствие исключений Appium.
