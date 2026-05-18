# Indicadores do World Bank

Este documento define os indicadores do World Bank selecionados para integração ao projeto.

O objetivo é enriquecer o dataset país-ano de conflitos com variáveis socioeconômicas, demográficas e estruturais. Esses indicadores são usados como features externas, não como variável-alvo.

## Papel metodológico

O modelo atual utiliza informações históricas de conflito da UCDP, features temporais de conflito e indicadores socioeconômicos externos do World Bank.

A variável-alvo permanece:

`target_conflict_next_year`

O objetivo é testar se indicadores externos em estrutura país-ano adicionam sinal preditivo além da persistência histórica do conflito.

## Indicadores já integrados

| Feature | Código World Bank | Interpretação | Papel esperado |
|---|---|---|---|
| `population_total` | `SP.POP.TOTL` | População total | Escala estrutural do país |
| `gdp_per_capita_current_usd` | `NY.GDP.PCAP.CD` | PIB per capita em US$ corrente | Proxy de desenvolvimento econômico |
| `gdp_growth_annual_pct` | `NY.GDP.MKTP.KD.ZG` | Crescimento anual do PIB (%) | Ciclo econômico / instabilidade |
| `inflation_consumer_prices_annual_pct` | `FP.CPI.TOTL.ZG` | Inflação anual ao consumidor (%) | Pressão econômica interna |
| `unemployment_total_pct` | `SL.UEM.TOTL.ZS` | Desemprego total (% da força de trabalho) | Fragilidade social/econômica |
| `military_expenditure_pct_gdp` | `MS.MIL.XPND.GD.ZS` | Gasto militar (% do PIB) | Dimensão militar/estratégica |

## Indicadores candidatos para segunda leva de integração

| Feature | Código World Bank | Interpretação | Papel esperado |
|---|---|---|---|
| `population_growth_annual_pct` | `SP.POP.GROW` | Crescimento anual da população (%) | Pressão demográfica |
| `urban_population_pct` | `SP.URB.TOTL.IN.ZS` | População urbana (% do total) | Urbanização / densidade |
| `school_enrollment_secondary_gross_pct` | `SE.SEC.ENRR` | Matrícula no ensino secundário, taxa bruta (%) | Proxy de educação/desenvolvimento humano |
| `natural_resources_rents_pct_gdp` | `NY.GDP.TOTL.RT.ZS` | Rendas totais de recursos naturais (% do PIB) | Dependência de recursos naturais / risco estrutural |

## Outputs integrados

Dataset processado atual do World Bank:

`data/processed/world_bank/world_bank_country_year_indicators.csv`

Dataset integrado conflito + World Bank:

`data/final/conflict_country_year_world_bank.csv`

Dataset atual com features derivadas do World Bank:

`data/final/conflict_country_year_world_bank_features.csv`

## Regras de integração

Cada indicador deve ser transformado para estrutura país-ano com, no mínimo:

- `country_code`
- `country_name`
- `year`
- uma coluna numérica por indicador

Antes de integrar ao dataset principal, devem ser verificados:

- número de países;
- intervalo de anos;
- percentual de valores ausentes por indicador;
- pares país-ano duplicados;
- compatibilidade entre códigos do World Bank e o mapeamento de países da UCDP.

## Status atual

Status: primeira integração World Bank concluída.

A primeira leva de indicadores já foi integrada, transformada em features temporais e avaliada nos modelos. A segunda leva deve ser adicionada com cuidado, validando valores ausentes e impacto no desempenho antes de expandir para mais variáveis.
