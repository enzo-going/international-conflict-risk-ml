"""
prepare_sipri_dataset.py
========================
ETL reproduzível para o SIPRI Military Expenditure Database.

Fonte   : SIPRI-Milex-data-1949-2025_v1_2.xlsx
    Entrada : data/raw/sipri/SIPRI-Milex-data-1949-2025_v1_2.xlsx
Saída   : data/intermediate/sipri_country_year_base.csv

Abas processadas
----------------
  Constant (2024) US$  → milex_constant_usd_m
  Share of GDP         → milex_share_gdp
  Current US$          → milex_current_usd_m
  Per capita           → milex_per_capita_usd

Decisões de design
------------------
  - Valores especiais "...", "…" (dado indisponível)  → NaN
  - Valores especiais "xxx" (país não existia)         → NaN  +  flag sipri_country_existed = 0
  - Linhas de região/sub-região                        → removidas
  - Nomes de país padronizados via mapeamento manual   → country_name_sipri
  - Coluna de notes (§, ‖, etc.)                       → removida do output
  - Nenhuma feature derivada neste script              → somente ETL

Posição no pipeline
-------------------
  src/data/prepare_sipri_dataset.py          ← ESTE SCRIPT
  src/features/build_sipri_features.py       → delta, ma3, zscore, spike flag
  src/data/build_conflict_country_year_sipri.py → JOIN com master dataset
"""

from pathlib import Path

import pandas as pd
import numpy as np


# ─────────────────────────────────────────────────────────────────────────────
# CAMINHOS
# ─────────────────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parents[2]

SIPRI_RAW_PATH  = PROJECT_ROOT / "data" / "raw" / "sipri" / "sipri_raw.xlsx"
OUTPUT_DIR      = PROJECT_ROOT / "data" / "intermediate"
OUTPUT_PATH     = OUTPUT_DIR / "sipri_country_year_base.csv"


# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DAS ABAS
# Offsets confirmados por inspeção direta do arquivo v1_2
# ─────────────────────────────────────────────────────────────────────────────

SHEET_CONFIG = {
    "milex_constant_usd_m": {
        "sheet_name"    : "Constant (2024) US$",
        "header_row"    : 5,
        "country_col"   : 0,
        "notes_col"     : 2,
        "first_year_col": 3,
        "first_year"    : 1949,
        "last_year"     : 2025,
    },
    "milex_share_gdp": {
        "sheet_name"    : "Share of GDP",
        "header_row"    : 5,
        "country_col"   : 0,
        "notes_col"     : 1,
        "first_year_col": 2,
        "first_year"    : 1949,
        "last_year"     : 2025,
    },
    "milex_current_usd_m": {
        "sheet_name"    : "Current US$",
        "header_row"    : 5,
        "country_col"   : 0,
        "notes_col"     : 1,
        "first_year_col": 2,
        "first_year"    : 1949,
        "last_year"     : 2025,
    },
    "milex_per_capita_usd": {
        "sheet_name"    : "Per capita",
        "header_row"    : 6,
        "country_col"   : 0,
        "notes_col"     : 1,
        "first_year_col": 2,
        "first_year"    : 1988,
        "last_year"     : 2025,
    },
}

# Regiões e sub-regiões — linhas sem dados numéricos, removidas do output
REGION_LABELS = {
    "Africa", "North Africa", "sub-Saharan Africa",
    "Americas", "Central America and the Caribbean",
    "North America", "South America",
    "Asia & Oceania", "Oceania", "South Asia",
    "East Asia", "South East Asia", "Central Asia",
    "Europe", "Central Europe", "Eastern Europe", "Western Europe",
    "Middle East",
}

# Valores especiais SIPRI → NaN
SPECIAL_VALUES = {"...", "…", "xxx", ". ."}

# Mapeamento de nomes SIPRI → nome padronizado do projeto
# Baseado nos nomes que aparecem no country_name_mapping_reviewed.csv
COUNTRY_NAME_MAP = {
    # África
    "Congo, DR"                         : "Congo, Dem. Rep.",
    "Congo, Republic"                   : "Congo, Rep.",
    "Cote d'Ivoire"                     : "Cote d'Ivoire",
    "Gambia, The"                       : "Gambia",
    "Sao Tome and Principe"             : "Sao Tome and Principe",
    # Américas
    "United States of America"          : "United States",
    "Trinidad and Tobago"               : "Trinidad and Tobago",
    # Ásia
    "Korea, North"                      : "Korea, Dem. Rep.",
    "Korea, South"                      : "Korea, Rep.",
    "Kyrgyzstan"                        : "Kyrgyz Republic",
    "Laos"                              : "Lao PDR",
    "Myanmar"                           : "Myanmar",
    "Taiwan"                            : "Taiwan",
    "Timor-Leste"                       : "Timor-Leste",
    "Vietnam"                           : "Vietnam",
    # Europa
    "Bosnia and Herzegovina"            : "Bosnia and Herzegovina",
    "Czechia"                           : "Czech Republic",
    "Kosovo"                            : "Kosovo",
    "Slovak Republic"                   : "Slovak Republic",
    "Türkiye"                           : "Turkiye",
    # Oriente Médio
    "Iran"                              : "Iran, Islamic Rep.",
    "Syria"                             : "Syrian Arab Republic",
    "Yemen"                             : "Yemen, Rep.",
    # Outros
    "Russia"                            : "Russian Federation",
    "Venezuela"                         : "Venezuela, RB",
    "Egypt"                             : "Egypt, Arab Rep.",
    "Bolivia"                           : "Bolivia",
    "Tanzania"                          : "Tanzania",
    "Eswatini"                          : "Eswatini",
    "Cabo Verde"                        : "Cabo Verde",
    "Micronesia"                        : "Micronesia, Fed. Sts.",
}


