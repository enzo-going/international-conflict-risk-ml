# Avaliação Preditiva por País

Este relatório traduz as probabilidades do modelo principal em uma análise preditiva por país.

## Escopo

- Ano-base analisado: 2023
- Ano previsto: 2024
- Unidade de análise: country-year
- Target: target_conflict_next_year
- Modelo principal: Logistic Regression scaled - World Bank all raw

## Observação metodológica

As probabilidades abaixo são estimativas experimentais do modelo, não previsões determinísticas.

A formulação correta é: o modelo estimou determinada probabilidade de ocorrência de violência organizada no ano seguinte, considerando o padrão aprendido nos dados históricos.

## Resumo executivo

- Países avaliados: 194
- Probabilidade média estimada: 0.3427
- Países classificados como risco alto ou muito alto: 59
- Países com previsão positiva pelo threshold atual: 60
- Países com conflito observado no ano previsto: 58

## Distribuição por faixa de risco

| risk_level | risk_level_description | countries | mean_probability | min_probability | max_probability | predicted_positive_count | actual_positive_count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| very_high | risco muito alto | 54 | 0.9507 | 0.8042 | 1.0000 | 54 | 48 |
| high | risco alto | 5 | 0.7183 | 0.6173 | 0.7946 | 5 | 3 |
| moderate | risco moderado | 4 | 0.4678 | 0.4143 | 0.5361 | 1 | 3 |
| low | risco baixo | 11 | 0.2716 | 0.2059 | 0.3759 | 0 | 0 |
| very_low | risco muito baixo | 120 | 0.0558 | 0.0009 | 0.1976 | 0 | 4 |

## Top 25 países com maior risco estimado

| country | region | forecast_year | predicted_probability_percent | risk_level_description | predicted_conflict_next_year | target_conflict_next_year | prediction_result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DR Congo (Zaire) | Africa | 2024 | 100.0% | risco muito alto | 1 | 1 | true_positive |
| Nigeria | Africa | 2024 | 100.0% | risco muito alto | 1 | 1 | true_positive |
| Brazil | Americas | 2024 | 100.0% | risco muito alto | 1 | 1 | true_positive |
| Ukraine | Europe | 2024 | 100.0% | risco muito alto | 1 | 1 | true_positive |
| Mexico | Americas | 2024 | 100.0% | risco muito alto | 1 | 1 | true_positive |
| Sudan | Africa | 2024 | 100.0% | risco muito alto | 1 | 1 | true_positive |
| India | Asia | 2024 | 100.0% | risco muito alto | 1 | 1 | true_positive |
| Colombia | Americas | 2024 | 100.0% | risco muito alto | 1 | 1 | true_positive |
| Mali | Africa | 2024 | 100.0% | risco muito alto | 1 | 1 | true_positive |
| Myanmar (Burma) | Asia | 2024 | 100.0% | risco muito alto | 1 | 1 | true_positive |
| Ethiopia | Africa | 2024 | 100.0% | risco muito alto | 1 | 1 | true_positive |
| Syria | Middle East | 2024 | 100.0% | risco muito alto | 1 | 1 | true_positive |
| Pakistan | Asia | 2024 | 100.0% | risco muito alto | 1 | 1 | true_positive |
| Cameroon | Africa | 2024 | 100.0% | risco muito alto | 1 | 1 | true_positive |
| Ecuador | Americas | 2024 | 100.0% | risco muito alto | 1 | 1 | true_positive |
| Somalia | Africa | 2024 | 100.0% | risco muito alto | 1 | 1 | true_positive |
| Niger | Africa | 2024 | 100.0% | risco muito alto | 1 | 1 | true_positive |
| Afghanistan | Asia | 2024 | 99.9% | risco muito alto | 1 | 1 | true_positive |
| Philippines | Asia | 2024 | 99.8% | risco muito alto | 1 | 1 | true_positive |
| Haiti | Americas | 2024 | 99.8% | risco muito alto | 1 | 1 | true_positive |
| Central African Republic | Africa | 2024 | 99.8% | risco muito alto | 1 | 1 | true_positive |
| South Sudan | Africa | 2024 | 99.8% | risco muito alto | 1 | 1 | true_positive |
| Israel | Middle East | 2024 | 99.8% | risco muito alto | 1 | 1 | true_positive |
| Burkina Faso | Africa | 2024 | 99.7% | risco muito alto | 1 | 1 | true_positive |
| Russia (Soviet Union) | Europe | 2024 | 99.5% | risco muito alto | 1 | 1 | true_positive |

_Exibindo 25 de 194 registros._

## Exemplos de interpretação

- Para o ano-base 2023, o modelo estimou 100.0% de probabilidade de violência organizada em 2024 para DR Congo (Zaire) (risco muito alto).
- Para o ano-base 2023, o modelo estimou 100.0% de probabilidade de violência organizada em 2024 para Nigeria (risco muito alto).
- Para o ano-base 2023, o modelo estimou 100.0% de probabilidade de violência organizada em 2024 para Brazil (risco muito alto).
- Para o ano-base 2023, o modelo estimou 100.0% de probabilidade de violência organizada em 2024 para Ukraine (risco muito alto).
- Para o ano-base 2023, o modelo estimou 100.0% de probabilidade de violência organizada em 2024 para Mexico (risco muito alto).

## Falsos negativos no ano previsto

| country | region | forecast_year | predicted_probability_percent | risk_level_description | predicted_conflict_next_year | target_conflict_next_year | prediction_result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Rwanda | Africa | 2024 | 44.5% | risco moderado | 0 | 1 | false_negative |
| France | Europe | 2024 | 41.4% | risco moderado | 0 | 1 | false_negative |
| Liberia | Africa | 2024 | 19.8% | risco muito baixo | 0 | 1 | false_negative |
| Gambia | Africa | 2024 | 10.5% | risco muito baixo | 0 | 1 | false_negative |
| Jordan | Middle East | 2024 | 9.3% | risco muito baixo | 0 | 1 | false_negative |
| Germany | Europe | 2024 | 4.7% | risco muito baixo | 0 | 1 | false_negative |

## Falsos positivos no ano previsto

| country | region | forecast_year | predicted_probability_percent | risk_level_description | predicted_conflict_next_year | target_conflict_next_year | prediction_result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Egypt | Middle East | 2024 | 93.7% | risco muito alto | 1 | 0 | false_positive |
| Tunisia | Africa | 2024 | 88.9% | risco muito alto | 1 | 0 | false_positive |
| Azerbaijan | Europe | 2024 | 87.5% | risco muito alto | 1 | 0 | false_positive |
| Armenia | Europe | 2024 | 85.2% | risco muito alto | 1 | 0 | false_positive |
| Peru | Americas | 2024 | 82.9% | risco muito alto | 1 | 0 | false_positive |
| Saudi Arabia | Middle East | 2024 | 81.2% | risco muito alto | 1 | 0 | false_positive |
| China | Asia | 2024 | 79.5% | risco alto | 1 | 0 | false_positive |
| Kingdom of eSwatini (Swaziland) | Africa | 2024 | 72.7% | risco alto | 1 | 0 | false_positive |

## Conclusão

Esta camada transforma a saída probabilística do modelo em avaliação preditiva interpretável por país.

Ela complementa as métricas globais, porque permite observar quais países receberam maior risco estimado, quais faixas de risco concentram mais casos e onde o modelo errou no ano previsto.
