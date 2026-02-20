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



def compute_model_season_briers(csv_path: Path) -> pd.DataFrame:
    """
    Compute Brier scores by season for multiple prediction models.
    
    Models:
        - Moneyline probabilistic model (ml_prob)
        - Bradley-Terry probabilistic model (bt_prob)
        - Home-bias model (dynamic expanding home-team win rate)
        - Pure coinflip model (predict 0.5 for every game)

    Args:
        csv_path (Path): Path object of CSV file with league game data.

    Returns:
        pd.DataFrame: DataFrame with 5 columns:
            season, ml_brier, bt_brier, home_bias_brier, coinflip_brier.
    """

    df = pd.read_csv(csv_path)

    # compute dynamic home win probability before filtering
    dynamic_home_probs = compute_dynamic_home_win_probability(df)

    # drop all first half of regular season games
    df = df[df["second_half"] == 1].copy()

    # moneyline Brier
    df["ml_brier"] = (df["ml_prob"] - df["result"]) ** 2

    # Bradley-Terry Brier
    df["bt_brier"] = (df["bt_prob"] - df["result"]) ** 2

    # coinflip Brier (always predicts 0.5)
    df["coinflip_brier"] = (0.5 - df["result"]) ** 2

    # home bias Brier — dynamic expanding baseline
    df["home_bias_prob"] = dynamic_home_probs
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