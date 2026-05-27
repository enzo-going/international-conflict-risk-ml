# Explicações Preditivas por País

Este relatório complementa a avaliação preditiva por país com explicações aproximadas baseadas nas features usadas pelo modelo.

## Escopo

- Ano-base: 2023
- Ano previsto: 2024
- Países avaliados: 194
- Modelo principal: Logistic Regression scaled - World Bank all raw

## Observação metodológica

As explicações são aproximações baseadas nos coeficientes do modelo e na posição relativa das features no ano-base analisado.

Elas indicam associação estatística no modelo, não causalidade direta.

Como o modelo usa padronização interna, os sinais calculados aqui devem ser lidos como apoio interpretativo, não como decomposição exata do logit.

## Resumo por grupo de variáveis

| feature_group | feature_group_label | mean_signal | mean_absolute_signal | total_absolute_signal | feature_count | country_count |
| --- | --- | --- | --- | --- | --- | --- |
| ucdp_conflict | histórico e intensidade de conflitos UCDP | 0.0948 | 0.1375 | 400.1219 | 15 | 194 |
| temporal_conflict | persistência temporal de conflito | 0.0388 | 0.1449 | 196.8006 | 7 | 194 |
| world_bank | indicadores socioeconômicos World Bank | -0.0041 | 0.0533 | 103.4175 | 10 | 194 |
| time_index | tendência temporal geral | 0.0000 | 0.0000 | 0.0000 | 1 | 194 |

## Top 25 países por risco estimado e grupos explicativos

