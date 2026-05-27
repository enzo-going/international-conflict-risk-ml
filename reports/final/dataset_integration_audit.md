# Auditoria de Integração de Datasets

Este relatório resume a situação dos datasets presentes no projeto e avalia sua compatibilidade com o pipeline principal de Machine Learning.

## Critério central

A unidade oficial do pipeline principal é `country-year`.

Datasets que não possuem país/localidade e ano precisam ser transformados, agregados ou mantidos como módulos experimentais antes de entrar no modelo principal.

## Resumo executivo

- Total de datasets auditados: 22
- Datasets compatíveis ou candidatos ao pipeline principal: 6
- Datasets experimentais/em revisão: 3
- Arquivos brutos preservados como suporte/rastreabilidade: 11
- Datasets que requerem transformação: 0
- Datasets ainda não prontos ou não integráveis diretamente: 2

## Contagem por decisão

| decision | count |
| --- | --- |
| supporting_raw_data | 11 |
| official | 6 |
| experimental | 3 |
| not_ready | 2 |

## Contagem por fonte detectada

| source_name | count |
| --- | --- |
| world_bank | 11 |
| ucdp_one_sided | 2 |
| country_mapping | 2 |
| project_final_dataset | 2 |
| project_world_bank_dataset | 2 |
| ucdp | 2 |
| wwi | 1 |

## Datasets oficiais, candidatos e experimentais

