import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



def plot_predicted_home_win_prob_hist(method: str) -> None:
    """
    Plots normalized (density) histograms of the predicted home win probability distribution for the prediction method by league.
    
    Args: 
        method (str): String object of name of method.
        
    Returns:    
        None
    """

    leagues = ['MLB', 'NBA', 'NFL', 'NHL']

    color_map = {
        "mlb": "red",
        "nba": "orange",
        "nfl": "green",
        "nhl": "blue"
    }

    method_map = {
        "ml": "Moneyline",
        "bt": "Bradley-Terry"
    }

    for league in leagues:
        df = pd.read_csv(f"processed_data/{league.lower()}.csv")

        # drop all first half of regular season games
        d = df[df["second_half"] == 1][f"{method}_prob"]

        bin_edges = np.linspace(0, 1, 30)

        # compute max density for y-axis
        counts, _ = np.histogram(d, bins=bin_edges, density=True)
        max_density = counts.max()

        plt.figure(figsize=(8, 5))

        plt.hist(
            d,
            bins=bin_edges,
            density=True,
            color=color_map[league.lower()],
            edgecolor="black",
            alpha=0.75,
        )

        plt.title(f"{league}", fontsize=18)
        plt.xlabel(f"{method_map[method]} Predicted Home Team Win Probability", fontsize=14)
        plt.ylabel("Density", fontsize=14)
        plt.ylim(0, max_density * 1.05)
        plt.grid(True, linestyle="--", alpha=0.5)

        plt.tight_layout()

        # save figure
        out_path = f"results/home_predictions/{method}_{league.lower()}_hist.png"
        plt.savefig(out_path, dpi=300, bbox_inches="tight")
        plt.close()



if __name__ == "__main__":
    methods = ["ml", "bt"]
    for method in methods:
        plot_predicted_home_win_prob_hist(method)