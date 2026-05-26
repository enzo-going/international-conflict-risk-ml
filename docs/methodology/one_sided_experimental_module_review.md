# Revisão do Módulo Experimental de One-Sided Violence

Este documento registra a revisão metodológica do módulo experimental criado para análise de violência unilateral com base no dataset UCDP One-Sided Violence.

## Arquivos relacionados

| Arquivo | Função |
|---|---|
| data/raw/ucdp/OneSided_v25_1.xlsx | Dataset bruto UCDP One-Sided Violence |
| data/final/UCDP_One-sided_Violence_Dataset_updated.csv | Versão simplificada/processada usada pelo módulo |
| src/models/ml_onesided_violence.py | Script experimental de modelagem |
| outputs/tables/one_sided_predictions.csv | Predições geradas pelo módulo |
| outputs/tables/one_sided_feature_importance.csv | Coeficientes/importância das features |
| outputs/tables/neighbors.json | Mapeamento de vizinhos geográficos |

## Objetivo do módulo

O módulo busca prever a ocorrência de violência unilateral no ano seguinte a partir de dados históricos agregados por localidade e ano.

O target utilizado no script é target_next_year.

O modelo utilizado é uma regressão logística com pipeline de imputação, padronização e classificação.

## Mérito técnico

O módulo possui valor para o projeto porque:

- adiciona uma frente específica para one-sided violence;
- explora dados UCDP além da base principal country-year;
- cria features temporais próprias;
- utiliza vizinhança geográfica como variável complementar;
- gera predições e coeficientes interpretáveis;
- amplia a contribuição técnica do grupo.

## Pontos de atenção

Apesar de útil, o módulo ainda não deve ser tratado como pipeline principal.

### Unidade de análise diferente

O pipeline principal do projeto trabalha com country-year.

O módulo experimental parece trabalhar mais próximo de location-year.

Essa diferença precisa ser mantida explícita para evitar mistura metodológica.

### Risco no target de anos finais

O arquivo de predições inclui linhas de 2024.

Como o target é target_next_year, é necessário verificar se o valor de 2024 representa ausência real de violência no ano seguinte ou apenas ausência de dados futuros.

Esse ponto é metodologicamente sensível.

### Dependência geográfica adicional

O módulo usa geopandas e dados de vizinhança geográfica.

Isso é interessante, mas aumenta a complexidade do projeto e exige cuidado com nomes de países, fronteiras, reprodutibilidade e consistência entre location e países do pipeline principal.

### Dataset processado sem rastreabilidade completa

O arquivo data/final/UCDP_One-sided_Violence_Dataset_updated.csv foi adicionado já processado.

Ainda é necessário documentar ou recuperar o script responsável por gerar esse CSV a partir do arquivo bruto.

## Decisão metodológica

O módulo ml_onesided_violence.py deve ser mantido como módulo experimental complementar.

Ele não substitui o modelo principal do projeto.

O modelo principal continua sendo Logistic Regression scaled - World Bank all raw.

A unidade de análise principal continua sendo country-year.

## Classificação atual

| Critério | Decisão |
|---|---|
| Deve ser removido? | Não |
| Deve ser usado como resultado principal? | Não |
| Deve ser documentado? | Sim |
| Deve ser tratado como contribuição experimental? | Sim |
| Pode ser integrado futuramente? | Sim, após validação |

## Próximas ações recomendadas

1. Verificar como UCDP_One-sided_Violence_Dataset_updated.csv foi gerado.
2. Criar script reprodutível para essa transformação, se necessário.
3. Comparar as informações do módulo com one_sided_violence_exists, one_sided_dyad_count e one_sided_deaths_best.
4. Avaliar se o módulo pode gerar features agregadas em country-year.
5. Verificar o tratamento correto dos anos finais, especialmente 2024.
6. Só integrar ao pipeline principal se houver ganho informacional claro.

## Conclusão

O módulo de one-sided violence é uma contribuição útil do grupo, mas ainda precisa ser tratado como frente paralela.

A decisão prudente é preservar o trabalho, documentar seus limites e não misturá-lo com o pipeline principal antes de validação metodológica.
