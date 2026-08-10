param(
    [Parameter(Mandatory = $true)][string]$Python,
    [Parameter(Mandatory = $true)][string]$MeekoCommand,
    [string]$OutputRoot = "audit-output/rcsb-legacy-pdb-comparator-20260809-run2"
)

$ErrorActionPreference = "Stop"
$repository = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$output = Join-Path $repository $OutputRoot
New-Item -ItemType Directory -Force -Path $output | Out-Null

& $Python (Join-Path $repository "scripts/audit_rcsb_legacy_pdb_preparation.py") `
    (Join-Path $repository "data/dude_targets.csv") `
    (Join-Path $repository "external-data/rcsb-legacy-pdb") `
    (Join-Path $output "work") `
    (Join-Path $output "preparation_audit.csv") `
    --meeko-command $MeekoCommand `
    --timeout-seconds 300 `
    --checkpoint-every 1

exit $LASTEXITCODE
