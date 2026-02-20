import pandas as pd
from pathlib import Path



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
            # drop all first half games
            df_method = df[df["second_half"] == 1]

            # drop games where method has prediction of 0.5
            df_method = df_method[df_method[f"{method}_prob"] != 0.5]


            preds = df_method[f"{method}_prob"].astype(float)
            pred_class = (preds > 0.5).astype(int)
            y = df_method["result"]

            row[method] = 100 * (pred_class == y).mean()

        # dynamic home win baseline
        df_home = df[df["second_half"] == 1].copy()
        df_home["home_base_prob"] = compute_dynamic_home_win_probability(df)

        home_pred_class = (df_home["home_base_prob"] >= 0.5).astype(int)
        row["home_win_base"] = 100 * (home_pred_class == df_home["result"]).mean()

        results.append(row)

    output_df = pd.DataFrame(results)
    output_df.to_csv("results/binary_accuracy.csv", index=False)