| country | region | forecast_year | predicted_probability_percent | risk_level_description | top_positive_factors | top_negative_factors | prediction_result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DR Congo (Zaire) | Africa | 2024 | 100.0% | risco muito alto | quantidade de díades de violência unilateral; quantidade de díades de conflito estatal; quantidade de díades de conflito não estatal | existência de conflito estatal no ano-base; existência de conflito não estatal; existência de violência unilateral | true_positive |
| Nigeria | Africa | 2024 | 100.0% | risco muito alto | quantidade de díades de conflito não estatal; quantidade de díades de violência unilateral; quantidade de díades de conflito estatal | existência de conflito estatal no ano-base; existência de conflito não estatal; existência de violência unilateral | true_positive |
| Brazil | Americas | 2024 | 100.0% | risco muito alto | quantidade de díades de conflito não estatal; quantidade de díades de violência unilateral; frequência de conflito nos últimos 5 anos | existência de conflito não estatal; existência de violência unilateral; mortes estimadas em conflitos não estatais | true_positive |
| Ukraine | Europe | 2024 | 100.0% | risco muito alto | mortes estimadas em conflitos interestatais; frequência de conflito nos últimos 5 anos; existência de violência organizada no ano-base | crescimento populacional anual; existência de conflito estatal no ano-base; existência de conflito interestatal | true_positive |
| Mexico | Americas | 2024 | 100.0% | risco muito alto | quantidade de díades de conflito não estatal; frequência de conflito nos últimos 5 anos; existência de violência organizada no ano-base | mortes estimadas em conflitos não estatais; existência de conflito não estatal; mortes acumuladas nos últimos 5 anos | true_positive |
| Sudan | Africa | 2024 | 100.0% | risco muito alto | quantidade de díades de conflito não estatal; frequência de conflito nos últimos 5 anos; quantidade de díades de conflito estatal | existência de conflito estatal no ano-base; existência de conflito não estatal; existência de violência unilateral | true_positive |
| India | Asia | 2024 | 100.0% | risco muito alto | quantidade de díades de conflito estatal; quantidade de díades de violência unilateral; frequência de conflito nos últimos 5 anos | existência de conflito estatal no ano-base; existência de conflito interestatal; existência de conflito não estatal | true_positive |
| Colombia | Americas | 2024 | 100.0% | risco muito alto | quantidade de díades de violência unilateral; quantidade de díades de conflito não estatal; quantidade de díades de conflito estatal | existência de conflito estatal no ano-base; existência de conflito não estatal; existência de violência unilateral | true_positive |
| Mali | Africa | 2024 | 100.0% | risco muito alto | quantidade de díades de conflito não estatal; quantidade de díades de violência unilateral; quantidade de díades de conflito estatal | existência de conflito estatal no ano-base; existência de conflito não estatal; existência de violência unilateral | true_positive |
| Myanmar (Burma) | Asia | 2024 | 100.0% | risco muito alto | quantidade de díades de conflito estatal; frequência de conflito nos últimos 5 anos; quantidade de díades de violência unilateral | existência de conflito estatal no ano-base; existência de violência unilateral; mortes estimadas em conflitos intraestatais | true_positive |
| Ethiopia | Africa | 2024 | 100.0% | risco muito alto | quantidade de díades de conflito não estatal; quantidade de díades de conflito estatal; frequência de conflito nos últimos 5 anos | mortes acumuladas nos últimos 5 anos; existência de conflito estatal no ano-base; existência de conflito não estatal | true_positive |
| Syria | Middle East | 2024 | 100.0% | risco muito alto | quantidade de díades de conflito estatal; quantidade de díades de conflito não estatal; quantidade de díades de violência unilateral | existência de conflito estatal no ano-base; existência de conflito interestatal; existência de conflito não estatal | true_positive |
| Pakistan | Asia | 2024 | 100.0% | risco muito alto | quantidade de díades de conflito estatal; quantidade de díades de violência unilateral; frequência de conflito nos últimos 5 anos | existência de conflito estatal no ano-base; existência de conflito interestatal; existência de conflito não estatal | true_positive |
| Cameroon | Africa | 2024 | 100.0% | risco muito alto | quantidade de díades de conflito estatal; quantidade de díades de violência unilateral; quantidade de díades de conflito não estatal | existência de conflito estatal no ano-base; existência de conflito não estatal; existência de violência unilateral | true_positive |
| Ecuador | Americas | 2024 | 100.0% | risco muito alto | quantidade de díades de conflito não estatal; frequência de conflito nos últimos 5 anos; existência de violência organizada no ano-base | existência de conflito não estatal; crescimento populacional anual; mortes estimadas em conflitos não estatais | true_positive |
| Somalia | Africa | 2024 | 100.0% | risco muito alto | quantidade de díades de conflito não estatal; frequência de conflito nos últimos 5 anos; quantidade de díades de violência unilateral | existência de conflito estatal no ano-base; existência de conflito não estatal; existência de violência unilateral | true_positive |
| Niger | Africa | 2024 | 100.0% | risco muito alto | quantidade de díades de conflito estatal; frequência de conflito nos últimos 5 anos; quantidade de díades de violência unilateral | existência de conflito estatal no ano-base; existência de conflito não estatal; existência de violência unilateral | true_positive |
| Afghanistan | Asia | 2024 | 99.9% | risco muito alto | quantidade de díades de conflito estatal; frequência de conflito nos últimos 5 anos; existência de violência organizada no ano-base | existência de conflito estatal no ano-base; existência de conflito interestatal; mortes acumuladas nos últimos 5 anos | true_positive |
| Philippines | Asia | 2024 | 99.8% | risco muito alto | quantidade de díades de conflito estatal; frequência de conflito nos últimos 5 anos; quantidade de díades de violência unilateral | existência de conflito estatal no ano-base; existência de violência unilateral; crescimento anual do PIB | true_positive |
| Haiti | Americas | 2024 | 99.8% | risco muito alto | quantidade de díades de violência unilateral; frequência de conflito nos últimos 5 anos; existência de violência organizada no ano-base | existência de conflito não estatal; existência de violência unilateral; desemprego | true_positive |
| Central African Republic | Africa | 2024 | 99.8% | risco muito alto | quantidade de díades de conflito estatal; frequência de conflito nos últimos 5 anos; quantidade de díades de violência unilateral | existência de conflito estatal no ano-base; existência de conflito não estatal; existência de violência unilateral | true_positive |
| South Sudan | Africa | 2024 | 99.8% | risco muito alto | quantidade de díades de conflito não estatal; frequência de conflito nos últimos 5 anos; existência de violência organizada no ano-base | existência de conflito estatal no ano-base; existência de conflito não estatal; existência de violência unilateral | true_positive |
| Israel | Middle East | 2024 | 99.8% | risco muito alto | quantidade de díades de conflito estatal; frequência de conflito nos últimos 5 anos; existência de violência organizada no ano-base | mortes estimadas em conflitos intraestatais; existência de conflito estatal no ano-base; PIB per capita | true_positive |
| Burkina Faso | Africa | 2024 | 99.7% | risco muito alto | frequência de conflito nos últimos 5 anos; quantidade de díades de violência unilateral; quantidade de díades de conflito estatal | existência de conflito estatal no ano-base; existência de conflito não estatal; existência de violência unilateral | true_positive |
| Russia (Soviet Union) | Europe | 2024 | 99.5% | risco muito alto | quantidade de díades de conflito estatal; frequência de conflito nos últimos 5 anos; existência de violência organizada no ano-base | existência de conflito estatal no ano-base; existência de conflito interestatal; crescimento populacional anual | true_positive |

