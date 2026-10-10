#Requires -Version 5.1
$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot
$py = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$artifacts = Join-Path $RepoRoot "selenium\artifacts\kt10"
New-Item -ItemType Directory -Force -Path $artifacts | Out-Null
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$log = Join-Path $artifacts "diagnose_kt10_$stamp.log"

function Log([string]$msg) {
    $line = "[$(Get-Date -Format o)] $msg"
    Write-Host $line
    Add-Content -Path $log -Value $line -Encoding UTF8
}

Log "=== KT10 diagnose ==="
Log ("python=" + (& $py --version 2>&1))
Log ("selenium=" + (& $py -c "import selenium; print(selenium.__version__)"))
Log ("pytest=" + (& $py -m pytest --version 2>&1))
Log ("pytest-html=" + (& $py -c "import pytest_html; print(pytest_html.__version__)"))

$chromePath = @(
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1
$ffPath = @(
    "$env:ProgramFiles\Mozilla Firefox\firefox.exe",
    "${env:ProgramFiles(x86)}\Mozilla Firefox\firefox.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1
Log ("chrome_exe=" + $chromePath)
Log ("firefox_exe=" + $ffPath)
if (-not $chromePath) { throw "Chrome not found" }
if (-not $ffPath) { throw "Firefox not found. Install via winget or choose another matrix." }

$smoke = Join-Path $PSScriptRoot "_kt10_browser_smoke.py"
& $py $smoke 2>&1 | ForEach-Object { Log ("$_") }
if ($LASTEXITCODE -ne 0) { throw "browser smoke failed" }

Log ("log=" + $log)
Write-Host "READY"
