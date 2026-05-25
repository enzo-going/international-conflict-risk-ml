# UCDP One-Sided Violence Dataset

Arquivo bruto adicionado ao projeto:

data/raw/ucdp/OneSided_v25_1.xlsx

## Status

Status atual: fonte bruta em revisão.

Este arquivo foi adicionado por integrante do grupo e ainda não foi integrado ao pipeline principal.

## Inspeção inicial

A inspeção inicial identificou:

- 1 sheet: OneSided_v25_1;
- 1330 linhas;
- 17 colunas;
- granularidade aproximada: ator/local/ano;
- variável temporal principal: year;
- variável geográfica principal: location;
- estimativa principal de fatalidades: best_fatality_estimate.

## Colunas principais

- conflict_id
- dyad_id
- actor_id
- actor_name
- year
- best_fatality_estimate
- low_fatality_estimate
- high_fatality_estimate
- is_government_actor
- location
- gwno_location
- region

## Avaliação metodológica

O dataset pode ser útil para:

- validar variáveis de violência unilateral já presentes no pipeline;
- criar features agregadas por país-ano;
- analisar violência de atores contra civis;
- enriquecer a camada UCDP do projeto.

Porém, ele não deve ser usado diretamente no modelo atual sem transformação, porque a unidade principal do projeto é country-year.

## Decisão provisória

Não integrar diretamente ao modelo principal neste momento.

Próxima ação recomendada:

1. verificar se as variáveis atuais one_sided_* já representam essa fonte;
2. comparar cobertura com o dataset UCDP Organized Violence;
3. se houver ganho, criar um script específico de agregação para país-ano;
4. só depois testar impacto no modelo.

## Arquivo processado adicionado pelo grupo

Também foi adicionado o arquivo:

`data/final/UCDP_One-sided_Violence_Dataset_updated.csv`

A inspeção inicial identificou:

- 1330 linhas;
- 4 colunas;
- colunas: `year`, `actor_name`, `location`, `best_fatality_estimate`;
- granularidade aproximada: ator/local/ano.

Esse arquivo parece ser uma versão simplificada do dataset bruto `OneSided_v25_1.xlsx`.

## Avaliação do arquivo processado

O arquivo pode ser útil como etapa intermediária de análise, mas ainda não deve ser considerado dataset final oficial do pipeline.

Motivos:

- não está claro qual script gerou o arquivo;
- ainda não está agregado para a unidade principal `country-year`;
- pode duplicar informações que já existem em `ucdp_organized_violence_country_year.csv`;
- precisa ser comparado com as variáveis atuais `one_sided_violence_exists`, `one_sided_dyad_count` e `one_sided_deaths_best`.

## Decisão provisória sobre o CSV processado

Manter como material em revisão.

Antes de integrar ao modelo, é necessário:

1. criar ou recuperar o script que gerou esse CSV;
2. comparar a cobertura contra o dataset UCDP organizado já usado;
3. verificar se há ganho informacional real;
4. transformar para país-ano, se for usado;
5. documentar a origem e a lógica de agregação.