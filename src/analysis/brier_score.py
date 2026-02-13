import pandas as pd
from pathlib import Path



def compute_brier_score(data_file: Path, method: str) -> float:
    """
    Compute the Brier score for a specified prediction method using only the rows valid for that method.

    Args:
        data_file (Path): Path object of CSV file containing game data.
        method (str): Name of the prediction method to evaluate (e.g., "ml").

    Returns:
        float: The Brier score for the specified method.
    """

    df = pd.read_csv(data_file)

    # drop all first half of regular season games
    df = df[df["second_half"] == 1]
    # drop all games where only this method probability is NaN
    df = df[df[f"{method}_prob"].notna()]

    preds = df[f"{method}_prob"].astype(float)
    y = df["result"]

    return ((preds - y) ** 2).mean()



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



def compute_home_win_brier(data_file: Path) -> float:
    """
    Compute Brier score for seasonal home win baseline method using the empirical home-team win rate.

    Args:
        data_file (Path): Path object of CSV file containing game data.

    Returns:
        float: Brier score for home win probability baseline method.
    """

    df = pd.read_csv(data_file)

    # get per-season first-half home win rate
    season_home_rate = compute_first_half_home_rates(data_file)

    # drop all first half of regular season games
    df = df[df["second_half"] == 1].copy()

    # map each game to its season’s first-half home win rate
    df["home_base_prob"] = df["season"].map(season_home_rate)

    y = df["result"]
    p = df["home_base_prob"]

    return ((p - y) ** 2).mean()



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    all_methods = ["ml", "bt"]

    results = []

    for league in leagues:
        data_file = Path(f"processed_data/{league}.csv")

        row = {"league": league}

        # model Brier scores
        for method in all_methods:
            row[method] = compute_brier_score(
                data_file=data_file,
                method=method
            )

        # home win baseline Brier (per season)
        row["home_win_base"] = compute_home_win_brier(
            data_file=data_file
        )

        results.append(row)

    output_df = pd.DataFrame(results)
    output_df.to_csv("results/brier_score.csv", index=False)