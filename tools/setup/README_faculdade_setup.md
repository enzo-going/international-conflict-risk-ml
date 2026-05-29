# Scripts de setup para PCs de faculdade/laboratório

## Objetivo

Permitir que qualquer integrante do grupo consiga preparar rapidamente um PC sem Git instalado e sem permissão de administrador.

## Script principal

```powershell
tools/setup/setup_pcg_faculdade.ps1
```

Ele faz:

- ativa ou baixa MinGit portable;
- clona ou atualiza o repositório;
- configura nome/e-mail do Git;
- cria `.venv`;
- instala dependências mínimas;
- roda validação;
- abre o dashboard.

## Uso em um PC novo da faculdade

Baixar o script e rodar:

```powershell
powershell -ExecutionPolicy Bypass -File ".\setup_pcg_faculdade.ps1"
```

Com parâmetros opcionais:

```powershell
powershell -ExecutionPolicy Bypass -File ".\setup_pcg_faculdade.ps1" -GitName "Seu Nome" -GitEmail "seu-email@exemplo.com"
```

## Uso dentro do repositório já clonado

```powershell
powershell -ExecutionPolicy Bypass -File ".\tools\setup\run_project_local.ps1"
```

## Observações

- O script evita instalar o `requirements.txt` inteiro em laboratório porque pacotes como Jupyter/Geopandas podem falhar por limite de caminho no Windows.
- O conjunto mínimo instalado cobre validação, modelagem principal, relatórios, gráficos e dashboard.
- Para `git push`, o GitHub pode pedir autenticação no navegador ou Personal Access Token.
- Não cole token em chats.
