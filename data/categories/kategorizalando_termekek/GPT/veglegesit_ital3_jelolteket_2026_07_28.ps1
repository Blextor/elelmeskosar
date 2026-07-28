$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$base = [System.IO.Path]::GetFullPath($PSScriptRoot)
$result = Join-Path $base "eredmeny.json"
$categories = Join-Path $base "kategoriak_2026-06-13.json"
$migration = Join-Path $base "alkalmaz_ital_eszreveteleket3_2026_07_28.py"
$checker = Join-Path $base "ellenoriz_ital_eszreveteleket3_2026_07_28.py"
$decisions = Join-Path $base "ital_eszrevetelek3_dontesek_2026_07_28.json"
$candidateResult = Join-Path $base ".eredmeny.ital3-20260728.candidate.json"
$candidateCategories = Join-Path $base ".kategoriak.ital3-20260728.candidate.json"
$backupResultBase = Join-Path $base "eredmeny.before-ital3-20260728.json"
$backupCategoriesBase = Join-Path $base "kategoriak_2026-06-13.before-ital3-20260728.json"
$expectedSourceResultHash = "EC3E11AB19116FC0147091857FE3FF61D28A3A31DA076E2AD15E28F9B51844E8"
$expectedSourceCategoriesHash = "1B0A1C30A3D95197EBDE279ABAEFB2E7D127FD72DDDD09B455C91861AFC54E5F"

function Assert-ScopedPath([string]$Path) {
    $fullPath = [System.IO.Path]::GetFullPath($Path)
    $prefix = $base.TrimEnd([System.IO.Path]::DirectorySeparatorChar) +
        [System.IO.Path]::DirectorySeparatorChar
    if (-not $fullPath.StartsWith(
        $prefix,
        [System.StringComparison]::OrdinalIgnoreCase
    )) {
        throw "Hatoskoron kivuli utvonal: $fullPath"
    }
}

function Assert-ScopedExistingFile([string]$Path) {
    Assert-ScopedPath $Path
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Hianyzo fajl: $Path"
    }
}

