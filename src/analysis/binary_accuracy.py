import pandas as pd
from pathlib import Path



def load_filtered_data(data_file: Path, usable_methods: list[str]) -> pd.DataFrame:
    """
    Load a game-level dataset and return only the rows that satisfy the filtering requirements for evaluation.

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



def compute_home_win_probability(data_file: Path) -> pd.Series:
    """
    Returns a Series mapping each season to its first-half home win rate.

    Args:
        data_file (Path): Path object of CSV file with game data.

    Returns:
        pd.Series: maps season to first-half of season home team win rate.
    """
    
    df = pd.read_csv(data_file)

    # group by season, take only first-half rows, compute mean of result
    season_home_win = (
        df[df["second_half"] == 0]
        .groupby("season")["result"]
        .mean()
    )

    return season_home_win




if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    all_methods = ["ml", "bt"]

    results = []

    for league in leagues:
        data_file = Path(f"processed_data/{league}.csv")

        row = {"league": league}

        # model binary accuracies
        df_valid = load_filtered_data(data_file, all_methods)

        for method in all_methods:
            preds = df_valid[f"{method}_prob"].astype(float)
            pred_class = (preds >= 0.5).astype(int)
            y = df_valid["result"]
            row[method] = (pred_class == y).mean()

        # seasonal home win baseline
        season_home_rate = compute_home_win_probability(data_file)
        df_valid["home_base_prob"] = df_valid["season"].map(season_home_rate)

        home_pred_class = (df_valid["home_base_prob"] >= 0.5).astype(int)
        row["home_win_base"] = (home_pred_class == df_valid["result"]).mean()

        results.append(row)

    # save results
    output_df = pd.DataFrame(results)
    output_df.to_csv("results/binary_accuracy.csv", index=False)
