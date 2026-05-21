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

## Escopo técnico atual

O escopo técnico atual do projeto envolve:

- construção de um pipeline reprodutível de dados e Machine Learning;
- uso da UCDP como base central de conflitos organizados;
- integração de indicadores socioeconômicos do World Bank;
- criação de features temporais e derivadas;
- avaliação com split temporal;
- comparação contra baseline de persistência;
- geração de métricas, predições e modelo treinado;
- documentação metodológica do processo;
- manutenção de um dashboard HTML para acompanhamento visual do projeto.

## Formulação técnica do problema

A unidade principal de análise é `country-year`.

O problema atual é tratado como uma tarefa de classificação supervisionada:

`target_conflict_next_year`

Esse target indica se um país apresentará violência organizada no ano seguinte.

A avaliação principal utiliza split temporal, treinando em anos anteriores e testando em anos posteriores. Isso evita misturar passado e futuro, tornando a avaliação mais coerente para um problema temporal.

A baseline obrigatória do projeto é a persistência de conflito:

`y_pred = organized_violence_exists`

Essa baseline é forte porque conflitos tendem a apresentar continuidade histórica. Por isso, qualquer modelo mais complexo precisa ser comparado contra ela.

## Estrutura do projeto

A estrutura do repositório segue uma organização modular para separar dados brutos, dados processados, scripts, notebooks, documentação e artefatos de saída.

Resumo das principais pastas:

- `data/raw/` — dados brutos preservados, sem edição manual;
- `data/interim/` — arquivos auxiliares de integração, como mapeamentos de países;
- `data/processed/` — dados processados e padronizados;
- `data/final/` — datasets finais usados em análise e modelagem;
- `docs/` — documentação metodológica, referências e dashboard HTML;
- `notebooks/exploration/` — notebooks de análise exploratória;
- `notebooks/modeling/` — notebooks de modelagem e avaliação;
- `src/data/` — scripts de ingestão, limpeza e integração;
- `src/features/` — scripts de engenharia de atributos;
- `src/models/` — scripts de treinamento e avaliação de modelos;
- `outputs/tables/` — métricas, predições e tabelas exportadas;
- `outputs/models/` — modelo treinado e metadados;
- `reports/` — materiais voltados à qualificação e entrega final.

Para uma visão mais detalhada da função de cada arquivo e do fluxo principal do projeto, consulte:

`docs/project_map.md`

## Status atual

O projeto já saiu da fase inicial de estruturação e atualmente possui um pipeline funcional de Machine Learning.

### Concluído até o momento

- [x] Estrutura inicial do repositório
- [x] Processamento da base UCDP Organized Violence Country-Year
- [x] Construção do dataset país-ano
- [x] Criação do target `target_conflict_next_year`
- [x] Análise exploratória inicial
- [x] Baseline de persistência
- [x] Modelos clássicos iniciais
- [x] Integração com indicadores do World Bank
- [x] Engenharia de features temporais
- [x] Script principal de treinamento reproduzível
- [x] Modelo principal salvo
- [x] Análise de probabilidade e threshold
- [x] Dashboard HTML publicado
- [x] Mapa técnico do projeto em `docs/project_map.md`

### Em andamento

- [ ] Reexecutar o modelo principal após a segunda expansão dos indicadores World Bank
- [ ] Atualizar métricas caso o desempenho mude
- [ ] Validar arquivos WWI adicionados pelo grupo
- [ ] Consolidar documentação para qualificação
- [ ] Testar modelos adicionais, como Gradient Boosting e MLP

## Principais fontes consideradas

- UCDP — Uppsala Conflict Data Program
- ACLED — Armed Conflict Location & Event Data
- SIPRI — Stockholm International Peace Research Institute
- UNHCR — United Nations High Commissioner for Refugees
- World Bank Open Data
- Correlates of War

## Observação

O projeto evita tratar a previsão de conflitos como uma previsão determinística. O objetivo é construir uma abordagem exploratória e probabilística, adequada às limitações dos dados históricos e à complexidade do fenômeno analisado.
