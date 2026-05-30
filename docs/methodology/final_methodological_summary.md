# Resumo Metodológico Final

Este documento consolida a formulação metodológica do projeto **International Conflict Risk ML**.

O objetivo é organizar, em uma narrativa única, as decisões técnicas tomadas durante o desenvolvimento do pipeline principal, os resultados obtidos, os módulos complementares em revisão e as limitações metodológicas do sistema.

Este arquivo deve servir como base para:

- apresentação acadêmica;
- explicação oral do projeto;
- relatório de qualificação;
- revisão final do README;
- alinhamento entre os integrantes do grupo.

---

## 1. Problema original e reformulação técnica

A motivação inicial do projeto partiu de uma questão ampla sobre tensões globais, escalada de conflitos e possibilidade de grandes crises internacionais.

Essa formulação inicial era interessante como tema, mas ampla demais para ser tratada diretamente como problema de Machine Learning. Prever uma guerra mundial ou um evento geopolítico específico exigiria hipóteses fortes, dados difíceis de padronizar e uma definição objetiva de target extremamente problemática.

Por isso, o problema foi reformulado de forma mais defensável:

**estimar, de maneira experimental e probabilística, se um país apresentará violência organizada no ano seguinte, com base em dados históricos, features temporais e indicadores externos.**

Essa reformulação torna o projeto mais adequado para Machine Learning porque permite definir:

- unidade de análise;
- variável-alvo;
- base histórica;
- baseline;
- modelo supervisionado;
- métricas quantitativas;
- avaliação temporal;
- comparação entre algoritmos.

A proposta não é prever eventos geopolíticos de forma absoluta. A proposta é construir um pipeline experimental capaz de identificar padrões históricos associados à persistência ou ocorrência futura de violência organizada.

---

## 2. Unidade de análise

A unidade principal do projeto é:

**country-year**

Isso significa que cada linha do dataset principal representa um país em um determinado ano.

Essa escolha foi importante porque:

- é compatível com bases históricas de conflito;
- permite integração com indicadores socioeconômicos anuais;
- facilita a criação de features temporais;
- permite avaliação por split temporal;
- reduz a complexidade em comparação com dados em nível de evento, ator ou díade.

A escolha por `country-year` também define o limite metodológico do projeto. O modelo principal não prevê batalhas, eventos individuais, relações diplomáticas específicas ou conflitos entre pares de países. Ele estima risco de violência organizada em nível agregado por país e ano.

---

## 3. Target supervisionado

O target principal do projeto é:

**target_conflict_next_year**

Esse target indica se um país apresentará violência organizada no ano seguinte.

A lógica é:

- usar informações disponíveis até o ano atual;
- prever se haverá conflito no próximo ano;
- avaliar o desempenho em anos posteriores.

Essa formulação evita transformar o modelo em uma simples classificação do presente. O objetivo não é apenas identificar se existe conflito no ano atual, mas testar se os dados históricos e indicadores externos possuem capacidade preditiva para o ano seguinte.

---

## 4. Fonte central de dados

A base central do projeto é o **UCDP Organized Violence Country-Year Dataset**.

Essa fonte foi escolhida porque já possui estrutura próxima da unidade desejada do projeto: país-ano.

A partir dela, o pipeline constrói ou utiliza variáveis relacionadas a:

- existência de violência organizada;
- conflitos state-based;
- conflitos intrastate;
- conflitos interstate;
- conflitos non-state;
- violência one-sided;
- contagem de díades;
- fatalidades;
- histórico cumulativo de mortes;
- região;
- identificação de país e ano.

Essa base funciona como a fundação do projeto. Outras fontes externas podem enriquecer o modelo, mas não substituem a estrutura central baseada em UCDP.

---

## 5. Integração com World Bank

A principal fonte externa integrada ao pipeline atual é o **World Bank Open Data**.

A integração com World Bank foi usada para adicionar variáveis socioeconômicas ao dataset principal.

Entre as variáveis utilizadas estão:

- população total;
- crescimento populacional;
- percentual de população urbana;
- PIB per capita;
- crescimento do PIB;
- inflação;
- desemprego;
- matrícula escolar secundária;
- gasto militar como percentual do PIB;
- renda de recursos naturais como percentual do PIB.

A hipótese é que fatores socioeconômicos podem complementar o histórico direto de conflito, ajudando o modelo a capturar padrões estruturais associados à instabilidade ou persistência de violência organizada.

A integração com World Bank também reforça a natureza heterogênea do projeto, pois combina dados de conflito com indicadores econômicos, sociais e demográficos.

---

## 6. Engenharia de features temporais

Além das variáveis diretas de conflito, foram criadas features temporais.

Essas features procuram capturar persistência histórica, recorrência e intensidade recente de conflito.

Exemplos:

