# KT06 — отчёт аудита среды (Android / Appium)

Дата аудита: **2026-10-09 21:15** (новый Windows ПК после миграции).

## Итог

| Компонент | Статус |
|---|---|
| Node.js / npm | OK (v22.14.0 / 10.9.2) |
| Java JDK + JAVA_HOME | OK (Android Studio JBR 21) |
| Android SDK + adb + emulator | OK |
| Appium 3 + UiAutomator2 | OK (doctor: 0 required fixes) |
| ApiDemos APK | OK (SHA-256 совпадает) |
| System images / AVD | OK — `Medium_Phone_API_36.1` (API 36) |
| Физическое Android-устройство | не использовалось |
| Готовность к запуску UI-тестов | **READY** |

**Вывод:** блокер снят. Прогон выполнен на существующем AVD `Medium_Phone_API_36.1`. Image API 33 / AVD `KT06_API33` **не** устанавливались (вариант B).

---

## Установленные версии

| Компонент | Версия / путь |
|---|---|
| OS | Windows 10.0.19045 (AMD64) |
| CPU | AMD Ryzen 5 5600; VirtualizationFirmwareEnabled=True |
| Acceleration | AEHD 2.2 installed and usable |
| RAM | ~16 ГБ |
| Node.js | v22.14.0 |
| npm | 10.9.2 |
| Java | OpenJDK **21.0.9** (Android Studio JBR) |
| JAVA_HOME | `C:\Program Files\Android\Android Studio\jbr` |
| Python | 3.13.2 |
| pytest | 8.4.2 |
| Appium (local `mobile/`) | **3.8.0** |
| Driver | **uiautomator2@8.7.0** |
| Appium-Python-Client | 5.3.1 (venv) |
| ANDROID_HOME | `C:\Users\user\AppData\Local\Android\Sdk` |
| adb | 1.0.41 / **36.0.2-14143358** |
| emulator | 36.4.9.0 |
| platforms | android-34, android-36, android-36.1 |
| system-images | `android-36.1;google_apis_playstore;x86_64` |
| AVD | **Medium_Phone_API_36.1** |
| `adb devices` | `emulator-5554 device` (API 36 / Android 16) |
| Android Studio | установлена (использован только JBR + уже имеющийся SDK) |
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

---

## Фактический прогон

- Диагностика: `test_app_starts_and_shows_home` — **PASS** (14.94 с).
- Suite №1: **6 PASS / 1 FAIL** (56.33 с) — FAIL `test_views_textfields_input` (нужен scroll).
- После фикса scroll: точечный PASS + suite №2 **7 PASS** (44.63 с).
- Отчёт: `reports/KT06.docx`.
