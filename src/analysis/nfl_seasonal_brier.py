import pandas as pd
from pathlib import Path



def compute_nfl_season_briers(csv_path: Path) -> pd.DataFrame:
    """
    Compute Brier scores by season for multiple NFL prediction models.
    
    Models:
        - Moneyline probabilistic model (ml_prob)
        - Elo probabilistic model (elo_prob)
        - Home-bias coinflip model (predict home-team win rate in that season)
        - Pure coinflip model (predict 0.5 for every game)

    Args:
        csv_path (Path): Path object of CSV file with league game data.

    Returns:
        DataFrame with columns:
            season, ml_brier, elo_brier, home_bias_brier, coinflip_brier
    """
    df = pd.read_csv(csv_path)

    # moneyline Brier
    df["ml_brier"] = (df["ml_prob"] - df["result"]) ** 2

    # Elo Brier
    df["elo_brier"] = (df["elo_prob"] - df["result"]) ** 2

    # coinflip Brier (always predicts 0.5)
    df["coinflip_brier"] = (0.5 - df["result"]) ** 2

    # home bias coinflip Brier
    # For each season: home win rate = average of "result"
    season_home_winrate = df.groupby("season")["result"].mean()

    # map season winrate into each row
    df["home_bias_prob"] = df["season"].map(season_home_winrate)

    # compute squared error
    df["home_bias_brier"] = (df["home_bias_prob"] - df["result"]) ** 2

    out = (
        df.groupby("season")
          .agg(
              ml_brier=("ml_brier", "mean"),
              elo_brier=("elo_brier", "mean"),
              home_bias_brier=("home_bias_brier", "mean"),
              coinflip_brier=("coinflip_brier", "mean"),
          )
          .reset_index()
    )

    return out



if __name__ == "__main__":
    nfl_df = compute_nfl_season_briers(Path("processed_data/nfl.csv"))
    nfl_df.to_csv("results/nfl_seasonal_brier.csv", index=False)
