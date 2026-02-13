import pandas as pd
from pathlib import Path



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
        df = pd.read_csv(data_file)

        row = {"league": league}

        # model binary accuracies
        for method in all_methods:
            # drop all first half of regular season games
            df_method = df[df["second_half"] == 1]
            # drop all games where only this method probability is NaN
            df_method = df_method[df_method[f"{method}_prob"].notna()]
            # drop all games where only this method probability is 0.5
            df_method = df_method[df_method[f"{method}_prob"] != 0.5]


            preds = df_method[f"{method}_prob"].astype(float)
            pred_class = (preds > 0.5).astype(int)
            y = df_method["result"]

            row[method] = 100 * (pred_class == y).mean()

        # seasonal home win baseline
        season_home_rate = compute_home_win_probability(data_file)

        df_home = df[df["second_half"] == 1].copy()
        df_home["home_base_prob"] = df_home["season"].map(season_home_rate)

        home_pred_class = (df_home["home_base_prob"] >= 0.5).astype(int)
        row["home_win_base"] = 100 * (home_pred_class == df_home["result"]).mean()

        results.append(row)


    # save results
    output_df = pd.DataFrame(results)
    output_df.to_csv("results/binary_accuracy.csv", index=False)