#Requires -Version 5.1
# Shared helpers for KT06 / future KT09 Appium scripts. Dot-source from sibling scripts.

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Write-Step([string]$Message) { Write-Host "`n=== $Message ===" -ForegroundColor Cyan }
function Write-Ok([string]$Message) { Write-Host "[OK] $Message" -ForegroundColor Green }
function Write-Warn([string]$Message) { Write-Host "[!] $Message" -ForegroundColor Yellow }
function Fail([string]$Message) {
    Write-Host "[ОШИБКА] $Message" -ForegroundColor Red
    exit 1
}

function Initialize-AndroidEnv {
    $sdkCandidates = @(
        $env:ANDROID_HOME,
        $env:ANDROID_SDK_ROOT,
        (Join-Path $env:LOCALAPPDATA "Android\Sdk"),
        (Join-Path $env:USERPROFILE "AppData\Local\Android\Sdk")
    ) | Where-Object { $_ } | Select-Object -Unique

    $sdk = $null
    foreach ($c in $sdkCandidates) {
        if ($c -and (Test-Path $c)) { $sdk = $c; break }
    }
    if (-not $sdk) {
        Fail "Android SDK не найден. Установите SDK и задайте ANDROID_HOME."
    }

    $env:ANDROID_HOME = $sdk
    $env:ANDROID_SDK_ROOT = $sdk

    $platformTools = Join-Path $sdk "platform-tools"
    $emulatorDir = Join-Path $sdk "emulator"
    $pathParts = $env:Path -split ";"
    foreach ($p in @($platformTools, $emulatorDir)) {
        if ((Test-Path $p) -and ($pathParts -notcontains $p)) {
            $env:Path = "$p;$env:Path"
        }
    }

    if (-not $env:JAVA_HOME -or -not (Test-Path $env:JAVA_HOME)) {
        $jdk = "C:\Program Files\Eclipse Adoptium\jdk-17.0.1.12-hotspot"
        if (Test-Path $jdk) { $env:JAVA_HOME = $jdk }
    }

    return $sdk
}

function Get-AdbPath {
    param([string]$Sdk)
    $adb = Join-Path $Sdk "platform-tools\adb.exe"
    if (-not (Test-Path $adb)) { Fail "adb не найден: $adb" }
    return $adb
}

function Get-ReadyAndroidDevices {
    param([string]$AdbPath)
    $lines = & $AdbPath devices | Where-Object { $_ -match "\tdevice$" }
    return @($lines | ForEach-Object { ($_ -split "\s+")[0] })
}

function Test-AppiumListening {
    param([string]$Url = "http://127.0.0.1:4723/status")
    try {
        $resp = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 3
        return ($resp.StatusCode -eq 200)
    } catch {
        return $false
    }
}

function Get-MobilePaths {
    param([string]$RepoRoot)
    return [pscustomobject]@{
        Mobile      = Join-Path $RepoRoot "mobile"
        AppiumCmd   = Join-Path $RepoRoot "mobile\node_modules\.bin\appium.cmd"
        VenvPython  = Join-Path $RepoRoot ".venv\Scripts\python.exe"
        Apk         = Join-Path $RepoRoot "mobile\apps\ApiDemos-debug.apk"
        Artifacts   = Join-Path $RepoRoot "mobile\artifacts"
        Screenshots = Join-Path $RepoRoot "screenshots\kt06"
    }
}
