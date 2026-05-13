\# UCDP Organized Violence Country-Year Notes



Notas técnicas iniciais sobre o dataset `organizedviolencecy\_v25\_1.xlsx`.



\## Arquivo bruto



Caminho no projeto:



`data/raw/ucdp/organizedviolencecy\_v25\_1.xlsx`



\## Estrutura inicial



Inspeção inicial:



\- abas: `Sheet1`

\- linhas: 6936

\- colunas: 74

\- granularidade: país-ano



\## Colunas de identificação



As principais colunas de identificação são:



\- `country\_id\_cy`

\- `country\_cy`

\- `year\_cy`

\- `region\_cy`

\- `main\_govt\_name\_cy`



\## Grupos de variáveis



\### State-based violence



Variáveis relacionadas a conflitos com participação estatal:



\- `sb\_exist\_cy`

\- `sb\_dyad\_count\_cy`

\- `sb\_total\_deaths\_best\_cy`

\- `sb\_intrastate\_exist\_cy`

\- `sb\_intrastate\_deaths\_best\_cy`

\- `sb\_interstate\_exist\_cy`

\- `sb\_interstate\_deaths\_best\_cy`



\### Non-state violence



Variáveis relacionadas a conflitos entre atores não estatais:



\- `ns\_exist\_cy`

\- `ns\_dyad\_count\_cy`

\- `ns\_total\_deaths\_best\_cy`



\### One-sided violence



Variáveis relacionadas a violência unilateral:



\- `os\_exist\_cy`

\- `os\_dyad\_count\_cy`

\- `os\_total\_deaths\_best\_cy`



\### Cumulative violence



Variáveis acumuladas de mortes por violência organizada:



\- `cumulative\_total\_deaths\_in\_orgvio\_best\_cy`



\## Colunas candidatas para o dataset processado inicial



A dataset processado inicial deve priorizar colunas numéricas e categóricas simples:



\- `country\_id\_cy`

\- `country\_cy`

\- `year\_cy`

\- `region\_cy`

\- `sb\_exist\_cy`

\- `sb\_dyad\_count\_cy`

\- `sb\_total\_deaths\_best\_cy`

\- `sb\_intrastate\_exist\_cy`

\- `sb\_intrastate\_deaths\_best\_cy`

\- `sb\_interstate\_exist\_cy`

\- `sb\_interstate\_deaths\_best\_cy`

\- `ns\_exist\_cy`

\- `ns\_dyad\_count\_cy`

\- `ns\_total\_deaths\_best\_cy`

\- `os\_exist\_cy`

\- `os\_dyad\_count\_cy`

\- `os\_total\_deaths\_best\_cy`

\- `cumulative\_total\_deaths\_in\_orgvio\_best\_cy`

\- `version`



\## Colunas mantidas fora do dataset inicial



Colunas textuais extensas, como nomes de díades, devem ficar fora da dataset processado inicial:



\- `sb\_dyad\_names\_cy`

\- `sb\_intrastate\_dyad\_names\_cy`

\- `sb\_interstate\_dyad\_names\_cy`

\- `ns\_dyad\_names\_cy`

\- `os\_dyad\_names\_cy`



Essas colunas podem ser úteis para análise qualitativa, mas não serão prioridade na primeira modelagem tabular.



\## Possíveis variáveis-alvo



A definição final do target ainda será validada.



Possíveis targets:



\- `target\_conflict\_next\_year`

\- `target\_state\_based\_conflict\_next\_year`

\- `target\_intensification\_next\_year`



A opção mais simples para baseline será prever se um país terá conflito organizado no ano seguinte.



\## Decisão inicial



O dataset UCDP Organized Violence Country-Year será a base central da fase inicial.



A primeira etapa técnica será criar uma versão processada enxuta em `data/processed/`, preservando apenas colunas essenciais para análise exploratória e construção da primeira variável-alvo.

