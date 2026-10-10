#Requires -Version 5.1
param(
    [switch]$GenerateOnly,
    [switch]$DiagnosticOnly,
    [string]$TestName = ""
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot

$py = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$artifacts = Join-Path $RepoRoot "grpc\artifacts\kt12"
New-Item -ItemType Directory -Force -Path $artifacts | Out-Null

Write-Host "=== Generate proto stubs ==="
& powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "generate_kt12_proto.ps1")
if ($LASTEXITCODE -ne 0) { throw "proto generation failed" }
if ($GenerateOnly) { exit 0 }

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$versions = Join-Path $artifacts "versions_$stamp.json"
& $py -c @"
import json, grpc
from google.protobuf import __version__ as pb
from pathlib import Path
Path(r'$versions').write_text(json.dumps({
  'grpcio': grpc.__version__,
  'protobuf': pb,
}, indent=2), encoding='utf-8')
print(Path(r'$versions').read_text(encoding='utf-8'))
"@

# Reset evidence for this suite run
$evidence = Join-Path $artifacts "evidence.jsonl"
if (Test-Path $evidence) { Remove-Item $evidence -Force }

$junit = Join-Path $artifacts "junit_kt12_$stamp.xml"
$html = Join-Path $artifacts "report_kt12_$stamp.html"
$log = Join-Path $artifacts "pytest_kt12_$stamp.log"
$summary = Join-Path $artifacts "summary_kt12_$stamp.json"

$testPath = "grpc\tests\test_kt12_grpc.py"
$extra = @()
if ($DiagnosticOnly) {
    $extra += @("-k", "tc12_01")
    Write-Host "=== KT12 diagnostic TC-12-01 ==="
} elseif ($TestName) {
    $extra += @("-k", $TestName)
    Write-Host ("=== KT12 targeted: " + $TestName + " ===")
} else {
    Write-Host "=== KT12 full suite (10 tests) ==="
}

# Avoid Tee-Object deadlock with pytest on Windows — redirect via cmd.
$argList = @(
    "-m", "pytest", $testPath, "-v", "--tb=short"
) + $extra + @(
    "--junitxml=$junit",
    "--html=$html",
    "--self-contained-html"
)
$joined = ($argList | ForEach-Object {
    if ($_ -match '[\s"]') { '"' + ($_ -replace '"', '\"') + '"' } else { $_ }
}) -join ' '
$cmd = "`"$py`" $joined"
cmd /c "$cmd > `"$log`" 2>&1"
$code = $LASTEXITCODE
Get-Content -LiteralPath $log

& $py -c @"
import json, re, xml.etree.ElementTree as ET
from pathlib import Path
log = Path(r'$log').read_text(encoding='utf-8', errors='replace')
m = re.search(r'=+ (.*) in ([0-9.]+)s =+', log)
summary = {'exit_code': $code, 'log_tail': log.strip().splitlines()[-8:]}
if m:
    summary['pytest_line'] = m.group(0)
    summary['duration_s'] = float(m.group(2))
junit = Path(r'$junit')
if junit.exists():
    root = ET.parse(junit).getroot()
    suite = root if root.tag == 'testsuite' else root.find('testsuite')
    if suite is not None:
        summary['tests'] = int(suite.get('tests', 0))
        summary['failures'] = int(suite.get('failures', 0))
        summary['errors'] = int(suite.get('errors', 0))
        summary['skipped'] = int(suite.get('skipped', 0))
Path(r'$summary').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))
"@

Write-Host ("kt12_exit=" + $code + " log=" + $log)
exit $code
