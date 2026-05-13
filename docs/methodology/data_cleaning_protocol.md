\# Data Cleaning Protocol



Protocolo de limpeza, padronização e preparação de datasets para o projeto `international-conflict-risk-ml`.



Este documento define regras mínimas para que datasets diferentes possam ser integrados futuramente em uma estrutura comum de análise, especialmente no formato `country-year`.



\## Objetivo



Evitar que cada dataset seja tratado de forma isolada e incompatível.



Todo dataset incorporado ao projeto deve passar por uma etapa mínima de documentação, limpeza e padronização antes de ser considerado para modelagem.



\## Estrutura esperada dos dados



Sempre que possível, os datasets devem ser organizados ou agregados para uma das seguintes granularidades:



1\. `event-level` — uma linha por evento;

2\. `country-year` — uma linha por país e ano;

3\. `global-year` — uma linha por ano, quando o dado não possuir país específico.



A prioridade da fase inicial é a estrutura:



`country-year`



\## Regras gerais de padronização



\### 1. Nome de arquivos



Usar nomes em inglês, minúsculos e com `\_`.



Exemplos:



\- `ucdp\_organized\_violence\_country\_year.csv`

\- `ucdp\_one\_sided\_violence.csv`

\- `nuclear\_features\_year.csv`



Evitar:



\- espaços;

\- acentos;

\- nomes muito longos;

\- nomes genéricos como `dados\_limpos.csv`.



\### 2. Nome de colunas



Todas as colunas devem seguir `snake\_case`.



Exemplos:



\- `country`

\- `country\_code`

\- `year`

\- `region`

\- `state\_based\_deaths`

\- `one\_sided\_deaths`



Evitar:



\- espaços;

\- acentos;

\- letras maiúsculas;

\- símbolos desnecessários.



\### 3. Colunas temporais



Todo dataset precisa ter uma coluna temporal clara.



Prioridade:



\- `year`

\- `date`

\- `month`

\- `month\_year`



Para a fase inicial, a coluna mais importante é:



`year`



\### 4. Colunas geográficas



Quando possível, o dataset deve conter:



\- `country`

\- `country\_code`

\- `region`



Se não houver país, o dataset pode ser tratado como `global-year`, desde que isso seja documentado.



\### 5. Valores ausentes



Valores ausentes devem ser tratados de forma explícita.



Regras iniciais:



\- não apagar linhas sem avaliar impacto;

\- registrar quantidade de valores ausentes;

\- não preencher valores críticos automaticamente sem justificativa;

\- documentar qualquer imputação.



\### 6. Tipos de dados



Tipos esperados:



\- `year`: inteiro;

\- contagens: inteiro;

\- mortes/valores acumulados: numérico;

\- categorias: texto padronizado;

\- flags binárias: `0` ou `1`.



\### 7. Duplicatas



Antes de salvar um dataset tratado, verificar duplicatas.



Para dados `country-year`, a combinação ideal deve ser única:



`country + year`



ou:



`country\_code + year`



\### 8. Agregações



Quando um dataset estiver em nível de evento, ele pode ser agregado para `country-year`.



Exemplos de agregação:



\- contagem de eventos por país e ano;

\- soma de mortes por país e ano;

\- média anual de indicadores;

\- máximo anual de intensidade;

\- número de atores distintos.



Toda agregação deve ser documentada.



\## Camadas de dados



\### data/raw/



Contém arquivos originais, sem alteração manual.



Regras:



\- preservar nomes originais quando fizer sentido;

\- não editar arquivos brutos;

\- manter referência da fonte.



\### data/interim/



Contém arquivos parcialmente tratados.



Exemplos:



\- colunas renomeadas;

\- encoding corrigido;

\- tipos convertidos;

\- filtros básicos aplicados.



\### data/processed/



Contém datasets padronizados e prontos para análise exploratória.



Exemplos:



\- dados UCDP padronizados;

\- datasets agregados por país-ano;

\- features auxiliares por ano.



\### data/final/



Contém o dataset final usado para modelagem.



Regra:



\- deve ser gerado por script;

\- não deve ser editado manualmente;

\- deve possuir documentação clara das features e do target.



\## Documentação obrigatória por dataset



Cada dataset incorporado deve ter, no mínimo:



\- nome do arquivo;

\- fonte;

\- link da fonte;

\- data de acesso;

\- descrição;

\- granularidade;

\- período coberto;

\- colunas principais;

\- transformações aplicadas;

\- limitações conhecidas;

\- status no projeto.



\## Padrão de saída recomendado



Para cada dataset importante, gerar preferencialmente:



1\. versão limpa;

2\. versão agregada para `country-year` ou `global-year`;

3\. dicionário de dados.



Exemplo:



\- `ucdp\_organized\_violence\_clean.csv`

\- `ucdp\_organized\_violence\_country\_year.csv`

\- `ucdp\_organized\_violence\_dictionary.md`



\## Decisões metodológicas da fase inicial



Para a fase inicial, a prioridade será:



1\. preservar os arquivos brutos;

2\. padronizar primeiro o UCDP Organized Violence Country-Year;

3\. criar uma base final mínima em formato `country-year`;

4\. definir o alvo preditivo somente após validar as colunas da base central;

5\. evitar datasets sintéticos ou opinativos como variável-alvo.



\## Datasets com cautela



Alguns datasets devem ser usados apenas com cuidado ou mantidos fora da fase inicial:



\- cenários de WW3;

\- dados sintéticos ou narrativos;

\- datasets sem país ou ano;

\- datasets de domínio muito distante, como intrusão em sensores;

\- arquivos com inconsistência geográfica grave.



\## Regra final



Nenhum dataset deve entrar em `data/final/` sem:



\- fonte conhecida;

\- estrutura documentada;

\- transformações reproduzíveis;

\- compatibilidade com o objetivo do projeto;

\- validação mínima de colunas, tipos e duplicatas.

