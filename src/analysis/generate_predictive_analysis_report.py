from __future__ import annotations

from pathlib import Path
import json
from typing import Any

import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PREDICTIONS_PATH = PROJECT_ROOT / "outputs" / "tables" / "conflict_risk_model_test_predictions.csv"
METRICS_PATH = PROJECT_ROOT / "outputs" / "tables" / "conflict_risk_model_metrics.csv"
COEFFICIENTS_PATH = PROJECT_ROOT / "outputs" / "tables" / "conflict_risk_model_coefficients.csv"
CANDIDATE_MODELS_PATH = PROJECT_ROOT / "outputs" / "tables" / "candidate_model_comparison.csv"
VALIDATION_SUMMARY_PATH = PROJECT_ROOT / "outputs" / "tables" / "project_validation_summary.json"

OUTPUT_TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"
REPORTS_FINAL_DIR = PROJECT_ROOT / "reports" / "final"

TOP_RISK_PATH = OUTPUT_TABLES_DIR / "predictive_top_risk_cases.csv"
ERROR_ANALYSIS_PATH = OUTPUT_TABLES_DIR / "predictive_error_analysis.csv"
REGION_SUMMARY_PATH = OUTPUT_TABLES_DIR / "predictive_region_summary.csv"
COUNTRY_SUMMARY_PATH = OUTPUT_TABLES_DIR / "predictive_country_summary.csv"
THRESHOLD_SUMMARY_PATH = OUTPUT_TABLES_DIR / "predictive_threshold_summary.csv"
SUMMARY_JSON_PATH = OUTPUT_TABLES_DIR / "predictive_analysis_summary.json"
MARKDOWN_REPORT_PATH = REPORTS_FINAL_DIR / "predictive_analysis_report.md"


