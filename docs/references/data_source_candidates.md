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

A unidade principal do projeto é:

```text
country-year