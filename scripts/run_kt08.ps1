#Requires -Version 5.1
param(
    [string]$TestPath = "selenium\tests\test_kt08_visual.py"
)
$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot
$venvPy = Join-Path $RepoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPy)) { throw "Missing .venv" }
$artifacts = Join-Path $RepoRoot "selenium\artifacts\kt08"
New-Item -ItemType Directory -Force -Path $artifacts, (Join-Path $RepoRoot "screenshots\kt08") | Out-Null
$baseline = Join-Path $RepoRoot "selenium\baselines\kt08\home_baseline.png"
if (-not (Test-Path $baseline)) {
    Write-Host "Baseline missing - generating..."
    & $venvPy "selenium\visual\generate_kt08_baselines.py"
}
$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$junit = Join-Path $artifacts "junit_kt08_$stamp.xml"
$html = Join-Path $artifacts "report_kt08_$stamp.html"
$log = Join-Path $artifacts "pytest_kt08_$stamp.log"
& $venvPy -m pytest $TestPath -v --tb=short --browser=chrome "--junitxml=$junit" "--html=$html" "--self-contained-html" 2>&1 | Tee-Object -FilePath $log
$code = $LASTEXITCODE
Write-Host "exit=$code log=$log"
exit $code