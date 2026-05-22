# Camada SQL

Esta pasta contém a camada SQL do projeto **International Conflict Risk ML**.

O objetivo desta camada é criar uma interface de banco de dados reproduzível sobre os principais artefatos do projeto:

- dataset final em estrutura país-ano;
- predições do modelo;
- métricas de avaliação;
- coeficientes interpretáveis do modelo;
- metadados do dataset e do experimento.

## Banco utilizado

A primeira implementação utilizará **SQLite**.

O SQLite foi escolhido porque é:

- portátil;
- simples de reproduzir;
- adequado para projeto acadêmico e portfólio;
- fácil de gerar a partir de arquivos CSV;
- compatível com Python e consultas SQL;
- não exige instalação de servidor de banco de dados.

O arquivo `.db` será gerado localmente e **não deve ser commitado no Git**.

## Estrutura da pasta

```text
sql/
├── schema.sql
├── README.md
└── queries/
```

| Caminho | Função |
|---|---|
| `schema.sql` | Define o schema inicial do banco SQLite. |
| `queries/` | Armazena consultas SQL analíticas. |
| `README.md` | Explica a função da camada SQL no projeto. |

## Fluxo planejado

```text
CSV outputs
→ banco SQLite
→ consultas SQL
→ documentação, dashboard ou futura API
```

## Tabelas planejadas

| Tabela | Função |
|---|---|
| `country_year_features` | Dataset analítico principal em estrutura país-ano. |
| `model_predictions` | Predições do modelo no conjunto de teste. |
| `model_coefficients` | Coeficientes extraídos da regressão logística. |
| `model_metrics` | Métricas de avaliação da baseline e do modelo principal. |
| `dataset_metadata` | Metadados sobre a geração do banco. |

## Status atual

Status: camada SQL inicial.

O schema foi definido em:

```text
sql/schema.sql
```

A geração automática do banco SQLite ainda será implementada em Python.

## Próximos passos

1. Criar script Python para gerar o banco SQLite a partir dos CSVs do projeto.
2. Carregar o dataset final em `country_year_features`.
3. Carregar predições em `model_predictions`.
4. Carregar métricas em `model_metrics`.
5. Carregar coeficientes em `model_coefficients`.
6. Criar consultas SQL em `sql/queries/`.