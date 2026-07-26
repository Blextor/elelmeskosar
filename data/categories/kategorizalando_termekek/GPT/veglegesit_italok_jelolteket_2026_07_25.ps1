$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$base = [System.IO.Path]::GetFullPath($PSScriptRoot)
$result = Join-Path $base "eredmeny.json"
$categories = Join-Path $base "kategoriak_2026-06-13.json"
$candidateResult = Join-Path $base ".eredmeny.italok-20260725.candidate.json"
$candidateCategories = Join-Path $base ".kategoriak.italok-20260725.candidate.json"
$backupResult = Join-Path $base "eredmeny.before-italok-20260725.json"
$backupCategories = Join-Path $base "kategoriak_2026-06-13.before-italok-20260725.json"
$replaceBackupResult = Join-Path $base ".eredmeny.italok-20260725.replace-backup.json"
$replaceBackupCategories = Join-Path $base ".kategoriak.italok-20260725.replace-backup.json"
$expectedBackupResultHash = "426F79FD4698CA596916484A4AEB322C50724A729992CA2262DC1C3ADF5C2E8E"
$expectedBackupCategoriesHash = "DD37310ACFD88DC5DE37DCEE6C031B92F1E8F9D358676D394D07ABE96FDD75D5"

function Assert-ScopedLeaf([string]$Path) {
    $fullPath = [System.IO.Path]::GetFullPath($Path)
    if (-not $fullPath.StartsWith($base, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Hatókörön kívüli útvonal: $fullPath"
    }
    if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
        throw "Hiányzó fájl: $fullPath"
    }
}

function Get-Sha256([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
}

foreach ($path in @($result, $categories, $candidateResult, $candidateCategories)) {
    Assert-ScopedLeaf $path
}

$originalResultHash = Get-Sha256 $result
$originalCategoriesHash = Get-Sha256 $categories
$candidateResultHash = Get-Sha256 $candidateResult
$candidateCategoriesHash = Get-Sha256 $candidateCategories

if (-not (Test-Path -LiteralPath $backupResult -PathType Leaf)) {
    Copy-Item -LiteralPath $result -Destination $backupResult
}
if (-not (Test-Path -LiteralPath $backupCategories -PathType Leaf)) {
    Copy-Item -LiteralPath $categories -Destination $backupCategories
}
if ((Get-Sha256 $backupResult) -ne $expectedBackupResultHash) {
    throw "Az eredmeny tartós backup SHA-256 értéke eltér a rögzített forrástól."
}
if ((Get-Sha256 $backupCategories) -ne $expectedBackupCategoriesHash) {
    throw "A kategóriafa tartós backup SHA-256 értéke eltér a rögzített forrástól."
}
foreach ($path in @($replaceBackupResult, $replaceBackupCategories)) {
    if (Test-Path -LiteralPath $path) {
        throw "Váratlan korábbi replace-backup: $path"
    }
}

try {
    [System.IO.File]::Replace(
        $candidateResult,
        $result,
        $replaceBackupResult,
        $true
    )
    [System.IO.File]::Replace(
        $candidateCategories,
        $categories,
        $replaceBackupCategories,
        $true
    )
    if ((Get-Sha256 $result) -ne $candidateResultHash) {
        throw "Az alkalmazott eredmeny SHA-256 értéke eltér a jelölttől."
    }
    if ((Get-Sha256 $categories) -ne $candidateCategoriesHash) {
        throw "Az alkalmazott kategóriafa SHA-256 értéke eltér a jelölttől."
    }
}
catch {
    [System.IO.File]::Copy($backupResult, $result, $true)
    [System.IO.File]::Copy($backupCategories, $categories, $true)
    if ((Get-Sha256 $result) -ne $expectedBackupResultHash) {
        throw "Az eredmeny visszaállítása utáni SHA-256 hibás."
    }
    if ((Get-Sha256 $categories) -ne $expectedBackupCategoriesHash) {
        throw "A kategóriafa visszaállítása utáni SHA-256 hibás."
    }
    throw
}

if ((Get-Sha256 $replaceBackupResult) -ne $originalResultHash) {
    throw "A replace-backup eredmeny SHA-256 értéke hibás."
}
if ((Get-Sha256 $replaceBackupCategories) -ne $originalCategoriesHash) {
    throw "A replace-backup kategóriafa SHA-256 értéke hibás."
}

[System.IO.File]::Delete($replaceBackupResult)
[System.IO.File]::Delete($replaceBackupCategories)

[pscustomobject]@{
    Status = "ok"
    ResultSHA256 = Get-Sha256 $result
    CategoriesSHA256 = Get-Sha256 $categories
    BackupResultSHA256 = Get-Sha256 $backupResult
    BackupCategoriesSHA256 = Get-Sha256 $backupCategories
}
