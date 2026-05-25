# Fontes Candidatas de Dados

Este documento lista fontes candidatas para expansão do projeto **International Conflict Risk ML**.

O objetivo é planejar a integração de novos datasets antes de adicioná-los ao pipeline principal, evitando acúmulo desorganizado de arquivos e reduzindo o risco de inserir variáveis pouco úteis, redundantes ou metodologicamente frágeis.

## Critérios de escolha

| Critério | Pergunta principal |
|---|---|
| Relevância | A fonte ajuda a explicar risco, persistência ou escalada de conflito? |
| Granularidade | O dado pode ser convertido para estrutura país-ano? |
| Cobertura temporal | A fonte cobre anos suficientes para treino e teste temporal? |
| Cobertura geográfica | A fonte cobre muitos países ou apenas casos específicos? |
| Integração | Existe chave clara para integrar com `country` e `year`? |
| Qualidade | O dado é confiável, documentado e reproduzível? |
| Custo metodológico | O ganho potencial justifica a complexidade adicional? |

## Prioridade atual

A unidade principal do projeto é `country-year`.

Portanto, fontes com dados anuais por país têm prioridade.

Fontes em formato de evento, relação entre países, tratados ou crises podem ser usadas depois, mas exigem transformação para país-ano.

## Fontes candidatas prioritárias

| Fonte | Tipo | Granularidade provável | Prioridade | Observação |
|---|---|---|---|---|
| Worldwide Governance Indicators — WGI | Governança e estabilidade institucional | Country-year | Alta | Boa próxima fonte; avaliar risco de proximidade conceitual com conflito. |
| V-Dem Dataset | Democracia, regime político e instituições | Country-year | Alta | Muito rico, mas exige seleção cuidadosa de poucas variáveis. |
| SIPRI Military Expenditure Database | Militarização e gastos de defesa | Country-year | Média-alta | Pode melhorar ou complementar o indicador militar do World Bank. |
| Correlates of War — Formal Alliances | Alianças e relações internacionais | Dyad/alliance-period | Média | Exige agregação para país-ano. |
| UNHCR Refugee Data | Refugiados e deslocamento forçado | Country-year | Média | Pode capturar instabilidade regional, mas pode ser consequência direta de conflito. |
| Fragile States Index | Fragilidade estatal e pressão social | Country-year | Média | Útil, mas verificar licença, cobertura e circularidade. |
| ND-GAIN Country Index | Vulnerabilidade climática e resiliência | Country-year | Média-baixa | Pode enriquecer a dimensão ambiental. |
| IMF / World Economic Outlook | Macroeconomia | Country-year | Média-baixa | Avaliar redundância com World Bank. |

## Próxima fonte sugerida

A próxima fonte a avaliar deve ser **Worldwide Governance Indicators — WGI**.

Motivos:

- tem forte relação conceitual com risco de conflito;
- possui estrutura próxima de país-ano;
- é compatível com a arquitetura atual;
- complementa o World Bank;
- tem número controlável de indicadores;
- permite testar ganho incremental sem explodir a complexidade.

## Estratégia de integração

Para cada nova fonte, seguir o padrão:

| Camada | Caminho esperado |
|---|---|
| Dados brutos | `data/raw/<source>/` |
| Dados processados | `data/processed/<source>/` |
| Dataset final | `data/final/` |
| Script de preparação | `src/data/prepare_<source>.py` |
| Script de features | `src/features/build_<source>_features.py` |
| Documentação da fonte | `docs/references/<source>_indicators.md` |
| Resultados experimentais | `outputs/tables/<source>_model_results.csv` |

## Regras metodológicas

1. Não integrar dezenas de variáveis sem seleção conceitual.
2. Não misturar granularidades sem documentação.
3. Não usar variável que seja praticamente o target disfarçado.
4. Não substituir o modelo principal sem comparação contra baseline.
5. Sempre manter split temporal.
6. Sempre preservar dados brutos.
7. Sempre gerar dados finais por script.
8. Sempre documentar fonte, variáveis, cobertura e limitações.

## Status

Status atual: planejamento de expansão de fontes.

Próximo passo técnico: avaliar e integrar WGI como próxima fonte externa.