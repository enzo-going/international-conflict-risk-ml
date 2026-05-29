# run_project_local.ps1
# Rode dentro da raiz do repositorio.
# Uso:
# powershell -ExecutionPolicy Bypass -File .\tools\setup\run_project_local.ps1

$ErrorActionPreference = "Stop"

$env:GIT_PAGER = "cat"
try { git config --global core.pager cat } catch {}

if (-not (Test-Path "README.md")) {
    throw "Execute este script na raiz do projeto."
}

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    python -m venv .venv
}

$py = ".venv\Scripts\python.exe"

& $py -m pip install --upgrade pip
& $py -m pip install pandas numpy scikit-learn matplotlib joblib openpyxl xlrd plotly

& $py src\validation\audit_dataset_integration.py
& $py src\analysis\generate_country_risk_assessment.py
& $py src\analysis\generate_country_risk_explanations.py

if (Test-Path "src\visualization\generate_predictive_charts.py") {
    & $py src\visualization\generate_predictive_charts.py
}

& $py src\validation\validate_project_artifacts.py

Start-Process "docs\index.html"

git status --short
