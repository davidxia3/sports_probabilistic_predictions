import pandas as pd
import numpy as np



def compute_binned_winrates() -> None:
    """
    Computes calibration data (binned winrates) with 10 bins by league and using moneyline predictions.

    Args:
        None

    Returns: 
        None
    """

    rows = []
    bin_edges = np.linspace(0, 1, 11)

    for i in range(10):
        low = bin_edges[i]
        high = bin_edges[i+1]

        leagues = ["mlb", "nba", "nfl", "nhl"]
        league_to_winrate = {}
        for league in leagues:
            csv_path = f"processed_data/{league}.csv"
            df = pd.read_csv(csv_path)

            # drop all first half of regular season games
            df = df[df["second_half"] == 1]

            # filter rows whose ml_prob is in this bin
            ml_df = df[(df["ml_prob"] >= low) & (df["ml_prob"] < high)]

            # winrate is mean of result
            ml_winrate = ml_df["result"].mean() if len(ml_df) > 0 else np.nan

            league_to_winrate[league] = ml_winrate

        rows.append({
            "bin": i,
            "mlb": league_to_winrate["mlb"],
            "nba": league_to_winrate["nba"],
            "nfl": league_to_winrate["nfl"],
            "nhl": league_to_winrate["nhl"]
        })

    out_df = pd.DataFrame(rows)
    out_df.to_csv("results/calibration/moneyline.csv", index=False)



if __name__ == "__main__":
    compute_binned_winrates()