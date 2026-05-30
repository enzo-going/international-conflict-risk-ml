# Mapa do Projeto

Este documento organiza a estrutura atual do repositório e diferencia o pipeline principal dos experimentos paralelos.

## Pipeline principal atual

O pipeline oficial do projeto utiliza:

- UCDP Organized Violence Country-Year como base central;
- World Bank como fonte socioeconômica externa;
- features temporais derivadas do histórico de conflito;
- estrutura de análise `country-year`;
- target supervisionado `target_conflict_next_year`;
- split temporal para avaliação;
- modelo principal reproduzível em `src/models/train_conflict_risk_model.py`;
- Logistic Regression com 33 features como configuração oficial atual.

Resultado oficial atual:

- Persistence baseline: F1-score `0.8571`;
- Logistic Regression scaled - World Bank all raw: F1-score `0.8722`;
- ganho aproximado sobre a persistência: `+0.0151`.

Esse ganho é moderado/pequeno e deve ser interpretado com cautela. O projeto não deve ser apresentado como previsão determinística de guerra mundial ou de eventos geopolíticos específicos.

## Fluxo principal de dados

Ordem atual dos principais scripts:

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
   - compara contra baseline de persistência;
   - salva métricas, predições, metadados e modelo treinado.

8. `src/models/train_candidate_models.py`
   - compara modelos candidatos;
   - avalia Logistic Regression, Random Forest, Gradient Boosting e MLP;
   - salva `outputs/tables/candidate_model_comparison.csv`.

9. `src/data/build_sqlite_database.py`
   - gera o banco SQLite local;
   - carrega features, predições, métricas, coeficientes e comparação de modelos;
   - usa o schema definido em `sql/schema.sql`.

## Datasets principais

### `data/raw/`

Dados brutos preservados.

- `data/raw/ucdp/organizedviolencecy_v25_1.xlsx`
- `data/raw/world_bank/*.json`

### `data/processed/`

Dados padronizados intermediários.

- `data/processed/ucdp_organized_violence_country_year.csv`
- `data/processed/world_bank/world_bank_country_year_indicators.csv`

### `data/interim/`

Arquivos auxiliares de integração.

- `country_name_mapping_candidates.csv`
- `country_name_mapping_reviewed.csv`

### `data/final/`

Datasets finais usados em análise e modelagem.

- `conflict_country_year_base.csv`
- `conflict_country_year_temporal.csv`
- `conflict_country_year_world_bank.csv`
- `conflict_country_year_world_bank_features.csv`

## Notebooks

### Exploração

- `notebooks/exploration/01_ucdp_country_year_eda.ipynb`

### Modelagem

- `notebooks/modeling/01_baseline_models.ipynb`
- `notebooks/modeling/02_temporal_features_models.ipynb`
- `notebooks/modeling/03_world_bank_features_models.ipynb`
- `notebooks/modeling/04_world_bank_engineered_features_models.ipynb`
- `notebooks/modeling/05_probability_calibration.ipynb`

Os notebooks documentam experimentos e análises. O pipeline principal reproduzível está em `src/models/train_conflict_risk_model.py`.

## Outputs principais

### `outputs/tables/`

Contém métricas, resultados de experimentos, thresholds e predições.

Arquivos importantes:

- `conflict_risk_model_metrics.csv`
- `conflict_risk_model_test_predictions.csv`
- `conflict_risk_model_coefficients.csv`
- `candidate_model_comparison.csv`
- `world_bank_ablation_results.csv`
- `probability_threshold_results.csv`
- `probability_calibration_bins.csv`

### `outputs/models/`

Contém o modelo principal treinado e metadados.

- `conflict_risk_logistic_regression_pipeline.joblib`
- `conflict_risk_model_features.json`

## Dashboard

O dashboard HTML está em:

`docs/index.html`

Página publicada:

`https://enzo-going.github.io/international-conflict-risk-ml/`

Ele funciona como camada visual de acompanhamento e apresentação do projeto.

Arquivos relacionados:

- `docs/index.html`
- `docs/assets/styles.css`
- `docs/assets/dashboard.js`


## Camada SQL e SQLite

A camada SQL está em:

- `sql/schema.sql`
- `sql/README.md`
- `sql/queries/`

O banco local é gerado em:

- `data/database/conflict_risk_ml.sqlite`

Esse arquivo `.sqlite` não é versionado no Git, pois pode ser reproduzido a partir dos CSVs e scripts do projeto.

Tabelas principais do banco:

- `country_year_features`
- `model_predictions`
- `model_metrics`
- `model_coefficients`
- `candidate_model_comparison`
- `dataset_metadata`

Consultas SQL principais:

- `01_highest_predicted_risk.sql`
- `02_false_positives.sql`
- `03_false_negatives.sql`
- `04_top_model_coefficients.sql`
- `05_model_metrics.sql`
- `06_candidate_model_comparison.sql`

## Documentação metodológica

Arquivos principais:

- `docs/project_scope.md`
- `docs/data_inventory.md`
- `docs/methodology/data_cleaning_protocol.md`
- `docs/methodology/ucdp_organized_violence_notes.md`
- `docs/methodology/modeling_notes.md`
- `docs/methodology/model_training_pipeline.md`
- `docs/methodology/final_methodological_summary.md`
- `docs/methodology/one_sided_experimental_module_review.md`
- `docs/database/database_design.md`
- `docs/references/world_bank_indicators.md`

