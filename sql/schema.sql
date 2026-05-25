-- SQLite schema for the International Conflict Risk ML project.
--
-- This database layer is designed as a reproducible analytical interface
-- over the project's country-year datasets, model predictions and model
-- interpretation outputs.
--
-- The SQLite database file itself should be generated locally and should
-- not be committed to Git.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS country_year_features (
    country TEXT NOT NULL,
    year INTEGER NOT NULL,

    organized_violence_exists INTEGER,
    target_conflict_next_year INTEGER,

    state_based_conflict_exists INTEGER,
    state_based_dyad_count REAL,
    state_based_deaths_best REAL,

    intrastate_conflict_exists INTEGER,
    intrastate_deaths_best REAL,

    interstate_conflict_exists INTEGER,
    interstate_deaths_best REAL,

    non_state_conflict_exists INTEGER,
    non_state_dyad_count REAL,
    non_state_deaths_best REAL,

    one_sided_violence_exists INTEGER,
    one_sided_dyad_count REAL,
    one_sided_deaths_best REAL,

    cumulative_organized_violence_deaths_best REAL,

    conflict_previous_year INTEGER,
    conflict_last_3_years_count REAL,
    conflict_last_5_years_count REAL,
    deaths_previous_year REAL,
    deaths_last_3_years_sum REAL,
    deaths_last_5_years_sum REAL,
    years_since_last_conflict REAL,

    population_total REAL,
    population_growth_annual_pct REAL,
    urban_population_pct REAL,
    gdp_per_capita_current_usd REAL,
    gdp_growth_annual_pct REAL,
    inflation_consumer_prices_annual_pct REAL,
    unemployment_total_pct REAL,
    school_enrollment_secondary_gross_pct REAL,
    military_expenditure_pct_gdp REAL,
    natural_resources_rents_pct_gdp REAL,

    PRIMARY KEY (country, year)
);

CREATE TABLE IF NOT EXISTS model_predictions (
    country TEXT NOT NULL,
    year INTEGER NOT NULL,

    y_true INTEGER,
    y_pred INTEGER,
    y_proba REAL,

    organized_violence_exists INTEGER,

    PRIMARY KEY (country, year),
    FOREIGN KEY (country, year)
        REFERENCES country_year_features(country, year)
);

CREATE TABLE IF NOT EXISTS model_coefficients (
    rank INTEGER PRIMARY KEY,
    feature TEXT NOT NULL,
    feature_group TEXT NOT NULL,
    coefficient REAL NOT NULL,
    absolute_coefficient REAL NOT NULL,
    effect TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS model_metrics (
    model TEXT PRIMARY KEY,
    accuracy REAL,
    precision REAL,
    recall REAL,
    f1_score REAL,
    tn INTEGER,
    fp INTEGER,
    fn INTEGER,
    tp INTEGER,
    f1_difference_vs_persistence REAL
);


CREATE TABLE IF NOT EXISTS candidate_model_comparison (
    model TEXT PRIMARY KEY,
    feature_count INTEGER,
    accuracy REAL,
    precision REAL,
    recall REAL,
    f1_score REAL,
    tn INTEGER,
    fp INTEGER,
    fn INTEGER,
    tp INTEGER,
    f1_difference_vs_persistence REAL
);

CREATE TABLE IF NOT EXISTS dataset_metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_country_year_features_year
    ON country_year_features(year);

CREATE INDEX IF NOT EXISTS idx_country_year_features_target
    ON country_year_features(target_conflict_next_year);

CREATE INDEX IF NOT EXISTS idx_model_predictions_year
    ON model_predictions(year);

CREATE INDEX IF NOT EXISTS idx_model_predictions_proba
    ON model_predictions(y_proba);
