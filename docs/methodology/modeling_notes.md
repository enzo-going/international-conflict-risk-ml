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
