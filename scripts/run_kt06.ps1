#Requires -Version 5.1
<#
.SYNOPSIS
  Однократный прогон KT06 Appium-тестов. Требует готовое устройство/эмулятор и Appium :4723.
#>
[CmdletBinding()]
param(
    [string]$AppiumServer = "http://127.0.0.1:4723",
    [string]$Udid = $env:ANDROID_UDID
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
. (Join-Path $ScriptDir "_kt06_common.ps1")
Set-Location $RepoRoot

$sdk = Initialize-AndroidEnv
$paths = Get-MobilePaths -RepoRoot $RepoRoot
$adb = Get-AdbPath -Sdk $sdk

if (-not (Test-Path $paths.VenvPython)) {
    Fail "Нет .venv. Создайте окружение и: pip install -r mobile\requirements.txt"
}
if (-not (Test-Path $paths.Apk)) {
    Fail "Нет APK. См. mobile\apps\README.md"
}

$devices = Get-ReadyAndroidDevices -AdbPath $adb
if ($devices.Count -eq 0) {
    Fail @"
Нет Android device/emulator (adb devices пуст).
KT06 НЕ запускается без реального устройства.
Диагностика: .\scripts\diagnose_kt06.ps1
Инструкции: mobile\environment-report.md
"@
}

if (-not (Test-AppiumListening)) {
    Write-Warn "Appium не слушает :4723 — запускаю start_kt06_services.ps1 -SkipEmulator"
    & (Join-Path $ScriptDir "start_kt06_services.ps1") -SkipEmulator
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

if (-not $Udid) { $Udid = $devices[0] }
Write-Ok "Используется устройство: $Udid (один session на suite, без рестарта эмулятора)"

New-Item -ItemType Directory -Force -Path $paths.Artifacts | Out-Null
New-Item -ItemType Directory -Force -Path $paths.Screenshots | Out-Null

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$junit = Join-Path $paths.Artifacts "junit_kt06_$stamp.xml"
$html = Join-Path $paths.Artifacts "report_kt06_$stamp.html"
$log = Join-Path $paths.Artifacts "pytest_kt06_$stamp.log"
$testFile = Join-Path $RepoRoot "mobile\tests\test_kt06_appium.py"

Write-Step "pytest KT06 (один прогон)"
Write-Host (& $paths.VenvPython -m pytest --version)

Push-Location $paths.Mobile
try {
    & $paths.VenvPython -m pytest `
        "tests/test_kt06_appium.py" `
        -v --tb=short --timeout=120 `
        "--junitxml=$junit" `
        "--html=$html" `
        "--self-contained-html" `
        "--appium-server=$AppiumServer" `
        "--udid=$Udid" `
        2>&1 | Tee-Object -FilePath $log
    $code = $LASTEXITCODE
} finally {
    Pop-Location
}

Write-Step "Артефакты"
Write-Host "log:    $log"
Write-Host "junit:  $junit"
Write-Host "html:   $html"
Write-Host "shots:  $($paths.Screenshots)"
Write-Host "exit:   $code"

if ($code -eq 0) {
    Write-Ok "KT06: все тесты PASS"
} else {
    Write-Warn "KT06 завершился с кодом $code (см. лог)."
}
exit $code
