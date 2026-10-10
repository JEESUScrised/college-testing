#Requires -Version 5.1
param(
    [ValidateSet("Full", "Pillow", "Public", "DiagnosticPublic")]
    [string]$Mode = "Full",
    [switch]$SkipAllureGenerate
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot
$venvPy = Join-Path $RepoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPy)) { throw "Missing .venv" }

$artifacts = Join-Path $RepoRoot "selenium\artifacts\kt08"
$allureResults = Join-Path $artifacts "allure-results"
$allureReport = Join-Path $artifacts "allure-report"
$shots = Join-Path $RepoRoot "screenshots\kt08"
New-Item -ItemType Directory -Force -Path $artifacts, $shots, $allureResults | Out-Null

$baseline = Join-Path $RepoRoot "selenium\baselines\kt08\home_baseline.png"
if (-not (Test-Path $baseline)) {
    Write-Host "Baseline missing - generating..."
    & $venvPy "selenium\visual\generate_kt08_baselines.py"
}

$allureCmd = $null
foreach ($c in @("allure", "C:\allure\allure-2.37.0\bin\allure.bat")) {
    if (Get-Command $c -ErrorAction SilentlyContinue) { $allureCmd = (Get-Command $c).Source; break }
    if (Test-Path $c) { $allureCmd = $c; break }
}

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$junit = Join-Path $artifacts "junit_kt08_$stamp.xml"
$html = Join-Path $artifacts "report_kt08_$stamp.html"
$log = Join-Path $artifacts "pytest_kt08_$stamp.log"

# Fresh Allure results for this run
if (Test-Path $allureResults) {
    Get-ChildItem $allureResults -Force | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
}
New-Item -ItemType Directory -Force -Path $allureResults | Out-Null

# Environment for Allure
$pyVer = (& $venvPy --version 2>&1 | Out-String).Trim()
$selVer = (& $venvPy -c "import selenium; print(selenium.__version__)").Trim()
$apVer = (& $venvPy -c "import importlib.metadata as m; print(m.version('allure-pytest'))").Trim()
@(
    "Browser=Chrome"
    "Python=$pyVer"
    "Selenium=$selVer"
    "AllurePytest=$apVer"
    "PublicSite=https://www.saucedemo.com/"
    "Viewport=1400x1000"
    "KT=08"
) | Set-Content -LiteralPath (Join-Path $allureResults "environment.properties") -Encoding UTF8

$tests = @()
switch ($Mode) {
    "Pillow" { $tests = @("selenium\tests\test_kt08_visual.py") }
    "Public" { $tests = @("selenium\tests\test_kt08_public_allure.py") }
    "DiagnosticPublic" { $tests = @("selenium\tests\test_kt08_public_allure.py::test_public_login_page_and_branding") }
    default {
        $tests = @(
            "selenium\tests\test_kt08_visual.py",
            "selenium\tests\test_kt08_public_allure.py"
        )
    }
}

Write-Host ("=== KT08 mode=" + $Mode + " ===")
$argList = @(
    "-m", "pytest"
) + $tests + @(
    "-v", "--tb=short",
    "--browser=chrome",
    "--page-load-strategy=eager",
    "--alluredir=$allureResults",
    "--junitxml=$junit",
    "--html=$html",
    "--self-contained-html"
)
$joined = ($argList | ForEach-Object {
    if ($_ -match '[\s"]') { '"' + ($_ -replace '"', '\"') + '"' } else { $_ }
}) -join ' '
$cmd = "`"$venvPy`" $joined"
# Avoid Tee-Object deadlock with pytest on Windows.
cmd /c "$cmd > `"$log`" 2>&1"
$code = $LASTEXITCODE
Get-Content -LiteralPath $log
Write-Host ("pytest_exit=" + $code + " log=" + $log)

if ((-not $SkipAllureGenerate) -and $allureCmd) {
    Write-Host ("=== Allure generate via " + $allureCmd + " ===")
    if (Test-Path $allureReport) { Remove-Item $allureReport -Recurse -Force }
    & $allureCmd generate $allureResults -o $allureReport --clean
    if ($LASTEXITCODE -ne 0) { throw "allure generate failed" }
    $index = Join-Path $allureReport "index.html"
    if (-not (Test-Path $index)) { throw "Allure report index.html missing" }
    Write-Host ("allure_report=" + $index)
} elseif (-not $allureCmd) {
    Write-Host "WARN: Allure CLI not found; results kept in $allureResults"
}

exit $code