REQUIRED_PREDICTION_COLUMNS = [
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


def require_columns(df: pd.DataFrame, required_columns: list[str], file_label: str) -> None:
    missing = [column for column in required_columns if column not in df.columns]
    if missing:
        raise ValueError(f"{file_label} sem colunas obrigatórias: {missing}")


def risk_band(probability: float) -> str:
    if probability >= 0.80:
        return "very_high"
    if probability >= 0.60:
        return "high"
    if probability >= 0.40:
        return "moderate"
    if probability >= 0.20:
        return "low"
    return "very_low"


def classify_error(row: pd.Series) -> str:
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


def safe_metric(metric_function: Any, y_true: pd.Series, y_pred: pd.Series) -> float:
    try:
        return float(metric_function(y_true, y_pred, zero_division=0))
    except TypeError:
        return float(metric_function(y_true, y_pred))



def format_markdown_value(value: Any) -> str:
    if pd.isna(value):
        return ""

    if isinstance(value, float):
        return f"{value:.4f}"

    return str(value).replace("\n", " ").replace("|", "\\|")


def dataframe_to_markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_Sem registros._"

    columns = [str(column) for column in df.columns]

    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"

    rows = []
    for _, row in df.iterrows():
        values = [format_markdown_value(row[column]) for column in df.columns]
        rows.append("| " + " | ".join(values) + " |")

    return "\n".join([header, separator, *rows])

def load_validation_summary() -> dict[str, Any]:
    if not VALIDATION_SUMMARY_PATH.exists():
        return {
            "available": False,
            "detail": "validation summary not found",
        }

    return {
        "available": True,
        "content": json.loads(VALIDATION_SUMMARY_PATH.read_text(encoding="utf-8")),
    }


def build_top_risk_table(predictions: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "country",
        "year",
        "region",
        "target_conflict_next_year",
        "organized_violence_exists",
        "predicted_conflict_next_year",
        "predicted_conflict_probability",
        "risk_band",
        "prediction_result",
    ]

    return (
        predictions.sort_values("predicted_conflict_probability", ascending=False)
        .loc[:, columns]
        .head(100)
        .reset_index(drop=True)
    )


def build_error_analysis(predictions: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "country",
        "year",
        "region",
        "target_conflict_next_year",
        "organized_violence_exists",
        "predicted_conflict_next_year",
        "predicted_conflict_probability",
        "risk_band",
        "prediction_result",
    ]

    errors = predictions[predictions["prediction_result"].isin(["false_positive", "false_negative"])]

    return (
        errors.sort_values(
            ["prediction_result", "predicted_conflict_probability"],
            ascending=[True, False],
        )
        .loc[:, columns]
        .reset_index(drop=True)
    )


def build_region_summary(predictions: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []

    for region, group in predictions.groupby("region", dropna=False):
        y_true = group["target_conflict_next_year"]
        y_pred = group["predicted_conflict_next_year"]

        tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()

        rows.append(
            {
                "region": region,
                "cases": int(len(group)),
                "countries": int(group["country"].nunique()),
                "actual_positive_rate": float(y_true.mean()),
                "predicted_positive_rate": float(y_pred.mean()),
                "mean_predicted_probability": float(group["predicted_conflict_probability"].mean()),
                "max_predicted_probability": float(group["predicted_conflict_probability"].max()),
                "accuracy": safe_metric(accuracy_score, y_true, y_pred),
                "precision": safe_metric(precision_score, y_true, y_pred),
                "recall": safe_metric(recall_score, y_true, y_pred),
                "f1_score": safe_metric(f1_score, y_true, y_pred),
                "true_negatives": int(tn),
                "false_positives": int(fp),
                "false_negatives": int(fn),
                "true_positives": int(tp),
            }
        )

    return pd.DataFrame(rows).sort_values(
        ["mean_predicted_probability", "actual_positive_rate"],
        ascending=False,
    )


def build_country_summary(predictions: pd.DataFrame) -> pd.DataFrame:
    grouped = predictions.groupby(["country", "region"], dropna=False)

    summary = grouped.agg(
        years_observed=("year", "count"),
        first_test_year=("year", "min"),
        last_test_year=("year", "max"),
        actual_conflict_years=("target_conflict_next_year", "sum"),
        predicted_conflict_years=("predicted_conflict_next_year", "sum"),
        previous_conflict_years=("organized_violence_exists", "sum"),
        mean_predicted_probability=("predicted_conflict_probability", "mean"),
        max_predicted_probability=("predicted_conflict_probability", "max"),
    ).reset_index()

    summary["actual_conflict_rate"] = (
        summary["actual_conflict_years"] / summary["years_observed"]
    )

    summary["predicted_conflict_rate"] = (
        summary["predicted_conflict_years"] / summary["years_observed"]
    )

    return summary.sort_values(
        ["max_predicted_probability", "mean_predicted_probability"],
        ascending=False,
    )


def build_threshold_summary(predictions: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []

    y_true = predictions["target_conflict_next_year"]
    probabilities = predictions["predicted_conflict_probability"]

    for threshold in [round(value / 100, 2) for value in range(10, 91, 5)]:
        y_pred = (probabilities >= threshold).astype(int)

        tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()

        rows.append(
            {
                "threshold": threshold,
                "predicted_positive_rate": float(y_pred.mean()),
                "accuracy": safe_metric(accuracy_score, y_true, y_pred),
                "precision": safe_metric(precision_score, y_true, y_pred),
                "recall": safe_metric(recall_score, y_true, y_pred),
                "f1_score": safe_metric(f1_score, y_true, y_pred),
                "true_negatives": int(tn),
                "false_positives": int(fp),
                "false_negatives": int(fn),
                "true_positives": int(tp),
            }
        )

    return pd.DataFrame(rows).sort_values("f1_score", ascending=False)


def load_main_metrics() -> dict[str, Any]:
    require_file(METRICS_PATH)

    metrics = pd.read_csv(METRICS_PATH)

    logistic = metrics[
        metrics["model"].astype(str).str.contains("Logistic Regression", case=False, na=False)
    ]

    baseline = metrics[
        metrics["model"].astype(str).str.contains("Persistence", case=False, na=False)
    ]

    result: dict[str, Any] = {
        "available": True,
        "rows": int(len(metrics)),
    }

    if not logistic.empty:
        result["main_model"] = logistic.iloc[0].to_dict()

    if not baseline.empty:
        result["baseline"] = baseline.iloc[0].to_dict()

    if "main_model" in result and "baseline" in result:
        result["f1_gain_vs_baseline"] = (
            float(result["main_model"]["f1_score"]) - float(result["baseline"]["f1_score"])
        )

    return result


def load_top_coefficients(limit: int = 15) -> list[dict[str, Any]]:
    if not COEFFICIENTS_PATH.exists():
        return []

    coefficients = pd.read_csv(COEFFICIENTS_PATH)

    if "absolute_coefficient" in coefficients.columns:
        coefficients = coefficients.sort_values("absolute_coefficient", ascending=False)

    return coefficients.head(limit).to_dict(orient="records")


def load_candidate_model_summary() -> list[dict[str, Any]]:
    if not CANDIDATE_MODELS_PATH.exists():
        return []

    candidates = pd.read_csv(CANDIDATE_MODELS_PATH)

    if "f1_score" in candidates.columns:
        candidates = candidates.sort_values("f1_score", ascending=False)

    return candidates.to_dict(orient="records")


def create_markdown_report(
    predictions: pd.DataFrame,
    top_risk: pd.DataFrame,
    errors: pd.DataFrame,
    region_summary: pd.DataFrame,
    threshold_summary: pd.DataFrame,
    summary: dict[str, Any],
) -> str:
    false_positives = errors[errors["prediction_result"] == "false_positive"]
    false_negatives = errors[errors["prediction_result"] == "false_negative"]

    best_threshold = threshold_summary.iloc[0].to_dict()

    lines: list[str] = []

    lines.append("# Relatório de Análise Preditiva")
    lines.append("")
    lines.append("Este relatório resume os principais resultados preditivos do modelo principal do projeto International Conflict Risk ML.")
    lines.append("")
    lines.append("## Escopo")
    lines.append("")
    lines.append("Unidade de análise: country-year.")
    lines.append("")
    lines.append("Target: target_conflict_next_year.")
    lines.append("")
    lines.append("Modelo principal: Logistic Regression scaled - World Bank all raw.")
    lines.append("")
    lines.append("## Resumo executivo")
    lines.append("")
    lines.append(f"- Casos avaliados: {len(predictions)}")
    lines.append(f"- Países avaliados: {predictions['country'].nunique()}")
    lines.append(f"- Intervalo temporal de teste: {int(predictions['year'].min())}-{int(predictions['year'].max())}")
    lines.append(f"- Taxa real de conflito no ano seguinte: {predictions['target_conflict_next_year'].mean():.4f}")
    lines.append(f"- Taxa prevista de conflito no ano seguinte: {predictions['predicted_conflict_next_year'].mean():.4f}")
    lines.append(f"- Probabilidade média prevista: {predictions['predicted_conflict_probability'].mean():.4f}")
    lines.append(f"- Falsos positivos: {len(false_positives)}")
    lines.append(f"- Falsos negativos: {len(false_negatives)}")
    lines.append("")
    lines.append("## Métrica principal")
    lines.append("")

    main_metrics = summary.get("main_metrics", {})
    if "main_model" in main_metrics:
        model = main_metrics["main_model"]
        lines.append(f"- Modelo: {model.get('model')}")
        lines.append(f"- Accuracy: {float(model.get('accuracy')):.4f}")
        lines.append(f"- Precision: {float(model.get('precision')):.4f}")
        lines.append(f"- Recall: {float(model.get('recall')):.4f}")
        lines.append(f"- F1-score: {float(model.get('f1_score')):.4f}")

    if "baseline" in main_metrics:
        baseline = main_metrics["baseline"]
        lines.append("")
        lines.append(f"- Baseline: {baseline.get('model')}")
        lines.append(f"- Baseline F1-score: {float(baseline.get('f1_score')):.4f}")

    if "f1_gain_vs_baseline" in main_metrics:
        lines.append(f"- Ganho de F1 vs baseline: {float(main_metrics['f1_gain_vs_baseline']):.4f}")

    lines.append("")
    lines.append("## Threshold com melhor F1 na varredura")
    lines.append("")
    lines.append(f"- Threshold: {float(best_threshold['threshold']):.2f}")
    lines.append(f"- Precision: {float(best_threshold['precision']):.4f}")
    lines.append(f"- Recall: {float(best_threshold['recall']):.4f}")
    lines.append(f"- F1-score: {float(best_threshold['f1_score']):.4f}")
    lines.append("")
    lines.append("## Top 10 maiores riscos previstos")
    lines.append("")
    lines.append(dataframe_to_markdown_table(top_risk.head(10)))
    lines.append("")
    lines.append("## Resumo por região")
    lines.append("")
    region_columns = [
        "region",
        "cases",
        "countries",
        "actual_positive_rate",
        "predicted_positive_rate",
        "mean_predicted_probability",
        "f1_score",
    ]
    lines.append(dataframe_to_markdown_table(region_summary.loc[:, region_columns]))
    lines.append("")
    lines.append("## Principais falsos positivos")
    lines.append("")
    if false_positives.empty:
        lines.append("Nenhum falso positivo encontrado.")
    else:
        lines.append(dataframe_to_markdown_table(false_positives.head(10)))
    lines.append("")
    lines.append("## Principais falsos negativos")
    lines.append("")
    if false_negatives.empty:
        lines.append("Nenhum falso negativo encontrado.")
    else:
        lines.append(dataframe_to_markdown_table(false_negatives.head(10)))
    lines.append("")
    lines.append("## Interpretação")
    lines.append("")
    lines.append("O modelo deve ser interpretado como um sistema experimental de estimativa de risco, não como previsão determinística de eventos geopolíticos.")
    lines.append("")
    lines.append("A análise de falsos positivos e falsos negativos é essencial para avaliar onde o modelo superestima ou subestima risco.")
    lines.append("")
    lines.append("O resultado mais relevante não é apenas o ranking de risco, mas a comparação entre baseline, modelo principal, thresholds e erros.")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    require_file(PREDICTIONS_PATH)

    predictions = pd.read_csv(PREDICTIONS_PATH)
    require_columns(predictions, REQUIRED_PREDICTION_COLUMNS, str(PREDICTIONS_PATH))

    predictions = predictions.copy()
    predictions["risk_band"] = predictions["predicted_conflict_probability"].apply(risk_band)
    predictions["prediction_result"] = predictions.apply(classify_error, axis=1)

    top_risk = build_top_risk_table(predictions)
    error_analysis = build_error_analysis(predictions)
    region_summary = build_region_summary(predictions)
    country_summary = build_country_summary(predictions)
    threshold_summary = build_threshold_summary(predictions)

    main_metrics = load_main_metrics()
    top_coefficients = load_top_coefficients()
    candidate_models = load_candidate_model_summary()
    validation_summary = load_validation_summary()

    summary = {
        "analysis_scope": {
            "unit": "country-year",
            "target": "target_conflict_next_year",
            "prediction_column": "predicted_conflict_probability",
            "test_start_year": int(predictions["year"].min()),
            "test_end_year": int(predictions["year"].max()),
            "n_cases": int(len(predictions)),
            "n_countries": int(predictions["country"].nunique()),
            "n_regions": int(predictions["region"].nunique()),
        },
        "prediction_distribution": {
            "actual_positive_rate": float(predictions["target_conflict_next_year"].mean()),
            "predicted_positive_rate": float(predictions["predicted_conflict_next_year"].mean()),
            "mean_probability": float(predictions["predicted_conflict_probability"].mean()),
            "median_probability": float(predictions["predicted_conflict_probability"].median()),
            "max_probability": float(predictions["predicted_conflict_probability"].max()),
            "min_probability": float(predictions["predicted_conflict_probability"].min()),
        },
        "error_counts": {
            key: int(value)
            for key, value in predictions["prediction_result"].value_counts().to_dict().items()
        },
        "risk_band_counts": {
            key: int(value)
            for key, value in predictions["risk_band"].value_counts().to_dict().items()
        },
        "main_metrics": main_metrics,
        "best_threshold_by_f1": threshold_summary.iloc[0].to_dict(),
        "top_coefficients": top_coefficients,
        "candidate_models": candidate_models,
        "validation_summary": validation_summary,
        "generated_files": {
            "top_risk": str(TOP_RISK_PATH.relative_to(PROJECT_ROOT)),
            "error_analysis": str(ERROR_ANALYSIS_PATH.relative_to(PROJECT_ROOT)),
            "region_summary": str(REGION_SUMMARY_PATH.relative_to(PROJECT_ROOT)),
            "country_summary": str(COUNTRY_SUMMARY_PATH.relative_to(PROJECT_ROOT)),
            "threshold_summary": str(THRESHOLD_SUMMARY_PATH.relative_to(PROJECT_ROOT)),
            "summary_json": str(SUMMARY_JSON_PATH.relative_to(PROJECT_ROOT)),
            "markdown_report": str(MARKDOWN_REPORT_PATH.relative_to(PROJECT_ROOT)),
        },
    }

    top_risk.to_csv(TOP_RISK_PATH, index=False)
    error_analysis.to_csv(ERROR_ANALYSIS_PATH, index=False)
    region_summary.to_csv(REGION_SUMMARY_PATH, index=False)
    country_summary.to_csv(COUNTRY_SUMMARY_PATH, index=False)
    threshold_summary.to_csv(THRESHOLD_SUMMARY_PATH, index=False)

    SUMMARY_JSON_PATH.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    markdown_report = create_markdown_report(
        predictions=predictions,
        top_risk=top_risk,
        errors=error_analysis,
        region_summary=region_summary,
        threshold_summary=threshold_summary,
        summary=summary,
    )

    MARKDOWN_REPORT_PATH.write_text(markdown_report, encoding="utf-8")

    print("Predictive analysis report generated")
    print("------------------------------------")
    print(f"Cases: {len(predictions)}")
    print(f"Countries: {predictions['country'].nunique()}")
    print(f"Years: {int(predictions['year'].min())}-{int(predictions['year'].max())}")
    print(f"Top risk table: {TOP_RISK_PATH}")
    print(f"Error analysis: {ERROR_ANALYSIS_PATH}")
    print(f"Region summary: {REGION_SUMMARY_PATH}")
    print(f"Country summary: {COUNTRY_SUMMARY_PATH}")
    print(f"Threshold summary: {THRESHOLD_SUMMARY_PATH}")
    print(f"Summary JSON: {SUMMARY_JSON_PATH}")
    print(f"Markdown report: {MARKDOWN_REPORT_PATH}")


if __name__ == "__main__":
    main()