_Exibindo 25 de 194 registros._

## Exemplos de explicação textual

- **DR Congo (Zaire): 100.0% de risco estimado para 2024, classificado como risco muito alto.**
  - Para DR Congo (Zaire), o modelo estimou 100.0% de probabilidade de violência organizada em 2024, classificando o caso como risco muito alto. Os principais grupos associados à estimativa foram: histórico e intensidade de conflitos UCDP; persistência temporal de conflito; indicadores socioeconômicos World Bank. Sinais que elevaram a estimativa: quantidade de díades de violência unilateral; quantidade de díades de conflito estatal; quantidade de díades de conflito não estatal. Sinais que reduziram a estimativa no modelo: existência de conflito estatal no ano-base; existência de conflito não estatal; existência de violência unilateral.

- **Nigeria: 100.0% de risco estimado para 2024, classificado como risco muito alto.**
  - Para Nigeria, o modelo estimou 100.0% de probabilidade de violência organizada em 2024, classificando o caso como risco muito alto. Os principais grupos associados à estimativa foram: histórico e intensidade de conflitos UCDP; persistência temporal de conflito; indicadores socioeconômicos World Bank. Sinais que elevaram a estimativa: quantidade de díades de conflito não estatal; quantidade de díades de violência unilateral; quantidade de díades de conflito estatal. Sinais que reduziram a estimativa no modelo: existência de conflito estatal no ano-base; existência de conflito não estatal; existência de violência unilateral.

- **Brazil: 100.0% de risco estimado para 2024, classificado como risco muito alto.**
  - Para Brazil, o modelo estimou 100.0% de probabilidade de violência organizada em 2024, classificando o caso como risco muito alto. Os principais grupos associados à estimativa foram: histórico e intensidade de conflitos UCDP; persistência temporal de conflito; indicadores socioeconômicos World Bank. Sinais que elevaram a estimativa: quantidade de díades de conflito não estatal; quantidade de díades de violência unilateral; frequência de conflito nos últimos 5 anos. Sinais que reduziram a estimativa no modelo: existência de conflito não estatal; existência de violência unilateral; mortes estimadas em conflitos não estatais.

- **Ukraine: 100.0% de risco estimado para 2024, classificado como risco muito alto.**
  - Para Ukraine, o modelo estimou 100.0% de probabilidade de violência organizada em 2024, classificando o caso como risco muito alto. Os principais grupos associados à estimativa foram: histórico e intensidade de conflitos UCDP; persistência temporal de conflito; indicadores socioeconômicos World Bank. Sinais que elevaram a estimativa: mortes estimadas em conflitos interestatais; frequência de conflito nos últimos 5 anos; existência de violência organizada no ano-base. Sinais que reduziram a estimativa no modelo: crescimento populacional anual; existência de conflito estatal no ano-base; existência de conflito interestatal.

