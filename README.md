# International Conflict Risk ML

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![GitHub Pages](https://img.shields.io/badge/Dashboard-GitHub%20Pages-222222?style=flat&logo=github&logoColor=white)

## Visualização do projeto

Este projeto possui uma página HTML publicada via GitHub Pages para facilitar a visualização geral da proposta, dos dados utilizados, do pipeline de Machine Learning e dos resultados parciais.

Acesse aqui:

[Dashboard do projeto](https://enzo-going.github.io/international-conflict-risk-ml/)

Projeto acadêmico de Machine Learning aplicado à análise preditiva de conflitos internacionais a partir de dados heterogêneos em formato tabular e temporal.

Este projeto faz parte da Pesquisa Curricularizada da Graduação em Ciência da Computação, envolvendo principalmente os componentes de Reconhecimento de Padrões com Inteligência Artificial e Banco de Dados.

## Objetivo

Desenvolver uma base analítica e experimental para estimar risco de ocorrência ou intensificação de conflitos internacionais utilizando dados históricos organizados em estrutura país-ano.

A proposta inicial partiu de uma questão ampla sobre tensões globais, escalada de conflitos e risco de grandes crises internacionais. Para tornar o problema tecnicamente defensável, o projeto foi reformulado como uma tarefa supervisionada de Machine Learning em estrutura `country-year`.

O objetivo atual não é prever uma guerra mundial de forma determinística. O objetivo é construir um sistema experimental, probabilístico e reprodutível para estimar se um país apresentará violência organizada no ano seguinte, com base em dados históricos, features temporais e indicadores externos.

## Escopo técnico atual

O escopo técnico atual do projeto envolve:

- construção de um pipeline reprodutível de dados e Machine Learning;
- uso da UCDP como base central de conflitos organizados;
- integração de indicadores socioeconômicos do World Bank;
- criação de features temporais e derivadas;
- avaliação com split temporal;
- comparação contra baseline de persistência;
- geração de métricas, predições e modelo treinado;
- documentação metodológica do processo;
- manutenção de um dashboard HTML para acompanhamento visual do projeto.

## Formulação técnica do problema

A unidade principal de análise é `country-year`.

O problema atual é tratado como uma tarefa de classificação supervisionada:

`target_conflict_next_year`

Esse target indica se um país apresentará violência organizada no ano seguinte.

A avaliação principal utiliza split temporal, treinando em anos anteriores e testando em anos posteriores. Isso evita misturar passado e futuro, tornando a avaliação mais coerente para um problema temporal.

A baseline obrigatória do projeto é a persistência de conflito:

`y_pred = organized_violence_exists`

Essa baseline é forte porque conflitos tendem a apresentar continuidade histórica. Por isso, qualquer modelo mais complexo precisa ser comparado contra ela.

## Arquitetura e organização do projeto

O repositório foi organizado para separar dados, código, documentação, experimentos e artefatos gerados pelo pipeline de Machine Learning.

A estrutura segue a lógica do fluxo técnico do projeto:

```text
ingestão de dados
→ limpeza e padronização
→ construção do dataset país-ano
→ criação do target supervisionado
→ engenharia de features temporais e socioeconômicas
→ treinamento do modelo
→ comparação com baseline
→ geração de métricas, predições e dashboard
```

### Estrutura de pastas

```text
international-conflict-risk-ml/
├── data/
│   ├── raw/           # Dados brutos originais, preservados sem edição manual
│   ├── interim/       # Arquivos auxiliares de integração, como mapeamentos de países
│   ├── processed/     # Dados limpos e padronizados
│   └── final/         # Datasets finais usados em análise e modelagem
│
├── src/
│   ├── data/          # Scripts de ingestão, limpeza e integração dos datasets
│   ├── features/      # Engenharia de atributos temporais e socioeconômicos
│   ├── models/        # Treinamento, avaliação e exportação dos modelos
│   └── visualization/ # Scripts futuros de visualização
│
├── notebooks/
│   ├── exploration/   # Análise exploratória dos dados
│   └── modeling/      # Experimentos de modelagem e avaliação
│
├── outputs/
│   ├── charts/        # Gráficos exportados
│   ├── tables/        # Métricas, predições e tabelas auxiliares
│   └── models/        # Modelo treinado e metadados
│
├── docs/
│   ├── academic/      # Materiais acadêmicos e entregas
│   ├── methodology/   # Documentação metodológica do pipeline
│   ├── references/    # Fontes, indicadores e referências externas
│   ├── index.html     # Dashboard publicado via GitHub Pages
│   └── project_map.md # Mapa técnico detalhado do projeto
│
└── reports/
    ├── qualification/ # Materiais da qualificação
    └── final/         # Materiais da entrega final
```

### Leitura prática das pastas

| Pasta | Função no projeto |
|---|---|
| `data/raw/` | Guarda os arquivos originais baixados das fontes, sem edição manual. |
| `data/processed/` | Contém dados limpos, padronizados e preparados para integração. |
| `data/interim/` | Armazena arquivos auxiliares, como mapeamentos entre nomes/códigos de países. |
| `data/final/` | Contém os datasets finais usados diretamente nas análises e modelos. |
| `src/data/` | Scripts que constroem os datasets a partir das fontes brutas e processadas. |
| `src/features/` | Scripts responsáveis por criar features temporais e socioeconômicas. |
| `src/models/` | Scripts de treinamento, avaliação e exportação dos modelos. |
| `notebooks/` | Ambiente de exploração, testes e experimentos comparativos. |
| `outputs/` | Resultados produzidos pelo pipeline: métricas, predições, tabelas e modelos. |
| `docs/` | Documentação metodológica, referências e dashboard visual do projeto. |
| `reports/` | Materiais voltados à qualificação e à entrega final. |

Para uma visão detalhada da função de cada arquivo e da ordem dos scripts, consulte:

`docs/project_map.md`

Para uma síntese metodológica final do projeto, consulte:

`docs/methodology/final_methodological_summary.md`

## Pipeline principal

O pipeline oficial do projeto utiliza:

- UCDP Organized Violence Country-Year como base central;
- World Bank Open Data como fonte externa socioeconômica;
- estrutura de análise `country-year`;
- target supervisionado `target_conflict_next_year`;
- split temporal para avaliação;
- modelo principal reproduzível em `src/models/train_conflict_risk_model.py`.

Ordem atual dos scripts principais:

1. `src/data/prepare_ucdp_organized_violence.py`
   - processa o arquivo bruto da UCDP.

2. `src/data/build_conflict_country_year_base.py`
   - cria o dataset base país-ano;
   - cria `organized_violence_exists`;
   - cria `target_conflict_next_year`.

3. `src/features/build_temporal_features.py`
   - cria features temporais de conflito.

4. `src/data/prepare_world_bank_indicators.py`
   - baixa e processa indicadores do World Bank.

5. `src/data/build_conflict_country_year_world_bank.py`
   - integra UCDP + World Bank usando mapeamento de países.

6. `src/features/build_world_bank_features.py`
   - cria features derivadas do World Bank.

7. `src/models/train_conflict_risk_model.py`
   - treina o modelo principal;
   - compara contra a baseline de persistência;
   - salva métricas, predições, metadados e modelo treinado.

## Resultado atual do modelo principal

No estado consolidado atual, o melhor modelo documentado permanece `Logistic Regression + World Bank all raw`. A camada de explicabilidade atual registra 33 features e 33 coeficientes para análise por país, enquanto novas fontes World Bank/PRIO foram auditadas como oficiais, candidatas ou dados de suporte antes de qualquer integração definitiva ao pipeline principal.

| Modelo | Accuracy | Precision | Recall | F1-score |
|---|---:|---:|---:|---:|
| Persistence baseline | 0.9072 | 0.8571 | 0.8571 | 0.8571 |
| Logistic Regression + World Bank all raw | 0.9197 | 0.9029 | 0.8435 | 0.8722 |

O modelo principal atual supera a baseline de persistência, com ganho aproximado de:

`+0.0151` em F1-score.

O melhor resultado histórico anterior era `0.8711`. Após a análise de ablação, o melhor conjunto passou a ser `World Bank all raw`, com F1-score de `0.8722`.

Esse resultado é metodologicamente relevante porque mostra que mais features nem sempre significam melhor desempenho. A análise de ablação indicou que os indicadores brutos completos do World Bank funcionaram melhor do que o conjunto com todas as features derivadas.

### Robustez temporal

Foi adicionada uma avaliação de robustez temporal para testar o modelo oficial em múltiplas janelas, além do split consolidado 2017-2023.

Resumo atual:

- split oficial reproduzido: F1 `0.8722` contra `0.8571` da persistência;
- rolling one-year test: 8 vitórias, 1 empate e 2 derrotas contra a persistência;
- expanding holdout: 7 vitórias em 7 janelas contra a persistência.

Interpretação: o modelo mantém ganho agregado e vence em todos os holdouts expansivos, mas a vantagem anual não é perfeitamente estável. Portanto, esse resultado deve ser tratado como evidência de robustez parcial, não como substituição do resultado principal.

Arquivos principais:

- `src/models/run_temporal_robustness_evaluation.py`
- `docs/methodology/temporal_robustness_evaluation.md`
- `outputs/tables/temporal_robustness_summary.json`

## Status atual

O projeto possui atualmente um pipeline principal funcional baseado em UCDP Organized Violence, indicadores World Bank, split temporal, baseline de persistência, comparação de modelos candidatos, análise preditiva por país, camada SQL, validação automática e dashboard via GitHub Pages.

Após as contribuições recentes do grupo, o repositório também passou a conter novas fontes World Bank/PRIO e módulos experimentais relacionados a One-Sided Violence, WWI, WWII, inflação, juros, PIB e escalada histórica. Essas fontes foram auditadas e classificadas, mas nem todas substituem ou alteram o modelo principal.

## Comparação de modelos candidatos

Além do modelo principal, foram testados modelos candidatos usando o mesmo split temporal e o mesmo conjunto de 33 features.

Modelos avaliados:

- Persistence baseline;
- Logistic Regression;
- Random Forest;
- Gradient Boosting;
- MLP simples.

Resultado resumido:

| Modelo | Accuracy | Precision | Recall | F1-score |
|---|---:|---:|---:|---:|
| Logistic Regression + World Bank all raw | 0.9197 | 0.9029 | 0.8435 | 0.8722 |
| Random Forest + World Bank all raw | 0.9124 | 0.8594 | 0.8730 | 0.8661 |
| Gradient Boosting + World Bank all raw | 0.9138 | 0.9197 | 0.8050 | 0.8585 |
| Persistence baseline | 0.9072 | 0.8571 | 0.8571 | 0.8571 |
| MLP + World Bank all raw | 0.9094 | 0.9206 | 0.7891 | 0.8498 |

A Logistic Regression permaneceu como modelo principal por apresentar o melhor F1-score, mantendo boa interpretabilidade e desempenho superior à baseline.

Os resultados completos estão em:

- `src/models/train_candidate_models.py`
- `outputs/tables/candidate_model_comparison.csv`

## Camada SQL e banco SQLite

Além dos scripts Python, notebooks e outputs em CSV, o projeto possui uma camada SQL inicial para consulta e organização dos dados.

Essa camada transforma os principais artefatos do pipeline em uma estrutura relacional consultável, reforçando a parte de Banco de Dados do projeto.

### Componentes da camada SQL

| Componente | Função |
|---|---|
| `sql/schema.sql` | Define o schema do banco SQLite. |
| `src/data/build_sqlite_database.py` | Gera o banco local a partir dos CSVs do projeto. |
| `data/database/conflict_risk_ml.sqlite` | Banco SQLite gerado localmente e ignorado pelo Git. |
| `sql/queries/` | Consultas SQL analíticas. |
| `docs/database/database_design.md` | Documentação do desenho da camada de banco. |

### Consultas SQL disponíveis

As queries em `sql/queries/` permitem consultar:

- países e anos com maior risco previsto;
- falsos positivos;
- falsos negativos;
- variáveis mais influentes do modelo;
- métricas comparativas entre baseline e modelo principal.

O banco local pode ser gerado com:

```powershell
python src\data\build_sqlite_database.py
```

O projeto já saiu da fase inicial de estruturação e atualmente possui um pipeline funcional de Machine Learning.

### Concluído até o momento

- [x] Estrutura inicial do repositório
- [x] Processamento da base UCDP Organized Violence Country-Year
- [x] Construção do dataset país-ano
- [x] Criação do target `target_conflict_next_year`
- [x] Análise exploratória inicial
- [x] Baseline de persistência
- [x] Modelos clássicos iniciais
- [x] Integração com indicadores do World Bank
- [x] Engenharia de features temporais
- [x] Script principal de treinamento reproduzível
- [x] Modelo principal salvo
- [x] Análise de probabilidade e threshold
- [x] Dashboard HTML publicado
- [x] Mapa técnico do projeto em `docs/project_map.md`
- [x] Reexecução do modelo principal após a segunda expansão dos indicadores World Bank
- [x] Atualização das métricas após a reexecução com indicadores World Bank expandidos

### Em andamento

- [ ] Validar arquivos WWI adicionados pelo grupo
- [ ] Consolidar documentação para qualificação
- [x] Testar modelos adicionais, como Random Forest, Gradient Boosting e MLP
- [ ] Avaliar seleção de features e impacto individual dos indicadores World Bank

## Análise preditiva por país

Além das métricas globais do modelo, o projeto gera uma avaliação preditiva por país.

Scripts principais:

- `src/analysis/generate_country_risk_assessment.py`
- `src/analysis/generate_country_risk_explanations.py`

Arquivos gerados:

- `outputs/tables/country_risk_assessment_latest_year.csv`
- `outputs/tables/country_risk_level_summary.csv`
- `outputs/tables/country_risk_explanations_latest_year.csv`
- `outputs/tables/country_risk_explanation_group_summary.csv`
- `reports/final/country_risk_assessment_latest_year.md`
- `reports/final/country_risk_explanations_latest_year.md`

Resultado atual:

| Item | Valor |
|---|---:|
| Ano-base | 2023 |
| Ano previsto | 2024 |
| Países avaliados | 194 |
| Probabilidade média estimada | 0.3427 |
| Países em risco alto ou muito alto | 59 |
| Previsões positivas pelo threshold atual | 60 |
| Casos positivos observados no ano previsto | 58 |
| Features usadas na explicação | 33 |
| Coeficientes usados | 33 |

Essa camada permite formular análises como: para o ano-base `2023`, o modelo estimou determinada probabilidade de violência organizada em `2024` para cada país.

As explicações são aproximações baseadas nas features e nos coeficientes do modelo. Elas indicam associação estatística, não causalidade direta.

## Auditoria de integração de datasets

Como o projeto recebeu datasets de diferentes integrantes do grupo, foi criada uma auditoria automática para classificar cada fonte antes de qualquer integração ao pipeline principal.

O script responsável é:

`src/validation/audit_dataset_integration.py`

A auditoria gera:

- `outputs/tables/dataset_integration_audit.csv`
- `outputs/tables/dataset_integration_summary.json`
- `reports/final/dataset_integration_audit.md`

Resultado atual da auditoria:

| Categoria | Quantidade |
|---|---:|
| Total de datasets auditados | 35 |
| Oficiais ou candidatos ao pipeline | 12 |
| Experimentais em revisão | 4 |
| Dados brutos preservados para rastreabilidade | 16 |
| Não prontos para integração direta | 3 |

A decisão metodológica adotada foi não integrar todos os datasets cegamente. Apenas fontes compatíveis com a unidade `country-year`, com chave geográfica e temporal, podem entrar no pipeline principal. As demais são preservadas como dados brutos de suporte, módulos experimentais ou fontes futuras.

## Validação automática dos artefatos

O projeto possui um script de validação automática para verificar a consistência dos principais arquivos, outputs, schemas e metadados do pipeline.

O script está em:

`src/validation/validate_project_artifacts.py`

Ele gera:

- `outputs/tables/project_validation_report.csv`
- `outputs/tables/project_validation_summary.json`

Na execução atual, a validação retornou 79 checks com status PASS, sem falhas.

Para executar:

`python src/validation/validate_project_artifacts.py`

## Documento de consolidação do projeto

Para uma visão consolidada do estado atual do projeto, incluindo pipeline principal, datasets oficiais/candidatos, módulos experimentais, resultados válidos, limitações e próximos passos, consulte:

`reports/final/project_consolidation_review.md`

## Como reproduzir o pipeline oficial

O pipeline oficial é o fluxo UCDP Organized Violence + features temporais + World Bank raw + Logistic Regression. Ele estima `target_conflict_next_year` em estrutura `country-year`; não é uma previsão determinística de guerra mundial ou de eventos geopolíticos específicos.

### Opção recomendada no Windows

O script PowerShell cria uma `.venv`, ativa o ambiente e chama o runner oficial em Python.

Para testar sem alterar arquivos:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_official_pipeline.ps1 -DryRun
```

Para criar o ambiente, instalar dependências e rodar o pipeline oficial:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_official_pipeline.ps1 -InstallRequirements
```

Parâmetros úteis:

- `-SkipDataPreparation`
- `-SkipTraining`
- `-SkipCharts`
- `-SkipValidation`
- `-DryRun`

### Opção manual com Python

Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Rode o runner oficial:

```powershell
python src\pipeline\run_official_pipeline.py
```

Para inspecionar a ordem das etapas sem executar:

```powershell
python src\pipeline\run_official_pipeline.py --dry-run
```

O runner oficial não executa download/preparação de World Bank por padrão. Ele usa os arquivos locais já processados para evitar dependência de rede na reprodução normal.

### Validações

Para validar o estado do pipeline e dos artefatos:

```powershell
python src\validation\validate_pipeline_state.py
python src\validation\validate_project_artifacts.py
python src\validation\validate_reproducibility_contract.py
```

Para regenerar apenas os gráficos preditivos:

```powershell
python src\visualization\generate_predictive_charts.py
```

Para regenerar a avaliação de robustez temporal:

```powershell
python src\models\run_temporal_robustness_evaluation.py
```

O treinamento principal gera:

- `outputs/models/conflict_risk_logistic_regression_pipeline.joblib`
- `outputs/models/conflict_risk_model_features.json`
- `outputs/tables/conflict_risk_model_metrics.csv`
- `outputs/tables/conflict_risk_model_test_predictions.csv`

## Notebooks

### Exploração

- `notebooks/exploration/01_ucdp_country_year_eda.ipynb`

### Modelagem

- `notebooks/modeling/01_baseline_models.ipynb`
- `notebooks/modeling/02_temporal_features_models.ipynb`
- `notebooks/modeling/03_world_bank_features_models.ipynb`
- `notebooks/modeling/04_world_bank_engineered_features_models.ipynb`
- `notebooks/modeling/05_probability_calibration.ipynb`

Os notebooks registram experimentos e análises. O pipeline reproduzível principal está em `src/models/train_conflict_risk_model.py`.

## Fontes utilizadas e consideradas

### Fontes já utilizadas

- UCDP — Uppsala Conflict Data Program
- World Bank Open Data

### Fontes consideradas para expansão futura

- ACLED — Armed Conflict Location & Event Data
- SIPRI — Stockholm International Peace Research Institute
- UNHCR — United Nations High Commissioner for Refugees
- Correlates of War

## Experimentos paralelos em revisão

Arquivos relacionados à Primeira Guerra Mundial foram adicionados pelo grupo e ainda precisam de validação antes de entrarem no pipeline oficial:

- `data/final/world_war_1_details_clean.csv`
- `src/data/wwi_predictive_analysis_scalability_of_conflict.py`
- `src/features/wwi_wwii_build_temporal_generation_wars_deaths.py`
- `src/models/train_model_wars_deaths.py`

Esses arquivos devem ser tratados como experimento paralelo ou material histórico até revisão metodológica, pois ainda não seguem claramente o mesmo fluxo `country-year` do pipeline principal UCDP + World Bank.

## Observação metodológica

O projeto evita tratar a previsão de conflitos como uma previsão determinística. O objetivo é construir uma abordagem exploratória, probabilística e reproduzível, adequada às limitações dos dados históricos e à complexidade do fenômeno analisado.

As saídas do modelo devem ser interpretadas como estimativas experimentais baseadas em padrões históricos e variáveis disponíveis, não como previsões absolutas sobre eventos geopolíticos futuros.
