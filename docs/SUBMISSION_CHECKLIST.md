# Чек-лист сдачи КТ

Для **каждой КТ** перед загрузкой ответа:
- [ ] Требования сверены с текстом задания и презентацией (если есть).
- [ ] Исходный код находится в нужной папке.
- [ ] Есть команды установки и запуска.
- [ ] Тесты реально запускались в указанном окружении.
- [ ] Зафиксирован результат каждого теста (PASS/FAIL/SKIP).
- [ ] Есть подлинные скриншоты/логи с подтверждением запуска.
- [ ] Составлен самостоятельный отчёт reports/KTNN.docx.
- [ ] Для дефектов указаны шаги, ожидаемое и фактическое поведение, среда, серьёзность, приоритет и доказательства.
- [ ] Обновлена таблица docs/STATUS.md.
- [ ] Файлы проверены, нет секретов или персональных данных.

## Структура отчёта
Титульная часть → цель → инструменты и среда → порядок работы → исходный код/ссылки на код → тест-кейсы → фактические результаты → скриншоты → вывод.

Отчёт не должен утверждать успех непроверенного теста.

## Финальный аудит (2026-10-11)

- [x] Все 12 DOCX существуют и парсятся (`docs/compliance/docx-audit.json`)
- [x] Матрица `docs/compliance/FINAL_REQUIREMENTS_MATRIX.md`
- [x] KT04 Jira remote verify KAN-4/5/6 Done + filter/summary/dashboard
- [x] Shared title metadata `reports/report_metadata.json`
- [x] Архив `submission/KT01-KT12_READY_FOR_SUBMISSION.zip` (старый `KT01-KT12_reports.zip` не трогать)
- [ ] Заполнить персональные поля в `reports/report_metadata.json` и пересобрать DOCX при необходимости
- [ ] KT09: пройти `mobile/docs/kt09-manual-execution-guide.md` человеком (Windows+Android)
- [ ] (Опционально) Утвердить создание native Jira Components
- [ ] (Опционально) В UI Edit настроить gadgets dashboard 10001 на filter 10002
- [ ] Push в GitHub — только по явному запросу

## Readiness

**PARTIALLY READY** — mandatory human KT09 checks still open; KT04 Components/reporting PARTIAL but evidenced.
