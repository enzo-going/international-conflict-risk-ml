"""
build_sipri_features.py
=======================
Militarization feature layer — SIPRI Military Expenditure Database.

Entrada : data/intermediate/sipri_country_year_base.csv
Saída   : data/final/conflict_country_year_sipri.csv

Features produzidas
-------------------
  sipri_milex_pct_gdp              Military expenditure as % of GDP (alias limpo de milex_share_gdp)
  sipri_milex_growth_5y            Taxa de crescimento anualizado em 5 anos (CAGR, lagged)
  sipri_milex_burden_rolling_3y    Média móvel de 3 anos do % do PIB (lagged)
  sipri_milex_std_5y               Desvio-padrão do gasto em 5 anos (lagged) — volatilidade orçamentária
  sipri_milex_acceleration         Diferença de crescimento YoY: (t-1 vs t-2) - (t-2 vs t-3) — aceleração/desaceleração

Princípios de design
--------------------
  - Toda feature usa apenas informação passada (shift antes de rolling).
  - Temporal leakage zero: o ano t nunca vê valores de t ou t+.
  - Compatibilidade country-year com o master dataset (LEFT JOIN sobre base).
  - Pipeline reproduzível: funções puras, sem side effects fora de save_dataset().
  - Nomenclatura prefixada sipri_ (espelho exato do prefixo prio_ no módulo PRIO).

Posição no pipeline
-------------------
  src/data/prepare_sipri_dataset.py     → data/intermediate/sipri_country_year_base.csv
  src/features/build_sipri_features.py  ← ESTE MÓDULO
  src/models/train_conflict_risk_model.py
"""

from pathlib import Path

import numpy as np
import pandas as pd


# ─────────────────────────────────────────────────────────────────────────────
# CAMINHOS
# ─────────────────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INTERMEDIATE_PATH = PROJECT_ROOT / "data" / "intermediate" / "sipri_country_year_base.csv"
BASE_PATH         = PROJECT_ROOT / "data" / "final"        / "conflict_country_year_base.csv"
OUTPUT_PATH       = PROJECT_ROOT / "data" / "final"        / "conflict_country_year_sipri.csv"


# ─────────────────────────────────────────────────────────────────────────────
# CATÁLOGO DE FEATURES
# ─────────────────────────────────────────────────────────────────────────────

SIPRI_FEATURE_COLS = [
    "sipri_milex_pct_gdp",
    "sipri_milex_growth_5y",
    "sipri_milex_burden_rolling_3y",
    "sipri_milex_std_5y",
    "sipri_milex_acceleration",
]


# ─────────────────────────────────────────────────────────────────────────────
# LOADERS
# ─────────────────────────────────────────────────────────────────────────────

def load_intermediate() -> pd.DataFrame:
    """Carrega o dataset SIPRI preparado da pasta intermediate."""
    if not INTERMEDIATE_PATH.exists():
        raise FileNotFoundError(
            f"Intermediate dataset não encontrado: {INTERMEDIATE_PATH}\n"
            "Execute src/data/prepare_sipri_dataset.py primeiro."
        )
    return pd.read_csv(INTERMEDIATE_PATH)


def load_base() -> pd.DataFrame:
    """Carrega o base conflict country-year dataset."""
    if not BASE_PATH.exists():
        raise FileNotFoundError(f"Base dataset não encontrado: {BASE_PATH}")
    return pd.read_csv(BASE_PATH)


# ─────────────────────────────────────────────────────────────────────────────
# FEATURE ENGINEERING — Funções individuais (puras, sem side effects)
# ─────────────────────────────────────────────────────────────────────────────

def add_level_feature(df: pd.DataFrame) -> pd.DataFrame:
    """
    sipri_milex_pct_gdp
    --------------------
    Alias limpo de milex_share_gdp com o prefixo do projeto.
    Representa o peso da despesa militar na economia em t-1
    (o valor já é histórico no contexto do ano corrente).

    Usa shift(1) para garantir que o ano t veja apenas o valor do ano t-1,
    eliminando qualquer possibilidade de leakage mesmo quando o CSV é atualizado
    com dados preliminares do ano corrente.
    """
    df = df.copy()
    g = df.groupby("country_name_sipri")

    df["sipri_milex_pct_gdp"] = g["milex_share_gdp"].transform(
        lambda s: s.shift(1)
    )
    return df


