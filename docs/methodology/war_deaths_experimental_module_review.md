# Revisão do Módulo Experimental WWI/WWII

Este documento registra a revisão metodológica dos arquivos adicionados ao projeto relacionados à Primeira e Segunda Guerra Mundial.

## Arquivos relacionados

Datasets:

- `data/final/world_war_1_details_clean.csv`
- `data/final/world_war_2_clean.csv`

Scripts:

- `src/data/wwi_predictive_analysis_scalability_of_conflict.py`
- `src/features/build_temporal_generation_wars_deaths.py`
- `src/features/build_features_wars_deaths.py`
- `src/models/train_model_wars_deaths.py`

## Estrutura dos datasets

Os datasets possuem colunas como:

- `event_id`
- `start_year`
- `end_year`
- `country`
- `alliance`
- `casualties_mil_k`
- `casualties_civ_k`
- `military_personnel_k`
- `front`
- `total_casualties_k`
- `casualty_ratio`

Essa estrutura é útil para análise histórica de guerras, baixas e intensidade de conflito, mas não está diretamente alinhada ao pipeline principal `country-year`.

## Diferença em relação ao pipeline principal

O pipeline oficial do projeto trabalha com:

- unidade: `country-year`;
- target: `target_conflict_next_year`;
- objetivo: prever violência organizada no ano seguinte;
- fontes principais: UCDP Organized Violence, features temporais e World Bank.

O módulo WWI/WWII parece trabalhar com:

- unidade próxima de evento histórico ou guerra-país;
- target `next_month_escalation`;
- foco em escalada mensal de mortes;
- modelo LightGBM.

Portanto, ele resolve um problema diferente do modelo principal.

## Decisão metodológica

O módulo WWI/WWII deve ser mantido como experimental.

Ele não deve substituir o pipeline principal e não deve ser usado como evidência direta do desempenho do modelo oficial.

## Potencial uso futuro

O módulo pode ser reaproveitado futuramente para:

1. estudar escalada histórica de grandes guerras;
2. gerar features agregadas sobre intensidade histórica de conflito;
3. testar modelos temporais de curto prazo;
4. enriquecer uma análise paralela sobre severidade e duração de guerras.

## Status atual

Classificação atual:

- status: experimental;
- integração ao modelo principal: não realizada;
- uso no dashboard final: apenas como expansão futura ou módulo em revisão;
- necessidade antes de integração: padronização para `country-year`, definição metodológica do target e validação separada.
