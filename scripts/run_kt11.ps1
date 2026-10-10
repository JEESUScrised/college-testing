#Requires -Version 5.1
param(
    [switch]$DryRun,
    [switch]$DiagnosticOnly,
    [string]$TestName = ""
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot

$py = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$robotDir = Join-Path $RepoRoot "robot"
$artifacts = Join-Path $robotDir "artifacts\kt11"
$shots = Join-Path $RepoRoot "screenshots\kt11"
New-Item -ItemType Directory -Force -Path $artifacts, $shots | Out-Null

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$consoleLog = Join-Path $artifacts "console_kt11_$stamp.log"
$suite = Join-Path $robotDir "tests\kt11.robot"

function Invoke-Robot {
    param([string[]]$RobotArgs)
    # Avoid Tee-Object: it can deadlock Robot Framework console pipes on Windows.
    $argLine = ($RobotArgs | ForEach-Object {
        if ($_ -match '[\s"]') { '"' + ($_ -replace '"', '\"') + '"' } else { $_ }
    }) -join ' '
    $cmd = "`"$py`" -m robot $argLine"
    Write-Host $cmd
    cmd /c "$cmd > `"$consoleLog`" 2>&1"
    $code = $LASTEXITCODE
    Get-Content -LiteralPath $consoleLog -ErrorAction SilentlyContinue
    return $code
}

$common = @(
    "--outputdir", $artifacts,
    "--output", "output.xml",
    "--log", "log.html",
    "--report", "report.html",
    "--xunit", "xunit.xml",
    "--name", "KT11 Robot Framework"
)

if ($DryRun) {
    Write-Host "=== KT11 dry-run (parse/list) ==="
    $code = Invoke-Robot @("--dryrun", "--outputdir", $artifacts, "--report", "NONE", "--log", "NONE", "--output", "NONE", $suite)
    exit $code
}

if ($DiagnosticOnly) {
    Write-Host "=== KT11 diagnostic: TC-11-01 ==="
    $code = Invoke-Robot ($common + @("--test", "TC-11-01*", $suite))
    Write-Host ("diagnostic_exit=" + $code + " log=" + $consoleLog)
    exit $code
}

if ($TestName) {
    Write-Host ("=== KT11 targeted: " + $TestName + " ===")
    $code = Invoke-Robot ($common + @("--test", $TestName, $suite))
} else {
    Write-Host "=== KT11 full suite (10 tests) ==="
    $code = Invoke-Robot ($common + @($suite))
}

Write-Host ("kt11_exit=" + $code + " log=" + $consoleLog)
Write-Host ("artifacts=" + $artifacts)
exit $code
