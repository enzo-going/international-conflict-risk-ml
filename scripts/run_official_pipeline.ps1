param(
    [switch]$InstallRequirements,
    [switch]$SkipDataPreparation,
    [switch]$SkipTraining,
    [switch]$SkipCharts,
    [switch]$SkipValidation,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$VenvDir = Join-Path $ProjectRoot ".venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
$Runner = Join-Path $ProjectRoot "src\pipeline\run_official_pipeline.py"

Write-Host "International Conflict Risk ML - official pipeline" -ForegroundColor Cyan
Write-Host "Project root: $ProjectRoot"

function Find-SystemPython {
    $candidates = @("python", "py")

    foreach ($candidate in $candidates) {
        $command = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($null -ne $command) {
            return $candidate
        }
    }

    $BundledPython = Join-Path $env:USERPROFILE ".cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
    if (Test-Path $BundledPython) {
        return $BundledPython
    }

    throw "Python was not found. Install Python 3 and make it available as 'python' or 'py', then rerun this script."
}

function Test-PythonExecutable {
    param([string]$PythonPath)

    $PreviousErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        & $PythonPath --version *> $null
        return $LASTEXITCODE -eq 0
    }
    catch {
        return $false
    }
    finally {
        $ErrorActionPreference = $PreviousErrorActionPreference
    }
}

$ExecutionPython = $null

if ($DryRun) {
    if ((Test-Path $VenvPython) -and (Test-PythonExecutable $VenvPython)) {
        Write-Host "Using existing local virtual environment: .venv"
        $ExecutionPython = $VenvPython
    }
    else {
        Write-Host "Dry-run mode: using system Python and leaving .venv unchanged." -ForegroundColor Yellow
        $ExecutionPython = Find-SystemPython
    }
}
else {
    if (-not (Test-Path $VenvPython)) {
        Write-Host "Creating local virtual environment at .venv ..."
        $SystemPython = Find-SystemPython
        & $SystemPython -m venv $VenvDir
        if ($LASTEXITCODE -ne 0) { throw "Failed to create .venv." }
    }
    else {
        Write-Host "Using existing local virtual environment: .venv"
    }

    if (-not (Test-Path $VenvPython)) {
        throw "Virtual environment was not created correctly: $VenvPython"
    }

    if (-not (Test-PythonExecutable $VenvPython)) {
        throw "The existing .venv Python is not executable. Recreate .venv or run this script from a shell with permission to execute $VenvPython."
    }

    $ExecutionPython = $VenvPython
}

if ($InstallRequirements) {
    if ($DryRun) {
        Write-Host "Dry-run mode: dependency installation was requested but will not be executed." -ForegroundColor Yellow
    }
    else {
        Write-Host "Installing requirements.txt into .venv ..."
        & $ExecutionPython -m pip install --upgrade pip
        if ($LASTEXITCODE -ne 0) { throw "Failed to upgrade pip." }
        & $ExecutionPython -m pip install -r (Join-Path $ProjectRoot "requirements.txt")
        if ($LASTEXITCODE -ne 0) { throw "Failed to install requirements.txt." }
    }
}
else {
    Write-Host "Skipping dependency installation. Pass -InstallRequirements to install requirements.txt."
}

$RunnerArgs = @()

if ($SkipDataPreparation) { $RunnerArgs += "--skip-data-preparation" }
if ($SkipTraining) { $RunnerArgs += "--skip-training" }
if ($SkipCharts) { $RunnerArgs += "--skip-charts" }
if ($SkipValidation) { $RunnerArgs += "--skip-validation" }
if ($DryRun) { $RunnerArgs += "--dry-run" }

Write-Host "Running official Python pipeline runner ..."
Write-Host "Command: $ExecutionPython $Runner $($RunnerArgs -join ' ')"

Push-Location $ProjectRoot
try {
    & $ExecutionPython $Runner @RunnerArgs
    if ($LASTEXITCODE -ne 0) { throw "Official pipeline runner failed with exit code $LASTEXITCODE." }
}
finally {
    Pop-Location
}
