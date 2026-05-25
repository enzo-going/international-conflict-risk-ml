# Design da Camada de Banco de Dados

Este documento descreve a camada de banco de dados do projeto **International Conflict Risk ML**.

A camada SQL foi adicionada para transformar os datasets e outputs do projeto em uma estrutura relacional consultável, reforçando a organização técnica do pipeline e permitindo análises via SQL.

## Objetivo

O objetivo da camada de banco de dados é criar uma interface estruturada para consultar:

- dataset final em estrutura país-ano;
- predições do modelo;
- métricas de avaliação;
- coeficientes interpretáveis da regressão logística;
- metadados da geração do banco.

Essa camada não substitui o pipeline em Python. Ela complementa o projeto com uma camada de persistência e consulta.

## Papel no projeto

O projeto atualmente possui quatro camadas principais:

```text
1. Dados brutos e processados
2. Pipeline Python de engenharia de dados e Machine Learning
3. Outputs analíticos em CSV
4. Banco SQLite gerado a partir dos outputs
```

O fluxo planejado é:

```text
CSV final + outputs do modelo
-> script Python de geração do banco
-> banco SQLite local
-> consultas SQL analíticas
-> documentação, dashboard ou futura API
```

## Banco escolhido

A primeira implementação utiliza **SQLite**.

A escolha por SQLite foi feita porque ele é:

- leve;
- portátil;
- reproduzível;
- adequado para GitHub e projeto acadêmico;
- fácil de gerar com Python;
- compatível com consultas SQL reais;
- independente de servidor.

O arquivo `.sqlite` é gerado localmente e não deve ser versionado no Git.

## Arquivos principais

| Caminho | Função |
|---|---|
| `sql/schema.sql` | Define o schema relacional do banco. |
| `src/data/build_sqlite_database.py` | Gera o banco SQLite a partir dos CSVs do projeto. |
| `data/database/conflict_risk_ml.sqlite` | Banco SQLite local gerado automaticamente. |
| `sql/queries/` | Consultas SQL analíticas. |

## Tabelas do banco

### `country_year_features`

Tabela principal do banco.

Granularidade:

```text
uma linha = um país em um ano
```

Chave primária:

```text
(country, year)
```

Contém:

- variáveis da UCDP;
- features temporais de conflito;
- indicadores brutos do World Bank;
- target supervisionado `target_conflict_next_year`.

Essa tabela representa a base analítica central do projeto.

### `model_predictions`

Tabela com as predições do modelo principal no conjunto de teste.

Contém:

- país;
- ano;
- valor real (`y_true`);
- predição binária (`y_pred`);
- probabilidade prevista (`y_proba`);
- indicador de violência organizada no ano atual.

Essa tabela permite consultar:

- maiores riscos previstos;
- falsos positivos;
- falsos negativos;
- acertos do modelo;
- casos em que o modelo diverge da baseline de persistência.

### `model_coefficients`

Tabela com os coeficientes da regressão logística.

Contém:

- ranking da variável;
- nome da feature;
- grupo da feature;
- coeficiente;
- magnitude absoluta;
- efeito estimado.

Essa tabela permite interpretar quais variáveis mais influenciam o modelo.

Importante: coeficientes indicam associação dentro do modelo, não causalidade.

### `model_metrics`

Tabela com métricas de avaliação.

Contém:

- modelo;
- accuracy;
- precision;
- recall;
- F1-score;
- matriz de confusão;
- diferença de F1-score em relação à baseline.

Essa tabela permite comparar a baseline de persistência com o modelo principal e futuros modelos candidatos.

### `dataset_metadata`

Tabela simples de metadados em formato chave-valor.

Pode armazenar:

- data de geração do banco;
- commit do projeto;
- caminho dos arquivos de origem;
- quantidade de linhas carregadas por tabela;
- versão do schema;
- informações do experimento.

## Consultas SQL disponíveis

As primeiras consultas foram adicionadas em `sql/queries/`.

| Query | Objetivo |
|---|---|
| `01_highest_predicted_risk.sql` | Lista os países/anos com maior probabilidade prevista de conflito. |
| `02_false_positives.sql` | Lista casos em que o modelo previu conflito, mas o target real foi 0. |
| `03_false_negatives.sql` | Lista casos em que o modelo não previu conflito, mas o target real foi 1. |
| `04_top_model_coefficients.sql` | Lista as features mais influentes do modelo. |
| `05_model_metrics.sql` | Lista as métricas da baseline e do modelo principal. |

## Modelo principal atual

O modelo principal atual utiliza:

```text
UCDP base features
+ temporal conflict features
+ raw World Bank indicators
```

Configuração atual:

```text
World Bank all raw
```

Resultado atual:

| Métrica | Valor |
|---|---:|
| Accuracy | 0.9197 |
| Precision | 0.9029 |
| Recall | 0.8435 |
| F1-score | 0.8722 |

A camada SQL permite consultar esses resultados diretamente a partir do banco local.

## Geração do banco

O banco é gerado com:

```powershell
python src\data\build_sqlite_database.py
```

O output local é:

```text
data/database/conflict_risk_ml.sqlite
```

Esse arquivo é ignorado pelo Git por regra no `.gitignore`.

## Status atual

Status: camada SQL funcional inicial.

Já foram implementados:

- schema SQLite;
- script Python de geração do banco;
- carregamento de features;
- carregamento de predições;
- carregamento de métricas;
- carregamento de coeficientes;
- queries SQL analíticas iniciais.

## Próximos passos

1. Expandir consultas SQL para análises por região e por ano.
2. Criar query para comparar modelo contra baseline de persistência.
3. Documentar exemplos de saída das queries.
4. Criar possível seção no dashboard explicando a camada SQL.
5. Avaliar integração futura com API ou visualização dinâmica.