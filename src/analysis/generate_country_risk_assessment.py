from __future__ import annotations

from pathlib import Path
import json
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PREDICTIONS_PATH = PROJECT_ROOT / "outputs" / "tables" / "conflict_risk_model_test_predictions.csv"

OUTPUT_TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"
REPORTS_FINAL_DIR = PROJECT_ROOT / "reports" / "final"

LATEST_RISK_PATH = OUTPUT_TABLES_DIR / "country_risk_assessment_latest_year.csv"
RISK_LEVEL_SUMMARY_PATH = OUTPUT_TABLES_DIR / "country_risk_level_summary.csv"
SUMMARY_JSON_PATH = OUTPUT_TABLES_DIR / "country_risk_assessment_summary.json"
MARKDOWN_REPORT_PATH = REPORTS_FINAL_DIR / "country_risk_assessment_latest_year.md"


REQUIRED_COLUMNS = [
    "country",
    "year",
    "region",
    "target_conflict_next_year",
    "organized_violence_exists",
    "predicted_conflict_next_year",
    "predicted_conflict_probability",
]


def require_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo obrigatório não encontrado: {path}")


def require_columns(df: pd.DataFrame, required_columns: list[str]) -> None:
    missing = [column for column in required_columns if column not in df.columns]
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing}")


def classify_risk_level(probability: float) -> str:
    if probability >= 0.80:
        return "very_high"
    if probability >= 0.60:
        return "high"
    if probability >= 0.40:
        return "moderate"
    if probability >= 0.20:
        return "low"
    return "very_low"


def classify_prediction_result(row: pd.Series) -> str:
    actual = int(row["target_conflict_next_year"])
    predicted = int(row["predicted_conflict_next_year"])

    if actual == 1 and predicted == 1:
        return "true_positive"
    if actual == 0 and predicted == 0:
        return "true_negative"
    if actual == 0 and predicted == 1:
        return "false_positive"
    if actual == 1 and predicted == 0:
        return "false_negative"

    return "unknown"


def risk_level_description(level: str) -> str:
    descriptions = {
        "very_high": "risco muito alto",
        "high": "risco alto",
        "moderate": "risco moderado",
        "low": "risco baixo",
        "very_low": "risco muito baixo",
    }

    return descriptions.get(level, "risco indefinido")


def format_probability(value: float) -> str:
    return f"{value * 100:.1f}%"


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


def build_latest_risk_assessment(predictions: pd.DataFrame) -> pd.DataFrame:
    latest_year = int(predictions["year"].max())
    forecast_year = latest_year + 1

    latest = predictions[predictions["year"] == latest_year].copy()

    latest["forecast_year"] = forecast_year
    latest["risk_level"] = latest["predicted_conflict_probability"].apply(classify_risk_level)
    latest["risk_level_description"] = latest["risk_level"].apply(risk_level_description)
    latest["predicted_probability_percent"] = latest["predicted_conflict_probability"].apply(format_probability)
    latest["prediction_result"] = latest.apply(classify_prediction_result, axis=1)

    latest["predictive_statement"] = latest.apply(
        lambda row: (
            f"Para o ano-base {int(row['year'])}, o modelo estimou "
            f"{format_probability(float(row['predicted_conflict_probability']))} de probabilidade "
            f"de violência organizada em {int(row['forecast_year'])} para {row['country']} "
            f"({risk_level_description(str(row['risk_level']))})."
        ),
        axis=1,
    )

    output_columns = [
        "country",
        "region",
        "year",
        "forecast_year",
        "organized_violence_exists",
        "target_conflict_next_year",
        "predicted_conflict_next_year",
        "predicted_conflict_probability",
        "predicted_probability_percent",
        "risk_level",
        "risk_level_description",
        "prediction_result",
        "predictive_statement",
    ]

    return (
        latest.loc[:, output_columns]
        .sort_values("predicted_conflict_probability", ascending=False)
        .reset_index(drop=True)
    )


