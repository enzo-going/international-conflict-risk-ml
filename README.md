# International Conflict Risk ML

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

Após a expansão dos indicadores do World Bank, o modelo principal foi reexecutado com 69 features.

| Modelo | Accuracy | Precision | Recall | F1-score |
|---|---:|---:|---:|---:|
| Persistence baseline | 0.9072 | 0.8571 | 0.8571 | 0.8571 |
| Logistic Regression + World Bank all raw | 0.9197 | 0.9029 | 0.8435 | 0.8722 |

O modelo principal atual supera a baseline de persistência, com ganho aproximado de:

`+0.0151` em F1-score.

O melhor resultado histórico anterior era `0.8711`. Após a análise de ablação, o melhor conjunto passou a ser `World Bank all raw`, com F1-score de `0.8722`.

Esse resultado é metodologicamente relevante porque mostra que mais features nem sempre significam melhor desempenho. A análise de ablação indicou que os indicadores brutos completos do World Bank funcionaram melhor do que o conjunto com todas as features derivadas.

## Status atual

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
- [ ] Testar modelos adicionais, como Gradient Boosting e MLP
- [ ] Avaliar seleção de features e impacto individual dos indicadores World Bank

## Como reproduzir o modelo principal

Instale as dependências:

```powershell
pip install -r requirements.txt
```

Execute o pipeline principal em ordem:

```powershell
python src\data\prepare_ucdp_organized_violence.py
python src\data\build_conflict_country_year_base.py
python src\features\build_temporal_features.py
python src\data\prepare_world_bank_indicators.py
python src\data\build_conflict_country_year_world_bank.py
python src\features\build_world_bank_features.py
python src\models\train_conflict_risk_model.py
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
- `src/features/wwi_build_temporal_features.py`
- `src/models/train_wwi_model.py`

Esses arquivos devem ser tratados como experimento paralelo ou material histórico até revisão metodológica, pois ainda não seguem claramente o mesmo fluxo `country-year` do pipeline principal UCDP + World Bank.

## Observação metodológica

O projeto evita tratar a previsão de conflitos como uma previsão determinística. O objetivo é construir uma abordagem exploratória, probabilística e reproduzível, adequada às limitações dos dados históricos e à complexidade do fenômeno analisado.

As saídas do modelo devem ser interpretadas como estimativas experimentais baseadas em padrões históricos e variáveis disponíveis, não como previsões absolutas sobre eventos geopolíticos futuros.