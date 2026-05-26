# Relatório de Análise Preditiva

Este relatório resume os principais resultados preditivos do modelo principal do projeto International Conflict Risk ML.

## Escopo

Unidade de análise: country-year.

Target: target_conflict_next_year.

Modelo principal: Logistic Regression scaled - World Bank all raw.

## Resumo executivo

- Casos avaliados: 1358
- Países avaliados: 194
- Intervalo temporal de teste: 2017-2023
- Taxa real de conflito no ano seguinte: 0.3247
- Taxa prevista de conflito no ano seguinte: 0.3034
- Probabilidade média prevista: 0.3389
- Falsos positivos: 40
- Falsos negativos: 69

## Métrica principal

- Modelo: Logistic Regression scaled - World Bank all raw
- Accuracy: 0.9197
- Precision: 0.9029
- Recall: 0.8435
- F1-score: 0.8722

- Baseline: Persistence baseline
- Baseline F1-score: 0.8571
- Ganho de F1 vs baseline: 0.0151

## Threshold com melhor F1 na varredura

- Threshold: 0.50
- Precision: 0.9029
- Recall: 0.8435
- F1-score: 0.8722

## Top 10 maiores riscos previstos

| country | year | region | target_conflict_next_year | organized_violence_exists | predicted_conflict_next_year | predicted_conflict_probability | risk_band | prediction_result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DR Congo (Zaire) | 2020 | Africa | 1 | 1 | 1 | 1.0000 | very_high | true_positive |
| DR Congo (Zaire) | 2022 | Africa | 1 | 1 | 1 | 1.0000 | very_high | true_positive |
| DR Congo (Zaire) | 2021 | Africa | 1 | 1 | 1 | 1.0000 | very_high | true_positive |
| Nigeria | 2020 | Africa | 1 | 1 | 1 | 1.0000 | very_high | true_positive |
| DR Congo (Zaire) | 2017 | Africa | 1 | 1 | 1 | 1.0000 | very_high | true_positive |
| DR Congo (Zaire) | 2019 | Africa | 1 | 1 | 1 | 1.0000 | very_high | true_positive |
| Nigeria | 2022 | Africa | 1 | 1 | 1 | 1.0000 | very_high | true_positive |
| DR Congo (Zaire) | 2018 | Africa | 1 | 1 | 1 | 1.0000 | very_high | true_positive |
| DR Congo (Zaire) | 2023 | Africa | 1 | 1 | 1 | 1.0000 | very_high | true_positive |
| Nigeria | 2019 | Africa | 1 | 1 | 1 | 1.0000 | very_high | true_positive |

## Resumo por região

| region | cases | countries | actual_positive_rate | predicted_positive_rate | mean_predicted_probability | f1_score |
| --- | --- | --- | --- | --- | --- | --- |
| Middle East | 105 | 15 | 0.5619 | 0.5619 | 0.5961 | 0.9153 |
| Africa | 371 | 53 | 0.5553 | 0.5256 | 0.5537 | 0.8778 |
| Americas | 245 | 35 | 0.2776 | 0.2531 | 0.2824 | 0.8615 |
| Asia | 301 | 43 | 0.2359 | 0.2193 | 0.2737 | 0.8759 |
| Europe | 336 | 48 | 0.1101 | 0.0893 | 0.1207 | 0.7761 |

## Principais falsos positivos

| country | year | region | target_conflict_next_year | organized_violence_exists | predicted_conflict_next_year | predicted_conflict_probability | risk_band | prediction_result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Rwanda | 2022 | Africa | 0 | 1 | 1 | 0.9657 | very_high | false_positive |
| Tanzania | 2022 | Africa | 0 | 1 | 1 | 0.9483 | very_high | false_positive |
| Egypt | 2023 | Middle East | 0 | 1 | 1 | 0.9375 | very_high | false_positive |
| Congo | 2020 | Africa | 0 | 1 | 1 | 0.9143 | very_high | false_positive |
| Congo | 2017 | Africa | 0 | 1 | 1 | 0.8973 | very_high | false_positive |
| Tunisia | 2023 | Africa | 0 | 1 | 1 | 0.8887 | very_high | false_positive |
| Lebanon | 2018 | Middle East | 0 | 1 | 1 | 0.8799 | very_high | false_positive |
| Azerbaijan | 2023 | Europe | 0 | 1 | 1 | 0.8746 | very_high | false_positive |
| China | 2017 | Asia | 0 | 1 | 1 | 0.8733 | very_high | false_positive |
| Peru | 2017 | Americas | 0 | 1 | 1 | 0.8653 | very_high | false_positive |

## Principais falsos negativos

| country | year | region | target_conflict_next_year | organized_violence_exists | predicted_conflict_next_year | predicted_conflict_probability | risk_band | prediction_result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Liberia | 2019 | Africa | 1 | 1 | 0 | 0.4919 | moderate | false_negative |
| Congo | 2018 | Africa | 1 | 0 | 0 | 0.4903 | moderate | false_negative |
| Peru | 2018 | Americas | 1 | 0 | 0 | 0.4856 | moderate | false_negative |
| Rwanda | 2020 | Africa | 1 | 0 | 0 | 0.4762 | moderate | false_negative |
| Lebanon | 2019 | Middle East | 1 | 0 | 0 | 0.4490 | moderate | false_negative |
| Rwanda | 2023 | Africa | 1 | 0 | 0 | 0.4455 | moderate | false_negative |
| Ghana | 2022 | Africa | 1 | 1 | 0 | 0.4365 | moderate | false_negative |
| France | 2023 | Europe | 1 | 1 | 0 | 0.4143 | moderate | false_negative |
| Zimbabwe (Rhodesia) | 2018 | Africa | 1 | 1 | 0 | 0.4114 | moderate | false_negative |
| Haiti | 2017 | Americas | 1 | 1 | 0 | 0.4023 | moderate | false_negative |

## Interpretação

O modelo deve ser interpretado como um sistema experimental de estimativa de risco, não como previsão determinística de eventos geopolíticos.

A análise de falsos positivos e falsos negativos é essencial para avaliar onde o modelo superestima ou subestima risco.

O resultado mais relevante não é apenas o ranking de risco, mas a comparação entre baseline, modelo principal, thresholds e erros.
