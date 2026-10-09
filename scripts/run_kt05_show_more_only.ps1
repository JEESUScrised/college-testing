#Requires -Version 5.1
<#
.SYNOPSIS
  Один целевой прогон ТОЛЬКО test_show_more_loads_additional_cards.
.DESCRIPTION
  Для ручного запуска без VPN после правки Page Object.
  Не повторяет полный suite KT05. Автоповторов нет.
#>
[CmdletBinding()]
param([switch]$Force)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Fail([string]$Message) {
    Write-Host "[ОШИБКА] $Message" -ForegroundColor Red
    exit 1
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $ScriptDir "..")).Path
Set-Location $RepoRoot

$ArtifactsDir = Join-Path $RepoRoot "selenium\artifacts\kt05"
$LockFile = Join-Path $ArtifactsDir "run.lock"
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogFile = Join-Path $ArtifactsDir "pytest_show_more_$Stamp.log"
$JUnitFile = Join-Path $ArtifactsDir "junit_show_more_$Stamp.xml"
$HtmlFile = Join-Path $ArtifactsDir "report_show_more_$Stamp.html"
$SummaryFile = Join-Path $ArtifactsDir "summary_show_more_$Stamp.txt"
$DriverExe = Join-Path $RepoRoot "selenium\drivers\chromedriver.exe"
$VenvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"

New-Item -ItemType Directory -Force -Path $ArtifactsDir | Out-Null

if ((Test-Path $LockFile) -and -not $Force) {
    Fail "Lock $LockFile существует. Удалите или запустите с -Force."
}
if ((Test-Path $LockFile) -and $Force) { Remove-Item $LockFile -Force }

@"
started=$Stamp
pid=$PID
mode=show_more_only
"@ | Set-Content $LockFile -Encoding UTF8

try {
    if (-not (Test-Path $VenvPython)) { Fail "Нет .venv — сначала prepare_kt05.ps1" }
    if (-not (Test-Path $DriverExe)) { Fail "Нет локального ChromeDriver — сначала prepare_kt05.ps1" }

    foreach ($name in @("HTTP_PROXY","HTTPS_PROXY","ALL_PROXY","http_proxy","https_proxy","all_proxy")) {
        if (Test-Path "Env:$name") { Remove-Item "Env:$name" -ErrorAction SilentlyContinue }
    }
    $env:SE_OFFLINE = "1"
    $env:SELENIUM_CHROMEDRIVER = $DriverExe
    $env:SE_AVOID_STATS = "true"

    Write-Host "ОДИН целевой тест: test_show_more_loads_additional_cards"
    Write-Host "VPN должен быть ОТКЛЮЧЁН вручную."
    Write-Host "Лог: $LogFile"

    $args = @(
        "-m", "pytest",
        "selenium\tests\test_kt05_vdnh_news.py::test_show_more_loads_additional_cards",
        "-v",
        "--browser=chrome",
        "--page-load-strategy=none",
        "--timeout=180",
        "--timeout-method=thread",
        "--junitxml=$JUnitFile",
        "--html=$HtmlFile",
        "--self-contained-html",
        "-p", "no:cacheprovider"
    )

    & $VenvPython @args 2>&1 | Tee-Object -FilePath $LogFile
    $code = $LASTEXITCODE

    $summary = @"
Целевой прогон show_more
Дата: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Exit code: $code
Log: $LogFile
JUnit: $JUnitFile
HTML: $HtmlFile
Screenshots: screenshots\kt05\09_before_show_more.png / 10_after_show_more*.png
"@
    $summary | Set-Content $SummaryFile -Encoding UTF8
    Write-Host $summary
    exit $code
}
finally {
    if (Test-Path $LockFile) { Remove-Item $LockFile -Force -ErrorAction SilentlyContinue }
}
