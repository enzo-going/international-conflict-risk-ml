from __future__ import annotations

from pathlib import Path
import json
from datetime import datetime
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIRS = [
    PROJECT_ROOT / "data" / "raw",
    PROJECT_ROOT / "data" / "interim",
    PROJECT_ROOT / "data" / "processed",
    PROJECT_ROOT / "data" / "final",
]

OUTPUT_TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"
REPORTS_FINAL_DIR = PROJECT_ROOT / "reports" / "final"

AUDIT_CSV_PATH = OUTPUT_TABLES_DIR / "dataset_integration_audit.csv"
SUMMARY_JSON_PATH = OUTPUT_TABLES_DIR / "dataset_integration_summary.json"
MARKDOWN_REPORT_PATH = REPORTS_FINAL_DIR / "dataset_integration_audit.md"

SUPPORTED_EXTENSIONS = {
    ".csv",
    ".xlsx",
    ".xls",
    ".json",
    ".parquet",
}


COUNTRY_HINTS = {
    "country",
    "country_name",
    "countryname",
    "state",
    "state_name",
    "location",
    "territory",
    "iso3",
    "iso_code",
    "world_bank_country_code",
    "world_bank_country_name",
}

YEAR_HINTS = {
    "year",
    "yr",
    "start_year",
    "end_year",
    "year_start",
    "year_end",
}

DATE_HINTS = {
    "date",
    "start_date",
    "end_date",
    "event_date",
    "date_start",
    "date_end",
}

EVENT_HINTS = {
    "event_id",
    "eventid",
    "event",
    "conflict_id",
    "dyad_id",
    "battle_id",
}

ACTOR_HINTS = {
    "actor",
    "actor_name",
    "actor1",
    "actor2",
    "side_a",
    "side_b",
    "source_actor",
    "target_actor",
}

TARGET_HINTS = {
    "target_conflict_next_year",
    "target_next_year",
    "target",
    "label",
    "y",
}

FATALITY_HINTS = {
    "deaths",
    "fatalities",
    "fatality",
    "best_fatality_estimate",
    "total_deaths",
    "total_fatalities",
    "casualties",
    "total_casualties",
}


def normalize_column_name(column: str) -> str:
    return (
        str(column)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace(".", "_")
        .replace("/", "_")
        .replace("(", "")
        .replace(")", "")
    )


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


def detect_layer(path: Path) -> str:
    parts = [part.lower() for part in path.parts]

    for layer in ["raw", "interim", "processed", "final", "database"]:
        if layer in parts:
            return layer

    return "unknown"


def detect_source_name(relative_path: str) -> str:
    text = relative_path.lower()

    source_keywords = [
        ("project_final_dataset", ["conflict_country_year_base", "conflict_country_year_temporal"]),
        ("project_world_bank_dataset", ["conflict_country_year_world_bank"]),
        ("world_bank", ["world_bank", "worldbank", "wb_"]),
        ("ucdp_one_sided", ["one-sided", "one_sided", "onesided"]),
        ("ucdp", ["ucdp", "organizedviolencecy"]),
        ("wwi", ["wwi", "world_war_1", "world war 1", "primeira_guerra"]),
        ("wwii", ["wwii", "world_war_2", "world war 2", "segunda_guerra"]),
        ("acled", ["acled"]),
        ("sipri", ["sipri"]),
        ("unhcr", ["unhcr", "refugee", "refugees"]),
        ("correlates_of_war", ["correlates", "cow_", "alliances"]),
        ("wgi", ["wgi", "governance"]),
        ("v_dem", ["v-dem", "v_dem", "vdem"]),
        ("fragile_states_index", ["fragile", "fsi"]),
        ("nd_gain", ["nd-gain", "nd_gain", "gain"]),
        ("imf", ["imf", "weo"]),
        ("country_mapping", ["mapping", "country_name_mapping"]),
    ]

    for source_name, keywords in source_keywords:
        if any(keyword in text for keyword in keywords):
            return source_name

    return "unknown"


def try_read_dataset(path: Path) -> tuple[pd.DataFrame | None, str]:
    suffix = path.suffix.lower()

    try:
        if suffix == ".csv":
            try:
                return pd.read_csv(path), "read_csv:utf8_or_default"
            except UnicodeDecodeError:
                return pd.read_csv(path, encoding="latin1"), "read_csv:latin1"

        if suffix in {".xlsx", ".xls"}:
            return pd.read_excel(path), "read_excel:first_sheet"

        if suffix == ".json":
            try:
                return pd.read_json(path), "read_json"
            except ValueError:
                data = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    return pd.DataFrame(data), "json:list_to_dataframe"
                if isinstance(data, dict):
                    return pd.json_normalize(data), "json:normalized_dict"
                return None, "json:unsupported_structure"

        if suffix == ".parquet":
            return pd.read_parquet(path), "read_parquet"

        return None, "unsupported_extension"

    except Exception as error:
        return None, f"read_error:{type(error).__name__}: {error}"


