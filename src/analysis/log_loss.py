import pandas as pd
from pathlib import Path
import numpy as np



def load_filtered_data(data_file: Path, usable_methods: list[str]) -> pd.DataFrame:
    """
    Load a game-level dataset and return only the rows that satisfy the
    filtering requirements for evaluation.

    Args:
        data_file (Path): Path object of CSV file containing prediction data.
        all_methods (list[str]): List of all prediction method names.

    Returns:
        pd.DataFrame: A filtered DataFrame containing only rows where all required probability columns exist and are non-null.
    """

    df = pd.read_csv(data_file)

    # drop all first half of regular season games
    df = df[df["second_half"] == 1]

    # mask for valid method probabilities
    prob_cols = [f"{m}_prob" for m in usable_methods]
    mask = df[prob_cols].notna().all(axis=1)

    return df.loc[mask]



def compute_log_loss(data_file: Path, method: str, usable_methods: list[str]) -> float:
    """
    Compute the Log loss for a specified prediction method using only the rows where all prediction method probability columns are present.

    Args:
        data_file (Path): Path object of CSV file containing game data.
        method (str): Name of the prediction method to evaluate (e.g., "ml").
        usable_methods (list[str]): List of all prediction method names.

    Returns:
        float: The Log loss for the specified method.
    """

    df_valid = load_filtered_data(data_file, usable_methods)

    preds = df_valid[f"{method}_prob"].astype(float)
    y = df_valid["result"]

    # numerical stability
    eps = 1e-15
    preds = preds.clip(eps, 1 - eps)

    log_loss = -(y * np.log(preds) + (1 - y) * np.log(1 - preds)).mean()

    return float(log_loss)



def compute_first_half_home_rates(data_file: Path) -> pd.Series:
    """
    Computes the seasonal home win rate baseline from first half of each season.
    
    Args:
        data_file (Path): Path object of CSV file with game data.

    Returns:
        pd.Series: maps season to first-half of season home team win rate.
    """

    df = pd.read_csv(data_file)

    first_half = df[df["second_half"] == 0]

    return first_half.groupby("season")["result"].mean()


def compute_home_win_log_loss(data_file: Path, usable_methods: list[str]) -> float:
    """
    Compute Log loss for seasonal home win baseline method of always predicting the home team to win using the empirical home-team win rate.

    Args:
        data_file (Path): Path object of CSV file containing game data.
        usable_methods (list[str]): List of all prediction method names.

    Returns:
        float: Log loss for home win probability baseline method.
    """

    # per-season first-half home win rate
    season_home_rate = compute_first_half_home_rates(data_file)

    # second-half valid rows for evaluation
    df_valid = load_filtered_data(data_file, usable_methods)

    # map baseline rate into the second-half data
    df_valid["home_base_prob"] = df_valid["season"].map(season_home_rate)

    # numerical stability
    eps = 1e-15
    p = df_valid["home_base_prob"].clip(eps, 1 - eps)

    y = df_valid["result"]
    log_loss = -(y * np.log(p) + (1 - y) * np.log(1 - p)).mean()

    return float(log_loss)



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    all_methods = ["ml", "bt"]

    results = []

    for league in leagues:
        data_file = Path(f"processed_data/{league}.csv")

        row = {"league": league}

        # model log losses
        for method in all_methods:
            row[method] = compute_log_loss(
                data_file=data_file,
                method=method,
                usable_methods=all_methods
            )

        # home win baseline log loss (per season)
        row["home_win_base"] = compute_home_win_log_loss(
            data_file=data_file,
            usable_methods=all_methods
        )

        results.append(row)

    output_df = pd.DataFrame(results)
    output_df.to_csv("results/log_loss.csv", index=False)