import pandas as pd
import numpy as np



def save_predicted_home_win_prob_hist_data(method: str) -> None:
    """
    Computes normalized histogram (density) values for predicted home win probability for each league and saves them to CSV files.
    
    Args:
        method (str): String object of name of prediction method.
        
    Returns:
        None
    """

    leagues = ["MLB", "NBA", "NFL", "NHL"]



    bin_edges = np.linspace(0, 1, 30)


    for league in leagues:
        df = pd.read_csv(f"processed_data/{league.lower()}.csv")

        # drop all first half of regular season games
        d = df[df["second_half"] == 1][f"{method}_prob"].dropna()

        # compute histogram density
        counts, edges = np.histogram(d, bins=bin_edges, density=True)

        # store midpoints for convenience
        bin_centers = 0.5 * (edges[:-1] + edges[1:])

        out_df = pd.DataFrame({
            "bin_left": edges[:-1],
            "bin_right": edges[1:],
            "bin_center": bin_centers,
            "density": counts
        })

        
        out_df.to_csv(f"results/home_predictions/{method}_{league.lower()}_hist.csv", index=False)



if __name__ == "__main__":
    methods = ["ml", "bt"]
    for method in methods:
        save_predicted_home_win_prob_hist_data(method)