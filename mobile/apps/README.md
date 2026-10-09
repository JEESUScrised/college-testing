# Android APK for KT06 / KT09

## ApiDemos (official Appium sample)

| Field | Value |
|---|---|
| Source | https://github.com/appium/android-apidemos |
| Release | [v6.0.18](https://github.com/appium/android-apidemos/releases/tag/v6.0.18) |
| Artifact | `ApiDemos-debug.apk` |
| Download | https://github.com/appium/android-apidemos/releases/download/v6.0.18/ApiDemos-debug.apk |
| Package | `io.appium.android.apis` |
| SHA-256 | `A9EECF37B26CD084855C530DB81C2BB1B91F4C1B095A04F47AA7C20E2791F686` |
| Size | 6521217 bytes |

APK files are **not** committed to Git (see `.gitignore`). Download locally:

```powershell
cd mobile\apps
Invoke-WebRequest -Uri "https://github.com/appium/android-apidemos/releases/download/v6.0.18/ApiDemos-debug.apk" -OutFile ApiDemos-debug.apk
Get-FileHash .\ApiDemos-debug.apk -Algorithm SHA256
```

Verify the hash matches the table above before running tests.
