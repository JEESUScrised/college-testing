# Чек-лист исполнения КТ 05

- [x] Целевой сайт: `https://vdnh.ru/news/`
- [x] Доступность проверена; стратегия `pageLoadStrategy=none`
- [x] Page Object в `selenium/pages/vdnh_pages.py`
- [x] 10 различных автотестов
- [x] Assertions без жёсткой привязки к конкретным заголовкам новостей
- [x] Маркеры `kt05` / `smoke`
- [x] Документация: test-plan, test-cases, checklist, RTM, test-report
- [x] Полный прогон без VPN: **9 PASS / 1 FAIL** (98.63 с)
- [x] Целевой повтор show_more: **PASS** (11.60 с) — отдельно от полного прогона
- [x] Скриншоты `screenshots/kt05/`
- [x] `reports/KT05.docx` (оба прогона отражены честно)
- [x] `docs/STATUS.md` обновлён (без ложного «10/10 одним прогоном»)
- [x] KT01–KT04 не ломались; KT04 seeded FAIL не маскировались
- [ ] Push в GitHub — только по отдельному запросу
