# setup_pcg_faculdade.ps1
# Bootstrap universal para PCs de faculdade/laboratorio sem admin.
#
# Uso rapido:
# powershell -ExecutionPolicy Bypass -File .\setup_pcg_faculdade.ps1
#
# Uso com URL customizada:
# powershell -ExecutionPolicy Bypass -File .\setup_pcg_faculdade.ps1 -RepoUrl "https://github.com/USUARIO/REPO.git"
#
# O que faz:
# - Baixa/ativa MinGit portable sem admin
# - Clona ou atualiza o repositorio
# - Configura Git
# - Cria .venv
# - Instala dependencias minimas
# - Roda validacao
# - Abre dashboard
#
# Nao faz push automatico.

param(
    [string]$RepoUrl = "https://github.com/enzo-going/international-conflict-risk-ml.git",
    [string]$RepoFolderName = "international-conflict-risk-ml-git",
    [string]$GitName = "",
    [string]$GitEmail = "",
    [switch]$SkipPythonInstall,
    [switch]$SkipValidation,
    [switch]$NoOpenDashboard
)

$ErrorActionPreference = "Stop"

$BaseDir = Join-Path $env:USERPROFILE "Downloads"
$GitDir = Join-Path $BaseDir "MinGit"
$GitZip = Join-Path $BaseDir "MinGit.zip"
$RepoDir = Join-Path $BaseDir $RepoFolderName
$GitUrl = "https://github.com/git-for-windows/git/releases/download/v2.54.0.windows.1/MinGit-2.54.0-64-bit.zip"

function Section($Text) {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor DarkGray
    Write-Host $Text -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor DarkGray
}

function Ensure-Git {
    Section "[1/8] Preparando Git portable"

    $gitAvailable = $false
    try {
        git --version | Out-Host
        $gitAvailable = $true
    } catch {
        $gitAvailable = $false
    }

    if (-not $gitAvailable) {
        if (-not (Test-Path (Join-Path $GitDir "cmd\git.exe"))) {
            Write-Host "Baixando MinGit portable..."
            Remove-Item $GitZip -Force -ErrorAction SilentlyContinue
            Remove-Item $GitDir -Recurse -Force -ErrorAction SilentlyContinue

            Invoke-WebRequest -Uri $GitUrl -OutFile $GitZip
            Expand-Archive -Path $GitZip -DestinationPath $GitDir -Force
        }

        $gitExe = Get-ChildItem $GitDir -Recurse -Filter git.exe |
            Where-Object { $_.FullName -match "\\cmd\\git\.exe$" } |
            Select-Object -First 1

        if (-not $gitExe) {
            Write-Host "ERRO: git.exe nao encontrado em $GitDir" -ForegroundColor Red
            Get-ChildItem $GitDir -Recurse -Filter git.exe | Select-Object FullName
            throw "Git portable nao encontrado."
        }

        $gitCmdDir = Split-Path $gitExe.FullName -Parent
        $env:Path = "$gitCmdDir;$env:Path"
    }

    $env:GIT_PAGER = "cat"
    git config --global core.pager cat

    Write-Host "Git ativo:"
    git --version
    where.exe git
}

function Configure-Git {
    Section "[2/8] Configurando Git"

    if ([string]::IsNullOrWhiteSpace($GitName)) {
        $currentName = ""
        try { $currentName = git config --global user.name } catch {}
        if ([string]::IsNullOrWhiteSpace($currentName)) {
            $GitName = Read-Host "Digite o nome para commits Git"
        } else {
            $GitName = $currentName
        }
    }

    if ([string]::IsNullOrWhiteSpace($GitEmail)) {
        $currentEmail = ""
        try { $currentEmail = git config --global user.email } catch {}
        if ([string]::IsNullOrWhiteSpace($currentEmail)) {
            $GitEmail = Read-Host "Digite o email do GitHub para commits"
        } else {
            $GitEmail = $currentEmail
        }
    }

    git config --global user.name "$GitName"
    git config --global user.email "$GitEmail"
    git config --global core.pager cat

    Write-Host "Nome:"
    git config --global user.name
    Write-Host "Email:"
    git config --global user.email
}