| dataset_path | source_name | layer | rows | columns | detected_unit | integration_status | decision | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| data/final/UCDP_One-sided_Violence_Dataset_updated.csv | ucdp_one_sided | final | 1330.0000 | 4.0000 | actor-country-year | experimental_review | experimental | Fonte adicionada pelo grupo ou módulo paralelo; requer validação e possível agregação antes de integração ao pipeline principal. |
| data/raw/ucdp/OneSided_v25_1.xlsx | ucdp_one_sided | raw | 1330.0000 | 17.0000 | actor-country-year | experimental_review | experimental | Fonte adicionada pelo grupo ou módulo paralelo; requer validação e possível agregação antes de integração ao pipeline principal. |
| data/final/world_war_1_details_clean.csv | wwi | final | 10000.0000 | 11.0000 | event-country-year | experimental_review | experimental | Fonte adicionada pelo grupo ou módulo paralelo; requer validação e possível agregação antes de integração ao pipeline principal. |
| data/final/conflict_country_year_base.csv | project_final_dataset | final | 6737.0000 | 22.0000 | country-year | official_project_dataset | official | Dataset final produzido pelo pipeline do projeto e compatível com a unidade country-year. |
| data/final/conflict_country_year_temporal.csv | project_final_dataset | final | 6737.0000 | 28.0000 | country-year | official_project_dataset | official | Dataset final produzido pelo pipeline do projeto e compatível com a unidade country-year. |
| data/final/conflict_country_year_world_bank.csv | project_world_bank_dataset | final | 6663.0000 | 43.0000 | country-year | official_project_dataset | official | Dataset final produzido pelo pipeline do projeto e compatível com a unidade country-year. |
| data/final/conflict_country_year_world_bank_features.csv | project_world_bank_dataset | final | 6663.0000 | 83.0000 | country-year | official_project_dataset | official | Dataset final produzido pelo pipeline do projeto e compatível com a unidade country-year. |
| data/processed/ucdp_organized_violence_country_year.csv | ucdp | processed | 6936.0000 | 20.0000 | country-year | official_or_candidate | official | Fonte UCDP em estrutura compatível com a unidade country-year. |
| data/processed/world_bank/world_bank_country_year_indicators.csv | world_bank | processed | 7595.0000 | 16.0000 | country-year | official_or_already_integrated | official | Fonte externa socioeconômica já utilizada ou alinhada ao pipeline principal. |
| data/raw/ucdp/organizedviolencecy_v25_1.xlsx | ucdp | raw | 6936.0000 | 74.0000 | unknown | official_raw_source | supporting_raw_data | Arquivo bruto UCDP preservado como fonte central; a modelagem usa versões processadas/finais. |
| data/raw/world_bank/FP.CPI.TOTL.ZG.json | world_bank | raw |  |  | unreadable_or_unsupported | raw_source_reference | supporting_raw_data | Arquivo bruto World Bank preservado para rastreabilidade; a integração ocorre por dataset processado/final. |
| data/raw/world_bank/MS.MIL.XPND.GD.ZS.json | world_bank | raw |  |  | unreadable_or_unsupported | raw_source_reference | supporting_raw_data | Arquivo bruto World Bank preservado para rastreabilidade; a integração ocorre por dataset processado/final. |
| data/raw/world_bank/NY.GDP.MKTP.KD.ZG.json | world_bank | raw |  |  | unreadable_or_unsupported | raw_source_reference | supporting_raw_data | Arquivo bruto World Bank preservado para rastreabilidade; a integração ocorre por dataset processado/final. |
| data/raw/world_bank/NY.GDP.PCAP.CD.json | world_bank | raw |  |  | unreadable_or_unsupported | raw_source_reference | supporting_raw_data | Arquivo bruto World Bank preservado para rastreabilidade; a integração ocorre por dataset processado/final. |
| data/raw/world_bank/NY.GDP.TOTL.RT.ZS.json | world_bank | raw |  |  | unreadable_or_unsupported | raw_source_reference | supporting_raw_data | Arquivo bruto World Bank preservado para rastreabilidade; a integração ocorre por dataset processado/final. |
| data/raw/world_bank/SE.SEC.ENRR.json | world_bank | raw |  |  | unreadable_or_unsupported | raw_source_reference | supporting_raw_data | Arquivo bruto World Bank preservado para rastreabilidade; a integração ocorre por dataset processado/final. |
| data/raw/world_bank/SL.UEM.TOTL.ZS.json | world_bank | raw |  |  | unreadable_or_unsupported | raw_source_reference | supporting_raw_data | Arquivo bruto World Bank preservado para rastreabilidade; a integração ocorre por dataset processado/final. |
| data/raw/world_bank/SP.POP.GROW.json | world_bank | raw |  |  | unreadable_or_unsupported | raw_source_reference | supporting_raw_data | Arquivo bruto World Bank preservado para rastreabilidade; a integração ocorre por dataset processado/final. |
| data/raw/world_bank/SP.POP.TOTL.json | world_bank | raw |  |  | unreadable_or_unsupported | raw_source_reference | supporting_raw_data | Arquivo bruto World Bank preservado para rastreabilidade; a integração ocorre por dataset processado/final. |
| data/raw/world_bank/SP.URB.TOTL.IN.ZS.json | world_bank | raw |  |  | unreadable_or_unsupported | raw_source_reference | supporting_raw_data | Arquivo bruto World Bank preservado para rastreabilidade; a integração ocorre por dataset processado/final. |

## Datasets não prontos

| dataset_path | source_name | layer | rows | columns | detected_unit | integration_status | decision | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| data/interim/country_name_mapping_candidates.csv | country_mapping | interim | 199.0000 | 7.0000 | country-only | requires_temporal_key | not_ready | Possui país/localidade, mas não possui chave temporal clara. |
| data/interim/country_name_mapping_reviewed.csv | country_mapping | interim | 199.0000 | 10.0000 | country-only | requires_temporal_key | not_ready | Possui país/localidade, mas não possui chave temporal clara. |

## Decisão metodológica

Nem todo dataset presente no repositório deve ser integrado automaticamente ao modelo principal.

A decisão atual é manter o pipeline oficial baseado em `country-year`, preservar módulos experimentais documentados e integrar novos datasets apenas quando houver chave temporal, chave geográfica e justificativa metodológica.

Essa abordagem evita que datasets adicionados pelo grupo prejudiquem a consistência do modelo final.
