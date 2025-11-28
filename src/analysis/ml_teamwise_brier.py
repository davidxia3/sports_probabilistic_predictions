import pandas as pd
from pathlib import Path



def compute_teamwise_brier(csv_path: Path) -> pd.DataFrame:
    """
    Compute the Brier score based on moneyline based predictions for games involving each team.
    
    Args:
        csv_path (Path): Path object of CSV file with league game data.

    Returns:
        pd.DataFrame: DataFrame object with 2 columns: team and Brier score.
    """
    df = pd.read_csv(csv_path)

    # expand each game into 2 rows, one for each team
    home_df = pd.DataFrame({
        "team": df["home_team"],
        "pred": df["ml_prob"],
        "actual": df["result"]
    })

    away_df = pd.DataFrame({
        "team": df["away_team"],
        "pred": 1 - df["ml_prob"],
        "actual": 1 - df["result"]
    })

    # combine
    long_df = pd.concat([home_df, away_df], ignore_index=True)

    # compute Brier
    long_df["brier"] = (long_df["pred"] - long_df["actual"]) ** 2

    # Compute per-team Brier score
    result = long_df.groupby("team")["brier"].mean().reset_index()
    result = result.rename(columns={"brier": "brier_score"})

    result = result.sort_values("brier_score")

    return result



if __name__ == "__main__":
    league_files = {
        "mlb": Path("processed_data/mlb.csv"),
        "nba": Path("processed_data/nba.csv"),
        "nfl": Path("processed_data/nfl.csv"),
        "nhl": Path("processed_data/nhl.csv"),
    }
    
    for league, path in league_files.items():
        league_df = compute_teamwise_brier(path)
        league_df.to_csv(f"results/ml_teamwise_brier/{league}.csv", index=False)