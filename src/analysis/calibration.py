import pandas as pd
import numpy as np
from pathlib import Path



def compute_binned_winrates(csv_path: Path, output_path: Path) -> None:
    """
    Computes calibration data (binned winrates) with 10 bins.

    Args:
        csv_path (Path): Path object of CSV file with league game data.
        output_path (Path): Path object of CSV file where calibration data is saved.

    Returns: 
        None
    """
    df = pd.read_csv(csv_path)

    # drop all first half of regular season games
    df = df[df["second_half"] == 1]


    rows = []
    bin_edges = np.linspace(0, 1, 11)

    for i in range(10):
        low = bin_edges[i]
        high = bin_edges[i+1]

        # filter rows whose ml_prob is in this bin
        ml_df = df[(df["ml_prob"] >= low) & (df["ml_prob"] < high)]
        bt_df = df[(df["bt_prob"] >= low) & (df["bt_prob"] < high)]

        # winrate is mean of result
        ml_winrate = ml_df["result"].mean() if len(ml_df) > 0 else np.nan
        bt_winrate = bt_df["result"].mean() if len(bt_df) > 0 else np.nan

        rows.append({
            "bin": i,
            "ml_winrate": ml_winrate,
            "bt_winrate": bt_winrate
        })

    out_df = pd.DataFrame(rows)
    out_df.to_csv(output_path, index=False)



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        compute_binned_winrates(f"processed_data/{league}.csv", f"results/calibration/{league}.csv")