#Requires -Version 5.1
<#
.SYNOPSIS
  Запуск Selenium Grid 4 в режиме Standalone (localhost:4444).
#>
[CmdletBinding()]
param(
    [string]$BindHost = "127.0.0.1",
    [int]$Port = 4444
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $ScriptDir "_common.ps1")
Ensure-RuntimeDirs

$java = Initialize-JavaEnv
$jar = Get-SeleniumServerJar
Assert-NoConflictingGrid -Port $Port

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logFile = Join-Path $ArtifactsDir "grid_standalone_${stamp}.log"

Write-Step "Standalone Grid $BindHost`:$Port"
Write-Host "JAVA_HOME=$env:JAVA_HOME"
Write-Host "JAR=$jar"

$args = @(
    "-jar", $jar,
    "standalone",
    "--host", $BindHost,
    "--port", "$Port",
    "--selenium-manager", "true",
    "--log", $logFile
)

$proc = Start-Process -FilePath $java `
    -ArgumentList $args `
    -WorkingDirectory $GridRoot `
    -PassThru -WindowStyle Hidden

Add-TrackedProcess -ProcessId $proc.Id -Role "standalone" -Mode "standalone" -LogFile $logFile
Write-Host "Started PID=$($proc.Id) log=$logFile"

$status = Wait-GridReady -BaseUrl "http://${BindHost}:$Port" -TimeoutSec 120
Write-Ok "Standalone ready=true"
Write-Host ("nodes={0}" -f @($status.value.nodes).Count)
$status | ConvertTo-Json -Depth 8 | Set-Content (Join-Path $ArtifactsDir "status_standalone_$stamp.json") -Encoding UTF8
Write-Ok "Status saved. UI: http://${BindHost}:$Port"
