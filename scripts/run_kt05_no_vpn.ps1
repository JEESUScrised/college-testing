#Requires -Version 5.1
<#
.SYNOPSIS
  Однократный запуск ТОЛЬКО KT05 без VPN / без Cursor.
.DESCRIPTION
  Использует локальный .venv и закэшированный ChromeDriver.
  Не скачивает пакеты и драйверы. Не меняет системный VPN/прокси.
  Один вызов = один прогон pytest KT05.
#>
[CmdletBinding()]
param(
    # Защита от случайного повторного запуска в том же каталоге артефактов.
    [switch]$Force
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Write-Step([string]$Message) { Write-Host "`n=== $Message ===" -ForegroundColor Cyan }
function Write-Ok([string]$Message) { Write-Host "[OK] $Message" -ForegroundColor Green }
function Write-Warn([string]$Message) { Write-Host "[!] $Message" -ForegroundColor Yellow }
function Fail([string]$Message) {
    Write-Host "[ОШИБКА] $Message" -ForegroundColor Red
    exit 1
}

# Resolve repo root from script location (independent of current directory).
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $ScriptDir "..")).Path
Set-Location $RepoRoot

$ArtifactsDir = Join-Path $RepoRoot "selenium\artifacts\kt05"
$LockFile = Join-Path $ArtifactsDir "run.lock"
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogFile = Join-Path $ArtifactsDir "pytest_$Stamp.log"
$JUnitFile = Join-Path $ArtifactsDir "junit_$Stamp.xml"
$HtmlFile = Join-Path $ArtifactsDir "report_$Stamp.html"
$SummaryFile = Join-Path $ArtifactsDir "summary_$Stamp.txt"
$DriverExe = Join-Path $RepoRoot "selenium\drivers\chromedriver.exe"
$VenvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$ScreenshotsDir = Join-Path $RepoRoot "screenshots\kt05"

New-Item -ItemType Directory -Force -Path $ArtifactsDir | Out-Null
New-Item -ItemType Directory -Force -Path $ScreenshotsDir | Out-Null

Write-Host "Репозиторий: $RepoRoot"
Write-Host "Режим: ОДИН прогон KT05 (без загрузки пакетов/драйверов)"

# --- Guard: single run / no automatic retries ---
if ((Test-Path $LockFile) -and -not $Force) {
    $lockInfo = Get-Content $LockFile -Raw
    Fail "Обнаружен lock-файл $LockFile.`n$lockInfo`nЕсли предыдущий запуск завершился аварийно — удалите lock вручную или запустите с -Force. Автоповторов нет."
}
if ((Test-Path $LockFile) -and $Force) {
    Write-Warn "Удаляю lock-файл по флагу -Force"
    Remove-Item $LockFile -Force
}

@"
started=$Stamp
pid=$PID
script=$($MyInvocation.MyCommand.Path)
"@ | Set-Content -Path $LockFile -Encoding UTF8