def add_growth_feature(df: pd.DataFrame) -> pd.DataFrame:
    """
    sipri_milex_growth_5y
    ----------------------
    Taxa de crescimento anualizado (CAGR) do gasto militar constante
    ao longo de uma janela de 5 anos, calculada inteiramente sobre
    valores passados.

    Fórmula:
        CAGR = (V_{t-1} / V_{t-5}) ^ (1/4) - 1

    Implementação:
        1. shift(1) para evitar leakage do ano t.
        2. pct_change(4) sobre a série já shiftada → crescimento de
           4 períodos no passado, equivalente ao CAGR de 5 anos.
        3. min_periods=5 para não produzir estimativas com janela incompleta.

    Interpretação:
        Positivo  → acumulação de capacidade militar no lustro anterior.
        Negativo  → contração orçamentária ou deflação real.
        NaN       → histórico insuficiente (< 5 anos de dados válidos).
    """
    df = df.copy()
    g = df.groupby("country_name_sipri")

    df["sipri_milex_growth_5y"] = g["milex_constant_usd_m"].transform(
        lambda s: (
            s.shift(1)
             .pct_change(periods=4, fill_method=None)
        )
    )

    # Substituir inf (divisão por zero quando valor inicial = 0) por NaN
    df["sipri_milex_growth_5y"] = df["sipri_milex_growth_5y"].replace(
        [np.inf, -np.inf], np.nan
    )
    return df


def add_rolling_burden_feature(df: pd.DataFrame) -> pd.DataFrame:
    """
    sipri_milex_burden_rolling_3y
    ------------------------------
    Média móvel de 3 anos do military burden (% do PIB), calculada
    exclusivamente sobre valores passados.

    Sequência anti-leakage:
        shift(1)  →  rolling(3, min_periods=2)  →  mean()

    O shift(1) desloca toda a série um período para trás antes de
    qualquer cálculo de janela; logo, a janela de rolling em t
    cobre [t-2, t-3, t-4] — nunca t.

    min_periods=2 permite produzir estimativas quando há 2 anos
    de histórico válido (comum em países com curta série histórica),
    sinalizando volatilidade alta nesses casos via NaN parcial em
    sipri_milex_std_5y.
    """
    df = df.copy()
    g = df.groupby("country_name_sipri")

    df["sipri_milex_burden_rolling_3y"] = g["milex_share_gdp"].transform(
        lambda s: s.shift(1).rolling(3, min_periods=2).mean()
    )
    return df


def add_volatility_feature(df: pd.DataFrame) -> pd.DataFrame:
    """
    sipri_milex_std_5y
    -------------------
    Desvio-padrão do gasto militar constante (USD) em janela de 5 anos,
    calculado sobre informação passada.

    Sequência anti-leakage:
        shift(1)  →  rolling(5, min_periods=3)  →  std(ddof=1)

    Interpretação:
        Alta  → orçamento militar volátil/errático (instabilidade política,
                crises, corridas armamentistas).
        Baixa → planejamento estável de defesa.
        NaN   → histórico insuficiente.

    min_periods=3 reduz NaNs nos primeiros anos da série sem comprometer
    a qualidade estatística do estimador.
    """
    df = df.copy()
    g = df.groupby("country_name_sipri")

    df["sipri_milex_std_5y"] = g["milex_constant_usd_m"].transform(
        lambda s: s.shift(1).rolling(5, min_periods=3).std(ddof=1)
    )
    return df


def add_acceleration_feature(df: pd.DataFrame) -> pd.DataFrame:
    """
    sipri_milex_acceleration
    -------------------------
    Segunda derivada discreta do gasto militar: variação da variação.

    Fórmula:
        accel_t = growth_{t-1} - growth_{t-2}

    onde  growth_t = (milex_t - milex_{t-1}) / milex_{t-1}

    Implementação:
        1. Calcular growth_1y sobre a série original (sem shift ainda).
        2. shift(1) na série de crescimento antes de diff(1) — assim
           em t usamos apenas [t-1, t-2] — nunca t.

    Interpretação:
        accel > 0  → gasto acelerando (corrida armamentista ou resposta a ameaça).
        accel < 0  → gasto desacelerando (cortes, fim de conflito, austeridade).
        accel ≈ 0  → crescimento estável.
    """
    df = df.copy()
    g = df.groupby("country_name_sipri")

    # Crescimento YoY sem shift (série histórica completa, sem ver o futuro)
    growth_yoy = g["milex_constant_usd_m"].transform(
        lambda s: s.pct_change(fill_method=None)
    )
    growth_yoy = growth_yoy.replace([np.inf, -np.inf], np.nan)

    # Aceleração: diff de crescimento, sempre sobre valores passados
    df["sipri_milex_acceleration"] = (
        growth_yoy.groupby(df["country_name_sipri"])
                  .transform(lambda s: s.shift(1).diff(1))
    )
    return df


# ─────────────────────────────────────────────────────────────────────────────
# MERGE COM BASE DATASET
# ─────────────────────────────────────────────────────────────────────────────

