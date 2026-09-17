param(
    [ValidatePattern('^[a-z0-9]+(-[a-z0-9]+)*$')]
    [string]$Name = 'content-writer',
    [string]$TargetRoot,
    [switch]$Check
)

$ErrorActionPreference = 'Stop'
if (-not $TargetRoot) {
    $codexDirectory = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }
    $TargetRoot = Join-Path $codexDirectory 'skills'
}
$source = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot $Name))
$destination = [IO.Path]::GetFullPath((Join-Path $TargetRoot $Name))
if (-not (Test-Path -LiteralPath (Join-Path $source 'SKILL.md') -PathType Leaf)) {
    throw "Source skill not found: $source"
}
if ($source -eq $destination -or $destination.StartsWith($source + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Source and destination must be separate directories.'
}

function Get-Inventory([string]$Directory) {
    $inventory = @{}
    if (Test-Path -LiteralPath $Directory) {
        $rootItem = Get-Item -LiteralPath $Directory
        $items = @(Get-ChildItem -LiteralPath $Directory -Recurse -Force)
        if (($rootItem.Attributes -band [IO.FileAttributes]::ReparsePoint) -or
            @($items | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) {
            throw "Linked directories/files require manual review: $Directory"
        }
        foreach ($item in $items | Where-Object { -not $_.PSIsContainer }) {
            $relative = $item.FullName.Substring($Directory.Length + 1)
            $inventory[$relative] = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash
        }
    }
    return $inventory
}

$sourceFiles = Get-Inventory $source
$targetFiles = Get-Inventory $destination
$extras = @($targetFiles.Keys | Where-Object { -not $sourceFiles.ContainsKey($_) })
if ($extras.Count) {
    throw "Runtime-only files require review before syncing (nothing changed): $($extras -join ', ')"
}
$changed = @($sourceFiles.Keys | Where-Object { $sourceFiles[$_] -ne $targetFiles[$_] } | Sort-Object)
Write-Output "Source: $source"
Write-Output "Runtime: $destination"
if ($Check -and $changed.Count) {
    throw "Skill copies differ: $($changed -join ', ')"
}
if (-not $Check -and $changed.Count) {
    $backup = Join-Path ([IO.Path]::GetTempPath()) ('codex-skill-backup-' + $Name + '-' + [guid]::NewGuid().ToString('N'))
    foreach ($relative in $changed) {
        $target = Join-Path $destination $relative
        if (Test-Path -LiteralPath $target) {
            $backupFile = Join-Path $backup $relative
            New-Item -ItemType Directory -Path (Split-Path $backupFile -Parent) -Force | Out-Null
            Copy-Item -LiteralPath $target -Destination $backupFile
        }
    }
    if (Test-Path -LiteralPath $backup) { Write-Output "Previous runtime files backed up: $backup" }
    foreach ($relative in $changed) {
        $target = Join-Path $destination $relative
        New-Item -ItemType Directory -Path (Split-Path $target -Parent) -Force | Out-Null
        Copy-Item -LiteralPath (Join-Path $source $relative) -Destination $target -Force
    }
}
$verified = Get-Inventory $destination
$sourceAfter = Get-Inventory $source
if ($sourceAfter.Count -ne $sourceFiles.Count -or
    @($sourceFiles.Keys | Where-Object { $sourceAfter[$_] -ne $sourceFiles[$_] }).Count) {
    throw 'Source changed during sync. Coordinate with the other agent, then rerun.'
}
if ($verified.Count -ne $sourceFiles.Count -or
    @($sourceFiles.Keys | Where-Object { $verified[$_] -ne $sourceFiles[$_] }).Count) {
    throw 'Post-sync SHA256 verification failed. Do not report deployment complete.'
}
Write-Output "Verified: $($sourceFiles.Count) files match by SHA256; changed: $($changed.Count)."
