import numpy as np
import pandas as pd

# ============================================================
# RANDOM SEED
# ============================================================

GLOBAL_RANDOM_STATE = 42

np.random.seed(GLOBAL_RANDOM_STATE)

# ============================================================
# MONTHLY DISTRIBUTION
# ============================================================

def generate_monthly_distribution(
    total_deaths,
    total_months,
    rng
):

    base = rng.gamma(
        shape=2.0,
        scale=1.0,
        size=total_months
    )

    local_noise = rng.normal(
        loc=1.0,
        scale=0.35,
        size=total_months
    )

    shocks = np.ones(total_months)

    num_shocks = rng.integers(
        2,
        max(4, total_months // 10)
    )

    shock_positions = rng.choice(
        total_months,
        size=num_shocks,
        replace=False
    )

    for pos in shock_positions:

        shocks[pos] *= rng.uniform(
            2.0,
            6.0
        )

    regime = np.ones(total_months)

    regime_points = rng.choice(
        total_months,
        size=max(2, total_months // 18),
        replace=False
    )

    for point in regime_points:

        factor = rng.uniform(
            0.4,
            2.5
        )

        regime[point:] *= factor

    signal = (
        base *
        local_noise *
        shocks *
        regime
    )

    signal = np.clip(
        signal,
        1e-6,
        None
    )

    weights = (
        signal / signal.sum()
    )

    monthly_deaths = (
        weights * total_deaths
    )

    return monthly_deaths

# ============================================================
# EXPAND CONFLICTS
# ============================================================

def expand_conflicts_monthly(df):

    print("\nGenerating Monthly Timeline...")

    expanded_rows = []

    total_conflicts = len(df)

    for idx, (_, row) in enumerate(df.iterrows()):

        if idx % 1000 == 0:

            print(
                f"Processing {idx:,}/{total_conflicts:,}"
            )

        conflict_id = row["event_id"]

        start_year = int(
            row["start_year"]
        )

        end_year = int(
            row["end_year"]
        )

        total_months = max(
            1,
            ((end_year - start_year) + 1) * 12
        )

        total_deaths = float(
            row["total_casualties_k"]
        )

        rng = np.random.default_rng(
            abs(hash(conflict_id)) % (2**32)
        )

        monthly_deaths = (
            generate_monthly_distribution(
                total_deaths,
                total_months,
                rng
            )
        )

        month_counter = 0

        for year in range(
            start_year,
            end_year + 1
        ):

            for month in range(1, 13):

                if month_counter >= total_months:
                    break

                expanded_rows.append({

                    "conflict_id":
                        conflict_id,

                    "war_name":
                        row["war_name"],

                    "year":
                        year,

                    "month":
                        month,

                    "time_index":
                        month_counter,

                    "country":
                        row["country"],

                    "alliance":
                        row["alliance"],

                    "front":
                        row["front"],

                    "casualties_mil_k":
                        row["casualties_mil_k"],

                    "casualties_civ_k":
                        row["casualties_civ_k"],

                    "military_personnel_k":
                        row["military_personnel_k"],

                    "casualty_ratio":
                        row["casualty_ratio"],

                    "current_deaths":
                        float(
                            monthly_deaths[
                                month_counter
                            ]
                        )
                })

                month_counter += 1

    expanded_df = pd.DataFrame(
        expanded_rows
    )

    print("\nExpanded Shape:")
    print(expanded_df.shape)

    return expanded_df