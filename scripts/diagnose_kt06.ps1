#Requires -Version 5.1
<#
.SYNOPSIS
  Диагностика среды KT06 (Android / Appium). Обновляет mobile/environment-report.md.
#>
[CmdletBinding()]
param()

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
. (Join-Path $ScriptDir "_kt06_common.ps1")
Set-Location $RepoRoot

Write-Host "Репозиторий: $RepoRoot"
$sdk = Initialize-AndroidEnv
$paths = Get-MobilePaths -RepoRoot $RepoRoot
$adb = Get-AdbPath -Sdk $sdk
$reportPath = Join-Path $paths.Mobile "environment-report.md"
$stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Step "Node.js / npm"
$nodeV = try { node -v } catch { "NOT FOUND" }
$npmV = try { npm -v } catch { "NOT FOUND" }
Write-Host "node=$nodeV npm=$npmV"

Write-Step "Java"
Write-Host "JAVA_HOME=$($env:JAVA_HOME)"
java -version 2>&1 | ForEach-Object { Write-Host $_ }

Write-Step "Android SDK"
Write-Host "ANDROID_HOME=$sdk"
& $adb version
Write-Host "`nadb devices:"
& $adb devices -l
$emu = Join-Path $sdk "emulator\emulator.exe"
if (Test-Path $emu) {
    Write-Host "`nemulator -list-avds:"
    $avds = & $emu -list-avds 2>&1
    if ($avds) { $avds | ForEach-Object { Write-Host $_ } } else { Write-Warn "AVD не найдены" }
}

Write-Step "Appium"
if (Test-Path $paths.AppiumCmd) {
    & $paths.AppiumCmd -v
    & $paths.AppiumCmd driver list --installed
    & $paths.AppiumCmd driver doctor uiautomator2
} else {
    Write-Warn "Appium не установлен. Выполните: cd mobile; npm install; npx appium driver install uiautomator2"
}

Write-Step "APK"
if (Test-Path $paths.Apk) {
    $hash = (Get-FileHash $paths.Apk -Algorithm SHA256).Hash
    Write-Ok "APK: $($paths.Apk) SHA-256=$hash"
} else {
    Write-Warn "APK отсутствует. См. mobile/apps/README.md"
}

$devices = Get-ReadyAndroidDevices -AdbPath $adb
Write-Step "Готовность к прогону"
if ($devices.Count -gt 0) {
    Write-Ok ("Устройства: " + ($devices -join ", "))
    Write-Host "STATUS: READY"
} else {
    Write-Warn "Нет подключённых устройств/эмуляторов → KT06 execution BLOCKED"
    Write-Host "STATUS: BLOCKED"
    Write-Host "Инструкции: mobile/environment-report.md"
}

Write-Ok "Диагностика завершена ($stamp). Подробности: $reportPath"
