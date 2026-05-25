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