def build_risk_level_summary(latest_risk: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []

    for risk_level, group in latest_risk.groupby("risk_level", dropna=False):
        rows.append(
            {
                "risk_level": risk_level,
                "risk_level_description": risk_level_description(str(risk_level)),
                "countries": int(len(group)),
                "mean_probability": float(group["predicted_conflict_probability"].mean()),
                "min_probability": float(group["predicted_conflict_probability"].min()),
                "max_probability": float(group["predicted_conflict_probability"].max()),
                "predicted_positive_count": int(group["predicted_conflict_next_year"].sum()),
                "actual_positive_count": int(group["target_conflict_next_year"].sum()),
            }
        )

    order = {
        "very_high": 5,
        "high": 4,
        "moderate": 3,
        "low": 2,
        "very_low": 1,
    }

    summary = pd.DataFrame(rows)
    summary["risk_level_order"] = summary["risk_level"].map(order).fillna(0)

    return (
        summary.sort_values("risk_level_order", ascending=False)
        .drop(columns=["risk_level_order"])
        .reset_index(drop=True)
    )


def create_markdown_report(
    latest_risk: pd.DataFrame,
    risk_level_summary: pd.DataFrame,
    summary: dict[str, Any],
) -> str:
    top_columns = [
        "country",
        "region",
        "forecast_year",
        "predicted_probability_percent",
        "risk_level_description",
        "predicted_conflict_next_year",
        "target_conflict_next_year",
        "prediction_result",
    ]

    false_negatives = latest_risk[latest_risk["prediction_result"] == "false_negative"]
    false_positives = latest_risk[latest_risk["prediction_result"] == "false_positive"]

    lines: list[str] = []

    lines.append("# Avaliação Preditiva por País")
    lines.append("")
    lines.append("Este relatório traduz as probabilidades do modelo principal em uma análise preditiva por país.")
    lines.append("")
    lines.append("## Escopo")
    lines.append("")
    lines.append(f"- Ano-base analisado: {summary['latest_year']}")
    lines.append(f"- Ano previsto: {summary['forecast_year']}")
    lines.append("- Unidade de análise: country-year")
    lines.append("- Target: target_conflict_next_year")
    lines.append("- Modelo principal: Logistic Regression scaled - World Bank all raw")
    lines.append("")
    lines.append("## Observação metodológica")
    lines.append("")
    lines.append("As probabilidades abaixo são estimativas experimentais do modelo, não previsões determinísticas.")
    lines.append("")
    lines.append("A formulação correta é: o modelo estimou determinada probabilidade de ocorrência de violência organizada no ano seguinte, considerando o padrão aprendido nos dados históricos.")
    lines.append("")
    lines.append("## Resumo executivo")
    lines.append("")
    lines.append(f"- Países avaliados: {summary['countries_evaluated']}")
    lines.append(f"- Probabilidade média estimada: {summary['mean_probability']:.4f}")
    lines.append(f"- Países classificados como risco alto ou muito alto: {summary['high_or_very_high_count']}")
    lines.append(f"- Países com previsão positiva pelo threshold atual: {summary['predicted_positive_count']}")
    lines.append(f"- Países com conflito observado no ano previsto: {summary['actual_positive_count']}")
    lines.append("")
    lines.append("## Distribuição por faixa de risco")
    lines.append("")
    lines.append(dataframe_to_markdown_table(risk_level_summary))
    lines.append("")
    lines.append("## Top 25 países com maior risco estimado")
    lines.append("")
    lines.append(dataframe_to_markdown_table(latest_risk.loc[:, top_columns], max_rows=25))
    lines.append("")
    lines.append("## Exemplos de interpretação")
    lines.append("")

    examples = latest_risk.head(5)
    for _, row in examples.iterrows():
        lines.append(f"- {row['predictive_statement']}")

    lines.append("")
    lines.append("## Falsos negativos no ano previsto")
    lines.append("")
    if false_negatives.empty:
        lines.append("Nenhum falso negativo encontrado para o ano-base analisado.")
    else:
        lines.append(dataframe_to_markdown_table(false_negatives.loc[:, top_columns], max_rows=20))

    lines.append("")
    lines.append("## Falsos positivos no ano previsto")
    lines.append("")
    if false_positives.empty:
        lines.append("Nenhum falso positivo encontrado para o ano-base analisado.")
    else:
        lines.append(dataframe_to_markdown_table(false_positives.loc[:, top_columns], max_rows=20))

    lines.append("")
    lines.append("## Conclusão")
    lines.append("")
    lines.append("Esta camada transforma a saída probabilística do modelo em avaliação preditiva interpretável por país.")
    lines.append("")
    lines.append("Ela complementa as métricas globais, porque permite observar quais países receberam maior risco estimado, quais faixas de risco concentram mais casos e onde o modelo errou no ano previsto.")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    OUTPUT_TABLES_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_FINAL_DIR.mkdir(parents=True, exist_ok=True)

    require_file(PREDICTIONS_PATH)

    predictions = pd.read_csv(PREDICTIONS_PATH)
    require_columns(predictions, REQUIRED_COLUMNS)

    latest_risk = build_latest_risk_assessment(predictions)
    risk_level_summary = build_risk_level_summary(latest_risk)

    latest_year = int(latest_risk["year"].max())
    forecast_year = int(latest_risk["forecast_year"].max())

    high_or_very_high = latest_risk[
        latest_risk["risk_level"].isin(["high", "very_high"])
    ]

    summary = {
        "latest_year": latest_year,
        "forecast_year": forecast_year,
        "countries_evaluated": int(len(latest_risk)),
        "mean_probability": float(latest_risk["predicted_conflict_probability"].mean()),
        "median_probability": float(latest_risk["predicted_conflict_probability"].median()),
        "max_probability": float(latest_risk["predicted_conflict_probability"].max()),
        "min_probability": float(latest_risk["predicted_conflict_probability"].min()),
        "high_or_very_high_count": int(len(high_or_very_high)),
        "predicted_positive_count": int(latest_risk["predicted_conflict_next_year"].sum()),
        "actual_positive_count": int(latest_risk["target_conflict_next_year"].sum()),
        "risk_level_counts": {
            str(key): int(value)
            for key, value in latest_risk["risk_level"].value_counts().to_dict().items()
        },
        "generated_files": {
            "latest_risk_csv": str(LATEST_RISK_PATH.relative_to(PROJECT_ROOT)),
            "risk_level_summary_csv": str(RISK_LEVEL_SUMMARY_PATH.relative_to(PROJECT_ROOT)),
            "summary_json": str(SUMMARY_JSON_PATH.relative_to(PROJECT_ROOT)),
            "markdown_report": str(MARKDOWN_REPORT_PATH.relative_to(PROJECT_ROOT)),
        },
    }

    latest_risk.to_csv(LATEST_RISK_PATH, index=False)
    risk_level_summary.to_csv(RISK_LEVEL_SUMMARY_PATH, index=False)

    SUMMARY_JSON_PATH.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    markdown_report = create_markdown_report(
        latest_risk=latest_risk,
        risk_level_summary=risk_level_summary,
        summary=summary,
    )

    MARKDOWN_REPORT_PATH.write_text(markdown_report, encoding="utf-8")

    print("Country risk assessment generated")
    print("---------------------------------")
    print(f"Latest year: {latest_year}")
    print(f"Forecast year: {forecast_year}")
    print(f"Countries evaluated: {summary['countries_evaluated']}")
    print(f"Mean probability: {summary['mean_probability']:.4f}")
    print(f"High or very high risk countries: {summary['high_or_very_high_count']}")
    print(f"Predicted positive count: {summary['predicted_positive_count']}")
    print(f"Actual positive count: {summary['actual_positive_count']}")
    print()
    print(f"Latest risk CSV: {LATEST_RISK_PATH}")
    print(f"Risk level summary CSV: {RISK_LEVEL_SUMMARY_PATH}")
    print(f"Summary JSON: {SUMMARY_JSON_PATH}")
    print(f"Markdown report: {MARKDOWN_REPORT_PATH}")


if __name__ == "__main__":
    main()