def detect_unit(columns: list[str]) -> str:
    normalized = {normalize_column_name(column) for column in columns}

    has_country = bool(normalized & COUNTRY_HINTS)
    has_year = bool(normalized & YEAR_HINTS)
    has_date = bool(normalized & DATE_HINTS)
    has_event = bool(normalized & EVENT_HINTS)
    has_actor = bool(normalized & ACTOR_HINTS)

    if has_country and has_year and not has_event and not has_actor:
        return "country-year"

    if has_country and has_year and has_actor:
        return "actor-country-year"

    if has_country and has_year and has_event:
        return "event-country-year"

    if has_country and has_date and has_event:
        return "event-level-with-country-date"

    if has_country and has_date:
        return "country-date"

    if has_country and not has_year and not has_date:
        return "country-only"

    if has_year and not has_country:
        return "year-only"

    if has_date and not has_country:
        return "date-only"

    return "unknown"


def detect_flags(columns: list[str]) -> dict[str, bool]:
    normalized = {normalize_column_name(column) for column in columns}

    return {
        "has_country": bool(normalized & COUNTRY_HINTS),
        "has_year": bool(normalized & YEAR_HINTS),
        "has_date": bool(normalized & DATE_HINTS),
        "has_event_id": bool(normalized & EVENT_HINTS),
        "has_actor": bool(normalized & ACTOR_HINTS),
        "has_target": bool(normalized & TARGET_HINTS),
        "has_fatality_signal": bool(normalized & FATALITY_HINTS),
    }


def classify_dataset(
    relative_path: str,
    source_name: str,
    layer: str,
    detected_unit: str,
    flags: dict[str, bool],
    columns: list[str],
    row_count: int | None,
) -> tuple[str, str, str]:
    path_lower = relative_path.lower()
    normalized_columns = {normalize_column_name(column) for column in columns}

    if "country_year_features" in path_lower or "conflict_risk_model" in path_lower:
        return (
            "official_pipeline",
            "official",
            "Artefato diretamente relacionado ao pipeline principal de modelagem.",
        )

    if source_name in {"project_final_dataset", "project_world_bank_dataset"}:
        return (
            "official_project_dataset",
            "official",
            "Dataset final produzido pelo pipeline do projeto e compatível com a unidade country-year.",
        )

    if source_name == "world_bank" and layer == "raw":
        return (
            "raw_source_reference",
            "supporting_raw_data",
            "Arquivo bruto World Bank preservado para rastreabilidade; a integração ocorre por dataset processado/final.",
        )

    if source_name == "world_bank":
        return (
            "official_or_already_integrated",
            "official",
            "Fonte externa socioeconômica já utilizada ou alinhada ao pipeline principal.",
        )

    if source_name == "ucdp" and layer == "raw":
        return (
            "official_raw_source",
            "supporting_raw_data",
            "Arquivo bruto UCDP preservado como fonte central; a modelagem usa versões processadas/finais.",
        )

    if source_name == "ucdp" and detected_unit == "country-year":
        return (
            "official_or_candidate",
            "official",
            "Fonte UCDP em estrutura compatível com a unidade country-year.",
        )

    if source_name in {"ucdp_one_sided", "wwi", "wwii"}:
        return (
            "experimental_review",
            "experimental",
            "Fonte adicionada pelo grupo ou módulo paralelo; requer validação e possível agregação antes de integração ao pipeline principal.",
        )

    if detected_unit == "country-year":
        return (
            "candidate_for_main_pipeline",
            "candidate",
            "Dataset possui sinais mínimos de país e ano, podendo ser avaliado para integração futura.",
        )

    if detected_unit in {
        "actor-country-year",
        "event-country-year",
        "event-level-with-country-date",
        "country-date",
    }:
        return (
            "requires_transformation",
            "candidate_after_processing",
            "Dataset pode ser útil, mas precisa ser agregado ou transformado para country-year.",
        )

    if flags["has_country"] and not flags["has_year"] and not flags["has_date"]:
        return (
            "requires_temporal_key",
            "not_ready",
            "Possui país/localidade, mas não possui chave temporal clara.",
        )

    if flags["has_year"] and not flags["has_country"]:
        return (
            "requires_country_key",
            "not_ready",
            "Possui ano, mas não possui país/localidade clara para integração.",
        )

    if row_count == 0:
        return (
            "empty_or_invalid",
            "reject",
            "Arquivo sem linhas úteis detectadas.",
        )

    return (
        "not_directly_integrable",
        "not_ready",
        "Não possui sinais mínimos suficientes para integração direta ao pipeline country-year.",
    )


