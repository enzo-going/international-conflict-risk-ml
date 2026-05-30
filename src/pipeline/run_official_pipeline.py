from __future__ import annotations

import argparse
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class PipelineStep:
    name: str
    script_path: Path
    group: str
    reason: str = ""


OFFICIAL_STEPS = [
    PipelineStep(
        name="Build UCDP country-year base",
        script_path=PROJECT_ROOT / "src" / "data" / "build_conflict_country_year_base.py",
        group="data",
    ),
    PipelineStep(
        name="Build temporal conflict features",
        script_path=PROJECT_ROOT / "src" / "features" / "build_temporal_features.py",
        group="data",
    ),
    PipelineStep(
        name="Merge local World Bank indicators",
        script_path=PROJECT_ROOT / "src" / "data" / "build_conflict_country_year_world_bank.py",
        group="data",
        reason="Uses the existing processed World Bank file; no external download is run by default.",
    ),
    PipelineStep(
        name="Build World Bank feature table",
        script_path=PROJECT_ROOT / "src" / "features" / "build_world_bank_features.py",
        group="data",
    ),
    PipelineStep(
        name="Train official conflict risk model",
        script_path=PROJECT_ROOT / "src" / "models" / "train_conflict_risk_model.py",
        group="training",
    ),
    PipelineStep(
        name="Generate predictive charts",
        script_path=PROJECT_ROOT / "src" / "visualization" / "generate_predictive_charts.py",
        group="charts",
    ),
    PipelineStep(
        name="Validate pipeline state",
        script_path=PROJECT_ROOT / "src" / "validation" / "validate_pipeline_state.py",
        group="validation",
    ),
    PipelineStep(
        name="Validate project artifacts",
        script_path=PROJECT_ROOT / "src" / "validation" / "validate_project_artifacts.py",
        group="validation",
    ),
    PipelineStep(
        name="Validate reproducibility contract",
        script_path=PROJECT_ROOT / "src" / "validation" / "validate_reproducibility_contract.py",
        group="validation",
    ),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the official reproducible pipeline for International Conflict Risk ML."
    )
    parser.add_argument(
        "--skip-data-preparation",
        action="store_true",
        help="Skip local dataset construction and feature-building steps.",
    )
    parser.add_argument(
        "--skip-training",
        action="store_true",
        help="Skip official model training.",
    )
    parser.add_argument(
        "--skip-charts",
        action="store_true",
        help="Skip predictive chart generation.",
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip validation scripts.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the steps that would run without executing them.",
    )
    return parser.parse_args()


def should_skip(step: PipelineStep, args: argparse.Namespace) -> str | None:
    if step.group == "data" and args.skip_data_preparation:
        return "skip-data-preparation"
    if step.group == "training" and args.skip_training:
        return "skip-training"
    if step.group == "charts" and args.skip_charts:
        return "skip-charts"
    if step.group == "validation" and args.skip_validation:
        return "skip-validation"
    if not step.script_path.exists():
        return "missing-script"
    return None


def run_step(step: PipelineStep) -> float:
    started = time.perf_counter()
    relative_script = step.script_path.relative_to(PROJECT_ROOT)
    print(f"\n[RUN] {step.name}")
    print(f"      script: {relative_script}")
    if step.reason:
        print(f"      note: {step.reason}")

    subprocess.run(
        [sys.executable, str(step.script_path)],
        cwd=PROJECT_ROOT,
        check=True,
    )

    elapsed = time.perf_counter() - started
    print(f"[OK] {step.name} completed in {elapsed:.1f}s")
    return elapsed


def main() -> int:
    args = parse_args()

    print("Official pipeline runner")
    print("------------------------")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Python executable: {sys.executable}")
    print("Network-dependent World Bank download/preparation is not run by default.")

    executed: list[tuple[str, float]] = []
    skipped: list[tuple[str, str]] = []

    for step in OFFICIAL_STEPS:
        skip_reason = should_skip(step, args)
        if skip_reason:
            skipped.append((step.name, skip_reason))
            print(f"[SKIP] {step.name} ({skip_reason})")
            continue

        relative_script = step.script_path.relative_to(PROJECT_ROOT)
        if args.dry_run:
            skipped.append((step.name, "dry-run"))
            print(f"[DRY-RUN] {step.name}: python {relative_script}")
            continue

        elapsed = run_step(step)
        executed.append((step.name, elapsed))

    print("\nPipeline summary")
    print("----------------")
    print(f"Executed steps: {len(executed)}")
    for name, elapsed in executed:
        print(f"  OK   {name} ({elapsed:.1f}s)")

    print(f"Skipped steps: {len(skipped)}")
    for name, reason in skipped:
        print(f"  SKIP {name} ({reason})")

    if args.dry_run:
        print("\nDry run completed. No files were changed by this runner.")
    else:
        print("\nOfficial pipeline completed.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
