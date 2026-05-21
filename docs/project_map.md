# Mapa do Projeto

Este documento organiza a estrutura atual do repositório e diferencia o pipeline principal dos experimentos paralelos.

## Pipeline principal atual

O pipeline oficial do projeto utiliza:

- UCDP Organized Violence Country-Year como base central;
- World Bank como fonte socioeconômica externa;
- estrutura de análise `country-year`;
- target supervisionado `target_conflict_next_year`;
- split temporal para avaliação;
- modelo principal reproduzível em `src/models/train_conflict_risk_model.py`.

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

## Documentação metodológica

Arquivos principais:

- `docs/project_scope.md`
- `docs/data_inventory.md`
- `docs/methodology/data_cleaning_protocol.md`
- `docs/methodology/ucdp_organized_violence_notes.md`
- `docs/methodology/modeling_notes.md`
- `docs/methodology/model_training_pipeline.md`
- `docs/references/world_bank_indicators.md`

## Experimentos paralelos / em revisão

Os seguintes arquivos foram adicionados posteriormente pelo grupo e ainda precisam de validação antes de entrarem no pipeline oficial:

- `data/final/world_war_1_details_clean.csv`
- `src/data/wwi_predictive_analysis_scalability_of_conflict.py`
- `src/features/wwi_build_temporal_features.py`
- `src/models/train_wwi_model.py`

Observação: o dataset WWI e os scripts WWI ainda parecem usar estruturas de colunas diferentes. Portanto, devem ser tratados como experimento paralelo ou material histórico até revisão.

## Próximas prioridades

1. Reexecutar o modelo principal após a segunda leva de indicadores World Bank.
2. Atualizar `README.md` com o estado real do projeto.
3. Validar ou reorganizar os arquivos WWI adicionados pelo grupo.
4. Atualizar o dashboard se houver novo resultado relevante.
5. Só depois testar novos algoritmos, como Gradient Boosting ou MLP.