def audit_file(path: Path) -> dict[str, Any]:
    relative_path = str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")
    stat = path.stat()

    layer = detect_layer(path)
    source_name = detect_source_name(relative_path)

    dataset, read_status = try_read_dataset(path)

    if dataset is None:
        columns: list[str] = []
        row_count = None
        column_count = None
        detected_unit = "unreadable_or_unsupported"
        flags = {
            "has_country": False,
            "has_year": False,
            "has_date": False,
            "has_event_id": False,
            "has_actor": False,
            "has_target": False,
            "has_fatality_signal": False,
        }
    else:
        columns = [str(column) for column in dataset.columns]
        row_count = int(len(dataset))
        column_count = int(len(dataset.columns))
        detected_unit = detect_unit(columns)
        flags = detect_flags(columns)

    integration_status, decision, reason = classify_dataset(
        relative_path=relative_path,
        source_name=source_name,
        layer=layer,
        detected_unit=detected_unit,
        flags=flags,
        columns=columns,
        row_count=row_count,
    )

    return {
        "dataset_path": relative_path,
        "file_name": path.name,
        "extension": path.suffix.lower(),
        "layer": layer,
        "source_name": source_name,
        "file_size_kb": round(stat.st_size / 1024, 2),
        "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
        "read_status": read_status,
        "rows": row_count,
        "columns": column_count,
        "detected_unit": detected_unit,
        "has_country": flags["has_country"],
        "has_year": flags["has_year"],
        "has_date": flags["has_date"],
        "has_event_id": flags["has_event_id"],
        "has_actor": flags["has_actor"],
        "has_target": flags["has_target"],
        "has_fatality_signal": flags["has_fatality_signal"],
        "integration_status": integration_status,
        "decision": decision,
        "reason": reason,
        "column_sample": ", ".join(columns[:18]),
    }


def collect_dataset_files() -> list[Path]:
    files: list[Path] = []

    for data_dir in DATA_DIRS:
        if not data_dir.exists():
            continue

        for path in data_dir.rglob("*"):
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
                files.append(path)

    return sorted(files)


