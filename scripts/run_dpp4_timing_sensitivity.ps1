param(
    [Parameter(Mandatory = $true)][string]$Python,
    [Parameter(Mandatory = $true)][string]$MeekoCommand,
    [string]$OutputRoot = "audit-output/dpp4-2i78-timing-sensitivity-20260809"
)

$ErrorActionPreference = "Stop"
$repository = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$output = Join-Path $repository $OutputRoot
New-Item -ItemType Directory -Force -Path $output | Out-Null

$source = Join-Path $repository "data/rcsb_mmcif/2i78.cif"
$sourceHash = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant()
$records = @()

for ($attempt = 1; $attempt -le 3; $attempt++) {
    $attemptRoot = Join-Path $output ("attempt-{0}" -f $attempt)
    $work = Join-Path $attemptRoot "work"
    $csv = Join-Path $attemptRoot "result.csv"
    New-Item -ItemType Directory -Force -Path $attemptRoot | Out-Null

    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    & $Python (Join-Path $repository "scripts/audit_rcsb_mmcif_preparation.py") `
        (Join-Path $repository "data/dude_targets.csv") `
        (Join-Path $repository "data/rcsb_mmcif") `
        $work `
        $csv `
        --meeko-command $MeekoCommand `
        --start-index 26 `
        --limit 1 `
        --timeout-seconds 300 `
        --checkpoint-every 1
    $runnerExitCode = $LASTEXITCODE
    $stopwatch.Stop()

    $row = Import-Csv -LiteralPath $csv
    $records += [PSCustomObject]@{
        attempt = $attempt
        wall_seconds = [Math]::Round($stopwatch.Elapsed.TotalSeconds, 3)
        runner_exit_code = $runnerExitCode
        source_sha256 = $sourceHash
        target = $row.target
        pdb_id = $row.pdb_id
        outcome = $row.outcome
        return_code = $row.return_code
        pdbqt_bytes = $row.pdbqt_bytes
        error_class = $row.error_class
    }
}

$records | Export-Csv -LiteralPath (Join-Path $output "timing_sensitivity_summary.csv") -NoTypeInformation
