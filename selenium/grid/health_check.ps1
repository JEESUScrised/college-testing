#Requires -Version 5.1
<#
.SYNOPSIS
  Проверка Selenium Grid /status и краткая сводка по нодам/браузерам.
#>
[CmdletBinding()]
param(
    [string]$BaseUrl = "http://127.0.0.1:4444",
    [string]$OutFile = ""
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $ScriptDir "_common.ps1")
Ensure-RuntimeDirs

$statusUrl = "$BaseUrl/status"
Write-Step "GET $statusUrl"

try {
    $resp = Invoke-WebRequest -Uri $statusUrl -UseBasicParsing -TimeoutSec 5
} catch {
    Fail "Grid недоступен: $_"
}

$json = $resp.Content | ConvertFrom-Json
$ready = $json.value.ready
$nodes = @($json.value.nodes)
Write-Host "ready=$ready"
Write-Host "nodes=$($nodes.Count)"

$slotSummary = @()
foreach ($node in $nodes) {
    $id = $node.id
    $uri = $node.uri
    $slots = @($node.slots)
    $browsers = $slots | ForEach-Object {
        $s = $_.stereotype
        if ($s.browserName) { $s.browserName } elseif ($s."browserName") { $s.browserName }
    } | Select-Object -Unique
    $busy = @($slots | Where-Object { $null -ne $_.session }).Count
    Write-Host ("- node {0} uri={1} slots={2} busy={3} browsers={4}" -f $id, $uri, $slots.Count, $busy, ($browsers -join ","))
    $slotSummary += [pscustomobject]@{
        id = $id; uri = $uri; slots = $slots.Count; busy = $busy; browsers = ($browsers -join ",")
    }
}

$report = [pscustomobject]@{
    checkedAt = (Get-Date).ToString("s")
    baseUrl   = $BaseUrl
    ready     = $ready
    nodeCount = $nodes.Count
    nodes     = $slotSummary
    raw       = $json
}

if (-not $OutFile) {
    $OutFile = Join-Path $ArtifactsDir ("health_" + (Get-Date -Format "yyyyMMdd_HHmmss") + ".json")
}
($report | ConvertTo-Json -Depth 12) | Set-Content $OutFile -Encoding UTF8
Write-Ok "Health saved: $OutFile"

if (-not $ready) { exit 2 }
exit 0