- **Mexico: 100.0% de risco estimado para 2024, classificado como risco muito alto.**
  - Para Mexico, o modelo estimou 100.0% de probabilidade de violência organizada em 2024, classificando o caso como risco muito alto. Os principais grupos associados à estimativa foram: histórico e intensidade de conflitos UCDP; persistência temporal de conflito; indicadores socioeconômicos World Bank. Sinais que elevaram a estimativa: quantidade de díades de conflito não estatal; frequência de conflito nos últimos 5 anos; existência de violência organizada no ano-base. Sinais que reduziram a estimativa no modelo: mortes estimadas em conflitos não estatais; existência de conflito não estatal; mortes acumuladas nos últimos 5 anos.

- **Sudan: 100.0% de risco estimado para 2024, classificado como risco muito alto.**
  - Para Sudan, o modelo estimou 100.0% de probabilidade de violência organizada em 2024, classificando o caso como risco muito alto. Os principais grupos associados à estimativa foram: histórico e intensidade de conflitos UCDP; persistência temporal de conflito; indicadores socioeconômicos World Bank. Sinais que elevaram a estimativa: quantidade de díades de conflito não estatal; frequência de conflito nos últimos 5 anos; quantidade de díades de conflito estatal. Sinais que reduziram a estimativa no modelo: existência de conflito estatal no ano-base; existência de conflito não estatal; existência de violência unilateral.

- **India: 100.0% de risco estimado para 2024, classificado como risco muito alto.**
  - Para India, o modelo estimou 100.0% de probabilidade de violência organizada em 2024, classificando o caso como risco muito alto. Os principais grupos associados à estimativa foram: histórico e intensidade de conflitos UCDP; persistência temporal de conflito; indicadores socioeconômicos World Bank. Sinais que elevaram a estimativa: quantidade de díades de conflito estatal; quantidade de díades de violência unilateral; frequência de conflito nos últimos 5 anos. Sinais que reduziram a estimativa no modelo: existência de conflito estatal no ano-base; existência de conflito interestatal; existência de conflito não estatal.

- **Colombia: 100.0% de risco estimado para 2024, classificado como risco muito alto.**
  - Para Colombia, o modelo estimou 100.0% de probabilidade de violência organizada em 2024, classificando o caso como risco muito alto. Os principais grupos associados à estimativa foram: histórico e intensidade de conflitos UCDP; persistência temporal de conflito; indicadores socioeconômicos World Bank. Sinais que elevaram a estimativa: quantidade de díades de violência unilateral; quantidade de díades de conflito não estatal; quantidade de díades de conflito estatal. Sinais que reduziram a estimativa no modelo: existência de conflito estatal no ano-base; existência de conflito não estatal; existência de violência unilateral.

- **Mali: 100.0% de risco estimado para 2024, classificado como risco muito alto.**
  - Para Mali, o modelo estimou 100.0% de probabilidade de violência organizada em 2024, classificando o caso como risco muito alto. Os principais grupos associados à estimativa foram: histórico e intensidade de conflitos UCDP; persistência temporal de conflito; indicadores socioeconômicos World Bank. Sinais que elevaram a estimativa: quantidade de díades de conflito não estatal; quantidade de díades de violência unilateral; quantidade de díades de conflito estatal. Sinais que reduziram a estimativa no modelo: existência de conflito estatal no ano-base; existência de conflito não estatal; existência de violência unilateral.

- **Myanmar (Burma): 100.0% de risco estimado para 2024, classificado como risco muito alto.**
  - Para Myanmar (Burma), o modelo estimou 100.0% de probabilidade de violência organizada em 2024, classificando o caso como risco muito alto. Os principais grupos associados à estimativa foram: histórico e intensidade de conflitos UCDP; persistência temporal de conflito; indicadores socioeconômicos World Bank. Sinais que elevaram a estimativa: quantidade de díades de conflito estatal; frequência de conflito nos últimos 5 anos; quantidade de díades de violência unilateral. Sinais que reduziram a estimativa no modelo: existência de conflito estatal no ano-base; existência de violência unilateral; mortes estimadas em conflitos intraestatais.


## Casos de falso negativo