try {
    # --- Preconditions (offline-safe) ---
    Write-Step "Проверка локальных предпосылок"
    if (-not (Test-Path $VenvPython)) {
        Fail "Не найден $VenvPython. Сначала выполните scripts\prepare_kt05.ps1 при включённом VPN."
    }
    if (-not (Test-Path $DriverExe)) {
        Fail "Не найден локальный ChromeDriver: $DriverExe`nСначала выполните scripts\prepare_kt05.ps1 при включённом VPN."
    }
    $required = @(
        "selenium\tests\test_kt05_vdnh_news.py",
        "selenium\pages\vdnh_pages.py",
        "selenium\conftest.py",
        "pytest.ini"
    )
    foreach ($rel in $required) {
        if (-not (Test-Path (Join-Path $RepoRoot $rel))) {
            Fail "Отсутствует $rel"
        }
    }
    Write-Ok "Python/драйвер/файлы KT05 на месте"

    # --- Clear proxy for THIS process only (do not change system VPN) ---
    Write-Step "Сетевые настройки процесса (без изменения системного VPN)"
    $proxyNames = @(
        "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy",
        "NO_PROXY", "no_proxy"
    )
    foreach ($name in $proxyNames) {
        if (Test-Path "Env:$name") {
            Write-Warn "Очищаю process-переменную $name (было: $((Get-Item Env:$name).Value))"
            Remove-Item "Env:$name" -ErrorAction SilentlyContinue
        }
    }
    # Prefer direct connection for Selenium Manager offline mode.
    $env:SE_OFFLINE = "1"
    $env:SELENIUM_CHROMEDRIVER = $DriverExe
    $env:SE_AVOID_STATS = "true"
    Write-Ok "SE_OFFLINE=1; SELENIUM_CHROMEDRIVER=$DriverExe"
    Write-Warn "VPN должен быть ОТКЛЮЧЁН вручную. Скрипт не управляет VPN."

    # Quick connectivity hint (non-fatal)
    try {
        $probe = Test-NetConnection vdnh.ru -Port 443 -WarningAction SilentlyContinue
        if ($probe.TcpTestSucceeded) {
            Write-Ok "TCP 443 до vdnh.ru доступен"
        } else {
            Write-Warn "TCP 443 до vdnh.ru недоступен — тесты, скорее всего, упадут по сети"
        }
    } catch {
        Write-Warn "Не удалось проверить TCP до vdnh.ru: $($_.Exception.Message)"
    }

    # --- Exactly one pytest invocation for KT05 only ---
    Write-Step "Запуск ОДНОГО прогона KT05"
    Write-Host "Лог:      $LogFile"
    Write-Host "JUnit:    $JUnitFile"
    Write-Host "HTML:     $HtmlFile"
    Write-Host "Скриншоты ожидаются в: $ScreenshotsDir"

    # Timeouts:
    # - page load bounded in conftest (strategy=none, ~20s)
    # - pytest-timeout per test (180s) to avoid indefinite hang
    # - no --count / no reruns
    $pytestArgs = @(
        "-m", "pytest",
        "selenium\tests\test_kt05_vdnh_news.py",
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

    $started = Get-Date
    # Tee output to log; preserve pytest exit code (no retries).
    & $VenvPython @pytestArgs 2>&1 | Tee-Object -FilePath $LogFile
    $exitCode = $LASTEXITCODE
    $ended = Get-Date
    $duration = New-TimeSpan -Start $started -End $ended

    # Parse rough summary from log
    $logText = Get-Content $LogFile -Raw -ErrorAction SilentlyContinue
    $summaryLine = ($logText -split "`n" | Where-Object { $_ -match "passed|failed|error|skipped" } | Select-Object -Last 3) -join " | "

    $statusWord = if ($exitCode -eq 0) { "УСПЕХ (PASS)" } else { "ЕСТЬ ПАДЕНИЯ / ОШИБКИ (FAIL)" }
    $color = if ($exitCode -eq 0) { "Green" } else { "Red" }

    $summary = @"
KT05 — итог одиночного прогона
Дата: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Длительность: $($duration.ToString())
Код выхода pytest: $exitCode
Интерпретация: $(if ($exitCode -eq 0) { "все собранные тесты KT05 прошли" } elseif ($exitCode -eq 1) { "были упавшие тесты (failed assertions)" } elseif ($exitCode -eq 2) { "ошибка выполнения/прерывание" } else { "см. лог pytest" })
Строки итога: $summaryLine

Артефакты:
- Лог: $LogFile
- JUnit XML: $JUnitFile
- HTML: $HtmlFile
- Скриншоты: $ScreenshotsDir
- Сводка: $SummaryFile

Важно: скрипт выполнил РОВНО один прогон и не делает автоматических повторов.
"@

    $summary | Set-Content -Path $SummaryFile -Encoding UTF8
    Write-Host "`n================ ИТОГ ================" -ForegroundColor $color
    Write-Host $summary -ForegroundColor $color

    exit $exitCode
}
finally {
    if (Test-Path $LockFile) {
        Remove-Item $LockFile -Force -ErrorAction SilentlyContinue
    }
}
