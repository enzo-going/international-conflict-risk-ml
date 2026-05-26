from __future__ import annotations

from pathlib import Path
import json

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"
OUTPUT_CHARTS_DIR = PROJECT_ROOT / "outputs" / "charts" / "predictive_analysis"
PUBLIC_CHARTS_DIR = PROJECT_ROOT / "docs" / "assets" / "charts" / "predictive_analysis"

OUTPUT_CHARTS_DIR.mkdir(parents=True, exist_ok=True)
PUBLIC_CHARTS_DIR.mkdir(parents=True, exist_ok=True)

THRESHOLD_PATH = OUTPUT_TABLES_DIR / "predictive_threshold_summary.csv"
REGION_PATH = OUTPUT_TABLES_DIR / "predictive_region_summary.csv"
COUNTRY_PATH = OUTPUT_TABLES_DIR / "predictive_country_summary.csv"
TOP_RISK_PATH = OUTPUT_TABLES_DIR / "predictive_top_risk_cases.csv"
SUMMARY_JSON_PATH = OUTPUT_TABLES_DIR / "predictive_analysis_summary.json"

CHART_INDEX_PATH = OUTPUT_CHARTS_DIR / "chart_index.json"


def require_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo obrigatório não encontrado: {path}")


def save_chart(path: Path) -> None:
    plt.tight_layout()
    plt.savefig(path, dpi=160, bbox_inches="tight")
    plt.close()

    public_path = PUBLIC_CHARTS_DIR / path.name
    public_path.write_bytes(path.read_bytes())


def plot_threshold_f1(threshold_df: pd.DataFrame) -> Path:
    output_path = OUTPUT_CHARTS_DIR / "threshold_f1_curve.png"

    df = threshold_df.sort_values("threshold")

    plt.figure(figsize=(10, 6))
    plt.plot(df["threshold"], df["f1_score"], marker="o")
    plt.xlabel("Threshold")
    plt.ylabel("F1-score")
    plt.title("F1-score por threshold")
    plt.grid(True, alpha=0.3)

    save_chart(output_path)
    return output_path


def plot_threshold_precision_recall(threshold_df: pd.DataFrame) -> Path:
    output_path = OUTPUT_CHARTS_DIR / "threshold_precision_recall_curve.png"

    df = threshold_df.sort_values("threshold")

    plt.figure(figsize=(10, 6))
    plt.plot(df["threshold"], df["precision"], marker="o", label="Precision")
    plt.plot(df["threshold"], df["recall"], marker="o", label="Recall")
    plt.xlabel("Threshold")
    plt.ylabel("Score")
    plt.title("Precision e recall por threshold")
    plt.legend()
    plt.grid(True, alpha=0.3)

    save_chart(output_path)
    return output_path


def plot_region_mean_probability(region_df: pd.DataFrame) -> Path:
    output_path = OUTPUT_CHARTS_DIR / "region_mean_predicted_probability.png"

    df = region_df.sort_values("mean_predicted_probability", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(df["region"], df["mean_predicted_probability"])
    plt.xlabel("Probabilidade média prevista")
    plt.ylabel("Região")
    plt.title("Risco médio previsto por região")
    plt.grid(axis="x", alpha=0.3)

    save_chart(output_path)
    return output_path


def plot_region_f1(region_df: pd.DataFrame) -> Path:
    output_path = OUTPUT_CHARTS_DIR / "region_f1_score.png"

    df = region_df.sort_values("f1_score", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(df["region"], df["f1_score"])
    plt.xlabel("F1-score")
    plt.ylabel("Região")
    plt.title("Desempenho do modelo por região")
    plt.grid(axis="x", alpha=0.3)

    save_chart(output_path)
    return output_path


def plot_risk_band_distribution(summary: dict) -> Path:
    output_path = OUTPUT_CHARTS_DIR / "risk_band_distribution.png"

    risk_band_counts = summary.get("risk_band_counts", {})
    order = ["very_low", "low", "moderate", "high", "very_high"]

    labels = [label for label in order if label in risk_band_counts]
    values = [risk_band_counts[label] for label in labels]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values)
    plt.xlabel("Faixa de risco")
    plt.ylabel("Quantidade de casos")
    plt.title("Distribuição das faixas de risco previstas")
    plt.grid(axis="y", alpha=0.3)

    save_chart(output_path)
    return output_path


def plot_prediction_result_counts(summary: dict) -> Path:
    output_path = OUTPUT_CHARTS_DIR / "prediction_result_counts.png"

    error_counts = summary.get("error_counts", {})
    order = ["true_negative", "true_positive", "false_positive", "false_negative"]

    labels = [label for label in order if label in error_counts]
    values = [error_counts[label] for label in labels]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values)
    plt.xlabel("Tipo de resultado")
    plt.ylabel("Quantidade de casos")
    plt.title("Distribuição dos acertos e erros do modelo")
    plt.xticks(rotation=20, ha="right")
    plt.grid(axis="y", alpha=0.3)

    save_chart(output_path)
    return output_path


