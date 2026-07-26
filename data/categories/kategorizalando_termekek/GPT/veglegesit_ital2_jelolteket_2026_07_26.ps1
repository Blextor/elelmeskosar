$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$base = [System.IO.Path]::GetFullPath($PSScriptRoot)
$result = Join-Path $base "eredmeny.json"
$categories = Join-Path $base "kategoriak_2026-06-13.json"
$checker = Join-Path $base "ellenoriz_ital_eszreveteleket2_2026_07_26.py"
$candidateResult = Join-Path $base ".eredmeny.ital2-20260726.candidate.json"
$candidateCategories = Join-Path $base ".kategoriak.ital2-20260726.candidate.json"
$backupResult = Join-Path $base "eredmeny.before-ital2-20260726.json"
$backupCategories = Join-Path $base "kategoriak_2026-06-13.before-ital2-20260726.json"
$replaceBackupResult = Join-Path $base ".eredmeny.ital2-20260726.replace-backup.json"
$replaceBackupCategories = Join-Path $base ".kategoriak.ital2-20260726.replace-backup.json"
$expectedSourceResultHash = "804B248BC371D54D01EB9D37F2D83EBC7843E5B3A067A44556B6325BB0B0FBB3"
$expectedSourceCategoriesHash = "6D12CC9A454CFF05F8839278123CB4453255D1B58D3E5E888757D25EB9EE150F"

function Assert-ScopedLeaf([string]$Path) {
    $fullPath = [System.IO.Path]::GetFullPath($Path)
    $prefix = $base.TrimEnd([System.IO.Path]::DirectorySeparatorChar) +
        [System.IO.Path]::DirectorySeparatorChar
    if (-not $fullPath.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Hatókörön kívüli útvonal: $fullPath"
    }
    if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
        throw "Hiányzó fájl: $fullPath"
    }
}

function Get-Sha256([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
}

function Invoke-Checker([string]$ProductsPath, [string]$CategoriesPath) {
    $failures = @()
    for ($attempt = 1; $attempt -le 3; $attempt++) {
        $env:PYTHONMALLOC = "malloc"
        $env:PYTHONIOENCODING = "utf-8"
        $output = & python $checker --products $ProductsPath --categories $CategoriesPath 2>&1
        $exitCode = $LASTEXITCODE
        if ($exitCode -eq 0) {
            return ($output -join [Environment]::NewLine)
        }
        $tail = $output | Select-Object -Last 40
        $failures += "$attempt. kísérlet, rc=$exitCode`n$($tail -join [Environment]::NewLine)"
    }
    throw "A független ellenőrző háromszor hibázott:`n$($failures -join [Environment]::NewLine)"
}

foreach ($path in @(
    $result,
    $categories,
    $checker,
    $candidateResult,
    $candidateCategories
)) {
    Assert-ScopedLeaf $path
}

$sourceResultHash = Get-Sha256 $result
$sourceCategoriesHash = Get-Sha256 $categories
if ($sourceResultHash -ne $expectedSourceResultHash) {
    throw "Az eredmeny.json nem a rögzített első javítási állapot: $sourceResultHash"
}
if ($sourceCategoriesHash -ne $expectedSourceCategoriesHash) {
    throw "A kategóriafa nem a rögzített első javítási állapot: $sourceCategoriesHash"
}

$candidateResultHash = Get-Sha256 $candidateResult
$candidateCategoriesHash = Get-Sha256 $candidateCategories
$candidateCheck = Invoke-Checker $candidateResult $candidateCategories

if (-not (Test-Path -LiteralPath $backupResult -PathType Leaf)) {
    Copy-Item -LiteralPath $result -Destination $backupResult
}
if (-not (Test-Path -LiteralPath $backupCategories -PathType Leaf)) {
    Copy-Item -LiteralPath $categories -Destination $backupCategories
}
if ((Get-Sha256 $backupResult) -ne $expectedSourceResultHash) {
    throw "Az eredmeny második kör előtti tartós backupja hibás."
}
if ((Get-Sha256 $backupCategories) -ne $expectedSourceCategoriesHash) {
    throw "A kategóriafa második kör előtti tartós backupja hibás."
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
    if ((Get-Sha256 $replaceBackupResult) -ne $expectedSourceResultHash) {
        throw "A replace-backup eredmeny SHA-256 értéke hibás."
    }
    if ((Get-Sha256 $replaceBackupCategories) -ne $expectedSourceCategoriesHash) {
        throw "A replace-backup kategóriafa SHA-256 értéke hibás."
    }
    $finalCheck = Invoke-Checker $result $categories
}
catch {
    [System.IO.File]::Copy($backupResult, $result, $true)
    [System.IO.File]::Copy($backupCategories, $categories, $true)
    if ((Get-Sha256 $result) -ne $expectedSourceResultHash) {
        throw "Az eredmeny visszaállítása utáni SHA-256 hibás."
    }
    if ((Get-Sha256 $categories) -ne $expectedSourceCategoriesHash) {
        throw "A kategóriafa visszaállítása utáni SHA-256 hibás."
    }
    foreach ($path in @($replaceBackupResult, $replaceBackupCategories)) {
        if (Test-Path -LiteralPath $path) {
            [System.IO.File]::Delete($path)
        }
    }
    throw
}

[System.IO.File]::Delete($replaceBackupResult)
[System.IO.File]::Delete($replaceBackupCategories)

[pscustomobject]@{
    Status = "ok"
    ResultSHA256 = Get-Sha256 $result
    CategoriesSHA256 = Get-Sha256 $categories
    BackupResultSHA256 = Get-Sha256 $backupResult
    BackupCategoriesSHA256 = Get-Sha256 $backupCategories
    CandidateCheck = $candidateCheck
    FinalCheck = $finalCheck
}
