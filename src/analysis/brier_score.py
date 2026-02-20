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
    

    preds = df[f"{method}_prob"].astype(float)
    y = df["result"]

    return ((preds - y) ** 2).mean()



def compute_dynamic_home_win_probability(df: pd.DataFrame) -> pd.Series:
    """
    For each second-half game, compute home win rate from all prior games in the same season (first half + earlier second-half games).

    Args:
        df: DataFrame with columns: season, date, second_half, result

    Returns:
        pd.Series: home win probability aligned to second-half game indices.
    """

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    second_half = df[df["second_half"] == 1].copy()
    probs = pd.Series(index=second_half.index, dtype=float)

    for season, season_df in df.groupby("season"):
        season_df = season_df.sort_values("date")
        mask = second_half["season"] == season
        sh_games = second_half.loc[mask].sort_values("date")

        for idx, game in sh_games.iterrows():
            prior = season_df[season_df["date"] < game["date"]]
            probs.at[idx] = prior["result"].mean() if len(prior) > 0 else 0.5

    return probs



def compute_home_win_brier(data_file: Path) -> float:
    """
    Compute Brier score for dynamic home win baseline method using expanding home-team win rate (all same-season games prior to each game).

    Args:
        data_file (Path): Path object of CSV file containing game data.

    Returns:
        float: Brier score for home win probability baseline method.
    """

    df = pd.read_csv(data_file)

    # drop all first half of regular season games
    df_home = df[df["second_half"] == 1].copy()

    # dynamic expanding home win probability
    df_home["home_base_prob"] = compute_dynamic_home_win_probability(df)

    y = df_home["result"]
    p = df_home["home_base_prob"]

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

        # home win baseline Brier (dynamic)
        row["home_win_base"] = compute_home_win_brier(
            data_file=data_file
        )

        results.append(row)

    output_df = pd.DataFrame(results)
    output_df.to_csv("results/brier_score.csv", index=False)