def plot_top_countries_mean_probability(country_df: pd.DataFrame, limit: int = 15) -> Path:
    output_path = OUTPUT_CHARTS_DIR / "top_countries_mean_predicted_probability.png"

    df = (
        country_df.sort_values("mean_predicted_probability", ascending=False)
        .head(limit)
        .sort_values("mean_predicted_probability", ascending=True)
    )

    plt.figure(figsize=(10, 8))
    plt.barh(df["country"], df["mean_predicted_probability"])
    plt.xlabel("Probabilidade média prevista")
    plt.ylabel("País")
    plt.title(f"Top {limit} países por risco médio previsto")
    plt.grid(axis="x", alpha=0.3)

    save_chart(output_path)
    return output_path



def plot_country_prediction_gap(country_df: pd.DataFrame, limit: int = 15) -> Path:
    output_path = OUTPUT_CHARTS_DIR / "country_prediction_gap.png"

    df = country_df.copy()
    df["prediction_gap"] = df["predicted_conflict_rate"] - df["actual_conflict_rate"]
    df["absolute_prediction_gap"] = df["prediction_gap"].abs()

    df = (
        df[df["years_observed"] >= 3]
        .sort_values("absolute_prediction_gap", ascending=False)
        .head(limit)
        .sort_values("absolute_prediction_gap", ascending=True)
    )

    df["case_label"] = df["country"].astype(str) + " (" + df["region"].astype(str) + ")"

    plt.figure(figsize=(10, 8))
    plt.barh(df["case_label"], df["absolute_prediction_gap"])
    plt.xlabel("Diferença absoluta entre taxa prevista e taxa real")
    plt.ylabel("País")
    plt.title(f"Top {limit} países com maior divergência preditiva")
    plt.grid(axis="x", alpha=0.3)

    save_chart(output_path)
    return output_path


def plot_top_cases_probability(top_risk_df: pd.DataFrame, limit: int = 20) -> Path:
    output_path = OUTPUT_CHARTS_DIR / "top_cases_predicted_probability.png"

    df = top_risk_df.head(limit).copy()
    df["case_label"] = df["country"].astype(str) + " - " + df["year"].astype(str)
    df = df.sort_values("predicted_conflict_probability", ascending=True)

    plt.figure(figsize=(10, 9))
    plt.barh(df["case_label"], df["predicted_conflict_probability"])
    plt.xlabel("Probabilidade prevista")
    plt.ylabel("Caso")
    plt.title(f"Top {limit} casos com maior risco previsto")
    plt.grid(axis="x", alpha=0.3)

    save_chart(output_path)
    return output_path


def main() -> None:
    require_file(THRESHOLD_PATH)
    require_file(REGION_PATH)
    require_file(COUNTRY_PATH)
    require_file(TOP_RISK_PATH)
    require_file(SUMMARY_JSON_PATH)

    threshold_df = pd.read_csv(THRESHOLD_PATH)
    region_df = pd.read_csv(REGION_PATH)
    country_df = pd.read_csv(COUNTRY_PATH)
    top_risk_df = pd.read_csv(TOP_RISK_PATH)
    summary = json.loads(SUMMARY_JSON_PATH.read_text(encoding="utf-8"))

    generated_paths = [
        plot_threshold_f1(threshold_df),
        plot_threshold_precision_recall(threshold_df),
        plot_region_mean_probability(region_df),
        plot_region_f1(region_df),
        plot_risk_band_distribution(summary),
        plot_prediction_result_counts(summary),
        plot_top_countries_mean_probability(country_df),
        plot_country_prediction_gap(country_df),
        plot_top_cases_probability(top_risk_df),
    ]

    chart_index = {
        "chart_count": len(generated_paths),
        "charts": [
            str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")
            for path in generated_paths
        ],
    }

    CHART_INDEX_PATH.write_text(
        json.dumps(chart_index, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    public_chart_index = {
        "chart_count": len(generated_paths),
        "charts": [
            f"assets/charts/predictive_analysis/{path.name}"
            for path in generated_paths
        ],
    }

    (PUBLIC_CHARTS_DIR / "chart_index.json").write_text(
        json.dumps(public_chart_index, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("Predictive charts generated")
    print("---------------------------")
    print(f"Charts generated: {len(generated_paths)}")

    for path in generated_paths:
        print(path)

    print()
    print(f"Chart index: {CHART_INDEX_PATH}")


if __name__ == "__main__":
    main()
