#Requires -Version 5.1
<#
.SYNOPSIS
  Сбор логов и результатов KT06 в mobile/artifacts/summary_*.md
#>
[CmdletBinding()]
param()

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
. (Join-Path $ScriptDir "_kt06_common.ps1")
Set-Location $RepoRoot

$sdk = Initialize-AndroidEnv
$paths = Get-MobilePaths -RepoRoot $RepoRoot
$adb = Get-AdbPath -Sdk $sdk
New-Item -ItemType Directory -Force -Path $paths.Artifacts | Out-Null

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$summary = Join-Path $paths.Artifacts "summary_$stamp.md"

$devices = & $adb devices -l 2>&1 | Out-String
$shots = @()
if (Test-Path $paths.Screenshots) {
    $shots = Get-ChildItem $paths.Screenshots -Filter *.png -ErrorAction SilentlyContinue
}
$logs = Get-ChildItem $paths.Artifacts -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending

$lines = @(
    "# KT06 artifacts summary",
    "",
    "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
    "",
    "## adb devices",
    '```',
    $devices.Trim(),
    '```',
    "",
    "## Screenshots (screenshots/kt06)",
    "Count: $($shots.Count)"
)
foreach ($s in $shots) {
    $lines += "- $($s.Name) ($($s.Length) bytes)"
}
$lines += ""
$lines += "## Recent mobile/artifacts"
foreach ($f in $logs | Select-Object -First 20) {
    $lines += "- $($f.Name) ($($f.Length) bytes, $($f.LastWriteTime.ToString('s')))"
}

$lines -join "`n" | Set-Content -Path $summary -Encoding UTF8
Write-Ok "Сводка: $summary"
Get-Content $summary
