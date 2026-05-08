\# Project Scope



Documento de escopo técnico do projeto `international-conflict-risk-ml`.



Este arquivo define a direção inicial do projeto, a formulação do problema de Machine Learning, os limites da V1 e as possibilidades de expansão futura.



\## Título técnico provisório



Sistema de aprendizado de máquina aplicado a dados heterogêneos para análise preditiva de conflitos internacionais.



\## Contexto



O projeto parte da ideia de utilizar dados históricos sobre conflitos, violência política e variáveis associadas para estudar padrões relacionados à ocorrência ou intensificação de conflitos internacionais.



A proposta acadêmica original mencionava a possibilidade de analisar tensões globais e risco de grandes conflitos. Para tornar o projeto mais tecnicamente defensável, a V1 será formulada como um problema de análise preditiva de conflitos em estrutura país-ano.



\## Unidade de análise



A unidade principal de análise será:



`country-year`



Cada linha do dataset final deverá representar um país em um determinado ano.



Exemplo conceitual:



| country | year | region | features... | target |

|---|---:|---|---|---|

| Brazil | 2001 | Americas | ... | 0 |

| Ukraine | 2022 | Europe | ... | 1 |



\## Base central



A base central da V1 será:



`UCDP Organized Violence Country-Year Dataset`



Motivo:



\- já possui estrutura compatível com país-ano;

\- contém registros históricos de violência organizada;

\- oferece variáveis relacionadas a conflitos estatais, não estatais e violência unilateral;

\- é uma fonte reconhecida academicamente para estudos sobre conflitos.



\## Problema inicial de Machine Learning



A V1 estudará a possibilidade de prever ou classificar risco de ocorrência ou intensificação de conflito armado em uma janela futura.



A formulação inicial será tratada como problema supervisionado de classificação.



Possíveis alvos iniciais:



1\. ocorrência de conflito no ano seguinte;

2\. intensificação de conflito no ano seguinte;

3\. classificação binária de risco a partir de mortes ou presença de conflito.



A definição final da variável-alvo dependerá da validação das colunas do dataset central.



\## Formulação provisória do alvo



A hipótese inicial é construir uma variável como:



`target\_conflict\_next\_year`



Essa variável indicaria se um país apresentou conflito armado no ano seguinte.



Outra possibilidade é:



`target\_intensification\_next\_year`



Essa variável indicaria se houve aumento relevante na intensidade do conflito no ano seguinte, por exemplo a partir de crescimento em mortes registradas ou quantidade de eventos/conflitos.



\## Features iniciais previstas



As primeiras features serão derivadas da própria base UCDP e de datasets complementares.



Possíveis grupos:



\### Histórico de conflito



\- existência de conflito estatal no ano atual;

\- mortes registradas em conflito estatal;

\- quantidade de díades/conflitos;

\- existência de violência não estatal;

\- mortes por violência não estatal;

\- existência de violência unilateral;

\- mortes por violência unilateral.



\### Estrutura temporal



\- ano;

\- região;

\- histórico recente de conflito;

\- médias ou somas defasadas em janelas temporais.



\### Features complementares



\- indicadores de violência unilateral;

\- temas de conflito;

\- variáveis nucleares agregadas por ano;

\- indicadores econômicos, sociais, geopolíticos e ambientais em versões futuras.



\## Modelos previstos



A V1 não deve começar diretamente pela rede neural.



A sequência recomendada será:



1\. baseline simples;

2\. modelo clássico de Machine Learning;

3\. rede neural pequena.



Modelos candidatos:



\- Logistic Regression;

\- Decision Tree;

\- Random Forest;

\- Gradient Boosting;

\- Multi-Layer Perceptron.



A rede neural será usada como etapa posterior, quando o dataset final e a variável-alvo estiverem validados.



\## Escopo da V1



A V1 deve entregar:



\- repositório organizado;

\- inventário de datasets;

\- definição clara do problema;

\- dataset final mínimo em formato país-ano;

\- análise exploratória inicial;

\- modelo baseline;

\- avaliação preliminar;

\- documentação metodológica;

\- material para qualificação acadêmica.



\## Fora do escopo da V1



A V1 não pretende:



\- prever diretamente a ocorrência de uma Terceira Guerra Mundial;

\- produzir previsões determinísticas;

\- garantir capacidade operacional de previsão real;

\- integrar todas as fontes possíveis de dados;

\- construir um sistema Big Data completo em produção.



\## Expansão futura



Após a V1, o projeto poderá evoluir para:



\- inclusão de mais fontes econômicas e sociais;

\- integração com World Bank Open Data;

\- integração com ACLED;

\- criação de features regionais;

\- análise de importância de variáveis;

\- calibração probabilística;

\- dashboards e visualizações web;

\- comparação entre modelos;

\- melhoria da documentação acadêmica;

\- publicação de uma versão de portfólio mais avançada.



\## Diretriz metodológica



O projeto deve ser tratado como uma abordagem exploratória e probabilística.



O objetivo não é prever conflitos com certeza, mas estudar padrões históricos e construir um pipeline reprodutível para análise de risco com base em dados tabulares e temporais.



\## Decisão atual



A direção técnica validada para a V1 é:



\- unidade de análise: país-ano;

\- base central: UCDP Organized Violence Country-Year;

\- tipo de problema: classificação supervisionada;

\- alvo inicial: conflito ou intensificação no ano seguinte;

\- abordagem: baseline clássico seguido de rede neural pequena;

\- foco: robustez metodológica antes de complexidade.

