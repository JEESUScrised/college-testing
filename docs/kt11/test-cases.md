# КТ 11 — Тест-кейсы

| ID | Название | Теги | Суть проверки |
|---|---|---|---|
| TC-11-01 | Page Opens And Title Is Correct | KT11, smoke, title | Title + heading home |
| TC-11-02 | Navigation Link Opens Expected Page | KT11, navigation | Nav → register.html |
| TC-11-03 | Valid Form Submission Succeeds | KT11, form, positive | Валидная форма → «принято» |
| TC-11-04 | Invalid Form Data Is Rejected | KT11, form, negative | Невалидные данные → ошибка |
| TC-11-05 | Checkbox Can Be Selected And Deselected | KT11, checkbox | Select/Unselect checkbox |
| TC-11-06 | Radio Button Selection Changes Active Option | KT11, radio | basic → pro |
| TC-11-07 | Dropdown Selection Produces Correct Value | KT11, dropdown | country=kz |
| TC-11-08 | Iframe Interaction And Return To Main Document | KT11, iframe | Select Frame / Unselect Frame |
| TC-11-09 | Open New Tab Switch Verify And Return | KT11, windows | Switch Window NEW / return |
| TC-11-10 | Dynamic UI Update Is Verified | KT11, dynamic | Статус «исходный» → «обновлено (1)» |

Файл: `robot/tests/kt11.robot`.  
Ключевые слова: `robot/resources/common.resource`, `robot/resources/pages.resource`.
