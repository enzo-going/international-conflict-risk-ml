# Revisão de Consolidação do Projeto

## 1. Objetivo deste documento

Este documento consolida o estado atual do projeto **Sistema Machine Learning de Análise Preditiva de Conflitos Internacionais** após a integração de novas fontes de dados, scripts experimentais e módulos complementares.

O objetivo é separar claramente:

- o pipeline principal validado;
- os datasets oficiais e candidatos;
- os módulos experimentais;
- os resultados que podem ser apresentados;
- os pontos que ainda exigem cuidado metodológico.

---

## 2. Problema central do projeto

A motivação original do projeto envolvia a análise de tensões internacionais, escalada de conflitos e risco de grandes crises globais.

Durante o desenvolvimento, a ideia foi reformulada para uma tarefa mensurável de Machine Learning:

> Dado o histórico de violência organizada e indicadores associados a um país em determinado ano, é possível estimar a ocorrência de violência organizada no ano seguinte com desempenho superior a uma baseline simples de persistência?

Essa reformulação torna o problema mais adequado para aprendizado supervisionado, pois trabalha com uma unidade observável:

- país;
- ano;
- histórico recente;
- target binário;
- avaliação temporal.

---

## 3. Pipeline principal validado

O pipeline principal do projeto trabalha com estrutura `country-year`.

### Unidade de análise

Cada linha representa um país em um determinado ano.

### Target principal

`target_conflict_next_year`

Esse alvo indica se há ocorrência de violência organizada no ano seguinte.

### Fontes centrais

As fontes centrais atuais são:

- UCDP Organized Violence;
- features temporais derivadas do histórico de conflito;
- indicadores World Bank integrados ao pipeline principal;
- outputs finais do modelo principal.

### Modelo principal atual

O modelo principal atual é:

`Logistic Regression + World Bank all raw`

Esse modelo foi mantido como principal por combinar:

- desempenho superior à baseline;
- interpretabilidade;
- simplicidade metodológica;
- compatibilidade com explicação por coeficientes;
- adequação ao escopo acadêmico do projeto.

---

## 4. Resultado preditivo atual

A camada de análise preditiva por país utiliza o ano-base mais recente do dataset final para gerar uma estimativa de risco para o ano seguinte.

Estado atual registrado nos outputs:

- ano-base: 2023;
- ano previsto: 2024;
- países avaliados: 194;
- probabilidade média estimada: aproximadamente 0.3427;
- países em risco alto ou muito alto: 59;
- previsões positivas pelo threshold atual: 60;
- casos positivos observados: 58.

A interpretação correta desses resultados é probabilística e experimental.

O modelo não afirma que um conflito ocorrerá com certeza. Ele estima risco com base nos padrões aprendidos a partir dos dados históricos e das features disponíveis.

---

## 5. Validação automática

O projeto possui validação automática dos principais artefatos.

Estado atual:

- total de checks: 79;
- checks aprovados: 79;
- falhas: 0.

Isso indica que, no estado atual, os principais arquivos esperados, schemas, outputs e relatórios estão consistentes.

A validação automática não prova que o modelo está perfeito, mas garante que o pipeline não está quebrado estruturalmente.

---

## 6. Auditoria de datasets

A auditoria atual reconhece 33 datasets no projeto.

Resumo atual:

- datasets oficiais/candidatos: 11;
- experimentais: 4;
- dados brutos de suporte: 16;
- não prontos/rejeitados: 2.

Essa auditoria é importante porque o projeto passou a ter múltiplas contribuições paralelas. Nem todo dataset deve entrar automaticamente no pipeline principal.

Critérios para entrada no pipeline oficial:

- possuir chave temporal clara;
- possuir chave geográfica clara;
- ser compatível com a estrutura `country-year`;
- ter relação metodológica plausível com o target;
- não introduzir vazamento temporal;
- conseguir ser reproduzido por script.

---

## 7. Módulos experimentais

O projeto possui módulos experimentais que foram preservados, mas não devem ser confundidos com o pipeline principal.

### Exemplos

- UCDP One-Sided Violence;
- WWI;
- WWII;
- modelos de mortes e escalada histórica;
- notebooks exploratórios de guerras mundiais.

Esses módulos podem ser úteis para expansão futura, mas atualmente possuem limitações como:

- granularidade diferente;
- target diferente;
- estrutura temporal diferente;
- ausência de integração completa ao pipeline `country-year`;
- risco de confundir análise histórica com previsão operacional.

Portanto, eles devem ser apresentados como experimentos complementares, não como evidência central do desempenho do modelo principal.

---

## 8. Novas fontes adicionadas

Foram adicionadas fontes relacionadas a World Bank e PRIO, incluindo indicadores como:

- inflação;
- taxa de juros real;
- crescimento do PIB;
- PIB per capita;
- dados PRIO de conflito;
- datasets limpos e brutos relacionados.

Essas fontes aumentam a riqueza potencial do projeto, mas nem todas devem ser integradas imediatamente ao modelo principal sem revisão.

A etapa correta é:

1. auditar;
2. padronizar;
3. transformar para `country-year`;
4. testar ganho de desempenho;
5. comparar contra baseline;
6. documentar impacto.

---

## 9. O que pode ser apresentado ao professor

O projeto já pode ser apresentado como um sistema acadêmico funcional com:

- pipeline de Machine Learning supervisionado;
- problema reformulado de forma mensurável;
- integração de dados heterogêneos;
- baseline de persistência;
- comparação de modelos;
- análise preditiva por país;
- explicabilidade aproximada;
- auditoria de datasets;
- validação automática;
- camada de dashboard;
- scripts de setup para reprodutibilidade.

A narrativa correta é:

> O projeto não prevê deterministicamente uma guerra mundial. Ele constrói uma base metodológica para estimar risco de violência organizada em escala país-ano, com possibilidade futura de evoluir para índices agregados de escalada sistêmica.

---

## 10. O que não deve ser prometido

Ainda não deve ser prometido:

- previsão direta de Terceira Guerra Mundial;
- causalidade entre features e conflito;
- integração completa de todos os datasets;
- precisão operacional para decisões reais;
- calibração probabilística perfeita;
- generalização geopolítica sem ressalvas;
- uso dos módulos WWI/WWII como modelo principal.

---

## 11. Próximas ações recomendadas

Antes da entrega final, as próximas ações devem ser:

1. atualizar o README para refletir 33 datasets e 79 checks;
2. revisar o dashboard oficial para reduzir seções desatualizadas;
3. destacar a análise preditiva por país;
4. separar visualmente pipeline oficial e módulos experimentais;
5. documentar as novas fontes World Bank/PRIO como candidatas;
6. evitar adicionar novos datasets sem ganho claro;
7. preparar uma narrativa final de apresentação.

---

## 12. Conclusão

O projeto está tecnicamente mais forte do que parece à primeira vista, mas precisa de consolidação narrativa.

A principal força atual está no fato de que há um pipeline funcional, validado e reproduzível, com análise preditiva por país e auditoria de datasets.

A principal fragilidade está na dispersão causada por múltiplos módulos experimentais e contribuições paralelas.

A direção correta é preservar esses módulos como expansão futura, enquanto o pipeline principal permanece centrado na previsão `country-year` de violência organizada no ano seguinte.
