import pandas as pd
from pathlib import Path



def compute_model_season_briers(csv_path: Path) -> pd.DataFrame:
    """
    Compute Brier scores by season for multiple prediction models.
    
    Models:
        - Moneyline probabilistic model (ml_prob)
        - Bradley-Terry probabilistic model (bt_prob)
        - Home-bias coinflip model (predict home-team win rate in that season)
        - Pure coinflip model (predict 0.5 for every game)

    Args:
        csv_path (Path): Path object of CSV file with league game data.

    Returns:
        pd.DataFrame: DataFrame with 5 columns:
            season, ml_brier, elo_brier, home_bias_brier, coinflip_brier.
    """

    df = pd.read_csv(csv_path)

    # compute first half home winrate by season
    df_first = df[df["second_half"] == 0]
    season_home_winrate = df_first.groupby("season")["result"].mean()

    # drop all first half of regular season games for second half Brier calculations
    df = df[df["second_half"] == 1].copy()

    # moneyline Brier
    df["ml_brier"] = (df["ml_prob"] - df["result"]) ** 2

    # Bradley-Terry Brier
    df["bt_brier"] = (df["bt_prob"] - df["result"]) ** 2

    # coinflip Brier (always predicts 0.5)
    df["coinflip_brier"] = (0.5 - df["result"]) ** 2

    # home bias coinflip Brier
    # home win rate is average of "result" column in first half of each regular season
    df["home_bias_prob"] = df["season"].map(season_home_winrate)
    df["home_bias_brier"] = (df["home_bias_prob"] - df["result"]) ** 2

    out = (
        df.groupby("season")
          .agg(
              ml_brier=("ml_brier", "mean"),
              bt_brier=("bt_brier", "mean"),
              home_bias_brier=("home_bias_brier", "mean"),
              coinflip_brier=("coinflip_brier", "mean"),
          )
          .reset_index()
    )

    return out



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        df = compute_model_season_briers(Path(f"processed_data/{league}.csv"))
        df.to_csv(f"results/model_seasonal_brier/{league}.csv", index=False)