function Get-Sha256([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
}

function Get-CollisionSafePath([string]$PreferredPath) {
    Assert-ScopedPath $PreferredPath
    if (-not (Test-Path -LiteralPath $PreferredPath)) {
        return $PreferredPath
    }

    $directory = [System.IO.Path]::GetDirectoryName($PreferredPath)
    $stem = [System.IO.Path]::GetFileNameWithoutExtension($PreferredPath)
    $extension = [System.IO.Path]::GetExtension($PreferredPath)
    for ($index = 1; $index -le 9999; $index++) {
        $suffix = $index.ToString("0000")
        $candidate = Join-Path $directory "$stem-$suffix$extension"
        if (-not (Test-Path -LiteralPath $candidate)) {
            return $candidate
        }
    }
    throw "Nem talalhato szabad backup-fajlnev ehhez: $PreferredPath"
}

function Invoke-CheckedPython(
    [string]$PythonPath,
    [string[]]$Arguments,
    [string]$Label
) {
    $env:PYTHONMALLOC = "malloc"
    $env:PYTHONIOENCODING = "utf-8"
    $failures = @()
    for ($attempt = 1; $attempt -le 3; $attempt++) {
        $output = @(& $PythonPath @Arguments 2>&1)
        $exitCode = $LASTEXITCODE
        if ($exitCode -eq 0) {
            return ($output -join [Environment]::NewLine)
        }
        $tail = $output | Select-Object -Last 80
        $failures += (
            "$attempt. kiserlet, rc=$exitCode`n" +
            ($tail -join [Environment]::NewLine)
        )
    }
    throw "$Label harom kiserletben hibazott:`n$($failures -join [Environment]::NewLine)"
}

function Invoke-Checker(
    [string]$PythonPath,
    [string]$ProductsPath,
    [string]$CategoriesPath,
    [string]$SourceProductsPath,
    [string]$SourceCategoriesPath
) {
    $output = Invoke-CheckedPython `
        -PythonPath $PythonPath `
        -Arguments @(
            $checker,
            "--products", $ProductsPath,
            "--categories", $CategoriesPath,
            "--source-products", $SourceProductsPath,
            "--source-categories", $SourceCategoriesPath,
            "--decisions", $decisions
        ) `
        -Label "A fuggetlen ellenorzo"
    try {
        return ($output | ConvertFrom-Json -ErrorAction Stop)
    }
    catch {
        throw "A fuggetlen ellenorzo nem ervenyes JSON-t adott vissza: $($_.Exception.Message)"
    }
}

foreach ($path in @(
    $result,
    $categories,
    $migration,
    $checker,
    $decisions
)) {
    Assert-ScopedExistingFile $path
}
foreach ($path in @(
    $candidateResult,
    $candidateCategories,
    $backupResultBase,
    $backupCategoriesBase
)) {
    Assert-ScopedPath $path
}

$sourceResultHash = Get-Sha256 $result
$sourceCategoriesHash = Get-Sha256 $categories
if ($sourceResultHash -ne $expectedSourceResultHash) {
    throw "Az eredmeny.json nem a rogzitett forrasallapot: $sourceResultHash"
}
if ($sourceCategoriesHash -ne $expectedSourceCategoriesHash) {
    throw "A kategoriafa nem a rogzitett forrasallapot: $sourceCategoriesHash"
}

$pythonCommand = Get-Command python -CommandType Application -ErrorAction Stop |
    Select-Object -First 1
$python = [string]$pythonCommand.Source

# Stale generated candidates must never be mistaken for this run's output.
foreach ($path in @($candidateResult, $candidateCategories)) {
    if (Test-Path -LiteralPath $path) {
        [System.IO.File]::Delete($path)
    }
}

$migrationOutput = Invoke-CheckedPython `
    -PythonPath $python `
    -Arguments @(
        $migration,
        "--prepare-only",
        "--products-source", $result,
        "--categories-source", $categories,
        "--decisions", $decisions
    ) `
    -Label "Az ital3 migracio"

Assert-ScopedExistingFile $candidateResult
Assert-ScopedExistingFile $candidateCategories

$candidateResultHash = Get-Sha256 $candidateResult
$candidateCategoriesHash = Get-Sha256 $candidateCategories
$candidateCheck = Invoke-Checker `
    -PythonPath $python `
    -ProductsPath $candidateResult `
    -CategoriesPath $candidateCategories `
    -SourceProductsPath $result `
    -SourceCategoriesPath $categories

$idempotenceOutput = Invoke-CheckedPython `
    -PythonPath $python `
    -Arguments @(
        $migration,
        "--assert-idempotent",
        "--products-source", $candidateResult,
        "--categories-source", $candidateCategories,
        "--decisions", $decisions
    ) `
    -Label "Az ital3 idempotenciateszt"

# The durable backups are new files on every attempt; an older backup is never
# overwritten or silently reused.
$backupResult = Get-CollisionSafePath $backupResultBase
$backupCategories = Get-CollisionSafePath $backupCategoriesBase
[System.IO.File]::Copy($result, $backupResult, $false)
[System.IO.File]::Copy($categories, $backupCategories, $false)
if ((Get-Sha256 $backupResult) -ne $expectedSourceResultHash) {
    throw "Az eredmeny tartos backupjanak SHA-256 erteke hibas: $backupResult"
}
if ((Get-Sha256 $backupCategories) -ne $expectedSourceCategoriesHash) {
    throw "A kategoriafa tartos backupjanak SHA-256 erteke hibas: $backupCategories"
}

$transactionId = [guid]::NewGuid().ToString("N")
$replaceBackupResult = Join-Path $base ".eredmeny.ital3-$transactionId.replace-backup.json"
$replaceBackupCategories = Join-Path $base ".kategoriak.ital3-$transactionId.replace-backup.json"
foreach ($path in @($replaceBackupResult, $replaceBackupCategories)) {
    Assert-ScopedPath $path
    if (Test-Path -LiteralPath $path) {
        throw "Varatlan replace-backup utkozes: $path"
    }
}

$finalCheck = $null
$resultReplaced = $false
try {
    # Recheck every saved input immediately before the first mutation.
    if ((Get-Sha256 $result) -ne $expectedSourceResultHash) {
        throw "Az eredmeny.json megvaltozott az ellenorzes utan."
    }
    if ((Get-Sha256 $categories) -ne $expectedSourceCategoriesHash) {
        throw "A kategoriafa megvaltozott az ellenorzes utan."
    }
    if ((Get-Sha256 $candidateResult) -ne $candidateResultHash) {
        throw "Az eredmeny jelolt megvaltozott az ellenorzes utan."
    }
    if ((Get-Sha256 $candidateCategories) -ne $candidateCategoriesHash) {
        throw "A kategoriafa jelolt megvaltozott az ellenorzes utan."
    }

    [System.IO.File]::Replace(
        $candidateResult,
        $result,
        $replaceBackupResult,
        $true
    )
    $resultReplaced = $true
    [System.IO.File]::Replace(
        $candidateCategories,
        $categories,
        $replaceBackupCategories,
        $true
    )

    if ((Get-Sha256 $result) -ne $candidateResultHash) {
        throw "Az alkalmazott eredmeny SHA-256 erteke elter a jelolttol."
    }
    if ((Get-Sha256 $categories) -ne $candidateCategoriesHash) {
        throw "Az alkalmazott kategoriafa SHA-256 erteke elter a jelolttol."
    }
    if ((Get-Sha256 $replaceBackupResult) -ne $expectedSourceResultHash) {
        throw "Az eredmeny tranzakcios backupjanak SHA-256 erteke hibas."
    }
    if ((Get-Sha256 $replaceBackupCategories) -ne $expectedSourceCategoriesHash) {
        throw "A kategoriafa tranzakcios backupjanak SHA-256 erteke hibas."
    }

    $finalCheck = Invoke-Checker `
        -PythonPath $python `
        -ProductsPath $result `
        -CategoriesPath $categories `
        -SourceProductsPath $backupResult `
        -SourceCategoriesPath $backupCategories
}
catch {
    $failure = $_
    $rollbackErrors = @()
    if ($resultReplaced) {
        try {
            if ((Get-Sha256 $backupResult) -ne $expectedSourceResultHash) {
                throw "Az eredmeny tartos backupja serult."
            }
            [System.IO.File]::Copy($backupResult, $result, $true)
            if ((Get-Sha256 $result) -ne $expectedSourceResultHash) {
                throw "Az eredmeny visszaallitasa utani SHA-256 hibas."
            }
        }
        catch {
            $rollbackErrors += $_.Exception.Message
        }
        try {
            if ((Get-Sha256 $backupCategories) -ne $expectedSourceCategoriesHash) {
                throw "A kategoriafa tartos backupja serult."
            }
            [System.IO.File]::Copy($backupCategories, $categories, $true)
            if ((Get-Sha256 $categories) -ne $expectedSourceCategoriesHash) {
                throw "A kategoriafa visszaallitasa utani SHA-256 hibas."
            }
        }
        catch {
            $rollbackErrors += $_.Exception.Message
        }
    }
    foreach ($path in @($replaceBackupResult, $replaceBackupCategories)) {
        if (Test-Path -LiteralPath $path) {
            [System.IO.File]::Delete($path)
        }
    }
    if ($rollbackErrors.Count -gt 0) {
        throw "A veglegesites hibazott: $($failure.Exception.Message)`nA rollback is hibazott: $($rollbackErrors -join '; ')"
    }
    throw $failure
}

foreach ($path in @($replaceBackupResult, $replaceBackupCategories)) {
    if (Test-Path -LiteralPath $path) {
        [System.IO.File]::Delete($path)
    }
}

[pscustomobject]@{
    Status = "ok"
    ResultSHA256 = Get-Sha256 $result
    CategoriesSHA256 = Get-Sha256 $categories
    BackupResult = $backupResult
    BackupResultSHA256 = Get-Sha256 $backupResult
    BackupCategories = $backupCategories
    BackupCategoriesSHA256 = Get-Sha256 $backupCategories
    CandidateCheck = $candidateCheck
    FinalCheck = $finalCheck
    IdempotenceOutputTail = (
        ($idempotenceOutput -split [Environment]::NewLine) |
            Select-Object -Last 20
    ) -join [Environment]::NewLine
    MigrationOutputTail = (
        ($migrationOutput -split [Environment]::NewLine) |
            Select-Object -Last 20
    ) -join [Environment]::NewLine
}
