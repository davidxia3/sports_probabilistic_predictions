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

    # drop all first half of regular season games for second half Brier calculations
    df = df[df["second_half"] == 1]

    # drop all games with even moneyline prediction
    df = df[df["ml_prob"] != 0.5]

    # drop all games with even Bradley-Terry prediction
    df = df[df["bt_prob"] != 0.5]

    # moneyline binary accuracy
    df["ml_accuracy"] = 100 * ((df["ml_prob"] >= 0.5) == df["result"]).astype(int)

    # Bradley-Terry binary accuracy
    df["bt_accuracy"] = 100 * ((df["bt_prob"] >= 0.5) == df["result"]).astype(int)

    # coinflip binary accuracy (always predicts 0.5)
    df["coinflip_accuracy"] = 50

    # home bias coinflip binary accuracy
    # home win rate is average of "result" column in first half of each regular season
    df["home_bias_prob"] = df["season"].map(season_home_winrate)
    df["home_bias_accuracy"] = 100 * ((df["home_bias_prob"] >= 0.5) == df["result"]).astype(int)

    out = (
        df.groupby("season")
          .agg(
              ml_accuracy=("ml_accuracy", "mean"),
              bt_accuracy=("bt_accuracy", "mean"),
              home_bias_accuracy=("home_bias_accuracy", "mean"),
              coinflip_accuracy=("coinflip_accuracy", "mean"),
          )
          .reset_index()
    )

    return out



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        df = compute_model_season_binary_accuracy(Path(f"processed_data/{league}.csv"))
        df.to_csv(f"results/model_seasonal_accuracy/{league}.csv", index=False)
