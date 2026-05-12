\# Modeling Notes



Notas metodológicas sobre a construção dos primeiros modelos de Machine Learning do projeto.



\## Dataset utilizado



O primeiro experimento de modelagem utiliza o arquivo:



`data/final/conflict\_country\_year\_v1.csv`



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