# ─────────────────────────────────────────────────────────────────────────────
# FUNÇÕES DE LIMPEZA
# ─────────────────────────────────────────────────────────────────────────────

def _is_region(country_name: str) -> bool:
    """Retorna True se a linha é um cabeçalho de região/sub-região."""
    return str(country_name).strip() in REGION_LABELS


def _clean_value(val) -> float:
    """
    Converte um valor de célula SIPRI para float ou NaN.

    Regras:
      - NaN nativo               → NaN
      - "...", "…", ". ."        → NaN  (dado indisponível)
      - "xxx"                    → NaN  (país não existia — tratado separadamente)
      - número (int ou float)    → float
      - string numérica          → float
    """
    if pd.isna(val):
        return np.nan
    val_str = str(val).strip()
    if val_str in SPECIAL_VALUES:
        return np.nan
    try:
        return float(val_str.replace(",", ""))
    except (ValueError, TypeError):
        return np.nan


def _is_xxx(val) -> bool:
    """Retorna True se o valor original era 'xxx' (país não existia naquele ano)."""
    if pd.isna(val):
        return False
    return str(val).strip() == "xxx"


def _parse_sheet(metric_col: str, config: dict, xlsx_path: Path) -> pd.DataFrame:
    """
    Lê uma aba do SIPRI e retorna um DataFrame long country-year.

    Parâmetros
    ----------
    metric_col : str
        Nome da coluna de valor no output (ex: "milex_constant_usd_m").
    config : dict
        Configuração de offsets para esta aba.
    xlsx_path : Path
        Caminho para o arquivo .xlsx.

    Retorna
    -------
    pd.DataFrame com colunas: country_name_sipri, year, <metric_col>,
                               sipri_country_existed
    """
    df_raw = pd.read_excel(xlsx_path, sheet_name=config["sheet_name"], header=None)

    header_row    = config["header_row"]
    country_col   = config["country_col"]
    first_year_col = config["first_year_col"]

    # Extrair os anos a partir do header
    year_values = [
        int(v) for v in df_raw.iloc[header_row, first_year_col:].tolist()
        if isinstance(v, (int, float)) and not pd.isna(v)
    ]

    # Linhas de dados começam logo após o header + linha em branco
    data_start = header_row + 1
    # Pular linhas completamente vazias logo após o header
    while data_start < len(df_raw) and df_raw.iloc[data_start, country_col] != df_raw.iloc[data_start, country_col]:
        data_start += 1

    records = []

    for row_idx in range(data_start, len(df_raw)):
        country_raw = df_raw.iloc[row_idx, country_col]

        # Pular NaN, regiões e linhas em branco
        if pd.isna(country_raw):
            continue
        country_str = str(country_raw).strip()
        if not country_str or _is_region(country_str):
            continue

        # Extrair valores para cada ano
        row_values = df_raw.iloc[row_idx, first_year_col:].tolist()

        for year, raw_val in zip(year_values, row_values):
            existed = 0 if _is_xxx(raw_val) else 1
            value   = _clean_value(raw_val)

            records.append({
                "country_name_sipri"     : country_str,
                "year"                   : int(year),
                metric_col               : value,
                "sipri_country_existed"  : existed,
            })

    df_long = pd.DataFrame(records)

    # Quando country_existed = 0, garantir que o valor é NaN
    mask_not_existed = df_long["sipri_country_existed"] == 0
    df_long.loc[mask_not_existed, metric_col] = np.nan

    return df_long


# ─────────────────────────────────────────────────────────────────────────────
# PADRONIZAÇÃO DE NOMES
# ─────────────────────────────────────────────────────────────────────────────

def _standardize_country_name(name: str) -> str:
    """
    Aplica mapeamento manual de nomes SIPRI → nomes padronizados do projeto.
    Nomes não mapeados são retornados como estão (sem alteração silenciosa).
    """
    return COUNTRY_NAME_MAP.get(name, name)


