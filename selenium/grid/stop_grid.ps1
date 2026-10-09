#Requires -Version 5.1
<#
.SYNOPSIS
  Останавливает только процессы Grid, запущенные нашими скриптами (по PID-файлу).
#>
[CmdletBinding()]
param(
    [switch]$ForceClearPidFile
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $ScriptDir "_common.ps1")

$state = Read-PidState
if (-not $state.processes -or @($state.processes).Count -eq 0) {
    Write-Warn "Нет отслеживаемых PID в $PidFile"
    if ($ForceClearPidFile -and (Test-Path $PidFile)) {
        Remove-Item $PidFile -Force
        Write-Ok "PID-файл очищен"
    }
    exit 0
}

Write-Step "Остановка отслеживаемых процессов Grid"
$remaining = @()
foreach ($entry in @($state.processes)) {
    $procId = [int]$entry.pid
    $role = [string]$entry.role
    $proc = Get-Process -Id $procId -ErrorAction SilentlyContinue
    if (-not $proc) {
        Write-Host "PID $procId ($role) уже не существует"
        continue
    }
    # Safety: only stop java processes we started
    if ($proc.ProcessName -notmatch "^(java|javaw)$") {
        Write-Warn "PID $procId ($($proc.ProcessName)) пропущен — не java (защита от чужих процессов)"
        $remaining += $entry
        continue
    }
    Write-Host "Stopping PID=$procId role=$role name=$($proc.ProcessName)"
    try {
        Stop-Process -Id $procId -Force -ErrorAction Stop
        Write-Ok "Stopped $procId"
    } catch {
        Write-Warn ("Не удалось остановить {0}: {1}" -f $procId, $_)
        $remaining += $entry
    }
}

Start-Sleep -Seconds 1
if ($remaining.Count -eq 0) {
    if (Test-Path $PidFile) { Remove-Item $PidFile -Force }
    Write-Ok "Все отслеживаемые процессы остановлены; PID-файл удалён"
} else {
    Write-PidState ([pscustomobject]@{ mode = $state.mode; processes = $remaining })
    Write-Warn "Остались записи в PID-файле: $($remaining.Count)"
    exit 1
}
