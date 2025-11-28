import pandas as pd
from pathlib import Path



def compute_brier_by_season(csv_path: Path, prob_col: str = "ml_prob", result_col: str = "result") -> pd.DataFrame:
    """
    Computes Brier scores per season for one league CSV. Returns a DataFrame with 2 columns: season and Brier score.

    Args:
        csv_path (Path): Path object of CSV file with league game data.
        prob_col (str): String object of name of prediction column in CSV.
        result_col (str): String object of name of result column in CSV.

    Returns:
        pd.DataFrame: DataFrame object with 2 columns: season and Brier score.
    """

    df = pd.read_csv(csv_path)

    df["brier"] = (df[prob_col] - df[result_col]) ** 2

    return df.groupby("season")["brier"].mean().reset_index()



if __name__ == "__main__":
    league_files = {
        "mlb": Path("processed_data/mlb.csv"),
        "nba": Path("processed_data/nba.csv"),
        "nfl": Path("processed_data/nfl.csv"),
        "nhl": Path("processed_data/nhl.csv"),
    }

    # compute Brier per season for each league
    league_briers = {}
    for league, path in league_files.items():
        brier_df = compute_brier_by_season(path)
        brier_df = brier_df.rename(columns={"brier": f"{league}_brier"})
        league_briers[league] = brier_df

    # merge all league season tables
    result = None
    for df in league_briers.values():
        if result is None:
            result = df
        else:
            result = result.merge(df, on="season", how="outer")

    # sort by season
    result = result.sort_values("season")

    # save results
    result.to_csv("results/ml_seasonal_brier.csv", index=False)