def merge_with_base(df_base: pd.DataFrame,
                    df_sipri_cy: pd.DataFrame) -> pd.DataFrame:
    """
    Left-join das features SIPRI no base country-year dataset.

    Estratégia de join:
    -------------------
    O base usa a coluna 'country' (padrão do projeto).
    O dataset SIPRI usa 'country_name_sipri'.
    O join é feito por ['country', 'year'] após normalizar case/espaços.

    Preenchimento de NaN:
    ---------------------
    Países sem cobertura SIPRI recebem NaN (não 0), pois ausência de dados
    militares é fundamentalmente diferente de ausência de gasto militar.
    O modelo downstream deve tratar esses NaNs explicitamente (imputer
    ou indicador de missingness).

    Preservação de linhas:
    ----------------------
    Todos os registros do base são mantidos (LEFT JOIN).
    Nenhuma linha é eliminada por falta de cobertura SIPRI.
    """
    df_base    = df_base.copy()
    df_sipri_cy = df_sipri_cy.copy()

    # Normalização de nomes para o join
    df_base["country"]                   = df_base["country"].str.strip().str.title()
    df_sipri_cy["country_name_sipri"]    = df_sipri_cy["country_name_sipri"].str.strip().str.title()

    feature_cols = [c for c in df_sipri_cy.columns if c.startswith("sipri_")]

    df_enriched = df_base.merge(
        df_sipri_cy[["country_name_sipri", "year"] + feature_cols].rename(
            columns={"country_name_sipri": "country"}
        ),
        on=["country", "year"],
        how="left",
    )

    return df_enriched


# ─────────────────────────────────────────────────────────────────────────────
# PIPELINE PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

def build_sipri_features(df_intermediate: pd.DataFrame,
                         df_base: pd.DataFrame
                         ) -> tuple[pd.DataFrame, list]:
    """
    Pipeline completo de feature engineering SIPRI.

    Ordem de execução:
        1. add_level_feature          → sipri_milex_pct_gdp
        2. add_growth_feature         → sipri_milex_growth_5y
        3. add_rolling_burden_feature → sipri_milex_burden_rolling_3y
        4. add_volatility_feature     → sipri_milex_std_5y
        5. add_acceleration_feature   → sipri_milex_acceleration
        6. merge_with_base            → left-join sobre conflict_country_year_base

    Retorna
    -------
    df_enriched : pd.DataFrame
        Base dataset com as features SIPRI adicionadas.
    feature_cols : list[str]
        Lista das colunas de feature criadas (todas com prefixo sipri_).
    """
    # Garantir ordenação cronológica dentro de cada país antes de qualquer
    # cálculo de janela temporal — crítico para rolling/shift corretos.
    df = df_intermediate.copy().sort_values(
        ["country_name_sipri", "year"]
    ).reset_index(drop=True)

    df = add_level_feature(df)
    df = add_growth_feature(df)
    df = add_rolling_burden_feature(df)
    df = add_volatility_feature(df)
    df = add_acceleration_feature(df)

    df_enriched  = merge_with_base(df_base, df)
    feature_cols = [c for c in df_enriched.columns if c.startswith("sipri_")]

    return df_enriched, feature_cols


# ─────────────────────────────────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────────────────────────────────

def save_dataset(df: pd.DataFrame) -> None:
    """Salva o dataset enriquecido com features SIPRI na pasta final."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")


# ─────────────────────────────────────────────────────────────────────────────
# ENTRYPOINT
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    df_intermediate = load_intermediate()
    df_base         = load_base()

    df_enriched, feature_cols = build_sipri_features(df_intermediate, df_base)
    save_dataset(df_enriched)

    print("SIPRI militarization feature layer construída com sucesso.")
    print(f"Input  (intermediate) : {INTERMEDIATE_PATH}")
    print(f"Input  (base)         : {BASE_PATH}")
    print(f"Output                : {OUTPUT_PATH}")
    print(f"Linhas                : {df_enriched.shape[0]}")
    print(f"Colunas               : {df_enriched.shape[1]}")
    print()
    print("Features SIPRI adicionadas:")

    for col in feature_cols:
        n_nonnan = df_enriched[col].notna().sum()
        pct      = 100 * n_nonnan / len(df_enriched)
        mean_val = df_enriched[col].mean()
        print(f"  {col:<35} {n_nonnan:>7,} non-null  ({pct:5.1f}%)  mean={mean_val:+.4f}")

    print()
    coverage = df_enriched["sipri_milex_pct_gdp"].notna().sum()
    total    = len(df_enriched)
    print(f"Cobertura SIPRI no base dataset : {coverage:,} / {total:,} ({100*coverage/total:.1f}%)")


if __name__ == "__main__":
    main()
