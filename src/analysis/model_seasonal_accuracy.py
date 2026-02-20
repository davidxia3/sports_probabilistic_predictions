import pandas as pd
from pathlib import Path



def compute_dynamic_home_win_probability(df: pd.DataFrame) -> pd.Series:
    """
    For each second-half game, compute home win rate from all prior games
    in the same season (first half + earlier second-half games).

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



def compute_model_season_binary_accuracy(csv_path: Path) -> pd.DataFrame:
    """
    Compute binary accuracy by season for multiple prediction models.
    
    Models:
        - Moneyline probabilistic model (ml_prob)
        - Bradley-Terry probabilistic model (bt_prob)
        - Home-bias model (dynamic expanding home-team win rate)
        - Pure coinflip model (predict 0.5 for every game)

    Args:
        csv_path (Path): Path object of CSV file with league game data.

    Returns:
        pd.DataFrame: DataFrame with 5 columns:
            season, ml_accuracy, bt_accuracy, home_bias_accuracy, coinflip_accuracy.
    """

    df = pd.read_csv(csv_path)

    # compute dynamic home win probability before filtering
    dynamic_home_probs = compute_dynamic_home_win_probability(df)

    # drop all first half of regular season games
    df = df[df["second_half"] == 1]


    # moneyline
    df_ml = df[df["ml_prob"] != 0.5].copy()
    df_ml["ml_accuracy"] = 100 * (
        (df_ml["ml_prob"] >= 0.5) == df_ml["result"]
    ).astype(int)

    ml_season = (
        df_ml.groupby("season")["ml_accuracy"]
        .mean()
        .reset_index()
    )


    # Bradley-Terry
    df_bt = df[df["bt_prob"] != 0.5].copy()
    df_bt["bt_accuracy"] = 100 * (
        (df_bt["bt_prob"] >= 0.5) == df_bt["result"]
    ).astype(int)

    bt_season = (
        df_bt.groupby("season")["bt_accuracy"]
        .mean()
        .reset_index()
    )


    # regular coinflip
    df_coin = df.copy()
    df_coin["coinflip_accuracy"] = 50

    coin_season = (
        df_coin.groupby("season")["coinflip_accuracy"]
        .mean()
        .reset_index()
    )


    # home win rate — dynamic expanding baseline
    df_home = df.copy()
    df_home["home_bias_prob"] = dynamic_home_probs
    df_home["home_bias_accuracy"] = 100 * (
        (df_home["home_bias_prob"] > 0.5) == df_home["result"]
    ).astype(int)

    home_season = (
        df_home.groupby("season")["home_bias_accuracy"]
        .mean()
        .reset_index()
    )

    # merge all seasonal results
    out = (
        ml_season
        .merge(bt_season, on="season", how="outer")
        .merge(home_season, on="season", how="outer")
        .merge(coin_season, on="season", how="outer")
    )

    return out



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        df = compute_model_season_binary_accuracy(Path(f"processed_data/{league}.csv"))
        df.to_csv(f"results/model_seasonal_accuracy/{league}.csv", index=False)