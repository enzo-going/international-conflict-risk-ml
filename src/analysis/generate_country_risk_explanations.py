from __future__ import annotations

from pathlib import Path
import json
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RISK_ASSESSMENT_PATH = PROJECT_ROOT / "outputs" / "tables" / "country_risk_assessment_latest_year.csv"
FEATURES_DATASET_PATH = PROJECT_ROOT / "data" / "final" / "conflict_country_year_world_bank_features.csv"
COEFFICIENTS_PATH = PROJECT_ROOT / "outputs" / "tables" / "conflict_risk_model_coefficients.csv"
MODEL_FEATURES_PATH = PROJECT_ROOT / "outputs" / "models" / "conflict_risk_model_features.json"

OUTPUT_TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"
REPORTS_FINAL_DIR = PROJECT_ROOT / "reports" / "final"

EXPLANATIONS_PATH = OUTPUT_TABLES_DIR / "country_risk_explanations_latest_year.csv"
GROUP_SUMMARY_PATH = OUTPUT_TABLES_DIR / "country_risk_explanation_group_summary.csv"
SUMMARY_JSON_PATH = OUTPUT_TABLES_DIR / "country_risk_explanation_summary.json"
MARKDOWN_REPORT_PATH = REPORTS_FINAL_DIR / "country_risk_explanations_latest_year.md"


FEATURE_GROUP_LABELS = {
    "ucdp_conflict": "histórico e intensidade de conflitos UCDP",
    "temporal_conflict": "persistência temporal de conflito",
    "world_bank": "indicadores socioeconômicos World Bank",
    "time_index": "tendência temporal geral",
}


def require_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo obrigatório não encontrado: {path}")


