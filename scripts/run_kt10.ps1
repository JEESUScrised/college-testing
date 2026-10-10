#Requires -Version 5.1
param(
    [switch]$FailureDemoOnly,
    [switch]$SkipFailureDemo
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot
$venvPy = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$artifacts = Join-Path $RepoRoot "selenium\artifacts\kt10"
New-Item -ItemType Directory -Force -Path $artifacts, (Join-Path $RepoRoot "screenshots\kt10") | Out-Null

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"

if ($FailureDemoOnly) {
    # Do not wipe matrix artifacts (events/run_summary/comparison) from a prior suite run.
    $junit = Join-Path $artifacts "junit_kt10_failure_demo_$stamp.xml"
    $html = Join-Path $artifacts "report_kt10_failure_demo_$stamp.html"
    $log = Join-Path $artifacts "pytest_kt10_failure_demo_$stamp.log"
    & $venvPy -m pytest "selenium\crossbrowser\tests\test_kt10_failure_demo.py" -v --tb=short `
        "--junitxml=$junit" "--html=$html" "--self-contained-html" `
        2>&1 | Tee-Object -FilePath $log
    Write-Host ("failure_demo_exit=" + $LASTEXITCODE + " log=" + $log)
    exit $LASTEXITCODE
}

foreach ($f in @("run_summary.jsonl", "events.jsonl", "failures.jsonl", "browser_comparison.json")) {
    $p = Join-Path $artifacts $f
    if (Test-Path $p) { Remove-Item $p -Force }
}

$junit = Join-Path $artifacts "junit_kt10_$stamp.xml"
$html = Join-Path $artifacts "report_kt10_$stamp.html"
$log = Join-Path $artifacts "pytest_kt10_$stamp.log"
& $venvPy -m pytest "selenium\crossbrowser\tests\test_kt10_matrix.py" -v --tb=short `
    "--junitxml=$junit" "--html=$html" "--self-contained-html" `
    2>&1 | Tee-Object -FilePath $log
$code = $LASTEXITCODE
Write-Host ("matrix_exit=" + $code + " log=" + $log)

& $venvPy (Join-Path $PSScriptRoot "_kt10_build_comparison.py") $artifacts

if ((-not $SkipFailureDemo) -and ($code -eq 0)) {
    Write-Host "Running controlled failure demo (expected nonzero exit)..."
    & $PSCommandPath -FailureDemoOnly
    Write-Host ("failure_demo_exit=" + $LASTEXITCODE + " (expected != 0)")
}

exit $code
