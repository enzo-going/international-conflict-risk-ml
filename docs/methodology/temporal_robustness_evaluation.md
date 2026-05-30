# Temporal Robustness Evaluation

## Objetivo

Esta avaliação testa se o modelo oficial mantém desempenho competitivo em diferentes janelas temporais, em vez de depender apenas do split consolidado atual.

O pipeline avaliado é o modelo oficial vigente:

- dataset: `data/final/conflict_country_year_world_bank_features.csv`;
- metadados de features: `outputs/models/conflict_risk_model_features.json`;
- unidade de análise: `country-year`;
- target: `target_conflict_next_year`;
- modelo: `SimpleImputer(strategy="median")`, `StandardScaler` e `LogisticRegression(class_weight="balanced")`;
- número de features: 33;
- baseline obrigatória: persistência de conflito, usando `organized_violence_exists`.

## Por que robustez temporal importa

Conflitos organizados têm forte dependência temporal. Um modelo pode parecer competitivo em um único recorte de treino/teste e ainda assim falhar quando avaliado em anos específicos ou períodos históricos diferentes.

Por isso, uma avaliação temporal mais rigorosa precisa verificar se o ganho sobre a baseline de persistência aparece de forma recorrente. A baseline é forte porque muitos conflitos continuam de um ano para o outro; superar essa referência em apenas um split não é evidência suficiente de estabilidade.

## Risco de confiar em um único split

O split oficial atual treina em anos até 2016 e testa em 2017-2023. Esse recorte é metodologicamente adequado por respeitar a ordem temporal, mas ainda concentra a conclusão em uma única janela histórica.

Se alguns anos forem mais fáceis ou mais difíceis de prever, a métrica agregada pode esconder instabilidade anual. Por isso, esta avaliação separa o desempenho por múltiplos cutoffs e compara cada janela contra a persistência.

## Rolling one-year test

No teste rolling anual, cada janela usa todo o histórico disponível até um ano de corte e testa apenas o ano seguinte.

Janelas usadas:

- cutoff 2012, teste 2013;
- cutoff 2013, teste 2014;
- cutoff 2014, teste 2015;
- cutoff 2015, teste 2016;
- cutoff 2016, teste 2017;
- cutoff 2017, teste 2018;
- cutoff 2018, teste 2019;
- cutoff 2019, teste 2020;
- cutoff 2020, teste 2021;
- cutoff 2021, teste 2022;
- cutoff 2022, teste 2023.

Esse desenho é mais sensível a variações ano a ano e ajuda a identificar se o modelo falha em períodos específicos.

## Expanding multi-year holdout

No holdout expansivo, cada janela treina até um cutoff e testa todos os anos posteriores até 2023.

Janelas usadas:

- cutoff 2012, teste 2013-2023;
- cutoff 2013, teste 2014-2023;
- cutoff 2014, teste 2015-2023;
- cutoff 2015, teste 2016-2023;
- cutoff 2016, teste 2017-2023;
- cutoff 2017, teste 2018-2023;
- cutoff 2018, teste 2019-2023.

Esse desenho é menos volátil que o teste anual, pois agrega múltiplos anos em cada avaliação.

## Comparação com baseline de persistência

Em todas as janelas, o modelo é comparado contra:

`y_pred = organized_violence_exists`

A métrica principal de comparação é `f1_difference_vs_persistence`, calculada como:

`F1(modelo) - F1(persistência)`

Valores positivos indicam ganho sobre a baseline. Valores iguais ou negativos indicam que o modelo não melhorou a regra simples de persistência naquela janela.

## Resultados principais

No split oficial reproduzido:

| Métrica | Modelo oficial | Persistência |
|---|---:|---:|
| Accuracy | 0.9197 | 0.9072 |
| Precision | 0.9029 | 0.8571 |
| Recall | 0.8435 | 0.8571 |
| F1-score | 0.8722 | 0.8571 |

O ganho de F1 no split oficial foi:

`+0.0151`

Métricas probabilísticas do modelo no split oficial:

| Métrica | Valor |
|---|---:|
| ROC AUC | 0.9651 |
| Average precision / PR AUC | 0.9482 |
| Brier score | 0.0630 |
| Log loss | 0.2142 |

No rolling one-year test:

| Item | Valor |
|---|---:|
| Janelas avaliadas | 11 |
| Vitórias contra persistência | 8 |
| Empates contra persistência | 1 |
| Derrotas contra persistência | 2 |
| F1 médio do modelo | 0.8639 |
| F1 médio da persistência | 0.8504 |
| Diferença média de F1 | 0.0135 |
| Menor diferença de F1 | -0.0176 |
| Maior diferença de F1 | 0.0393 |

No expanding holdout:

| Item | Valor |
|---|---:|
| Janelas avaliadas | 7 |
| Vitórias contra persistência | 7 |
| Empates contra persistência | 0 |
| Derrotas contra persistência | 0 |
| F1 médio do modelo | 0.8663 |
| F1 médio da persistência | 0.8554 |
| Diferença média de F1 | 0.0109 |
| Menor diferença de F1 | 0.0063 |
| Maior diferença de F1 | 0.0154 |

## O modelo vence de forma estável?

Não em todas as janelas.

O modelo vence a baseline de persistência no split oficial e em todas as janelas de expanding holdout. Porém, no rolling one-year test, há 2 anos em que o modelo fica abaixo da persistência e 1 ano em que empata.

A conclusão metodológica é cautelosa: o modelo mostra ganho agregado e bom comportamento em janelas multi-ano, mas a vantagem anual não é perfeitamente estável. Portanto, a avaliação temporal reforça que o resultado oficial é promissor, mas ainda não deve ser apresentado como evidência forte de superioridade robusta em qualquer período.

## Outputs gerados

Tabelas:

- `outputs/tables/temporal_robustness_one_year.csv`
- `outputs/tables/temporal_robustness_expanding_holdout.csv`
- `outputs/tables/temporal_robustness_official_split.csv`
- `outputs/tables/temporal_robustness_summary.json`

Gráficos:

- `outputs/charts/temporal_robustness/f1_by_test_year.png`
- `outputs/charts/temporal_robustness/f1_gain_vs_persistence_by_year.png`
- `outputs/charts/temporal_robustness/precision_recall_by_year.png`
- `outputs/charts/temporal_robustness/expanding_holdout_f1.png`
- `outputs/charts/temporal_robustness/brier_score_by_year.png`

Script:

- `src/models/run_temporal_robustness_evaluation.py`

## Limitações

- A avaliação usa o mesmo conjunto oficial de 33 features; ela não testa novas fontes externas.
- A baseline de persistência é simples, mas forte para esse domínio.
- O rolling anual pode ser volátil porque cada teste contém apenas um ano.
- As métricas probabilísticas dependem da calibração do modelo, que deve continuar sendo analisada separadamente.
- A avaliação mede associação preditiva histórica, não causalidade.

## Interpretação cautelosa

Esta avaliação não transforma o modelo em um sistema determinístico de previsão geopolítica. O resultado deve ser apresentado como uma análise probabilística e experimental de risco de violência organizada no ano seguinte, respeitando a estrutura `country-year`, o split temporal e a comparação obrigatória contra persistência.
