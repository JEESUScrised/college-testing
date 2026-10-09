# Selenium Grid 4 (КТ 07)

Удалённый запуск браузерных тестов через **Selenium Grid 4** (Standalone и Hub + Node) на localhost.

## Требования

- Java 11+ (`JAVA_HOME`; на этом ПК — Android Studio JBR 21)
- Google Chrome
- Python venv с Selenium 4 (`pip install -r selenium/requirements.txt`)
- Официальный `selenium-server-*.jar` (не в Git)

## Безопасность

Скрипты по умолчанию поднимают Grid на **`127.0.0.1`**, без публикации в интернет.  
Не пробрасывайте порты 4444/4442/4443/555x наружу без firewall/ACL.

## Установка JAR

```powershell
.\selenium\grid\download_server.ps1
```

Источник: [SeleniumHQ GitHub Releases](https://github.com/SeleniumHQ/selenium/releases)  
(`selenium-server-4.50.0.jar`).

## Standalone

```powershell
.\selenium\grid\start_standalone.ps1
.\selenium\grid\health_check.ps1
# UI / status:
# http://127.0.0.1:4444
# http://127.0.0.1:4444/status
.\scripts\run_kt07.ps1
.\selenium\grid\stop_grid.ps1
```

## Hub + Node

Не запускайте одновременно со Standalone на порту 4444.

По умолчанию Node слушает **5556** (порт **5555** на этой машине часто занят Android emulator/qemu).

Скрипт явно задаёт Event Bus на `tcp://127.0.0.1:4442` и `:4443`. Иначе на машинах с VPN Grid может рекламировать чужой IP (например `26.x`) и Node не зарегистрируется.

```powershell
.\selenium\grid\stop_grid.ps1   # если Standalone ещё работает
.\selenium\grid\start_hub_node.ps1
.\selenium\grid\health_check.ps1
.\scripts\run_kt07.ps1
.\selenium\grid\stop_grid.ps1
```

## Остановка

`stop_grid.ps1` завершает **только** Java-процессы, чьи PID записаны в `selenium/grid/runtime/grid.pids.json` нашими скриптами. Чужие Java/браузеры не трогает.

## Тесты

- Фикстура `grid_driver` — `webdriver.Remote(...)` (Selenium 4 Options API)
- Локальная фикстура `driver` (KT01–KT05) **не изменяется**
- HTML отдаётся HTTP-сервером (`fixture_http_server`), не через `file://`

```powershell
.\.venv\Scripts\python.exe -m pytest selenium\tests\test_kt07_grid.py -v --browser=chrome --grid-url=http://127.0.0.1:4444
```

## Standalone vs Hub+Node vs «несколько машин»

| Режим | Что демонстрирует |
|---|---|
| Standalone | Все компоненты Grid в одном процессе; RemoteWebDriver на `:4444` |
| Hub + Node (localhost) | Регистрация Node, маршрутизация сессий Hub → Node |
| Несколько физических машин | **Не тестировалось** в этой работе; архитектура та же, но Node на другом host |

Localhost Hub+Node — это настоящий Grid-протокол (регистрация Node, слоты, session id), но не кросс-машинный кластер.