## Experimentos paralelos / em revisão

Os seguintes arquivos foram adicionados posteriormente pelo grupo e ainda precisam de validação antes de entrarem no pipeline oficial:

- `data/final/world_war_1_details_clean.csv`
- `src/data/wwi_predictive_analysis_scalability_of_conflict.py`
- `src/features/wwi_build_temporal_features.py`
- `src/models/train_wwi_model.py`

Observação: o dataset WWI e os scripts WWI ainda parecem usar estruturas de colunas diferentes. Portanto, devem ser tratados como experimento paralelo ou material histórico até revisão.

## Análise preditiva por país

Scripts:

- `src/analysis/generate_country_risk_assessment.py`
- `src/analysis/generate_country_risk_explanations.py`

Outputs:

- `outputs/tables/country_risk_assessment_latest_year.csv`
- `outputs/tables/country_risk_assessment_summary.json`
- `outputs/tables/country_risk_level_summary.csv`
- `outputs/tables/country_risk_explanations_latest_year.csv`
- `outputs/tables/country_risk_explanation_group_summary.csv`
- `outputs/tables/country_risk_explanation_summary.json`
- `reports/final/country_risk_assessment_latest_year.md`
- `reports/final/country_risk_explanations_latest_year.md`

Função:

- traduzir probabilidades do modelo em faixas de risco;
- gerar frases interpretáveis por país;
- cruzar probabilidades, features, coeficientes e grupos de variáveis;
- apoiar a apresentação do projeto como sistema de análise preditiva.

## Auditoria de integração de datasets

A auditoria automática de datasets está em:

- `src/validation/audit_dataset_integration.py`

Outputs gerados:

- `outputs/tables/dataset_integration_audit.csv`
- `outputs/tables/dataset_integration_summary.json`
- `reports/final/dataset_integration_audit.md`
- `reports/final/project_consolidation_review.md`

Função da auditoria:

- listar todos os datasets presentes nas camadas `raw`, `interim`, `processed` e `final`;
- detectar colunas relacionadas a país, ano, data, evento e ator;
- estimar a unidade de análise de cada arquivo;
- classificar cada fonte como oficial, experimental, dado bruto de suporte ou não pronta;
- evitar integração desorganizada de datasets adicionados pelo grupo.

Resumo atual:

- total de datasets auditados: 35;
- oficiais ou candidatos ao pipeline: 12;
- experimentais em revisão: 4;
- dados brutos preservados: 16;
- não prontos para integração direta: 3.

## Validação automática

O projeto possui uma camada de validação em:

- `src/validation/validate_project_artifacts.py`

Esse script verifica:

- existência dos principais arquivos do projeto;
- schemas dos CSVs principais;
- métricas do modelo principal;
- metadados das features;
- artefatos do módulo experimental One-Sided Violence.

Outputs gerados:

- `outputs/tables/project_validation_report.csv`
- `outputs/tables/project_validation_summary.json`

## Próximas prioridades

1. Refinar a seleção de features do modelo principal.
2. Testar novas fontes externas de dados além do World Bank.
3. Avaliar modelos candidatos com validação mais robusta e análise de estabilidade.
4. Atualizar o dashboard quando houver novo ganho metodológico ou resultado relevante.
5. Validar ou reorganizar os arquivos WWI adicionados pelo grupo antes de integrá-los ao pipeline oficial.

## Separação entre oficial e experimental

### Oficial

- UCDP Organized Violence Country-Year;
- features temporais de conflito;
- indicadores World Bank integrados em estrutura `country-year`;
- Logistic Regression scaled - World Bank all raw com 33 features;
- baseline de persistência como comparação obrigatória.

### Experimental, paralelo ou candidato

- SIPRI: fonte candidata/apoio; ainda não integra o modelo principal.
- PRIO: fonte candidata; ainda não há integração oficial consolidada no pipeline principal.
- WWI/WWII: módulo histórico experimental com granularidade e target diferentes.
- One-sided violence: módulo experimental complementar, separado das variáveis one-sided já existentes no dataset UCDP principal.
- Shock features: experimento adicional; não superou o modelo oficial atual.
- Global inflation: feature/fonte de suporte ou experimento, não resultado principal separado.

Esses módulos podem apoiar discussão acadêmica e evolução futura, mas não devem ser vendidos como resultado principal do pipeline oficial atual.

## Módulo experimental WWI/WWII

O projeto possui um módulo experimental relacionado à análise histórica de mortes e escalada em guerras mundiais.

Documento de revisão:

- `docs/methodology/war_deaths_experimental_module_review.md`

Arquivos relacionados:

- `data/final/world_war_1_details_clean.csv`
- `data/final/world_war_2_clean.csv`
- `src/data/wwi_predictive_analysis_scalability_of_conflict.py`
- `src/features/build_temporal_generation_wars_deaths.py`
- `src/features/build_features_wars_deaths.py`
- `src/models/train_model_wars_deaths.py`

Status: experimental. Não integra o pipeline principal `country-year`.
