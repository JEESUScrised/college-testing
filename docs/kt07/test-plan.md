# План тестирования — КТ 07 (Selenium Grid 4)

## Цель

Продемонстрировать удалённый запуск браузерных автотестов через **Selenium Grid 4**: создание RemoteWebDriver-сессий, Standalone и Hub + Node, стабильные сценарии на локальных HTTP-фикстурах.

## Объект

- Grid: `selenium-server-4.50.0.jar` (официальный релиз SeleniumHQ)
- Браузер: Google Chrome (через Selenium Manager на Node/Standalone)
- Фикстуры: `selenium/fixtures/kt07/`, `selenium/fixtures/kt02/` (через HTTP)

## Архитектура

1. **Standalone** — все компоненты Grid в одном процессе на `127.0.0.1:4444`.
2. **Hub + Node** — Hub на `:4444`, Node на `:5556` (порт 5555 занят Android emulator), Event Bus принудительно на `127.0.0.1:4442/4443`.

## Область (in scope)

- Remote WebDriver (Selenium 4 Options API)
- 5 независимых UI-сценариев
- Подтверждение session id / capabilities
- Скриншоты и артефакты прогона

## Вне области

- Кросс-машинный кластер на разных физических ПК
- Firefox/Edge (не установлены на этом ПК)
- Изменение seeded-дефектов KT04 и повторный медленный KT05

## Риски

- VPN/виртуальные адаптеры могут «рекламировать» Event Bus на чужой IP — скрипты явно биндят loopback.
- Публикация Grid в интернет опасна; используется только localhost.
