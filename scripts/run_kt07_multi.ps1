#Requires -Version 5.1
<#
.SYNOPSIS
  Start Hub+2 Nodes (if needed), run multi-browser KT07 tests + parallel overlap proof.
#>
[CmdletBinding()]
param(
    [string]$GridUrl = "http://127.0.0.1:4444",
    [switch]$SkipStart
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot
$venvPy = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$artifacts = Join-Path $RepoRoot "selenium\artifacts\kt07"
New-Item -ItemType Directory -Force -Path $artifacts, (Join-Path $RepoRoot "screenshots\kt07\multi") | Out-Null

function Test-GridReady([string]$Url, [int]$MinNodes = 2) {
    try {
        $resp = Invoke-WebRequest -Uri "$Url/status" -UseBasicParsing -TimeoutSec 5
        $json = $resp.Content | ConvertFrom-Json
        $nodes = @($json.value.nodes)
        return ($json.value.ready -eq $true) -and ($nodes.Count -ge $MinNodes)
    } catch {
        return $false
    }
}

if (-not $SkipStart) {
    if (-not (Test-GridReady $GridUrl 2)) {
        Write-Host "Starting Hub + 2 Nodes..."
        & (Join-Path $RepoRoot "selenium\grid\stop_grid.ps1")
        & (Join-Path $RepoRoot "selenium\grid\start_hub_multi_node.ps1")
    } else {
        Write-Host "[OK] Grid already ready with >=2 nodes"
    }
}

if (-not (Test-GridReady $GridUrl 2)) {
    throw "Grid not ready with >=2 nodes at $GridUrl"
}

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$log = Join-Path $artifacts "pytest_kt07_multi_$stamp.log"
Write-Host "=== Multi-browser pytest ==="
& $venvPy -m pytest selenium\tests\test_kt07_multi_node.py -v --tb=short `
    --grid-url=$GridUrl --page-load-strategy=eager `
    --junitxml=(Join-Path $artifacts "junit_kt07_multi_$stamp.xml") `
    --html=(Join-Path $artifacts "report_kt07_multi_$stamp.html") `
    --self-contained-html 2>&1 | Tee-Object -FilePath $log
$code1 = $LASTEXITCODE

Write-Host "=== Parallel overlap proof ==="
$plog = Join-Path $artifacts "parallel_proof_$stamp.log"
& $venvPy (Join-Path $RepoRoot "scripts\run_kt07_parallel_proof.py") 2>&1 | Tee-Object -FilePath $plog
$code2 = $LASTEXITCODE

Write-Host "pytest_exit=$code1 parallel_exit=$code2"
if ($code1 -ne 0 -or $code2 -ne 0) { exit 1 }
exit 0
