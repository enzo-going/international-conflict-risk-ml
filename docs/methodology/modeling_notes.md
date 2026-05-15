\# Modeling Notes



Notas metodológicas sobre a construção dos primeiros modelos de Machine Learning do projeto.



\## Dataset utilizado



O primeiro experimento de modelagem utiliza o arquivo:



`data/final/conflict\_country\_year\_base.csv`



Esse dataset foi construído a partir do UCDP Organized Violence Country-Year Dataset, usando a estrutura país-ano como unidade principal de análise.



\## Variável-alvo



A variável-alvo inicial é:



`target\_conflict\_next\_year`



Ela indica se um país apresentou violência organizada no ano seguinte.



\- `0`: ausência de violência organizada no ano seguinte

\- `1`: presença de violência organizada no ano seguinte



\## Variável de persistência



Foi criada também a variável:



`organized\_violence\_exists`



Ela indica se houve violência organizada no país no ano atual, considerando:



\- conflitos state-based

\- conflitos non-state

\- violência one-sided



Essa variável se mostrou muito importante porque conflitos apresentam forte persistência temporal.



\## Estratégia de divisão treino/teste



Foi adotado um split temporal, em vez de divisão aleatória.



\- treino: 1989–2016

\- teste: 2017–2023



Essa escolha evita que o modelo seja avaliado de forma artificialmente otimista por misturar passado e futuro no treinamento e no teste.



\## Distribuição do target



No conjunto completo, o target apresentou aproximadamente:



\- classe 0: 70,5%

\- classe 1: 29,5%



No conjunto de teste, a classe positiva ficou em torno de 32%.



O problema é moderadamente desbalanceado, mas não extremo.



\## Baseline de persistência



A primeira baseline usada foi

## Experimento com features temporais

Após a construção do dataset com features temporais, foi realizado um novo experimento comparando o dataset base com o dataset enriquecido por variáveis históricas de conflito.

As features temporais adicionadas foram:

- `conflict_previous_year`
- `conflict_last_3_years_count`
- `conflict_last_5_years_count`
- `deaths_previous_year`
- `deaths_last_3_years_sum`
- `deaths_last_5_years_sum`
- `years_since_last_conflict`

O mesmo split temporal foi mantido:

- treino: 1989 a 2016;
- teste: 2017 a 2023.

A baseline de persistência continuou sendo usada como referência principal:

- `y_pred = organized_violence_exists`

### Resultado principal

O melhor resultado foi obtido com Logistic Regression usando o dataset com features temporais:

| Experimento | Modelo | Accuracy | Precision | Recall | F1-score |
|---|---:|---:|---:|---:|---:|
| reference | Persistence baseline | 0.9082 | 0.8571 | 0.8571 | 0.8571 |
| dataset base | Random Forest | 0.9082 | 0.8571 | 0.8571 | 0.8571 |
| dataset temporal | Logistic Regression | 0.9133 | 0.8546 | 0.8798 | 0.8670 |
| dataset temporal | Logistic Regression scaled | 0.9162 | 0.8937 | 0.8390 | 0.8655 |

A Logistic Regression com features temporais apresentou ganho de aproximadamente `+0.0099` em F1-score em relação à baseline de persistência.

### Interpretação

O ganho observado é pequeno, mas metodologicamente relevante. Ele indica que as features temporais adicionam algum sinal preditivo além da simples persistência do conflito no ano atual.

Ao mesmo tempo, a melhora modesta reforça que a ocorrência de violência organizada possui forte dependência temporal. Portanto, a baseline de persistência deve continuar sendo tratada como referência obrigatória em qualquer experimento posterior.

A Logistic Regression sem escalonamento apresentou aviso de convergência, então seus resultados devem ser interpretados com cautela. A versão com StandardScaler apresentou desempenho próximo, maior precisão e maior estabilidade numérica, embora com recall menor.

Para a qualificação, este resultado deve ser apresentado como evidência de evolução metodológica: a engenharia temporal melhora levemente o desempenho, mas ainda não elimina a força da persistência histórica como principal padrão observado.

## Experimento com indicadores World Bank

Após a integração dos indicadores socioeconômicos do World Bank, foi criado o dataset `conflict_country_year_world_bank.csv`, combinando informações históricas de conflito, features temporais e variáveis externas por país-ano.

