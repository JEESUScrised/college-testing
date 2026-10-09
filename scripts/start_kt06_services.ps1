#Requires -Version 5.1
<#
.SYNOPSIS
  Запуск локальных сервисов KT06: эмулятор (если есть AVD) + Appium 3 на :4723.
  Не дублирует уже запущенные процессы.
#>
[CmdletBinding()]
param(
    [string]$AvdName = $env:ANDROID_AVD_NAME,
    [switch]$SkipEmulator
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
. (Join-Path $ScriptDir "_kt06_common.ps1")
Set-Location $RepoRoot

$sdk = Initialize-AndroidEnv
$paths = Get-MobilePaths -RepoRoot $RepoRoot
$adb = Get-AdbPath -Sdk $sdk
$emu = Join-Path $sdk "emulator\emulator.exe"

Write-Step "Проверка устройств"
$devices = Get-ReadyAndroidDevices -AdbPath $adb
if ($devices.Count -gt 0) {
    Write-Ok ("Уже готовы: " + ($devices -join ", "))
} elseif (-not $SkipEmulator) {
    if (-not (Test-Path $emu)) {
        Fail "emulator.exe не найден. Установите Android Emulator или подключите устройство."
    }
    $avds = @(& $emu -list-avds 2>&1 | Where-Object { $_ -and $_.ToString().Trim() })
    if (-not $AvdName) {
        if ($avds.Count -eq 0) {
            Fail @"
Нет AVD и нет подключённых устройств.
Установите system image и создайте AVD (см. mobile/environment-report.md),
либо подключите телефон с USB debugging.
"@
        }
        $AvdName = $avds[0]
    }
    Write-Step "Запуск эмулятора $AvdName (один раз)"
    Start-Process -FilePath $emu -ArgumentList @("-avd", $AvdName, "-netdelay", "none", "-netspeed", "full") -WindowStyle Normal
    Write-Host "Ожидание boot completed..."
    $deadline = (Get-Date).AddMinutes(3)
    do {
        Start-Sleep -Seconds 5
        $devices = Get-ReadyAndroidDevices -AdbPath $adb
        $booted = $false
        if ($devices.Count -gt 0) {
            $prop = & $adb -s $devices[0] shell getprop sys.boot_completed 2>$null
            $booted = ($prop -match "1")
        }
    } while (-not $booted -and (Get-Date) -lt $deadline)
    if (-not $booted) {
        Fail "Эмулятор не загрузился за 3 минуты. Проверьте AVD вручную."
    }
    Write-Ok ("Эмулятор готов: " + $devices[0])
} else {
    Fail "Нет устройств и -SkipEmulator задан."
}

Write-Step "Appium server http://127.0.0.1:4723"
if (Test-AppiumListening) {
    Write-Ok "Appium уже слушает :4723 — новый процесс не запускаю"
} else {
    if (-not (Test-Path $paths.AppiumCmd)) {
        Fail "Appium не найден. cd mobile; npm ci; npx appium driver install uiautomator2"
    }
    New-Item -ItemType Directory -Force -Path $paths.Artifacts | Out-Null
    $log = Join-Path $paths.Artifacts ("appium_" + (Get-Date -Format "yyyyMMdd_HHmmss") + ".log")
    $proc = Start-Process -FilePath $paths.AppiumCmd -ArgumentList @("--address", "127.0.0.1", "--port", "4723") `
        -WorkingDirectory $paths.Mobile -RedirectStandardOutput $log -RedirectStandardError $log -PassThru -WindowStyle Hidden
    Write-Host "Appium PID=$($proc.Id), log=$log"
    $ok = $false
    for ($i = 0; $i -lt 30; $i++) {
        Start-Sleep -Seconds 1
        if (Test-AppiumListening) { $ok = $true; break }
    }
    if (-not $ok) { Fail "Appium не ответил на /status за 30 с. См. $log" }
    Write-Ok "Appium запущен"
}

Write-Ok "Сервисы KT06 готовы. Далее: .\scripts\run_kt06.ps1"
