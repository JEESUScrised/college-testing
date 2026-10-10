#Requires -Version 5.1
<#
.SYNOPSIS
  Download host ChromeDriver matching Android emulator Chrome 134.x (Chrome for Testing).
#>
param(
    [string]$Version = "134.0.6998.165"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$OutDir = Join-Path $RepoRoot "mobile\drivers"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$url = "https://storage.googleapis.com/chrome-for-testing-public/$Version/win64/chromedriver-win64.zip"
$zip = Join-Path $OutDir "chromedriver-$Version.zip"
$extract = Join-Path $OutDir "chromedriver-$Version-extract"
$exe = Join-Path $OutDir "chromedriver-134.exe"

Write-Host "Downloading $url"
Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
if (Test-Path $extract) { Remove-Item $extract -Recurse -Force }
Expand-Archive -Path $zip -DestinationPath $extract -Force
$found = Get-ChildItem $extract -Recurse -Filter chromedriver.exe | Select-Object -First 1
if (-not $found) { throw "chromedriver.exe not found in archive" }
Copy-Item $found.FullName $exe -Force
& $exe --version
@"
VERSION=$Version
SOURCE=$url
BROWSER_ANDROID_TARGET=134.0.6998.135
EXE=mobile/drivers/chromedriver-134.exe
"@ | Set-Content (Join-Path $OutDir "chromedriver-134.meta") -Encoding UTF8
Write-Host "[OK] $exe"
