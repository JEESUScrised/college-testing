# Чек-лист сдачи КТ

Для **каждой КТ** перед загрузкой ответа:
- [x] Требования сверены с текстом задания и презентацией (если есть).
- [x] Исходный код находится в нужной папке.
- [x] Есть команды установки и запуска.
- [x] Тесты реально запускались в указанном окружении.
- [x] Зафиксирован результат каждого теста (PASS/FAIL/SKIP).
- [x] Есть подлинные скриншоты/логи с подтверждением запуска.
- [x] Составлен самостоятельный отчёт reports/KTNN.docx.
- [x] Для дефектов указаны шаги, ожидаемое и фактическое поведение, среда, серьёзность, приоритет и доказательства.
- [x] Обновлена таблица docs/STATUS.md.
- [x] Файлы проверены, нет секретов или персональных данных (кроме учебного SauceDemo `standard_user` / `secret_sauce`).

## Структура отчёта
Титульная часть → цель → инструменты и среда → порядок работы → исходный код/ссылки на код → тест-кейсы → фактические результаты → скриншоты → вывод.

Отчёт не должен утверждать успех непроверенного теста.

## Финальный аудит (2026-10-12)

- [x] Все 12 DOCX существуют и парсятся (`docs/compliance/docx-audit.json`)
- [x] Матрица `docs/compliance/FINAL_REQUIREMENTS_MATRIX.md`
- [x] Персональные поля: Прилепов Никита Алексеевич / 4P1.23; поле преподавателя отсутствует
- [x] Скриншотный аудит `docs/compliance/SCREENSHOT_VISUAL_AUDIT.md` (170 GOOD + 3 intentional blank excl. KT09)
- [x] KT02/03/05/08/10 screenshots пересняты; Allure overview/suites показывают реальные данные
- [x] KT09 visual evidence = `automated/windows` + `automated/android`; corrupt `unusable-visual/` удалён из дерева
- [x] KT04 Jira remote verify KAN-4/5/6 Done + filter/summary/dashboard
- [x] KT04 Components: documented UNAVAILABLE on team-managed (POST 405); labels substitute
- [x] Единственный архив сдачи: `submission/KT01-KT12_READY_FOR_SUBMISSION.zip` (устаревшие ZIP в `submission/` удалены; untracked `KT01-KT12_reports.zip` не трогать)
- [ ] KT09: пройти `mobile/docs/kt09-manual-execution-guide.md` человеком (Windows+Android) — **PENDING**
- [ ] Push в GitHub — только по явному запросу

## Readiness

**READY FOR PUBLICATION** с оговорками: KT09 manual human verification всё ещё PENDING; KT04 Components platform-limited; KT07 Grid на одном хосте; iOS NOT RUN.