# ─────────────────────────────────────────────────────────────────────────────
# PIPELINE PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

def run() -> None:
    """Executa o ETL completo e salva o output em data/intermediate/."""

    print("=" * 60)
    print("SIPRI Military Expenditure — ETL")
    print("=" * 60)
    print()

    # ── 1. Verificar arquivo fonte ────────────────────────────────
    if not SIPRI_RAW_PATH.exists():
        raise FileNotFoundError(
            f"Arquivo SIPRI não encontrado em:\n  {SIPRI_RAW_PATH}\n\n"
            "Coloque o arquivo em data/raw/sipri/ e re-execute."
        )
    print(f"[1] Arquivo fonte   : {SIPRI_RAW_PATH.name}")

    # ── 2. Parsear cada aba ───────────────────────────────────────
    print("[2] Processando abas:")
    dfs = {}

    for metric_col, config in SHEET_CONFIG.items():
        print(f"    {config['sheet_name']:<30} → {metric_col}")
        dfs[metric_col] = _parse_sheet(metric_col, config, SIPRI_RAW_PATH)

    # ── 3. Merge das 4 métricas em um único DataFrame long ────────
    print()
    print("[3] Unindo métricas em estrutura country-year...")

    # Base: constant_usd (cobertura mais ampla — 1949-2025)
    base_cols   = ["country_name_sipri", "year", "sipri_country_existed"]
    metric_cols = list(SHEET_CONFIG.keys())

    df_merged = dfs["milex_constant_usd_m"][base_cols + ["milex_constant_usd_m"]].copy()

    for col in ["milex_share_gdp", "milex_current_usd_m", "milex_per_capita_usd"]:
        df_other = dfs[col][["country_name_sipri", "year", col]].copy()
        df_merged = df_merged.merge(df_other, on=["country_name_sipri", "year"], how="left")

    # ── 4. Padronizar nomes ───────────────────────────────────────
    print("[4] Padronizando nomes de país...")
    df_merged["country_name_sipri_raw"] = df_merged["country_name_sipri"].copy()
    df_merged["country_name_sipri"]     = df_merged["country_name_sipri"].apply(_standardize_country_name)

    # Relatório de nomes que não têm mapeamento explícito
    unmapped = set(df_merged["country_name_sipri_raw"].unique()) - set(COUNTRY_NAME_MAP.keys())
    print(f"    Países com mapeamento explícito : {len(COUNTRY_NAME_MAP)}")
    print(f"    Países sem mapeamento (mantidos): {len(unmapped)}")

    # ── 5. Diagnóstico de nulos ───────────────────────────────────
    print()
    print("[5] Diagnóstico de valores ausentes:")
    for col in metric_cols:
        n_total = len(df_merged)
        n_nan   = df_merged[col].isna().sum()
        n_xxx   = (df_merged["sipri_country_existed"] == 0).sum() if col == "milex_constant_usd_m" else 0
        pct     = 100 * n_nan / n_total
        print(f"    {col:<30} NaN={n_nan:5d} ({pct:5.1f}%)")

    # ── 6. Ordenar e finalizar ────────────────────────────────────
    df_merged = df_merged.sort_values(
        ["country_name_sipri", "year"]
    ).reset_index(drop=True)

    # Remover coluna auxiliar de nome bruto
    df_merged = df_merged.drop(columns=["country_name_sipri_raw"])

    # Reordenar colunas de forma lógica
    output_cols = [
        "country_name_sipri",
        "year",
        "sipri_country_existed",
        "milex_constant_usd_m",
        "milex_current_usd_m",
        "milex_share_gdp",
        "milex_per_capita_usd",
    ]
    df_merged = df_merged[output_cols]

    # ── 7. Salvar ─────────────────────────────────────────────────
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df_merged.to_csv(OUTPUT_PATH, index=False)

    # ── 8. Sumário final ──────────────────────────────────────────
    print()
    print("[6] Output:")
    print(f"    Caminho : {OUTPUT_PATH}")
    print(f"    Shape   : {df_merged.shape}")
    print(f"    Anos    : {int(df_merged['year'].min())} – {int(df_merged['year'].max())}")
    print(f"    Países  : {df_merged['country_name_sipri'].nunique()}")
    print()
    print("[7] Amostra (primeiras linhas com dados):")
    sample = df_merged[df_merged["milex_constant_usd_m"].notna()].head(5)
    print(sample.to_string(index=False))
    print()
    print("ETL concluído.")
    print()
    print("Próximo passo:")
    print("  src/features/build_sipri_features.py")
    print("  → delta anual, ma3, z-score, spike flag")
    print("  → JOIN com conflict_country_year_base.csv")


if __name__ == "__main__":
    run()