function Clone-Or-Pull {
    Section "[3/8] Clonando ou atualizando repositorio"

    Set-Location $BaseDir

    if (Test-Path (Join-Path $RepoDir ".git")) {
        Write-Host "Repositorio existente. Atualizando..."
        Set-Location $RepoDir
        git pull --rebase origin main
    } else {
        Write-Host "Clonando repositorio em:"
        Write-Host $RepoDir
        Remove-Item $RepoDir -Recurse -Force -ErrorAction SilentlyContinue
        git clone $RepoUrl $RepoDir
        Set-Location $RepoDir
    }

    Write-Host ""
    Write-Host "Log recente:"
    git --no-pager log --oneline -5
}

function Prepare-Local-Ignores {
    Section "[4/8] Preparando ignores locais"

    $excludePath = Join-Path $RepoDir ".git\info\exclude"

    $ignoreItems = @(
        ".venv/",
        "start_faculdade_session.ps1",
        "setup_pcg_faculdade.ps1"
    )

    foreach ($item in $ignoreItems) {
        $pattern = "^" + [regex]::Escape($item) + "$"
        if (-not (Select-String -Path $excludePath -Pattern $pattern -Quiet -ErrorAction SilentlyContinue)) {
            Add-Content -Path $excludePath -Value $item
        }
    }

    Write-Host "Status antes do Python:"
    git status --short
}

function Prepare-Python {
    Section "[5/8] Preparando Python"

    Set-Location $RepoDir

    if (-not (Test-Path ".venv\Scripts\python.exe")) {
        python -m venv .venv
    }

    $script:Py = Join-Path $RepoDir ".venv\Scripts\python.exe"

    & $script:Py --version
    & $script:Py -c "import sys; print(sys.executable)"

    if ($SkipPythonInstall) {
        Write-Host "Instalacao de dependencias pulada por parametro."
        return
    }

    Section "[6/8] Instalando dependencias minimas"

    & $script:Py -m pip install --upgrade pip

    # Conjunto suficiente para validacao/modelagem/dashboard.
    # Evita requirements completo porque Jupyter/Geopandas podem falhar por Windows Long Path em laboratorio.
    & $script:Py -m pip install pandas numpy scikit-learn matplotlib joblib openpyxl xlrd plotly

    Write-Host ""
    Write-Host "Testando imports:"
    & $script:Py -c "import pandas; print('pandas OK')"
    & $script:Py -c "import sklearn; print('sklearn OK')"
    & $script:Py -c "import matplotlib; print('matplotlib OK')"
    & $script:Py -c "import joblib; print('joblib OK')"
}

function Validate-And-Open {
    if (-not $SkipValidation) {
        Section "[7/8] Validando projeto"
        Set-Location $RepoDir
        & $script:Py src\validation\validate_project_artifacts.py
    } else {
        Section "[7/8] Validacao pulada"
    }

    Section "[8/8] Abrindo dashboard"

    if (-not $NoOpenDashboard) {
        if (Test-Path "docs\index.html") {
            Start-Process "docs\index.html"
        } else {
            Write-Host "ERRO: docs\index.html nao encontrado." -ForegroundColor Red
        }
    } else {
        Write-Host "Abertura do dashboard pulada por parametro."
    }

    Write-Host ""
    Write-Host "Status Git final:"
    git status --short

    Write-Host ""
    Write-Host "Repositorio pronto em:"
    Get-Location

    Write-Host ""
    Write-Host "Comandos de trabalho:"
    Write-Host 'git status --short'
    Write-Host 'git add CAMINHO_DO_ARQUIVO'
    Write-Host 'git commit -m "mensagem"'
    Write-Host 'git pull --rebase origin main'
    Write-Host 'git push origin main'
    Write-Host ""
    Write-Host "No push, se pedir senha, use um GitHub Personal Access Token. Nao cole o token em chats."
}

Ensure-Git
Configure-Git
Clone-Or-Pull
Prepare-Local-Ignores
Prepare-Python
Validate-And-Open

Write-Host ""
Write-Host "SETUP FINALIZADO." -ForegroundColor Green