def normalize_numeric(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    median = numeric.median()
    std = numeric.std()

    if pd.isna(std) or std == 0:
        return pd.Series([0.0] * len(series), index=series.index)

    return ((numeric - median) / std).fillna(0.0)


def format_probability(value: float) -> str:
    return f"{value * 100:.1f}%"


def format_float(value: Any, digits: int = 4) -> str:
    try:
        if pd.isna(value):
            return ""
        return f"{float(value):.{digits}f}"
    except Exception:
        return str(value)


def dataframe_to_markdown_table(df: pd.DataFrame, max_rows: int = 30) -> str:
    if df.empty:
        return "_Sem registros._"

    sample = df.head(max_rows).copy()
    columns = [str(column) for column in sample.columns]

    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"

    rows = []
    for _, row in sample.iterrows():
        values = []
        for column in sample.columns:
            value = row[column]

            if pd.isna(value):
                values.append("")
            elif isinstance(value, float):
                values.append(f"{value:.4f}")
            else:
                values.append(str(value).replace("\n", " ").replace("|", "\\|"))

        rows.append("| " + " | ".join(values) + " |")

    suffix = ""
    if len(df) > max_rows:
        suffix = f"\n\n_Exibindo {max_rows} de {len(df)} registros._"

    return "\n".join([header, separator, *rows]) + suffix


def feature_label(feature: str) -> str:
    labels = {
        "state_based_conflict_exists": "existência de conflito estatal no ano-base",
        "state_based_dyad_count": "quantidade de díades de conflito estatal",
        "state_based_deaths_best": "mortes estimadas em conflitos estatais",
        "intrastate_conflict_exists": "existência de conflito intraestatal",
        "intrastate_deaths_best": "mortes estimadas em conflitos intraestatais",
        "interstate_conflict_exists": "existência de conflito interestatal",
        "interstate_deaths_best": "mortes estimadas em conflitos interestatais",
        "non_state_conflict_exists": "existência de conflito não estatal",
        "non_state_dyad_count": "quantidade de díades de conflito não estatal",
        "non_state_deaths_best": "mortes estimadas em conflitos não estatais",
        "one_sided_violence_exists": "existência de violência unilateral",
        "one_sided_dyad_count": "quantidade de díades de violência unilateral",
        "one_sided_deaths_best": "mortes estimadas por violência unilateral",
        "cumulative_organized_violence_deaths_best": "mortes acumuladas por violência organizada",
        "organized_violence_exists": "existência de violência organizada no ano-base",
        "conflict_previous_year": "conflito no ano anterior",
        "conflict_last_3_years_count": "frequência de conflito nos últimos 3 anos",
        "conflict_last_5_years_count": "frequência de conflito nos últimos 5 anos",
        "deaths_previous_year": "mortes por conflito no ano anterior",
        "deaths_last_3_years_sum": "mortes acumuladas nos últimos 3 anos",
        "deaths_last_5_years_sum": "mortes acumuladas nos últimos 5 anos",
        "years_since_last_conflict": "anos desde o último conflito",
        "population_total": "população total",
        "population_growth_annual_pct": "crescimento populacional anual",
        "urban_population_pct": "população urbana",
        "gdp_per_capita_current_usd": "PIB per capita",
        "gdp_growth_annual_pct": "crescimento anual do PIB",
        "inflation_consumer_prices_annual_pct": "inflação anual",
        "unemployment_total_pct": "desemprego",
        "school_enrollment_secondary_gross_pct": "matrícula no ensino secundário",
        "military_expenditure_pct_gdp": "gasto militar como percentual do PIB",
        "natural_resources_rents_pct_gdp": "renda de recursos naturais como percentual do PIB",
        "year": "tendência temporal do conjunto",
    }

    return labels.get(feature, feature)


def effect_direction_text(coefficient: float, standardized_value: float) -> str:
    signal = coefficient * standardized_value

    if signal > 0:
        return "aumenta o risco estimado"
    if signal < 0:
        return "reduz o risco estimado"
    return "efeito neutro na explicação aproximada"


def build_feature_contribution_table(
    features_latest: pd.DataFrame,
    coefficients: pd.DataFrame,
    feature_columns: list[str],
) -> pd.DataFrame:
    working = features_latest.copy()

    available_features = [
        feature for feature in feature_columns
        if feature in working.columns and feature in set(coefficients["feature"])
    ]

    if not available_features:
        raise ValueError("Nenhuma feature do modelo foi encontrada no dataset final.")

    for feature in available_features:
        working[f"{feature}__standardized_signal"] = normalize_numeric(working[feature])

    coefficient_map = coefficients.set_index("feature")["coefficient"].to_dict()
    group_map = coefficients.set_index("feature")["feature_group"].to_dict()

    rows: list[dict[str, Any]] = []

    for _, country_row in working.iterrows():
        country = country_row["country"]
        year = int(country_row["year"])

        for feature in available_features:
            raw_value = country_row.get(feature)
            standardized_value = float(country_row.get(f"{feature}__standardized_signal", 0.0))
            coefficient = float(coefficient_map[feature])
            approximate_signal = coefficient * standardized_value
            feature_group = str(group_map.get(feature, "unknown"))

            rows.append(
                {
                    "country": country,
                    "year": year,
                    "feature": feature,
                    "feature_label": feature_label(feature),
                    "feature_group": feature_group,
                    "feature_group_label": FEATURE_GROUP_LABELS.get(feature_group, feature_group),
                    "raw_value": raw_value,
                    "standardized_signal": standardized_value,
                    "coefficient": coefficient,
                    "approximate_signal": approximate_signal,
                    "absolute_signal": abs(approximate_signal),
                    "effect_direction": effect_direction_text(coefficient, standardized_value),
                }
            )

    return pd.DataFrame(rows)


def summarize_country_explanations(
    risk_assessment: pd.DataFrame,
    contribution_table: pd.DataFrame,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []

    for _, risk_row in risk_assessment.iterrows():
        country = risk_row["country"]
        country_contrib = contribution_table[contribution_table["country"] == country].copy()

        positive = (
            country_contrib[country_contrib["approximate_signal"] > 0]
            .sort_values("approximate_signal", ascending=False)
            .head(3)
        )

        negative = (
            country_contrib[country_contrib["approximate_signal"] < 0]
            .sort_values("approximate_signal", ascending=True)
            .head(3)
        )

        group_summary = (
            country_contrib.groupby(["feature_group", "feature_group_label"], dropna=False)
            .agg(
                group_signal=("approximate_signal", "sum"),
                group_abs_signal=("absolute_signal", "sum"),
            )
            .reset_index()
            .sort_values("group_abs_signal", ascending=False)
        )

        top_groups = group_summary.head(3)

        main_positive_factors = "; ".join(
            [
                f"{row.feature_label}"
                for row in positive.itertuples()
            ]
        )

        main_negative_factors = "; ".join(
            [
                f"{row.feature_label}"
                for row in negative.itertuples()
            ]
        )

        main_groups = "; ".join(
            [
                f"{row.feature_group_label}"
                for row in top_groups.itertuples()
            ]
        )

        short_explanation = (
            f"{country}: {risk_row['predicted_probability_percent']} de risco estimado para "
            f"{int(risk_row['forecast_year'])}, classificado como {risk_row['risk_level_description']}."
        )

        explanation = (
            f"Para {country}, o modelo estimou {risk_row['predicted_probability_percent']} "
            f"de probabilidade de violência organizada em {int(risk_row['forecast_year'])}, "
            f"classificando o caso como {risk_row['risk_level_description']}. "
            f"Os principais grupos associados à estimativa foram: {main_groups}."
        )

        if main_positive_factors:
            explanation += f" Sinais que elevaram a estimativa: {main_positive_factors}."

        if main_negative_factors:
            explanation += f" Sinais que reduziram a estimativa no modelo: {main_negative_factors}."

        technical_warning = (
            "Explicação aproximada baseada em coeficientes e valores relativos das features; "
            "não representa causalidade direta."
        )

        rows.append(
            {
                "country": country,
                "region": risk_row["region"],
                "year": int(risk_row["year"]),
                "forecast_year": int(risk_row["forecast_year"]),
                "predicted_conflict_probability": float(risk_row["predicted_conflict_probability"]),
                "predicted_probability_percent": risk_row["predicted_probability_percent"],
                "risk_level": risk_row["risk_level"],
                "risk_level_description": risk_row["risk_level_description"],
                "predicted_conflict_next_year": int(risk_row["predicted_conflict_next_year"]),
                "target_conflict_next_year": int(risk_row["target_conflict_next_year"]),
                "prediction_result": risk_row["prediction_result"],
                "main_explanation_groups": main_groups,
                "top_positive_factors": main_positive_factors,
                "top_negative_factors": main_negative_factors,
                "short_explanation": short_explanation,
                "explanation_text": explanation,
                "technical_warning": technical_warning,
            }
        )

    return pd.DataFrame(rows).sort_values(
        "predicted_conflict_probability",
        ascending=False,
    )


def build_group_summary(explanations: pd.DataFrame, contribution_table: pd.DataFrame) -> pd.DataFrame:
    latest_countries = set(explanations["country"])

    filtered = contribution_table[contribution_table["country"].isin(latest_countries)].copy()

    group_summary = (
        filtered.groupby(["feature_group", "feature_group_label"], dropna=False)
        .agg(
            mean_signal=("approximate_signal", "mean"),
            mean_absolute_signal=("absolute_signal", "mean"),
            total_absolute_signal=("absolute_signal", "sum"),
            feature_count=("feature", "nunique"),
            country_count=("country", "nunique"),
        )
        .reset_index()
        .sort_values("total_absolute_signal", ascending=False)
    )

    return group_summary


def create_markdown_report(
    explanations: pd.DataFrame,
    group_summary: pd.DataFrame,
    summary: dict[str, Any],
) -> str:
    display_columns = [
        "country",
        "region",
        "forecast_year",
        "predicted_probability_percent",
        "risk_level_description",
        "top_positive_factors",
        "top_negative_factors",
        "prediction_result",
    ]

    lines: list[str] = []

    lines.append("# Explicações Preditivas por País")
    lines.append("")
    lines.append("Este relatório complementa a avaliação preditiva por país com explicações aproximadas baseadas nas features usadas pelo modelo.")
    lines.append("")
    lines.append("## Escopo")
    lines.append("")
    lines.append(f"- Ano-base: {summary['latest_year']}")
    lines.append(f"- Ano previsto: {summary['forecast_year']}")
    lines.append(f"- Países avaliados: {summary['countries_evaluated']}")
    lines.append("- Modelo principal: Logistic Regression scaled - World Bank all raw")
    lines.append("")
    lines.append("## Observação metodológica")
    lines.append("")
    lines.append("As explicações são aproximações baseadas nos coeficientes do modelo e na posição relativa das features no ano-base analisado.")
    lines.append("")
    lines.append("Elas indicam associação estatística no modelo, não causalidade direta.")
    lines.append("")
    lines.append("Como o modelo usa padronização interna, os sinais calculados aqui devem ser lidos como apoio interpretativo, não como decomposição exata do logit.")
    lines.append("")
    lines.append("## Resumo por grupo de variáveis")
    lines.append("")
    lines.append(dataframe_to_markdown_table(group_summary, max_rows=20))
    lines.append("")
    lines.append("## Top 25 países por risco estimado e grupos explicativos")
    lines.append("")
    lines.append(dataframe_to_markdown_table(explanations.loc[:, display_columns], max_rows=25))
    lines.append("")
    lines.append("## Exemplos de explicação textual")
    lines.append("")

    for _, row in explanations.head(10).iterrows():
        lines.append(f"- **{row['short_explanation']}**")
        lines.append(f"  - {row['explanation_text']}")
        lines.append("")

    lines.append("")
    lines.append("## Casos de falso negativo")
    lines.append("")
    false_negatives = explanations[explanations["prediction_result"] == "false_negative"]
    if false_negatives.empty:
        lines.append("Nenhum falso negativo encontrado.")
    else:
        lines.append(dataframe_to_markdown_table(false_negatives.loc[:, display_columns], max_rows=20))

    lines.append("")
    lines.append("## Casos de falso positivo")
    lines.append("")
    false_positives = explanations[explanations["prediction_result"] == "false_positive"]
    if false_positives.empty:
        lines.append("Nenhum falso positivo encontrado.")
    else:
        lines.append(dataframe_to_markdown_table(false_positives.loc[:, display_columns], max_rows=20))

    lines.append("")
    lines.append("## Conclusão")
    lines.append("")
    lines.append("Esta camada conecta a probabilidade prevista aos grupos de features usados pelo modelo.")
    lines.append("")
    lines.append("Ela reforça a leitura do projeto como um sistema de análise preditiva, pois permite sair da métrica global e observar, por país, quais fatores do dataset integrado aparecem associados ao risco estimado.")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    OUTPUT_TABLES_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_FINAL_DIR.mkdir(parents=True, exist_ok=True)

    require_file(RISK_ASSESSMENT_PATH)
    require_file(FEATURES_DATASET_PATH)
    require_file(COEFFICIENTS_PATH)
    require_file(MODEL_FEATURES_PATH)

    risk_assessment = pd.read_csv(RISK_ASSESSMENT_PATH)
    features = pd.read_csv(FEATURES_DATASET_PATH)
    coefficients = pd.read_csv(COEFFICIENTS_PATH)
    model_features = json.loads(MODEL_FEATURES_PATH.read_text(encoding="utf-8"))

    feature_columns = model_features.get("feature_columns", [])

    latest_year = int(risk_assessment["year"].max())

    features_latest = features[features["year"] == latest_year].copy()

    required_feature_keys = {"country", "year"}
    if not required_feature_keys.issubset(features_latest.columns):
        raise ValueError("Dataset de features precisa conter country e year.")

    available_countries = set(features_latest["country"])
    risk_assessment = risk_assessment[risk_assessment["country"].isin(available_countries)].copy()

    contribution_table = build_feature_contribution_table(
        features_latest=features_latest,
        coefficients=coefficients,
        feature_columns=feature_columns,
    )

    explanations = summarize_country_explanations(
        risk_assessment=risk_assessment,
        contribution_table=contribution_table,
    )

    group_summary = build_group_summary(
        explanations=explanations,
        contribution_table=contribution_table,
    )

    summary = {
        "latest_year": latest_year,
        "forecast_year": int(explanations["forecast_year"].max()),
        "countries_evaluated": int(len(explanations)),
        "feature_count_from_model_metadata": int(len(feature_columns)),
        "coefficient_count": int(len(coefficients)),
        "explanation_method": "heuristic_coefficient_feature_signal",
        "methodological_warning": (
            "Signals are approximate explanations based on coefficients and relative feature values; "
            "they are not causal effects and not an exact SHAP/logit decomposition."
        ),
        "generated_files": {
            "explanations_csv": str(EXPLANATIONS_PATH.relative_to(PROJECT_ROOT)),
            "group_summary_csv": str(GROUP_SUMMARY_PATH.relative_to(PROJECT_ROOT)),
            "summary_json": str(SUMMARY_JSON_PATH.relative_to(PROJECT_ROOT)),
            "markdown_report": str(MARKDOWN_REPORT_PATH.relative_to(PROJECT_ROOT)),
        },
    }

    explanations.to_csv(EXPLANATIONS_PATH, index=False)
    group_summary.to_csv(GROUP_SUMMARY_PATH, index=False)

    SUMMARY_JSON_PATH.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    markdown_report = create_markdown_report(
        explanations=explanations,
        group_summary=group_summary,
        summary=summary,
    )

    MARKDOWN_REPORT_PATH.write_text(markdown_report, encoding="utf-8")

    print("Country risk explanations generated")
    print("-----------------------------------")
    print(f"Latest year: {summary['latest_year']}")
    print(f"Forecast year: {summary['forecast_year']}")
    print(f"Countries evaluated: {summary['countries_evaluated']}")
    print(f"Feature count: {summary['feature_count_from_model_metadata']}")
    print(f"Coefficient count: {summary['coefficient_count']}")
    print()
    print(f"Explanations CSV: {EXPLANATIONS_PATH}")
    print(f"Group summary CSV: {GROUP_SUMMARY_PATH}")
    print(f"Summary JSON: {SUMMARY_JSON_PATH}")
    print(f"Markdown report: {MARKDOWN_REPORT_PATH}")


if __name__ == "__main__":
    main()
