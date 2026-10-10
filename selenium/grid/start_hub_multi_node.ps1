#Requires -Version 5.1
<#
.SYNOPSIS
  Selenium Grid 4: Hub + two Nodes on localhost (multi-node remediation).
.NOTES
  Node A :5556, Node B :5557. Event Bus forced to 127.0.0.1 (VPN-safe).
  Do not run alongside Standalone / single-node Hub on :4444.
#>
[CmdletBinding()]
param(
    [string]$BindHost = "127.0.0.1",
    [int]$HubPort = 4444,
    [int]$NodePortA = 5556,
    [int]$NodePortB = 5557
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $ScriptDir "_common.ps1")
Ensure-RuntimeDirs

$java = Initialize-JavaEnv
$jar = Get-SeleniumServerJar
Assert-NoConflictingGrid -Port $HubPort

foreach ($p in @($NodePortA, $NodePortB)) {
    if (-not (Test-PortFree $p)) {
        Fail "Порт Node $p занят. Освободите порт или укажите другой."
    }
}

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$publishEvents = "tcp://${BindHost}:4442"
$subscribeEvents = "tcp://${BindHost}:4443"

Write-Step "Hub $BindHost`:$HubPort (multi-node; events $publishEvents / $subscribeEvents)"
$hubLog = Join-Path $ArtifactsDir "grid_hub_multi_${stamp}.log"
$hubArgs = @(
    "-jar", $jar, "hub",
    "--host", $BindHost, "--port", "$HubPort",
    "--publish-events", $publishEvents,
    "--subscribe-events", $subscribeEvents,
    "--log", $hubLog
)
$hub = Start-Process -FilePath $java -ArgumentList $hubArgs -WorkingDirectory $GridRoot `
    -PassThru -WindowStyle Hidden
Add-TrackedProcess -ProcessId $hub.Id -Role "hub" -Mode "hub-multi-node" -LogFile $hubLog
Write-Host "Hub PID=$($hub.Id) log=$hubLog"
$null = Wait-GridHttp -BaseUrl "http://${BindHost}:$HubPort" -TimeoutSec 90
Write-Ok "Hub HTTP /status отвечает"

function Start-GridNode {
    param([int]$Port, [string]$Label)
    Write-Step "Node $Label $BindHost`:$Port -> hub http://${BindHost}:$HubPort"
    $nodeLog = Join-Path $ArtifactsDir "grid_node_${Label}_${stamp}.log"
    $nodeArgs = @(
        "-jar", $jar, "node",
        "--host", $BindHost, "--port", "$Port",
        "--hub", "http://${BindHost}:$HubPort",
        "--publish-events", $publishEvents,
        "--subscribe-events", $subscribeEvents,
        "--selenium-manager", "true",
        "--log", $nodeLog
    )
    $proc = Start-Process -FilePath $java -ArgumentList $nodeArgs -WorkingDirectory $GridRoot `
        -PassThru -WindowStyle Hidden
    Add-TrackedProcess -ProcessId $proc.Id -Role "node-$Label" -Mode "hub-multi-node" -LogFile $nodeLog
    Write-Host "Node $Label PID=$($proc.Id) log=$nodeLog"
}

Start-GridNode -Port $NodePortA -Label "A"
Start-GridNode -Port $NodePortB -Label "B"

$json = Wait-GridReady -BaseUrl "http://${BindHost}:$HubPort" -TimeoutSec 180 -MinNodes 2
$nodeCount = @($json.value.nodes).Count
if ($nodeCount -lt 2) {
    Fail "Ожидались 2 Node, зарегистрировано $nodeCount. См. логи в $ArtifactsDir"
}

$statusPath = Join-Path $ArtifactsDir "status_hub_multi_node_$stamp.json"
$json | ConvertTo-Json -Depth 12 | Set-Content $statusPath -Encoding UTF8
Write-Ok ("Hub+2 Nodes ready; nodes={0}; status={1}" -f $nodeCount, $statusPath)
Write-Host "UI: http://${BindHost}:$HubPort"
