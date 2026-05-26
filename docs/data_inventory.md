\# Dataset Inventory



Inventário inicial dos datasets considerados para o projeto `international-conflict-risk-ml`.



Este documento organiza as bases disponíveis, avalia sua utilidade para o projeto e define uma prioridade inicial de uso. O objetivo é evitar coleta desorganizada de dados e manter uma base técnica clara para a construção do dataset final.



\## Estratégia inicial



A fase técnica inicial do projeto será construída em torno de uma unidade de análise `country-year`.



A base central será o UCDP Organized Violence Country-Year Dataset, por já apresentar dados estruturados por país e ano, o que facilita a integração com variáveis históricas e a construção de modelos de Machine Learning.



\## Critérios de avaliação



Cada dataset será avaliado pelos seguintes critérios:



\- possui dimensão temporal clara;

\- possui país, região ou código geográfico;

\- pode ser agregado para estrutura país-ano;

\- possui relação direta ou indireta com risco de conflito;

\- tem fonte confiável;

\- apresenta viabilidade de integração no prazo do projeto.



\## Inventário inicial



| Dataset | Fonte | Status | Prioridade | Função no projeto | Observações |

|---|---|---|---|---|---|

| UCDP Organized Violence Country-Year | UCDP | disponível | alta | base central | Melhor candidato para estruturar o dataset final em país-ano |

| UCDP One-sided Violence | UCDP | disponível | alta | feature complementar | Pode representar violência unilateral e ataques contra civis |

| UCDP Conflict Issues | UCDP | disponível | média | feature complementar | Pode ajudar a classificar tipos ou temas de conflito |

| Nuclear Explosions Dataset | Kaggle | limpo/parcialmente tratado | média | feature histórica global | Útil como indicador militar/nuclear agregado por ano |

| Nuclear Features | derivado interno | disponível | média | feature anual global | Já parece estar agregado por ano |

| Strategic Military Operations | Kaggle | bruto | baixa/média | possível feature militar | Precisa validação; há indícios de problemas em latitude/longitude |

| World War I Details | Kaggle | bruto | baixa | contexto histórico | Não deve ser usado como base principal de ML |

| World War II Details | Kaggle | bruto | baixa | contexto histórico | Pode servir apenas como referência contextual |

| World War III Risk Scenarios | Kaggle | bruto | baixa/descartável | material exploratório | Risco alto de ser dataset sintético/opinativo; não usar como alvo principal |

| Land Mines Dataset | UCI/Kaggle | bruto | baixa | incerto | Relação com conflito precisa ser validada |

| WSN Intrusion Dataset | UCI | bruto | descartável | fora do escopo principal | Dataset de intrusão/sensores, pouco relacionado a conflitos internacionais |



\## Decisão inicial



A fase inicial do projeto deve priorizar:



1\. UCDP Organized Violence Country-Year como base central;

2\. UCDP One-sided Violence como feature complementar;

3\. UCDP Conflict Issues como feature complementar;

4\. Nuclear Features como variável global histórica por ano.



Datasets de guerras mundiais e cenários de WW3 não devem ser usados como alvo principal, pois podem gerar problemas metodológicos e comprometer a validade acadêmica do modelo.



\## Próximas ações



\- \[ ] Validar colunas principais do UCDP Organized Violence Country-Year

\- \[ ] Definir variável-alvo inicial

\- \[ ] Definir se o alvo será ocorrência de conflito ou intensificação de conflito

\- \[ ] Mapear chaves de integração por país e ano

\- \[ ] Criar protocolo de limpeza e padronização dos datasets

\- \[ ] Separar datasets descartados, secundários e prioritários

## UCDP One-sided Violence — arquivos adicionados pelo grupo

Foram adicionados dois arquivos relacionados à violência unilateral:

| Arquivo | Camada | Status | Observação |
|---|---|---|---|
| `data/raw/ucdp/OneSided_v25_1.xlsx` | raw | em revisão | Dataset bruto UCDP One-Sided Violence. |
| `data/final/UCDP_One-sided_Violence_Dataset_updated.csv` | final/provisório | em revisão | Versão simplificada com `year`, `actor_name`, `location` e `best_fatality_estimate`. |

Esses arquivos ainda não fazem parte do pipeline principal.

Antes de integrar ao modelo, é necessário comparar essas informações com as variáveis já existentes no dataset principal:

- `one_sided_violence_exists`
- `one_sided_dyad_count`
- `one_sided_deaths_best`

Decisão provisória: manter como material em revisão até validação metodológica.