- conflito no ano anterior;
- contagem de conflito nos últimos 3 anos;
- contagem de conflito nos últimos 5 anos;
- mortes no ano anterior;
- soma de mortes nos últimos 3 anos;
- soma de mortes nos últimos 5 anos;
- anos desde o último conflito.

Essa etapa é central porque conflitos apresentam forte dependência temporal. Um país que teve violência organizada recentemente tende a ter maior probabilidade de continuar apresentando instabilidade nos anos seguintes.

Por esse motivo, uma baseline simples de persistência já apresenta desempenho elevado. O modelo de Machine Learning precisa ser comparado contra essa baseline para demonstrar ganho real.

---

## 7. Baseline de persistência

A baseline principal do projeto é a persistência de conflito.

A regra da baseline é:

**se o país teve violência organizada no ano atual, prever violência organizada no ano seguinte.**

Em termos práticos:

**y_pred = organized_violence_exists**

Essa baseline é forte, simples e metodologicamente necessária.

Ela representa a hipótese de que o melhor preditor inicial de conflito futuro é a existência de conflito recente. Como conflitos têm continuidade histórica, qualquer modelo mais complexo precisa superar essa referência para justificar sua utilidade.

No projeto atual, a baseline alcançou:

| Modelo | Accuracy | Precision | Recall | F1-score |
|---|---:|---:|---:|---:|
| Persistence baseline | 0.9072 | 0.8571 | 0.8571 | 0.8571 |

Esse resultado confirma que o problema possui forte componente temporal e que não basta treinar um algoritmo mais complexo sem comparar contra um ponto de referência adequado.

---

## 8. Modelo principal

O modelo principal atual é:

**Logistic Regression scaled - World Bank all raw**

A configuração geral envolve:

- imputação de valores ausentes;
- padronização das features;
- regressão logística;
- balanceamento de classes;
- split temporal;
- comparação com baseline.

A regressão logística foi mantida como modelo principal porque combina:

- bom desempenho;
- interpretabilidade;
- estabilidade;
- simplicidade metodológica;
- possibilidade de análise de coeficientes;
- desempenho superior à baseline.

O resultado principal atual é:

| Modelo | Accuracy | Precision | Recall | F1-score |
|---|---:|---:|---:|---:|
| Logistic Regression + World Bank all raw | 0.9197 | 0.9029 | 0.8435 | 0.8722 |

O ganho em relação à baseline de persistência foi de aproximadamente:

**+0.0151 em F1-score**

Esse ganho é modesto, mas metodologicamente relevante, porque mostra que a integração de indicadores externos e features temporais consegue superar uma baseline forte.

---

## 9. Comparação com modelos candidatos

Além da regressão logística, foram testados modelos candidatos usando o mesmo split temporal e o mesmo conjunto de features.

Modelos avaliados:

- Persistence baseline;
- Logistic Regression;
- Random Forest;
- Gradient Boosting;
- MLP simples.

Resultado resumido:

| Modelo | Accuracy | Precision | Recall | F1-score | Diferença vs baseline |
|---|---:|---:|---:|---:|---:|
| Logistic Regression + World Bank all raw | 0.9197 | 0.9029 | 0.8435 | 0.8722 | +0.0151 |
| Random Forest + World Bank all raw | 0.9124 | 0.8594 | 0.8730 | 0.8661 | +0.0090 |
| Gradient Boosting + World Bank all raw | 0.9138 | 0.9197 | 0.8050 | 0.8585 | +0.0014 |
| Persistence baseline | 0.9072 | 0.8571 | 0.8571 | 0.8571 | 0.0000 |
| MLP + World Bank all raw | 0.9094 | 0.9206 | 0.7891 | 0.8498 | -0.0073 |

A comparação mostrou que modelos mais complexos não superaram a regressão logística no critério principal de F1-score.

O Random Forest apresentou maior recall, mas com redução de precision. Isso sugere que ele pode ser útil como modelo alternativo mais sensível, mas não como substituto direto do modelo principal.

O Gradient Boosting apresentou alta precision, mas recall menor. A MLP simples não superou a baseline de persistência.

A decisão metodológica foi manter a regressão logística como modelo principal.

---

## 10. Interpretação dos coeficientes

A análise de coeficientes da regressão logística foi usada para identificar quais variáveis mais influenciam a predição.

Entre as variáveis mais importantes aparecem:

- contagem de díades non-state;
- contagem de díades state-based;
- contagem de díades one-sided;
- conflito nos últimos 5 anos;
- existência de violência organizada;
- anos desde o último conflito;
- PIB per capita;
- matrícula escolar secundária;
- crescimento populacional;
- crescimento do PIB;
- população total;
- renda de recursos naturais.

A presença de variáveis UCDP no topo confirma que o histórico direto de conflito ainda é o componente mais forte do modelo.

