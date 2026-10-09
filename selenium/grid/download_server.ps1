#Requires -Version 5.1
<#
.SYNOPSIS
  Скачивает официальный selenium-server JAR с GitHub SeleniumHQ releases.
#>
[CmdletBinding()]
param(
    [string]$Version = "4.50.0"
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
. (Join-Path $ScriptDir "_common.ps1")
Ensure-RuntimeDirs

$jarName = "selenium-server-$Version.jar"
$jarPath = Join-Path $GridRoot $jarName
$url = "https://github.com/SeleniumHQ/selenium/releases/download/selenium-$Version/$jarName"

Write-Step "Источник: SeleniumHQ GitHub release selenium-$Version"
Write-Host "URL: $url"

if (Test-Path $jarPath) {
    $hash = (Get-FileHash $jarPath -Algorithm SHA256).Hash
    Write-Ok "JAR уже есть: $jarPath"
    Write-Host "SHA-256: $hash size=$((Get-Item $jarPath).Length)"
    exit 0
}

Write-Host "Загрузка..."
Invoke-WebRequest -Uri $url -OutFile $jarPath -UseBasicParsing
if (-not (Test-Path $jarPath)) { Fail "Загрузка не удалась" }

$item = Get-Item $jarPath
$hash = (Get-FileHash $jarPath -Algorithm SHA256).Hash
$magic = [System.IO.File]::ReadAllBytes($jarPath)[0..1]
if ($magic[0] -ne 0x50 -or $magic[1] -ne 0x4B) {
    Remove-Item $jarPath -Force
    Fail "Файл не похож на JAR/ZIP (ожидался PK header)"
}

@"
SELENIUM_SERVER_VERSION=$Version
SELENIUM_SERVER_JAR=$jarName
SELENIUM_SERVER_URL=$url
SELENIUM_SERVER_SHA256=$hash
SELENIUM_SERVER_SIZE=$($item.Length)
DOWNLOADED_AT=$((Get-Date).ToString("s"))
"@ | Set-Content (Join-Path $GridRoot "server.meta") -Encoding UTF8

Write-Ok "Сохранён $jarPath ($($item.Length) bytes)"
Write-Host "SHA-256: $hash"
Write-Host "Бинарник в Git не коммитится (*.jar в .gitignore)."
