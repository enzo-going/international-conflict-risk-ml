# World Bank Indicators - Initial Selection

This document defines the initial World Bank indicators selected for integration into the project.

The goal is to enrich the current country-year conflict dataset with socioeconomic and structural variables. These indicators will be used as external features, not as target variables.

## Methodological role

The current model is based mainly on historical conflict information from UCDP. The next step is to test whether external socioeconomic indicators add predictive signal beyond conflict persistence and temporal features.

The target remains:

`target_conflict_next_year`

## Initial indicators

| Feature name | World Bank code | Interpretation | Expected role |
|---|---|---|---|
| `population_total` | `SP.POP.TOTL` | Total population | Structural country scale |
| `gdp_per_capita_current_usd` | `NY.GDP.PCAP.CD` | GDP per capita, current US$ | Economic development proxy |
| `gdp_growth_annual_pct` | `NY.GDP.MKTP.KD.ZG` | GDP growth, annual % | Economic instability / cycle |
| `inflation_consumer_prices_annual_pct` | `FP.CPI.TOTL.ZG` | Inflation, consumer prices, annual % | Internal economic pressure |
| `unemployment_total_pct` | `SL.UEM.TOTL.ZS` | Unemployment, total % of labor force | Social/economic fragility |
| `military_expenditure_pct_gdp` | `MS.MIL.XPND.GD.ZS` | Military expenditure, % of GDP | Military/strategic dimension |

## Integration rules

Each indicator must be transformed into country-year format with the following minimum columns:

- `country_code`
- `country_name`
- `year`
- one numeric column per indicator

The processed output should be saved as:

`data/processed/world_bank/world_bank_country_year_indicators.csv`

## Validation checks

Before merging with the main dataset, the following checks are required:

- number of countries;
- year range;
- missing value percentage by indicator;
- duplicated country-year pairs;
- compatibility between World Bank country codes and the main dataset country identifiers.

## Current status

Status: planned for integration.

The first implementation should prioritize correctness and transparency over quantity of indicators.
