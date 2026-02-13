import pandas as pd
from pathlib import Path



def compute_model_season_binary_accuracy(csv_path: Path) -> pd.DataFrame:
    """
    Compute binary accuracy by season for multiple prediction models.
    
    Models:
        - Moneyline probabilistic model (ml_prob)
        - Bradley-Terry probabilistic model (bt_prob)
        - Home-bias coinflip model (predict home-team win rate in that season)
        - Pure coinflip model (predict 0.5 for every game)

    Args:
        csv_path (Path): Path object of CSV file with league game data.

    Returns:
        pd.DataFrame: DataFrame with 5 columns:
            season, ml_accuracy, elo_accuracy, home_bias_accuracy, coinflip_accuracy.
    """

    df = pd.read_csv(csv_path)

    # compute first half home winrate by season
    df_first = df[df["second_half"] == 0]
    season_home_winrate = df_first.groupby("season")["result"].mean()

    # drop all first half of regular season games for second half evaluation
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




    # home win rate is average of "result" column in first half of each regular season
    df_home = df.copy()
    df_home["home_bias_prob"] = df_home["season"].map(season_home_winrate)
    df_home["home_bias_accuracy"] = 100 * (
        (df_home["home_bias_prob"] >= 0.5) == df_home["result"]
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