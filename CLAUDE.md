# CLAUDE.md

## Project context

This repository contains an academic Machine Learning project focused on predictive analysis of international conflict risk.

The project is not intended to deterministically predict wars or world wars. It estimates conflict risk experimentally based on historical, temporal and socioeconomic data.

Main framing:

* Machine Learning system for international conflict risk analysis.
* Unit of analysis: country-year.
* Central dataset: UCDP Organized Violence Country-Year.
* Target: conflict occurrence in the following year when applicable.
* Evaluation should prioritize temporal validation.
* Persistence baseline is mandatory for comparison.

## Working rules

Always work in small, reviewable steps.

Before editing files:

1. Inspect the current repository state.
2. Explain what you found.
3. Propose a minimal plan.
4. Wait for approval when the change is non-trivial.

Do not modify raw data manually.

Generated datasets must come from scripts.

Prefer reproducible scripts over manual notebook-only changes.

Do not commit, push, merge or create pull requests unless explicitly asked.

Do not install packages unless explicitly approved.

Do not run expensive model training, data processing scripts or destructive commands without approval.

When suggesting commands, label the environment clearly:

* PowerShell
* CMD
* Python
* Jupyter
* SQL

When analyzing terminal output, explain the result before suggesting the next command.

## Data and modeling rules

Preserve raw datasets.

Document important decisions.

Avoid data leakage.

Use temporal split when appropriate.

Compare models against simple baselines, especially persistence baseline.

Prioritize interpretability and methodological clarity.

Do not overclaim results.

Treat all conclusions as experimental and limited by available data.

## Documentation rules

Documentation should be technical, academic and clear.

README, reports and dashboard text should be suitable for GitHub, portfolio and academic presentation.

Avoid generic AI-style writing.

Do not invent metrics, dataset contents, model results or conclusions.

If information is missing, say so explicitly.

## Current expected use of Claude Code

Use Claude Code mainly for:

* repository audit
* code organization
* documentation improvement
* reproducibility checks
* pipeline review
* identifying inconsistencies
* proposing small improvements

Avoid large rewrites unless explicitly requested.
