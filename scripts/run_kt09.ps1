#Requires -Version 5.1
param(
    [string]$AppiumServer = "http://127.0.0.1:4723",
    [string]$Udid = $env:ANDROID_UDID,
    [string]$TestPath = "tests/test_kt09_gestures.py"
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
. (Join-Path $ScriptDir "_kt06_common.ps1")
Set-Location $RepoRoot

$sdk = Initialize-AndroidEnv
$paths = Get-MobilePaths -RepoRoot $RepoRoot
$adb = Get-AdbPath -Sdk $sdk
$artifacts = Join-Path $RepoRoot "mobile\artifacts\kt09"
New-Item -ItemType Directory -Force -Path $artifacts, (Join-Path $RepoRoot "screenshots\kt09") | Out-Null

if (-not (Test-Path $paths.VenvPython)) { Fail "Missing .venv" }
if (-not (Test-Path $paths.Apk)) { Fail "Missing ApiDemos APK" }

$devices = Get-ReadyAndroidDevices -AdbPath $adb
if ($devices.Count -eq 0) {
    Write-Warn "No device - starting emulator via start_kt06_services.ps1"
    & (Join-Path $ScriptDir "start_kt06_services.ps1") -AvdName "Medium_Phone_API_36.1"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    $devices = Get-ReadyAndroidDevices -AdbPath $adb
}
if (-not $Udid) { $Udid = $devices[0] }

if (-not (Test-AppiumListening)) {
    & (Join-Path $ScriptDir "start_kt06_services.ps1") -SkipEmulator
}

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$junit = Join-Path $artifacts "junit_kt09_$stamp.xml"
$html = Join-Path $artifacts "report_kt09_$stamp.html"
$log = Join-Path $artifacts "pytest_kt09_$stamp.log"

Push-Location $paths.Mobile
try {
    & $paths.VenvPython -m pytest $TestPath -v --tb=short --timeout=120 `
        "--junitxml=$junit" "--html=$html" "--self-contained-html" `
        "--appium-server=$AppiumServer" "--udid=$Udid" `
        2>&1 | Tee-Object -FilePath $log
    $code = $LASTEXITCODE
} finally {
    Pop-Location
}
Write-Host "exit=$code log=$log"
exit $code
