# KT12 — Тест-кейсы

| ID | Функция pytest | Ожидание |
|---|---|---|
| TC-12-01 | `test_tc12_01_create_item_successfully` | CreateItem OK, поля совпадают |
| TC-12-02 | `test_tc12_02_retrieve_existing_item` | GetItem возвращает созданный Item |
| TC-12-03 | `test_tc12_03_reject_duplicate_item_id` | `ALREADY_EXISTS` |
| TC-12-04 | `test_tc12_04_reject_invalid_item_data` | `INVALID_ARGUMENT` (имя / quantity) |
| TC-12-05 | `test_tc12_05_retrieve_missing_item` | `NOT_FOUND` |
| TC-12-06 | `test_tc12_06_update_inventory_stock` | quantity после delta = 13 |
| TC-12-07 | `test_tc12_07_server_side_streaming` | ListItems: 3 id без дублей |
| TC-12-08 | `test_tc12_08_client_side_streaming` | BulkCreate count=3 + GetItem |
| TC-12-09 | `test_tc12_09_bidirectional_streaming` | EchoWatch 1:1 порядок FOUND/MISSING |
| TC-12-10 | `test_tc12_10_rpc_deadline_exceeded` | `DEADLINE_EXCEEDED` (timeout 0.1s / delay 800ms) |
