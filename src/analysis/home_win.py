import pandas as pd



def compute_home_win() -> None:
    """
    Computes the home win percentage (entire regular season) for MLB, NBA, NFL, and NHL, and outputs a single CSV.

    Args:
        None

    Returns:
        None
    """

    leagues = ["mlb", "nba", "nfl", "nhl"]
    league_tables = {}

    for league in leagues:
        df = pd.read_csv(f"processed_data/{league}.csv")

        # drop first half of season games
        df = df[df["second_half"]==1]
        

        league_tables[league] = 100 * len(df[df["result"]==1]) / len(df)

    final_df = pd.DataFrame([league_tables])
    final_df.insert(0, "league", "home_win")
    final_df.to_csv("results/home_win.csv", index=False)



if __name__ == "__main__":
    compute_home_win()