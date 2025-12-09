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

    dfs = [pd.read_csv(f"processed_data/{league.lower()}.csv") for league in leagues]

    # drop all first half of regular season games
    data = [df[df["second_half"] == 1][f"{method}_prob"] for df in dfs]

    bin_edges = np.linspace(0, 1, 30)
    max_density = 0
    for d in data:
        counts, _ = np.histogram(d, bins=bin_edges, density=True)
        max_density = max(max_density, counts.max())

    _, axes = plt.subplots(4, 1, figsize=(10, 10), sharex=True, sharey=True)

    for ax, league, d in zip(axes, leagues, data):
        color = color_map[league.lower()]

        ax.hist(
            d,
            bins=bin_edges,
            density=True,
            color=color,
            edgecolor="black",
            alpha=0.75
        )

        ax.set_title(f"{league}", fontsize=16)
        ax.set_ylim(0, max_density * 1.05)
        ax.grid(True, linestyle="--", alpha=0.5)

    plt.xlabel(f"{method_map[method]} Predicted Home Team Win Probability Density", fontsize=16)
    plt.tight_layout()

    plt.savefig(f"figures/predicted_home_win_prob/{method}_hist.png", dpi=300, bbox_inches='tight')
    plt.close()



if __name__ == "__main__":
    methods = ["ml", "bt"]
    for method in methods:
        plot_predicted_home_win_prob_hist(method)