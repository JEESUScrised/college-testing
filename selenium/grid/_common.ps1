#Requires -Version 5.1
# Shared helpers for KT07 Selenium Grid PowerShell scripts.

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$GridRoot = $PSScriptRoot
$RepoRoot = Resolve-Path (Join-Path $GridRoot "..\..")
$RuntimeDir = Join-Path $GridRoot "runtime"
$ArtifactsDir = Join-Path $RepoRoot "selenium\artifacts\kt07"
$MetaFile = Join-Path $GridRoot "server.meta"
$PidFile = Join-Path $RuntimeDir "grid.pids.json"
$DefaultHost = "127.0.0.1"
$DefaultGridPort = 4444
# Android emulator (qemu) often binds 5555 on this PC — use 5556 for Node.
$DefaultNodePort = 5556

function Write-Step([string]$Message) { Write-Host "`n=== $Message ===" -ForegroundColor Cyan }
function Write-Ok([string]$Message) { Write-Host "[OK] $Message" -ForegroundColor Green }
function Write-Warn([string]$Message) { Write-Host "[!] $Message" -ForegroundColor Yellow }
function Fail([string]$Message) {
    Write-Host "[ОШИБКА] $Message" -ForegroundColor Red
    exit 1
}

function Initialize-JavaEnv {
    if (-not $env:JAVA_HOME -or -not (Test-Path $env:JAVA_HOME)) {
        $candidates = @(
            "C:\Program Files\Android\Android Studio\jbr",
            "C:\Program Files\Java\jdk-22",
            "C:\Program Files\Java\jdk-21"
        )
        foreach ($c in $candidates) {
            if (Test-Path (Join-Path $c "bin\java.exe")) {
                $env:JAVA_HOME = $c
                break
            }
        }
    }
    if (-not $env:JAVA_HOME -or -not (Test-Path (Join-Path $env:JAVA_HOME "bin\java.exe"))) {
        Fail "JAVA_HOME не задан и JDK/JBR не найден."
    }
    $javaBin = Join-Path $env:JAVA_HOME "bin"
    if (($env:Path -split ";") -notcontains $javaBin) {
        $env:Path = "$javaBin;$env:Path"
    }
    return (Join-Path $env:JAVA_HOME "bin\java.exe")
}

function Get-SeleniumServerJar {
    if (Test-Path $MetaFile) {
        $meta = Get-Content $MetaFile | ForEach-Object {
            if ($_ -match "^(?<k>[^=]+)=(?<v>.*)$") { @{ $Matches.k = $Matches.v } }
        }
        $jarName = ($meta | Where-Object { $_.ContainsKey("SELENIUM_SERVER_JAR") } | Select-Object -First 1).SELENIUM_SERVER_JAR
        if (-not $jarName) { $jarName = "selenium-server-4.50.0.jar" }
    } else {
        $jarName = "selenium-server-4.50.0.jar"
    }
    $jar = Join-Path $GridRoot $jarName
    if (-not (Test-Path $jar)) {
        Fail "JAR не найден: $jar. Сначала: .\selenium\grid\download_server.ps1"
    }
    return $jar
}

function Ensure-RuntimeDirs {
    New-Item -ItemType Directory -Force -Path $RuntimeDir, $ArtifactsDir | Out-Null
}

function Read-PidState {
    if (-not (Test-Path $PidFile)) {
        return [pscustomobject]@{ mode = $null; processes = @() }
    }
    $raw = Get-Content $PidFile -Raw -Encoding UTF8 | ConvertFrom-Json
    if (-not $raw.processes) { $raw | Add-Member -NotePropertyName processes -NotePropertyValue @() -Force }
    return $raw
}

function Write-PidState($State) {
    Ensure-RuntimeDirs
    ($State | ConvertTo-Json -Depth 5) | Set-Content -Path $PidFile -Encoding UTF8
}

function Add-TrackedProcess {
    param(
        [Parameter(Mandatory)][int]$ProcessId,
        [Parameter(Mandatory)][string]$Role,
        [Parameter(Mandatory)][string]$Mode,
        [string]$LogFile = ""
    )
    $state = Read-PidState
    $state.mode = $Mode
    $list = @($state.processes)
    $list += [pscustomobject]@{
        pid     = $ProcessId
        role    = $Role
        mode    = $Mode
        log     = $LogFile
        started = (Get-Date).ToString("s")
    }
    $state.processes = $list
    Write-PidState $state
}

function Test-PortFree([int]$Port) {
    $busy = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    return -not [bool]$busy
}

function Wait-GridHttp {
    param(
        [string]$BaseUrl = "http://127.0.0.1:4444",
        [int]$TimeoutSec = 90
    )
    $deadline = (Get-Date).AddSeconds($TimeoutSec)
    $statusUrl = "$BaseUrl/status"
    do {
        try {
            $resp = Invoke-WebRequest -Uri $statusUrl -UseBasicParsing -TimeoutSec 3
            if ($resp.StatusCode -eq 200) {
                return ($resp.Content | ConvertFrom-Json)
            }
        } catch {
            # retry until listening
        }
        Start-Sleep -Seconds 2
    } while ((Get-Date) -lt $deadline)
    Fail "Grid HTTP /status не ответил за $TimeoutSec с: $statusUrl"
}

function Wait-GridReady {
    param(
        [string]$BaseUrl = "http://127.0.0.1:4444",
        [int]$TimeoutSec = 90,
        [int]$MinNodes = 0
    )
    $deadline = (Get-Date).AddSeconds($TimeoutSec)
    $statusUrl = "$BaseUrl/status"
    do {
        try {
            $resp = Invoke-WebRequest -Uri $statusUrl -UseBasicParsing -TimeoutSec 3
            if ($resp.StatusCode -eq 200) {
                $json = $resp.Content | ConvertFrom-Json
                $nodes = @($json.value.nodes)
                $readyOk = ($json.value.ready -eq $true)
                $nodesOk = ($nodes.Count -ge $MinNodes)
                if ($readyOk -and $nodesOk) { return $json }
            }
        } catch {
            # retry
        }
        Start-Sleep -Seconds 2
    } while ((Get-Date) -lt $deadline)
    Fail "Grid не стал ready (minNodes=$MinNodes) за $TimeoutSec с: $statusUrl"
}

function Assert-NoConflictingGrid {
    param([int]$Port = 4444)
    if (-not (Test-PortFree $Port)) {
        Fail "Порт $Port занят. Остановите текущий Grid: .\selenium\grid\stop_grid.ps1 (или освободите порт)."
    }
}