| country | region | forecast_year | predicted_probability_percent | risk_level_description | top_positive_factors | top_negative_factors | prediction_result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Rwanda | Africa | 2024 | 44.5% | risco moderado | frequência de conflito nos últimos 5 anos; conflito no ano anterior; matrícula no ensino secundário | crescimento anual do PIB; desemprego; gasto militar como percentual do PIB | false_negative |
| France | Europe | 2024 | 41.4% | risco moderado | existência de violência organizada no ano-base; quantidade de díades de conflito não estatal; quantidade de díades de violência unilateral | PIB per capita; existência de conflito não estatal; existência de violência unilateral | false_negative |
| Liberia | Africa | 2024 | 19.8% | risco muito baixo | frequência de conflito nos últimos 5 anos; crescimento populacional anual; PIB per capita | crescimento anual do PIB; população total; gasto militar como percentual do PIB | false_negative |
| Gambia | Africa | 2024 | 10.5% | risco muito baixo | crescimento populacional anual; PIB per capita; inflação anual | crescimento anual do PIB; gasto militar como percentual do PIB; desemprego | false_negative |
| Jordan | Middle East | 2024 | 9.3% | risco muito baixo | gasto militar como percentual do PIB; crescimento populacional anual; PIB per capita | desemprego; inflação anual | false_negative |
| Germany | Europe | 2024 | 4.7% | risco muito baixo | crescimento anual do PIB; população total; desemprego | PIB per capita; crescimento populacional anual; matrícula no ensino secundário | false_negative |

## Casos de falso positivo

| country | region | forecast_year | predicted_probability_percent | risk_level_description | top_positive_factors | top_negative_factors | prediction_result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Egypt | Middle East | 2024 | 93.7% | risco muito alto | frequência de conflito nos últimos 5 anos; existência de violência organizada no ano-base; existência de conflito intraestatal | existência de conflito estatal no ano-base; existência de violência unilateral; crescimento anual do PIB | false_positive |
| Tunisia | Africa | 2024 | 88.9% | risco muito alto | frequência de conflito nos últimos 5 anos; existência de violência organizada no ano-base; existência de conflito intraestatal | existência de conflito estatal no ano-base; desemprego; crescimento populacional anual | false_positive |
| Azerbaijan | Europe | 2024 | 87.5% | risco muito alto | frequência de conflito nos últimos 5 anos; existência de violência organizada no ano-base; existência de conflito intraestatal | existência de conflito estatal no ano-base; crescimento populacional anual; mortes acumuladas nos últimos 5 anos | false_positive |
| Armenia | Europe | 2024 | 85.2% | risco muito alto | frequência de conflito nos últimos 5 anos; existência de violência organizada no ano-base; existência de conflito intraestatal | existência de conflito estatal no ano-base; crescimento anual do PIB; crescimento populacional anual | false_positive |
| Peru | Americas | 2024 | 82.9% | risco muito alto | frequência de conflito nos últimos 5 anos; existência de violência organizada no ano-base; existência de conflito intraestatal | existência de conflito estatal no ano-base; matrícula no ensino secundário; PIB per capita | false_positive |
| Saudi Arabia | Middle East | 2024 | 81.2% | risco muito alto | frequência de conflito nos últimos 5 anos; existência de violência organizada no ano-base; existência de conflito intraestatal | existência de conflito estatal no ano-base; PIB per capita; inflação anual | false_positive |
| China | Asia | 2024 | 79.5% | risco alto | população total; existência de violência organizada no ano-base; existência de conflito intraestatal | existência de conflito estatal no ano-base; crescimento populacional anual; crescimento anual do PIB | false_positive |
| Kingdom of eSwatini (Swaziland) | Africa | 2024 | 72.7% | risco alto | frequência de conflito nos últimos 5 anos; existência de violência organizada no ano-base; quantidade de díades de violência unilateral | desemprego; existência de violência unilateral; crescimento populacional anual | false_positive |

## Conclusão

Esta camada conecta a probabilidade prevista aos grupos de features usados pelo modelo.

Ela reforça a leitura do projeto como um sistema de análise preditiva, pois permite sair da métrica global e observar, por país, quais fatores do dataset integrado aparecem associados ao risco estimado.
