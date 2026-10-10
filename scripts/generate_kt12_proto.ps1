#Requires -Version 5.1
$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot
$py = Join-Path $RepoRoot ".venv\Scripts\python.exe"
$protoDir = Join-Path $RepoRoot "grpc\proto"
$outDir = Join-Path $RepoRoot "grpc\generated"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

& $py -m grpc_tools.protoc `
  -I $protoDir `
  --python_out=$outDir `
  --grpc_python_out=$outDir `
  (Join-Path $protoDir "inventory.proto")

if ($LASTEXITCODE -ne 0) { throw "protoc failed" }

# Marker so the directory is importable when added to sys.path (not a nested package named grpc).
$init = Join-Path $outDir "__init__.py"
@"
# Generated stubs live here. Import as ``import inventory_pb2`` after adding this
# directory to sys.path (see grpc/conftest.py). Do not place an ``__init__.py``
# in the parent ``grpc/`` folder — that would shadow the installed ``grpc`` package.
"@ | Set-Content -LiteralPath $init -Encoding UTF8

Write-Host "Generated stubs in $outDir"
Get-ChildItem $outDir | Select-Object Name, Length
