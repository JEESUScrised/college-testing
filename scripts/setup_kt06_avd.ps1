#Requires -Version 5.1
<#
.SYNOPSIS
  Установка system image API 33 + создание AVD KT06_API33 (для KT06/KT09).
.DESCRIPTION
  Не скачивает multi-GB image без явного -ApproveDownload.
  Не устанавливает Android Studio. Не меняет виртуализацию Windows.
.PARAMETER ApproveDownload
  Явное согласие на загрузку system-images;android-33;google_apis;x86_64 (~1–2+ ГБ).
.PARAMETER Force
  Пересоздать AVD, если уже существует.
#>
[CmdletBinding()]
param(
    [switch]$ApproveDownload,
    [switch]$Force,
    [string]$AvdName = "KT06_API33",
    [string]$Package = "system-images;android-33;google_apis;x86_64",
    [string]$DeviceProfile = "pixel_6"
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
. (Join-Path $ScriptDir "_kt06_common.ps1")
Set-Location $RepoRoot

$logDir = Join-Path $RepoRoot "mobile\artifacts"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$logFile = Join-Path $logDir ("setup_avd_" + (Get-Date -Format "yyyyMMdd_HHmmss") + ".log")

function Log([string]$Message) {
    $line = "[{0}] {1}" -f (Get-Date -Format "HH:mm:ss"), $Message
    Add-Content -Path $logFile -Value $line -Encoding UTF8
    Write-Host $line
}

function Invoke-Logged {
    param([string]$FilePath, [string[]]$ArgumentList, [string]$Label)
    Log "CMD: $FilePath $($ArgumentList -join ' ')"
    $out = & $FilePath @ArgumentList 2>&1
    $text = ($out | Out-String)
    Add-Content -Path $logFile -Value $text -Encoding UTF8
    if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) {
        Write-Host $text
        Fail "$Label failed with exit $LASTEXITCODE. Log: $logFile"
    }
    return $text
}

Write-Step "setup_kt06_avd — log: $logFile"
$sdk = Initialize-AndroidEnv
Log "ANDROID_HOME=$sdk"
Log "JAVA_HOME=$($env:JAVA_HOME)"

$sdkmanager = Join-Path $sdk "cmdline-tools\latest\bin\sdkmanager.bat"
$avdmanager = Join-Path $sdk "cmdline-tools\latest\bin\avdmanager.bat"
$emu = Join-Path $sdk "emulator\emulator.exe"
$adb = Get-AdbPath -Sdk $sdk

if (-not (Test-Path $sdkmanager)) {
    Fail "sdkmanager не найден: $sdkmanager. Установите cmdline-tools в SDK\cmdline-tools\latest."
}
if (-not (Test-Path $avdmanager)) {
    Fail "avdmanager не найден: $avdmanager"
}

Write-Step "Preflight: acceleration"
$accel = & $emu -accel-check 2>&1 | Out-String
Log $accel.Trim()
if ($accel -notmatch "usable|WHPX|HAXM|AEHD|Windows Hypervisor") {
    Fail @"
Аппаратное ускорение эмулятора недоступно (emulator -accel-check).
Не переключаюсь на крайне медленную software-эмуляцию.
Включите Windows Hypervisor Platform / виртуализацию в BIOS, затем повторите.
Вывод:
$accel
"@
}
if ($accel -match "not usable|is NOT|disabled|ERROR") {
    # WHPX line often says "usable" — only fail on clear negatives without usable
    if ($accel -notmatch "is installed and usable") {
        Fail "Acceleration blocker:`n$accel"
    }
}
Write-Ok "Acceleration OK (WHPX/HAXM usable)"

Write-Step "Disk / memory"
$drive = (Get-Item $sdk).PSDrive.Name
$freeGB = [math]::Round((Get-PSDrive $drive).Free / 1GB, 2)
$os = Get-CimInstance Win32_OperatingSystem
$freeRamGB = [math]::Round(($os.FreePhysicalMemory / 1MB), 2)
Log "SDK drive ${drive}: free=${freeGB} GB; Free RAM≈${freeRamGB} GB"
Write-Host "Требуется пакет: $Package"
Write-Host "Ориентировочный размер загрузки: ~1.0–2.5 ГБ (+ место AVD userdata)."
Write-Host "Свободно на ${drive}:: $freeGB GB"
if ($freeGB -lt 6) {
    Fail "Мало места на диске ${drive}: ($freeGB GB). Нужно ≥6 ГБ свободно."
}

Write-Step "Проверка установленного image"
$installed = & $sdkmanager --list_installed 2>&1 | Out-String
Add-Content -Path $logFile -Value $installed -Encoding UTF8
$imageInstalled = $installed -match [regex]::Escape($Package)
$imagePath = Join-Path $sdk ("system-images\android-33\google_apis\x86_64")
if ((Test-Path $imagePath) -and (Test-Path (Join-Path $imagePath "system.img"))) {
    $imageInstalled = $true
}
Log "Image installed=$imageInstalled pathExists=$(Test-Path $imagePath)"