A comparação foi feita no mesmo conjunto de países e anos do dataset integrado, para evitar uma comparação injusta entre amostras diferentes.

Foram avaliados dois grupos principais:

- `temporal_only`: features de conflito + features temporais;
- `temporal_world_bank`: features de conflito + features temporais + indicadores World Bank.

A baseline de persistência permaneceu como referência principal.

### Resultado principal

| Experimento | Modelo | Accuracy | Precision | Recall | F1-score | Diferença vs persistência |
|---|---:|---:|---:|---:|---:|---:|
| reference | Persistence baseline | 0.9072 | 0.8571 | 0.8571 | 0.8571 | 0.0000 |
| temporal_only | Logistic Regression scaled | 0.9161 | 0.8959 | 0.8390 | 0.8665 | +0.0094 |
| temporal_world_bank | Logistic Regression scaled | 0.9153 | 0.8918 | 0.8413 | 0.8658 | +0.0087 |
| temporal_world_bank | Random Forest | 0.9043 | 0.8344 | 0.8798 | 0.8565 | -0.0006 |
| temporal_world_bank | Decision Tree | 0.9013 | 0.8218 | 0.8889 | 0.8540 | -0.0031 |

### Interpretação

A inclusão inicial dos indicadores World Bank não superou o melhor modelo baseado apenas em features temporais. O melhor F1-score continuou sendo obtido pelo experimento `temporal_only` com Logistic Regression scaled.

No entanto, os modelos com World Bank apresentaram aumento de recall em alguns casos, especialmente Decision Tree e Random Forest. Isso indica que os indicadores externos podem aumentar a sensibilidade para identificar países que terão conflito no ano seguinte, mas também aumentaram falsos positivos, reduzindo a precisão e limitando o ganho em F1-score.

Esse resultado não invalida a integração de dados heterogêneos. Ele indica que a simples adição de indicadores socioeconômicos brutos não é suficiente. A próxima etapa deve envolver engenharia de features sobre os indicadores World Bank, incluindo variações temporais, defasagens, médias móveis e flags de valores ausentes.

## Experimento com features derivadas do World Bank

Após a integração inicial dos indicadores World Bank, foi criada uma nova camada de engenharia de features socioeconômicas temporais.

As features derivadas incluíram:

- valores defasados em 1 ano (`lag1`);
- variações anuais (`change_1y`);
- médias móveis de 3 anos (`rolling_3y_mean`);
- flags de ausência (`missing`).

O objetivo foi testar se os indicadores socioeconômicos externos, quando transformados temporalmente, agregam mais sinal preditivo do que os valores brutos.

### Resultado principal

| Experimento | Modelo | Accuracy | Precision | Recall | F1-score | Diferença vs persistência |
|---|---:|---:|---:|---:|---:|---:|
| reference | Persistence baseline | 0.9072 | 0.8571 | 0.8571 | 0.8571 | 0.0000 |
| temporal_only | Logistic Regression scaled | 0.9161 | 0.8959 | 0.8390 | 0.8665 | +0.0094 |
| temporal_world_bank_raw | Logistic Regression scaled | 0.9153 | 0.8918 | 0.8413 | 0.8658 | +0.0087 |
| temporal_world_bank_engineered | Logistic Regression scaled | 0.9183 | 0.8929 | 0.8503 | 0.8711 | +0.0139 |
| temporal_world_bank_engineered | Random Forest | 0.9116 | 0.8512 | 0.8821 | 0.8664 | +0.0092 |

### Interpretação

As features derivadas do World Bank produziram o melhor desempenho observado até o momento. O modelo `temporal_world_bank_engineered` com Logistic Regression scaled alcançou F1-score de `0.8711`, superando a baseline de persistência, o modelo temporal puro e o modelo com World Bank bruto.

Esse resultado indica que os indicadores socioeconômicos externos podem contribuir para a previsão, mas principalmente quando transformados em sinais temporais, como defasagens, variações anuais e médias móveis.

A melhora ainda é moderada, mas metodologicamente importante, pois mostra que a integração de dados heterogêneos não deve ser feita apenas pela adição direta de colunas. A engenharia de atributos é uma etapa central para extrair valor preditivo desses dados.
