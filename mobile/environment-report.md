# KT06 — отчёт аудита среды (Android / Appium)

Дата аудита: **2026-10-09 13:32** (локальный Windows).

## Итог

| Компонент | Статус |
|---|---|
| Node.js / npm | OK (совместимо с Appium 3) |
| Java JDK + JAVA_HOME | OK |
| Android SDK + adb + emulator binary | OK |
| Appium 3 + UiAutomator2 | OK (doctor: 0 required fixes) |
| ApiDemos APK | OK (скачан, SHA-256 совпадает) |
| System images / AVD | **ОТСУТСТВУЮТ** |
| Физическое Android-устройство | **НЕ ПОДКЛЮЧЕНО** |
| Готовность к запуску UI-тестов | **BLOCKED** |

**Вывод:** проект KT06 подготовлен, но **реальный прогон Appium невозможен** без AVD (нужен system image, несколько ГБ) или подключённого устройства с USB debugging. Автоматическая загрузка образов эмулятора **не выполнялась**.

---

## Установленные версии

| Компонент | Версия / путь |
|---|---|
| OS | Windows 10.0.26100 |
| Node.js | v25.0.0 (`^20.19.0 \|\| ^22.12.0 \|\| >=24.0.0` — OK для Appium 3) |
| npm | 11.6.2 (≥10 — OK) |
| Java | OpenJDK Temurin **17.0.1** |
| JAVA_HOME | `C:\Program Files\Eclipse Adoptium\jdk-17.0.1.12-hotspot\` |
| Python | 3.13.9 |
| pytest | 8.4.2 |
| Appium (local `mobile/`) | **3.8.0** |
| Driver | **uiautomator2@8.7.0** |
| Appium-Python-Client | 5.3.1 (venv) |
| ANDROID_HOME / ANDROID_SDK_ROOT | `C:\Users\admnp\AppData\Local\Android\Sdk` |
| adb | 1.0.41 / **37.0.0-14910828** |
| emulator.exe | присутствует |
| platforms | android-33, android-36, android-36.1 |
| system-images | **НЕ УСТАНОВЛЕНЫ** |
| AVD (`emulator -list-avds`) | **пусто** |
| `adb devices` | список пуст (нет устройств/эмуляторов) |
| Android Studio | не найден в типичных путях |
| ApiDemos APK | `mobile/apps/ApiDemos-debug.apk`, 6521217 bytes |
| SHA-256 APK | `A9EECF37B26CD084855C530DB81C2BB1B91F4C1B095A04F47AA7C20E2791F686` |

---

## Appium driver doctor (uiautomator2)

```
Running 7 doctor checks for the "uiautomator2" driver
✔ ANDROID_HOME is set
✔ adb, emulator exist under SDK
✔ JAVA_HOME is set
✔ bin\java.exe exists under JAVA_HOME
✖ bundletool.jar cannot be found          (optional)
✖ ffmpeg.exe cannot be found              (optional)
✖ gst-launch / gst-inspect cannot be found (optional)

Diagnostic completed, 0 required fixes needed, 3 optional fixes possible.
```

Опциональные предупреждения не блокируют базовые UiAutomator2 UI-тесты.

---

## Приложение под тест

- Источник: https://github.com/appium/android-apidemos
- Релиз: v6.0.18
- Package: `io.appium.android.apis`
- Activity: `.ApiDemos`
- Подробности: `mobile/apps/README.md`

---

## Что нужно для снятия BLOCKED

### Вариант A — эмулятор (рекомендуется для учёбы)

1. Установить **Android Studio** или SDK Command-line Tools.
2. Через SDK Manager скачать **system image** (например `system-images;android-34;google_apis;x86_64`) — **несколько гигабайт**.
3. Создать AVD:

```powershell
$env:ANDROID_HOME = "$env:LOCALAPPDATA\Android\Sdk"
& "$env:ANDROID_HOME\cmdline-tools\latest\bin\sdkmanager.bat" "system-images;android-34;google_apis;x86_64"
& "$env:ANDROID_HOME\cmdline-tools\latest\bin\avdmanager.bat" create avd -n Pixel_API_34 -k "system-images;android-34;google_apis;x86_64" -d pixel
```

4. Запустить эмулятор один раз, затем:

```powershell
.\scripts\diagnose_kt06.ps1
.\scripts\start_kt06_services.ps1
.\scripts\run_kt06.ps1
```

### Вариант B — физическое устройство

1. Включить «Для разработчиков» → USB debugging.
2. Подключить USB, разрешить отладку.
3. Проверить: `adb devices` показывает `device`.
4. Запустить те же скрипты KT06.

---

## Совместимость с KT09

Среда спроектирована для повторного использования:

- тот же Appium 3 + uiautomator2 (`mobile/package.json`);
- те же Python-зависимости (`mobile/requirements.txt`);
- тот же APK / package;
- session-scoped driver в `mobile/conftest.py` (один эмулятор на suite);
- скрипты сервисов и диагностики в `scripts/`.

KT09 **не реализован** в этом коммите.
