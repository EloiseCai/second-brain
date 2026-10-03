param([string]$TargetRoot, [switch]$Check)
$ErrorActionPreference = 'Stop'
$manifest = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'writing-pack.json') -Raw | ConvertFrom-Json
$names = @($manifest.skills)
if (-not $names.Count -or @($names | Select-Object -Unique).Count -ne $names.Count) {
    throw 'Invalid or duplicate skill manifest.'
}
foreach ($name in $names) {
    if ($name -notmatch '^[a-z0-9]+(-[a-z0-9]+)*$' -or
        -not (Test-Path -LiteralPath (Join-Path $PSScriptRoot "$name/SKILL.md") -PathType Leaf)) {
        throw "Missing or invalid skill: $name"
    }
}
Write-Output "Writing pack $($manifest.version); status: $($manifest.status)"
foreach ($name in $names) {
    $arguments = @{ Name = $name; Check = $Check }
    if ($TargetRoot) { $arguments.TargetRoot = $TargetRoot }
    & (Join-Path $PSScriptRoot 'sync-skill.ps1') @arguments
}
Write-Output 'All listed skills verified. Cloud access and tools require separate validation.'