def build_markdown_report(audit_df: pd.DataFrame, summary: dict[str, Any]) -> str:
    lines: list[str] = []

    lines.append("# Auditoria de Integração de Datasets")
    lines.append("")
    lines.append("Este relatório resume a situação dos datasets presentes no projeto e avalia sua compatibilidade com o pipeline principal de Machine Learning.")
    lines.append("")
    lines.append("## Critério central")
    lines.append("")
    lines.append("A unidade oficial do pipeline principal é `country-year`.")
    lines.append("")
    lines.append("Datasets que não possuem país/localidade e ano precisam ser transformados, agregados ou mantidos como módulos experimentais antes de entrar no modelo principal.")
    lines.append("")
    lines.append("## Resumo executivo")
    lines.append("")
    lines.append(f"- Total de datasets auditados: {summary['total_datasets']}")
    lines.append(f"- Datasets compatíveis ou candidatos ao pipeline principal: {summary['candidate_or_official_count']}")
    lines.append(f"- Datasets experimentais/em revisão: {summary['experimental_count']}")
    lines.append(f"- Arquivos brutos preservados como suporte/rastreabilidade: {summary.get('supporting_raw_data_count', 0)}")
    lines.append(f"- Datasets que requerem transformação: {summary['requires_transformation_count']}")
    lines.append(f"- Datasets ainda não prontos ou não integráveis diretamente: {summary['not_ready_or_reject_count']}")
    lines.append("")
    lines.append("## Contagem por decisão")
    lines.append("")
    decision_df = (
        audit_df["decision"]
        .value_counts()
        .rename_axis("decision")
        .reset_index(name="count")
    )
    lines.append(dataframe_to_markdown_table(decision_df))
    lines.append("")
    lines.append("## Contagem por fonte detectada")
    lines.append("")
    source_df = (
        audit_df["source_name"]
        .value_counts()
        .rename_axis("source_name")
        .reset_index(name="count")
    )
    lines.append(dataframe_to_markdown_table(source_df))
    lines.append("")
    lines.append("## Datasets oficiais, candidatos e experimentais")
    lines.append("")
    relevant = audit_df[
        audit_df["decision"].isin(
            ["official", "candidate", "candidate_after_processing", "experimental", "supporting_raw_data"]
        )
    ].copy()

    display_columns = [
        "dataset_path",
        "source_name",
        "layer",
        "rows",
        "columns",
        "detected_unit",
        "integration_status",
        "decision",
        "reason",
    ]

    lines.append(dataframe_to_markdown_table(relevant.loc[:, display_columns], max_rows=40))
    lines.append("")
    lines.append("## Datasets não prontos")
    lines.append("")
    not_ready = audit_df[
        audit_df["decision"].isin(["not_ready", "reject"])
    ].copy()

    lines.append(dataframe_to_markdown_table(not_ready.loc[:, display_columns], max_rows=40))
    lines.append("")
    lines.append("## Decisão metodológica")
    lines.append("")
    lines.append("Nem todo dataset presente no repositório deve ser integrado automaticamente ao modelo principal.")
    lines.append("")
    lines.append("A decisão atual é manter o pipeline oficial baseado em `country-year`, preservar módulos experimentais documentados e integrar novos datasets apenas quando houver chave temporal, chave geográfica e justificativa metodológica.")
    lines.append("")
    lines.append("Essa abordagem evita que datasets adicionados pelo grupo prejudiquem a consistência do modelo final.")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    OUTPUT_TABLES_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_FINAL_DIR.mkdir(parents=True, exist_ok=True)

    files = collect_dataset_files()

    rows = [audit_file(path) for path in files]

    audit_df = pd.DataFrame(rows)

    if audit_df.empty:
        audit_df = pd.DataFrame(
            columns=[
                "dataset_path",
                "file_name",
                "extension",
                "layer",
                "source_name",
                "file_size_kb",
                "modified_at",
                "read_status",
                "rows",
                "columns",
                "detected_unit",
                "has_country",
                "has_year",
                "has_date",
                "has_event_id",
                "has_actor",
                "has_target",
                "has_fatality_signal",
                "integration_status",
                "decision",
                "reason",
                "column_sample",
            ]
        )

    audit_df = audit_df.sort_values(
        ["decision", "source_name", "layer", "dataset_path"],
        ascending=[True, True, True, True],
    )

    audit_df.to_csv(AUDIT_CSV_PATH, index=False)

    decision_counts = audit_df["decision"].value_counts().to_dict()
    integration_counts = audit_df["integration_status"].value_counts().to_dict()
    source_counts = audit_df["source_name"].value_counts().to_dict()
    unit_counts = audit_df["detected_unit"].value_counts().to_dict()

    summary = {
        "total_datasets": int(len(audit_df)),
        "candidate_or_official_count": int(
            audit_df["decision"].isin(["official", "candidate"]).sum()
        ),
        "experimental_count": int((audit_df["decision"] == "experimental").sum()),
        "requires_transformation_count": int(
            audit_df["decision"].isin(["candidate_after_processing"]).sum()
        ),
        "supporting_raw_data_count": int((audit_df["decision"] == "supporting_raw_data").sum()),
        "not_ready_or_reject_count": int(
            audit_df["decision"].isin(["not_ready", "reject"]).sum()
        ),
        "decision_counts": {str(key): int(value) for key, value in decision_counts.items()},
        "integration_status_counts": {
            str(key): int(value) for key, value in integration_counts.items()
        },
        "source_counts": {str(key): int(value) for key, value in source_counts.items()},
        "detected_unit_counts": {str(key): int(value) for key, value in unit_counts.items()},
        "generated_files": {
            "audit_csv": str(AUDIT_CSV_PATH.relative_to(PROJECT_ROOT)),
            "summary_json": str(SUMMARY_JSON_PATH.relative_to(PROJECT_ROOT)),
            "markdown_report": str(MARKDOWN_REPORT_PATH.relative_to(PROJECT_ROOT)),
        },
    }

    SUMMARY_JSON_PATH.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    markdown_report = build_markdown_report(audit_df, summary)
    MARKDOWN_REPORT_PATH.write_text(markdown_report, encoding="utf-8")

    print("Dataset integration audit generated")
    print("-----------------------------------")
    print(f"Datasets audited: {summary['total_datasets']}")
    print(f"Official/candidate: {summary['candidate_or_official_count']}")
    print(f"Experimental: {summary['experimental_count']}")
    print(f"Requires transformation: {summary['requires_transformation_count']}")
    print(f"Not ready/reject: {summary['not_ready_or_reject_count']}")
    print()
    print(f"Audit CSV: {AUDIT_CSV_PATH}")
    print(f"Summary JSON: {SUMMARY_JSON_PATH}")
    print(f"Markdown report: {MARKDOWN_REPORT_PATH}")


if __name__ == "__main__":
    main()
