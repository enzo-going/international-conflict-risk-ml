# International Conflict Risk ML

## Visualização do projeto

Este projeto possui uma página HTML publicada via GitHub Pages para facilitar a visualização geral da proposta, dos dados utilizados, do pipeline de Machine Learning e dos resultados parciais.

Acesse aqui:

[Dashboard do projeto](https://enzo-going.github.io/international-conflict-risk-ml/)

Projeto acadêmico de Machine Learning aplicado à análise preditiva de conflitos internacionais a partir de dados heterogêneos em formato tabular e temporal.

Este projeto faz parte da Pesquisa Curricularizada da Graduação em Ciência da Computação, envolvendo os componentes de Reconhecimento de Padrões com Inteligência Artificial e Banco de Dados.

## Objetivo

Desenvolver uma base analítica e experimental para estimar risco de ocorrência ou intensificação de conflitos internacionais utilizando dados históricos organizados em estrutura país-ano.

A proposta inicial é utilizar o UCDP Organized Violence Country-Year Dataset como base central e integrar, progressivamente, outras fontes relacionadas a violência unilateral, temas de conflito, indicadores militares, econômicos, sociais, geopolíticos e ambientais.

## Escopo inicial

A fase técnica inicial do projeto terá como foco:

- estruturação do repositório;
- inventário dos datasets disponíveis;
- definição da base central de análise;
- padronização inicial dos dados em formato país-ano;
- construção de um dataset final mínimo;
- análise exploratória dos dados;
- criação de modelos baseline de Machine Learning;
- documentação metodológica do processo.

## Formulação inicial do problema

A unidade principal de análise será country-year.

O objetivo inicial de Machine Learning será estudar a previsão/classificação de ocorrência ou intensificação de conflito armado em uma janela futura, com base em informações históricas e variáveis derivadas.

## Estrutura do projeto

- data/raw/ — dados brutos originais
- data/interim/ — dados parcialmente tratados
- data/processed/ — dados processados e padronizados
- data/final/ — dataset final utilizado em modelagem
- docs/academic/ — documentos acadêmicos e entregas
- docs/methodology/ — documentação metodológica
- docs/references/ — referências, artigos e fontes
- notebooks/exploration/ — notebooks de análise exploratória
- notebooks/modeling/ — notebooks de modelagem
- src/data/ — scripts de ingestão e processamento
- src/features/ — engenharia de atributos
- src/models/ — treinamento e avaliação de modelos
- src/visualization/ — geração de gráficos e visualizações
- outputs/charts/ — gráficos exportados
- outputs/tables/ — tabelas exportadas
- outputs/models/ — artefatos de modelos
- reports/qualification/ — materiais da qualificação
- reports/final/ — materiais da entrega final

## Status atual

Projeto em fase inicial de estruturação técnica.

### Em andamento

- [ ] Inventário dos datasets disponíveis
- [ ] Definição do escopo técnico inicial
- [ ] Organização da documentação acadêmica
- [ ] Seleção das fontes principais
- [ ] Construção do dataset país-ano
- [ ] Análise exploratória inicial
- [ ] Criação de modelos baseline

## Principais fontes consideradas

- UCDP — Uppsala Conflict Data Program
- ACLED — Armed Conflict Location & Event Data
- SIPRI — Stockholm International Peace Research Institute
- UNHCR — United Nations High Commissioner for Refugees
- World Bank Open Data
- Correlates of War

## Observação

O projeto evita tratar a previsão de conflitos como uma previsão determinística. O objetivo é construir uma abordagem exploratória e probabilística, adequada às limitações dos dados históricos e à complexidade do fenômeno analisado.
