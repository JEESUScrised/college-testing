#Requires -Version 5.1
<#
.SYNOPSIS
  Прогон KT07 против уже запущенного Selenium Grid (:4444).
#>
[CmdletBinding()]
param(
    [string]$GridUrl = "http://127.0.0.1:4444",
    [string]$TestPath = "selenium\tests\test_kt07_grid.py",
    [string]$ExtraArgs = ""
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot

$venvPy = Join-Path $RepoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPy)) { throw "Нет .venv" }

$artifacts = Join-Path $RepoRoot "selenium\artifacts\kt07"
New-Item -ItemType Directory -Force -Path $artifacts, (Join-Path $RepoRoot "screenshots\kt07") | Out-Null

# Health
try {
    $status = Invoke-WebRequest -Uri "$GridUrl/status" -UseBasicParsing -TimeoutSec 5
    $ready = ($status.Content | ConvertFrom-Json).value.ready
    if (-not $ready) { throw "Grid ready=false" }
    Write-Host "[OK] Grid ready at $GridUrl"
} catch {
    throw "Grid недоступен ($GridUrl). Сначала start_standalone.ps1 или start_hub_node.ps1. $_"
}

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$junit = Join-Path $artifacts "junit_kt07_$stamp.xml"
$html = Join-Path $artifacts "report_kt07_$stamp.html"
$log = Join-Path $artifacts "pytest_kt07_$stamp.log"

$argList = @(
    "-m", "pytest",
    $TestPath,
    "-v", "--tb=short",
    "--browser=chrome",
    "--grid-url=$GridUrl",
    "--junitxml=$junit",
    "--html=$html",
    "--self-contained-html"
)
if ($ExtraArgs) { $argList += $ExtraArgs.Split(" ") }

Write-Host "pytest $($argList -join ' ')"
& $venvPy @argList 2>&1 | Tee-Object -FilePath $log
$code = $LASTEXITCODE
Write-Host "exit=$code log=$log"
exit $code
