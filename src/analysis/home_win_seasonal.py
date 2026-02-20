import pandas as pd



def compute_seasonal_home_win() -> None:
    """
    Computes the seasonal home win percentage (entire regular season) for MLB, NBA, NFL, and NHL, and outputs a single CSV.

    Args:
        None

    Returns:
        None
    """

    leagues = ["mlb", "nba", "nfl", "nhl"]
    league_tables = {}

    for league in leagues:
        df = pd.read_csv(f"processed_data/{league}.csv")

        # season-level home win percentage
        season_home = (
            df.groupby("season")["result"]
              .mean()
              .mul(100)
              .rename(league)
        )

        league_tables[league] = season_home

    final_df = pd.concat(league_tables.values(), axis=1).reset_index()
    final_df = final_df[["season", "mlb", "nba", "nfl", "nhl"]]
    final_df.to_csv("results/home_win_seasonal.csv", index=False)



if __name__ == "__main__":
    compute_seasonal_home_win()