if (-not $imageInstalled) {
    if (-not $ApproveDownload) {
        Write-Warn @"

=== ТРЕБУЕТСЯ ЯВНОЕ СОГЛАСИЕ НА ЗАГРУЗКУ ===
Будет скачан multi-gigabyte package:
  $Package
Диск: ${drive}: свободно $freeGB GB
После согласия выполните:
  .\scripts\setup_kt06_avd.ps1 -ApproveDownload

"@
        Fail "Загрузка отменена: нет -ApproveDownload."
    }
    Write-Step "Установка $Package (sdkmanager)"
    Log "User approved download via -ApproveDownload"
    # Accept licenses non-interactively
    $licenses = "y`ny`ny`ny`ny`ny`ny`ny`ny`ny`n"
    $licenses | & $sdkmanager --licenses 2>&1 | Out-Null
    Log "Installing package via sdkmanager..."
    $proc = Start-Process -FilePath $sdkmanager -ArgumentList @($Package) `
        -NoNewWindow -Wait -PassThru -RedirectStandardOutput (Join-Path $logDir "sdkmanager_stdout.log") `
        -RedirectStandardError (Join-Path $logDir "sdkmanager_stderr.log")
    # Also try with yes pipe for license prompts during install
    if ($proc.ExitCode -ne 0) {
        Log "First sdkmanager exit=$($proc.ExitCode); retry with yes pipe"
        cmd /c "echo y| `"$sdkmanager`" `"$Package`"" 2>&1 | Tee-Object -FilePath (Join-Path $logDir "sdkmanager_retry.log")
        if ($LASTEXITCODE -ne 0) {
            Fail "sdkmanager не установил $Package. См. $logDir"
        }
    }
    if (-not (Test-Path (Join-Path $imagePath "system.img"))) {
        Fail "После установки не найден system.img в $imagePath"
    }
    Write-Ok "System image установлен"
} else {
    Write-Ok "System image уже установлен — повторная загрузка не нужна"
}

Write-Step "AVD $AvdName"
$existing = @(& $emu -list-avds 2>&1 | ForEach-Object { $_.ToString().Trim() } | Where-Object { $_ })
Log ("Existing AVDs: " + ($existing -join ", "))
if ($existing -contains $AvdName) {
    if (-not $Force) {
        Write-Ok "AVD $AvdName уже существует — создание пропущено"
        Write-Host "Для пересоздания: .\scripts\setup_kt06_avd.ps1 -Force -ApproveDownload"
        Log "Done (reuse existing AVD)"
        exit 0
    }
    Log "Force: deleting AVD $AvdName"
    & $avdmanager delete avd -n $AvdName 2>&1 | Tee-Object -FilePath $logFile -Append
}

# List device profiles; fall back if pixel_6 missing
$devicesOut = & $avdmanager list device 2>&1 | Out-String
Add-Content -Path $logFile -Value $devicesOut -Encoding UTF8
$profile = $DeviceProfile
if ($devicesOut -notmatch [regex]::Escape("id: $DeviceProfile") -and $devicesOut -notmatch "`"$DeviceProfile`"") {
    foreach ($candidate in @("pixel_6", "pixel_5", "pixel_4", "pixel", "medium_phone")) {
        if ($devicesOut -match [regex]::Escape($candidate)) { $profile = $candidate; break }
    }
    Log "Selected device profile: $profile"
}

Write-Host "Creating AVD: name=$AvdName package=$Package device=$profile"
# echo no = do not create custom hardware profile interactively
$createOut = cmd /c "echo no| `"$avdmanager`" create avd -n $AvdName -k `"$Package`" -d $profile --force" 2>&1
$createText = $createOut | Out-String
Add-Content -Path $logFile -Value $createText -Encoding UTF8
Write-Host $createText

$after = @(& $emu -list-avds 2>&1 | ForEach-Object { $_.ToString().Trim() } | Where-Object { $_ })
if ($after -notcontains $AvdName) {
    Fail "AVD $AvdName не появился в emulator -list-avds. Log: $logFile"
}

# Tune config for modest RAM host
$avdIni = Join-Path $env:USERPROFILE ".android\avd\${AvdName}.avd\config.ini"
if (Test-Path $avdIni) {
    $cfg = Get-Content $avdIni -Raw
    $cfg = $cfg -replace "(?m)^hw\.ramSize=.*$", "hw.ramSize=2048"
    $cfg = $cfg -replace "(?m)^hw\.keyboard=.*$", "hw.keyboard=yes"
    if ($cfg -notmatch "(?m)^hw\.keyboard=") { $cfg += "`nhw.keyboard=yes`n" }
    if ($cfg -notmatch "(?m)^hw\.ramSize=") { $cfg += "`nhw.ramSize=2048`n" }
    Set-Content -Path $avdIni -Value $cfg -Encoding UTF8
    Log "Updated $avdIni (hw.ramSize=2048, keyboard=yes)"
}

Write-Ok "AVD $AvdName готов"
Write-Host "Далее: .\scripts\start_kt06_services.ps1 -AvdName $AvdName"
Log "SUCCESS"
exit 0
