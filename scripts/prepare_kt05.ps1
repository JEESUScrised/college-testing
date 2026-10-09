#Requires -Version 5.1
<#
.SYNOPSIS
  Подготовка окружения KT05 (при включённом VPN / доступе в интернет).
.DESCRIPTION
  Проверяет Python/.venv, зависимости, Chrome, кэширует ChromeDriver локально,
  выполняет pytest --collect-only для KT05 без запуска браузера на сайте.
#>
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Write-Step([string]$Message) { Write-Host "`n=== $Message ===" -ForegroundColor Cyan }
function Write-Ok([string]$Message) { Write-Host "[OK] $Message" -ForegroundColor Green }
function Write-Warn([string]$Message) { Write-Host "[!] $Message" -ForegroundColor Yellow }
function Fail([string]$Message) {
    Write-Host "[ОШИБКА] $Message" -ForegroundColor Red
    exit 1
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
Set-Location $RepoRoot

Write-Host "Репозиторий: $RepoRoot"
Write-Host "Режим: подготовка KT05 (допускается скачивание пакетов/драйверов)"

# --- Python / venv ---
Write-Step "Python и виртуальное окружение"
$VenvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$VenvPip = Join-Path $RepoRoot ".venv\Scripts\pip.exe"

if (-not (Get-Command py -ErrorAction SilentlyContinue) -and -not (Get-Command python -ErrorAction SilentlyContinue)) {
    Fail "Не найден Python. Установите Python 3.10+ и повторите."
}

if (-not (Test-Path $VenvPython)) {
    Write-Warn ".venv не найден — создаю..."
    if (Get-Command py -ErrorAction SilentlyContinue) {
        py -3 -m venv .venv
    } else {
        python -m venv .venv
    }
}

if (-not (Test-Path $VenvPython)) {
    Fail "Не удалось создать .venv. Проверьте установку Python."
}

$pyVer = & $VenvPython -c "import sys; print(sys.version.split()[0])"
Write-Ok "Интерпретатор: $VenvPython ($pyVer)"

# --- Dependencies ---
Write-Step "Зависимости KT05 (pytest, selenium, html/timeout)"
& $VenvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { Fail "pip upgrade завершился с кодом $LASTEXITCODE" }

$Req = Join-Path $RepoRoot "selenium\requirements.txt"
if (-not (Test-Path $Req)) { Fail "Не найден файл $Req" }
& $VenvPip install -r $Req
if ($LASTEXITCODE -ne 0) { Fail "Установка зависимостей из selenium\requirements.txt не удалась (код $LASTEXITCODE)" }

& $VenvPython -c "import pytest, selenium, pytest_html, pytest_timeout; print('pytest', pytest.__version__); print('selenium', selenium.__version__)"
if ($LASTEXITCODE -ne 0) { Fail "Импорт зависимостей KT05 не удался" }
Write-Ok "Пакеты pytest/selenium/pytest-html/pytest-timeout установлены"

# --- Required project files ---
Write-Step "Локальные файлы KT05"
$required = @(
    "selenium\conftest.py",
    "selenium\pages\vdnh_pages.py",
    "selenium\tests\test_kt05_vdnh_news.py",
    "pytest.ini",
    "scripts\_cache_chromedriver.py"
)
foreach ($rel in $required) {
    $full = Join-Path $RepoRoot $rel
    if (-not (Test-Path $full)) { Fail "Отсутствует обязательный файл: $rel" }
    Write-Ok $rel
}

# --- Chrome ---
Write-Step "Google Chrome"
$chromeCandidates = @(
    "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
)
$chromePath = $chromeCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $chromePath) {
    Fail "Google Chrome не найден. Установите Chrome и повторите подготовку."
}
$chromeVer = (Get-Item $chromePath).VersionInfo.FileVersion
Write-Ok "Chrome: $chromePath ($chromeVer)"

# --- Cache ChromeDriver locally ---
Write-Step "Локальный ChromeDriver (кэш для запуска без VPN)"
$DriversDir = Join-Path $RepoRoot "selenium\drivers"
New-Item -ItemType Directory -Force -Path $DriversDir | Out-Null
$DriverExe = Join-Path $DriversDir "chromedriver.exe"

& $VenvPython (Join-Path $RepoRoot "scripts\_cache_chromedriver.py")
if ($LASTEXITCODE -ne 0) {
    Fail "Не удалось скачать/закэшировать ChromeDriver. Проверьте VPN/интернет и повторите."
}
if (-not (Test-Path $DriverExe)) {
    Fail "Файл selenium\drivers\chromedriver.exe не появился после кэширования."
}
$driverSize = (Get-Item $DriverExe).Length
Write-Ok "ChromeDriver готов: $DriverExe ($driverSize байт)"

# Smoke: start chromedriver binary briefly (--version)
$driverVerOut = & $DriverExe --version 2>&1
Write-Ok "Версия драйвера: $driverVerOut"

# --- Proxy diagnostics (informational) ---
Write-Step "Проверка proxy-переменных окружения"
$proxyVars = @("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy", "NO_PROXY", "no_proxy")
$foundProxy = $false
foreach ($name in $proxyVars) {
    $val = [Environment]::GetEnvironmentVariable($name, "Process")
    if (-not $val) { $val = [Environment]::GetEnvironmentVariable($name, "User") }
    if (-not $val) { $val = [Environment]::GetEnvironmentVariable($name, "Machine") }
    if ($val) {
        $foundProxy = $true
        Write-Warn "$name=$val"
    }
}
if ($foundProxy) {
    Write-Warn "Обнаружены proxy-переменные. Скрипт запуска очистит их в своём процессе."
    Write-Warn "Если после отключения VPN трафик всё ещё идёт через прокси — проверьте системные настройки Windows."
} else {
    Write-Ok "Явных proxy-переменных не найдено"
}

# --- Collect-only (no browser against vdnh) ---
Write-Step "Сбор тестов KT05 (pytest --collect-only, без открытия сайта)"
$env:SELENIUM_CHROMEDRIVER = $DriverExe
$collectLog = Join-Path $RepoRoot "selenium\artifacts\kt05\prepare_collect.txt"
New-Item -ItemType Directory -Force -Path (Split-Path $collectLog) | Out-Null

& $VenvPython -m pytest selenium\tests\test_kt05_vdnh_news.py --collect-only -q --browser=chrome 2>&1 |
    Tee-Object -FilePath $collectLog
if ($LASTEXITCODE -ne 0) {
    Fail "pytest --collect-only завершился с кодом $LASTEXITCODE. Смотрите $collectLog"
}

$collectText = Get-Content $collectLog -Raw
if ($collectText -notmatch "test_kt05") {
    Fail "В collect-only не видно тестов KT05. Проверьте selenium\tests\test_kt05_vdnh_news.py"
}
Write-Ok "Тесты KT05 успешно собраны (лог: $collectLog)"

Write-Step "Подготовка завершена"
Write-Host @"

Дальнейшие шаги:
  1. ОТКЛЮЧИТЕ VPN вручную.
  2. Откройте отдельное окно PowerShell.
  3. Выполните:
       cd `"$RepoRoot`"
       .\scripts\run_kt05_no_vpn.ps1
  4. Дождитесь завершения одного прогона.
  5. Включите VPN и передайте артефакты из selenium\artifacts\kt05\ и screenshots\kt05\

"@ -ForegroundColor Green

exit 0
