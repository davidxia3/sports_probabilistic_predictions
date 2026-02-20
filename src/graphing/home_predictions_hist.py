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

    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm",
        "axes.unicode_minus": False
    })

    leagues = ['MLB', 'NBA', 'NFL', 'NHL']

    color_map = {
        "mlb": "#c91f37",
        "nba": "#ff8936",
        "nfl": "#057748",
        "nhl": "#2e4e7e"
    }

    for league in leagues:
        df = pd.read_csv(f"processed_data/{league.lower()}.csv")

        # drop all first half of regular season games
        d = 100 * df[df["second_half"] == 1][f"{method}_prob"]

        bin_edges = np.linspace(0, 100, 30)


        plt.figure(figsize=(10, 6))

        plt.hist(
            d,
            bins=bin_edges,
            density=True,
            color=color_map[league.lower()],
            edgecolor="black"        )

        plt.ylabel("Density", fontsize=16)
        plt.ylim(0, 0.044)
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()
        # save figure
        plt.savefig(f"results/home_predictions/{method}_{league.lower()}_hist.png", dpi=300, bbox_inches="tight")
        plt.savefig(f"results/home_predictions/{method}_{league.lower()}_hist.pdf", dpi=300, bbox_inches="tight")
        plt.show()
        plt.close()




if __name__ == "__main__":
    methods = ["ml", "bt"]
    for method in methods:
        plot_predicted_home_win_prob_hist(method)