A presença de variáveis World Bank entre os coeficientes relevantes indica que indicadores externos adicionam informação, mesmo que o ganho final seja moderado.

---

## 11. Camada SQL e banco SQLite

O projeto possui uma camada SQL baseada em SQLite.

Essa camada transforma artefatos do pipeline em uma estrutura relacional consultável.

Ela inclui tabelas como:

- country_year_features;
- model_predictions;
- model_metrics;
- model_coefficients;
- candidate_model_comparison;
- dataset_metadata.

A camada SQL permite consultar:

- países e anos com maior risco previsto;
- falsos positivos;
- falsos negativos;
- coeficientes mais influentes;
- métricas do modelo principal;
- comparação entre modelos candidatos.

Essa camada reforça a organização técnica do projeto e conecta a disciplina de Banco de Dados ao pipeline de Machine Learning.

O banco SQLite é gerado localmente e não é versionado no Git, pois pode ser reproduzido a partir dos CSVs e scripts do projeto.

---

## 12. Dashboard

O projeto possui um dashboard HTML publicado via GitHub Pages.

O dashboard serve como camada visual de apresentação e acompanhamento do projeto.

Ele resume:

- formulação do problema;
- arquitetura técnica;
- camadas de dados;
- comparação de modelos;
- matriz de confusão;
- interpretação do modelo;
- análise probabilística;
- módulo futuro de termômetro experimental de escalada.

O dashboard não substitui a documentação metodológica, mas ajuda a comunicar o projeto de forma mais acessível para professores, colegas e avaliadores.

---

## 13. Módulo experimental: UCDP One-Sided Violence

Além do pipeline principal, o projeto possui um módulo experimental criado a partir do dataset UCDP One-Sided Violence.

Arquivos relacionados:

- data/raw/ucdp/OneSided_v25_1.xlsx;
- data/final/UCDP_One-sided_Violence_Dataset_updated.csv;
- src/models/ml_onesided_violence.py;
- outputs/tables/one_sided_predictions.csv;
- outputs/tables/one_sided_feature_importance.csv;
- outputs/tables/neighbors.json.

Esse módulo busca prever violência unilateral no ano seguinte, usando uma lógica própria e features derivadas do histórico de violência one-sided.

A revisão metodológica classificou esse módulo como:

**experimental complementar**

Ele não substitui o modelo principal, porque:

- possui unidade de análise mais próxima de location-year;
- utiliza dataset processado específico;
- depende de vizinhança geográfica;
- exige validação adicional sobre anos finais, especialmente 2024;
- ainda precisa ser comparado com as variáveis one_sided já existentes no dataset principal.

A decisão atual é preservar o módulo, documentar seus limites e não integrá-lo ao pipeline principal antes de validação metodológica.

---

## 14. Módulos históricos e paralelos em revisão

Arquivos relacionados à Primeira Guerra Mundial foram adicionados pelo grupo em uma frente paralela.

Esses arquivos são tratados como material histórico ou experimento complementar até revisão metodológica.

A razão é que eles ainda não seguem claramente o mesmo padrão do pipeline principal:

- unidade country-year;
- target target_conflict_next_year;
- split temporal;
- comparação com baseline;
- integração com UCDP + World Bank.

A decisão atual é não misturar esses arquivos com o pipeline oficial sem validação.

---

## Camada de análise preditiva por país

Para tornar o projeto mais próximo de um sistema de análise preditiva, foi criada uma camada específica de avaliação por país.

Essa camada utiliza:

- probabilidades previstas pelo modelo principal;
- dataset final integrado em formato `country-year`;
- coeficientes extraídos da regressão logística;
- grupos de features relacionados a UCDP, persistência temporal e World Bank.

A avaliação atual considera o ano-base `2023` e estima risco para `2024`, avaliando 194 países.

Resultados resumidos:

| Item | Valor |
|---|---:|
| Probabilidade média estimada | 0.3427 |
| Países classificados como risco alto ou muito alto | 59 |
| Previsões positivas pelo threshold atual | 60 |
| Casos positivos observados no ano previsto | 58 |
| Features consideradas nas explicações | 33 |

A camada gera frases interpretáveis como:

> Para determinado país, o modelo estimou uma probabilidade de violência organizada no ano seguinte e associou essa estimativa a grupos de variáveis como histórico de conflitos UCDP, persistência temporal e indicadores World Bank.

As explicações são aproximações baseadas nos coeficientes e valores relativos das features. Elas não devem ser lidas como causalidade direta.

## Módulo experimental WWI/WWII

Além do pipeline principal, o repositório contém um módulo experimental relacionado à Primeira e Segunda Guerra Mundial.

Esse módulo trabalha com datasets históricos de guerras, baixas militares e civis, alianças, frentes de batalha e intensidade de mortes.

