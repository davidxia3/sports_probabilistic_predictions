import pandas as pd
from pathlib import Path
import numpy as np



def compute_log_loss(data_file: Path, method: str) -> float:
    """
    Compute the Log loss for a specified prediction method using only the rows valid for that method.

    Args:
        data_file (Path): Path object of CSV file containing game data.
        method (str): Name of the prediction method to evaluate (e.g., "ml").

    Returns:
        float: The Log loss for the specified method.
    """

    df = pd.read_csv(data_file)

    # drop all first half of regular season games
    df = df[df["second_half"] == 1]

    # drop all games where only this method probability is NaN
    df = df[df[f"{method}_prob"].notna()]


    preds = df[f"{method}_prob"].astype(float)
    y = df["result"]

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



def compute_home_win_log_loss(data_file: Path) -> float:
    """
    Compute Log loss for seasonal home win baseline method using the
    empirical home-team win rate.

    Args:
        data_file (Path): Path object of CSV file containing game data.

    Returns:
        float: Log loss for home win probability baseline method.
    """

    df = pd.read_csv(data_file)

    # per-season first-half home win rate
    season_home_rate = compute_first_half_home_rates(data_file)

    # drop all first half of regular season games
    df = df[df["second_half"] == 1].copy()

    # map baseline rate into the second-half data
    df["home_base_prob"] = df["season"].map(season_home_rate)

    # numerical stability
    eps = 1e-15
    p = df["home_base_prob"].clip(eps, 1 - eps)

    y = df["result"]
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
                method=method
            )

        # home win baseline log loss (per season)
        row["home_win_base"] = compute_home_win_log_loss(
            data_file=data_file
        )

        results.append(row)

    output_df = pd.DataFrame(results)
    output_df.to_csv("results/log_loss.csv", index=False)