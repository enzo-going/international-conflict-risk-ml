# Relatório de Qualificação — Sistema Machine Learning de Análise Preditiva de Conflitos Internacionais

## 1. Introdução

Este relatório apresenta o desenvolvimento de um sistema de Machine Learning aplicado à análise preditiva de conflitos internacionais. O projeto foi construído a partir de dados tabulares heterogêneos, com foco na estrutura país-ano (`country-year`) e na previsão da ocorrência de violência organizada no ano seguinte.

A proposta combina dados históricos de conflitos, indicadores socioeconômicos, auditoria de datasets, comparação de modelos, análise preditiva por país e documentação metodológica. O objetivo não é prever eventos geopolíticos de forma determinística, mas construir uma base técnica mensurável para estimar risco futuro com critérios reprodutíveis.

## 2. Motivação e reformulação do problema

A motivação inicial do projeto envolvia a investigação de tensões internacionais, escalada de conflitos e risco de grandes crises globais. No entanto, ao longo do desenvolvimento, essa ideia foi reformulada para evitar uma abordagem metodologicamente frágil.

Prever diretamente uma Terceira Guerra Mundial seria inadequado para aprendizado supervisionado, pois se trata de um evento raro, de difícil definição operacional e com poucas amostras históricas. Por isso, o problema foi transformado em uma tarefa observável: estimar, para cada país em determinado ano, a probabilidade de ocorrência de violência organizada no ano seguinte.

Essa reformulação preserva a motivação original, mas torna o projeto tecnicamente avaliável por meio de dados, target supervisionado, baseline, modelos candidatos e métricas de desempenho.

## 3. Pergunta de pesquisa

Dado o histórico de violência organizada e indicadores socioeconômicos associados a um país em determinado ano, é possível estimar a ocorrência de violência organizada no ano seguinte com desempenho superior a uma baseline simples de persistência?

## 4. Objetivo geral

Desenvolver e avaliar um sistema de Machine Learning aplicado à análise preditiva de conflitos internacionais, utilizando dados tabulares em estrutura país-ano e considerando a integração de fontes heterogêneas para estimar risco futuro de violência organizada.

## 5. Objetivos específicos

- Construir uma base de dados país-ano a partir de fontes históricas de conflito.
- Definir um target supervisionado para previsão de violência organizada no ano seguinte.
- Comparar o desempenho de modelos candidatos contra uma baseline de persistência.
- Integrar indicadores socioeconômicos ao pipeline principal.
- Avaliar a contribuição de novas features e fontes de dados.
- Produzir análises preditivas por país e por região.
- Documentar limitações metodológicas, módulos experimentais e critérios de validação.

## 6. Fundamentação metodológica

O projeto utiliza aprendizado supervisionado aplicado a dados tabulares. A unidade de análise adotada é `country-year`, em que cada registro representa um país em determinado ano. Essa estrutura permite relacionar informações históricas de conflito e indicadores externos com um alvo de previsão definido para o ano seguinte.

O target principal do projeto é `target_conflict_next_year`, variável binária que indica se há ocorrência de violência organizada no ano posterior ao registro analisado. Essa escolha permite transformar uma questão geopolítica ampla em um problema técnico mensurável de classificação.

A estratégia de avaliação utiliza separação temporal entre treino e teste. O modelo é treinado com dados até 2016 e avaliado no período de 2017 a 2023. Essa abordagem evita misturar anos futuros no treinamento e torna a avaliação mais próxima de um cenário real de previsão.

A baseline adotada é a persistência do conflito: se houve violência organizada no ano atual, assume-se que haverá violência organizada no ano seguinte. Essa baseline é forte porque conflitos apresentam continuidade temporal. Portanto, qualquer modelo candidato precisa demonstrar ganho real sobre essa referência simples.

O modelo principal consolidado é uma Regressão Logística com imputação por mediana, padronização das variáveis e balanceamento de classe. A escolha desse modelo se justifica pela combinação entre desempenho, interpretabilidade e adequação ao escopo acadêmico do projeto.

## 7. Datasets utilizados

O projeto utiliza como base central o dataset **UCDP Organized Violence**, responsável por representar ocorrências de violência organizada em estrutura país-ano. A partir dessa fonte, foram construídas variáveis relacionadas à existência de conflito, quantidade de díades, mortes estimadas e histórico recente de violência.

Além da base central de conflitos, o projeto integra indicadores do **World Bank**, incluindo população, crescimento populacional, urbanização, PIB per capita, crescimento do PIB, inflação, desemprego, escolarização, gasto militar e dependência de recursos naturais. Esses indicadores permitem enriquecer o modelo com variáveis socioeconômicas externas ao histórico direto de conflito.

A auditoria atual do projeto reconhece **35 datasets**, classificados em diferentes categorias:

| Categoria | Quantidade |
|---|---:|
| Oficiais ou candidatos ao pipeline | 12 |
| Experimentais | 4 |
| Dados brutos de suporte | 16 |
| Não prontos ou rejeitados | 3 |

O dataset **SIPRI** foi incorporado como fonte candidata, principalmente por sua relação com militarização e gastos militares. No entanto, ele ainda não substitui o pipeline principal e precisa ser avaliado de forma controlada antes de ser tratado como fonte oficial do modelo.

Os módulos **WWI/WWII** e **One-Sided Violence** foram preservados como experimentais. Eles são úteis para exploração histórica e expansão futura, mas não devem ser confundidos com o modelo principal, que permanece centrado na previsão de violência organizada em estrutura `country-year`.

## 8. Pipeline de Machine Learning

## 9. Modelos avaliados

## 10. Resultado principal

## 11. Análise preditiva por país

## 12. Experimentos complementares

### 12.1 Features de choque econômico

### 12.2 SIPRI

### 12.3 WWI/WWII

### 12.4 One-Sided Violence

## 13. Validação automática e reprodutibilidade

## 14. Limitações metodológicas

## 15. Conclusão

## 16. Referências e fontes de dados

