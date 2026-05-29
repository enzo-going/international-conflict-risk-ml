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

## 7. Datasets utilizados

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