A revisão metodológica concluiu que esse módulo não deve substituir o pipeline principal, porque trabalha com outra granularidade e outro objetivo preditivo:

- pipeline principal: previsão de violência organizada no ano seguinte em estrutura `country-year`;
- módulo WWI/WWII: análise experimental de escalada e mortes em guerras históricas.

Portanto, o módulo foi preservado como expansão experimental e possível base futura para estudos de severidade, duração e escalada de guerras.

## Auditoria e governança dos datasets

Durante a execução do projeto, diferentes integrantes do grupo adicionaram datasets e arquivos derivados ao repositório.

Para evitar integração desorganizada, foi criada uma auditoria automática de datasets. Essa auditoria classifica cada arquivo de dados conforme sua compatibilidade com o pipeline principal.

A auditoria atual identificou:

| Categoria | Quantidade |
|---|---:|
| Total de datasets auditados | 35 |
| Oficiais ou candidatos ao pipeline principal | 12 |
| Experimentais em revisão | 4 |
| Dados brutos preservados para rastreabilidade | 16 |
| Não prontos para integração direta | 3 |

A decisão metodológica foi manter o pipeline principal baseado na unidade `country-year`.

Datasets que não possuem chave geográfica e temporal clara não devem ser integrados automaticamente ao modelo final. Nesses casos, eles são preservados como:

- fonte bruta de suporte;
- módulo experimental;
- material candidato para expansão futura;
- ou arquivo não pronto para integração direta.

Essa decisão evita que a adição de múltiplos datasets prejudique a consistência do target `target_conflict_next_year`, do split temporal e da interpretação do modelo.

## 15. Fontes candidatas futuras

O projeto possui um documento separado para fontes candidatas de dados.

Entre as fontes consideradas para expansão futura estão:

- Worldwide Governance Indicators — WGI;
- V-Dem Dataset;
- SIPRI Military Expenditure Database;
- Correlates of War — Formal Alliances;
- UNHCR Refugee Data;
- Fragile States Index;
- ND-GAIN Country Index;
- IMF / World Economic Outlook.

A próxima fonte sugerida no planejamento é WGI, por sua relação com governança, estabilidade institucional e risco político.

No entanto, considerando o prazo mais próximo, a decisão mais prudente é não iniciar nova integração antes de consolidar a entrega atual.

---

## 16. Limitações metodológicas

O projeto possui limitações importantes.

### 16.1 O modelo não prevê guerra mundial

O projeto não prevê uma guerra mundial de forma determinística.

A formulação atual estima risco de violência organizada em estrutura país-ano.

A ideia original de escalada global foi preservada como motivação conceitual, mas não como target direto do modelo.

### 16.2 O ganho sobre a baseline é moderado

A baseline de persistência é forte.

O modelo principal supera essa baseline, mas o ganho em F1-score é moderado.

Isso mostra que o problema é difícil e que grande parte do risco de conflito é explicada por persistência histórica.

### 16.3 O dataset é agregado

A unidade country-year reduz complexidade, mas também perde detalhes.

Eventos locais, atores específicos, alianças, choques políticos e mudanças rápidas podem não ser capturados adequadamente.

### 16.4 Variáveis externas podem ter limitações

Indicadores socioeconômicos anuais podem conter atrasos, lacunas ou problemas de cobertura.

Além disso, algumas variáveis podem ter relação indireta ou defasada com conflito.

### 16.5 Risco de circularidade

Algumas fontes futuras, especialmente índices de fragilidade ou estabilidade política, podem conter variáveis conceitualmente próximas ao próprio fenômeno de conflito.

Isso exige cuidado para evitar vazamento conceitual.

### 16.6 Interpretação probabilística

As saídas do modelo devem ser interpretadas como estimativas experimentais baseadas em padrões históricos.

Elas não devem ser lidas como previsões absolutas de eventos geopolíticos futuros.

---

## 17. Conclusão metodológica

O projeto alcançou uma versão funcional e metodologicamente defensável.

O principal resultado não é apenas o F1-score obtido, mas a construção de um pipeline completo:

- coleta e preservação de dados brutos;
- processamento e padronização;
- construção de dataset country-year;
- criação de target supervisionado;
- engenharia de features temporais;
- integração de indicadores externos;
- baseline de persistência;
- treinamento de modelo principal;
- comparação com modelos candidatos;
- análise de coeficientes;
- camada SQL;
- dashboard;
- documentação metodológica;
- classificação de módulos experimentais.

A decisão final do estágio atual é manter o pipeline UCDP + World Bank como eixo central do projeto e tratar expansões adicionais como módulos complementares ou futuras linhas de pesquisa.

O projeto deve ser apresentado como um sistema experimental de Machine Learning aplicado à análise preditiva de violência organizada, com foco em reprodutibilidade, comparação metodológica e interpretação crítica dos resultados.
