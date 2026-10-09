#Requires -Version 5.1
<#
.SYNOPSIS
  Запуск Selenium Grid 4: Hub + один Node на той же машине.
.NOTES
  Не запускайте одновременно со Standalone на том же порту Hub.
  Node по умолчанию на 5556 (5555 часто занят Android emulator/qemu).
#>
[CmdletBinding()]
param(
    [string]$BindHost = "127.0.0.1",
    [int]$HubPort = 4444,
    [int]$NodePort = 5556
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $ScriptDir "_common.ps1")
Ensure-RuntimeDirs

$java = Initialize-JavaEnv
$jar = Get-SeleniumServerJar
Assert-NoConflictingGrid -Port $HubPort

if (-not (Test-PortFree $NodePort)) {
    Fail "Порт Node $NodePort занят. Укажите другой -NodePort."
}

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"

# Force Event Bus onto loopback. Otherwise Grid may advertise a VPN/LAN IP
# (e.g. 26.x ZeroTier) and Node registration events never reach the Hub.
$publishEvents = "tcp://${BindHost}:4442"
$subscribeEvents = "tcp://${BindHost}:4443"

Write-Step "Hub $BindHost`:$HubPort (events $publishEvents / $subscribeEvents)"
$hubLog = Join-Path $ArtifactsDir "grid_hub_${stamp}.log"
$hubArgs = @(
    "-jar", $jar,
    "hub",
    "--host", $BindHost,
    "--port", "$HubPort",
    "--publish-events", $publishEvents,
    "--subscribe-events", $subscribeEvents,
    "--log", $hubLog
)
$hub = Start-Process -FilePath $java -ArgumentList $hubArgs -WorkingDirectory $GridRoot `
    -PassThru -WindowStyle Hidden
Add-TrackedProcess -ProcessId $hub.Id -Role "hub" -Mode "hub-node" -LogFile $hubLog
Write-Host "Hub PID=$($hub.Id) log=$hubLog"

# Hub without nodes often reports ready=false — wait only for HTTP /status
$null = Wait-GridHttp -BaseUrl "http://${BindHost}:$HubPort" -TimeoutSec 90
Write-Ok "Hub HTTP /status отвечает (ожидаем Node для ready=true)"

Write-Step "Node $BindHost`:$NodePort -> hub http://${BindHost}:$HubPort"
$nodeLog = Join-Path $ArtifactsDir "grid_node_${stamp}.log"
$nodeArgs = @(
    "-jar", $jar,
    "node",
    "--host", $BindHost,
    "--port", "$NodePort",
    "--hub", "http://${BindHost}:$HubPort",
    "--publish-events", $publishEvents,
    "--subscribe-events", $subscribeEvents,
    "--selenium-manager", "true",
    "--log", $nodeLog
)
$node = Start-Process -FilePath $java -ArgumentList $nodeArgs -WorkingDirectory $GridRoot `
    -PassThru -WindowStyle Hidden
Add-TrackedProcess -ProcessId $node.Id -Role "node" -Mode "hub-node" -LogFile $nodeLog
Write-Host "Node PID=$($node.Id) log=$nodeLog"

$json = Wait-GridReady -BaseUrl "http://${BindHost}:$HubPort" -TimeoutSec 120 -MinNodes 1
if (@($json.value.nodes).Count -lt 1) {
    Fail "Node не зарегистрировался на Hub. См. $nodeOut / $nodeErr"
}

$json | ConvertTo-Json -Depth 10 | Set-Content (Join-Path $ArtifactsDir "status_hub_node_$stamp.json") -Encoding UTF8
Write-Ok ("Hub+Node ready; nodes={0}" -f @($json.value.nodes).Count)
Write-Host "UI: http://${BindHost}:$HubPort"
