import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



def plot_predicted_home_win_prob(method: str) -> None:
    """
    Plots box plot of the predicted home win probability distribution for the prediction method by league.

    Args:
        method (str): String object of name of method.

    Returns:
        None
    """

    leagues = ['MLB', 'NBA', 'NFL', 'NHL']

    # only NFL has Elo
    if method == "elo":
        leagues = ["NFL"]

    color_map = {
        "mlb": "red",
        "nba": "orange",
        "nfl": "green",
        "nhl": "blue"
    }

    method_map = {
        "ml": "Moneyline",
        "elo": "Elo",
        "elopoint": "Elo Point",
        "elowin": "Elo Win",
        "keener": "Keener",
        "massey": "Massey",
        "od": "Offense-Defense",
        "bt": "Bradley-Terry"
    }

    colors = [color_map[league.lower()] for league in leagues]

    column_name = f"{method}_prob"
    dfs = [pd.read_csv(f"processed_data/{league.lower()}.csv") for league in leagues]
    data = [df[column_name].dropna() for df in dfs]

    leagues_reversed = leagues[::-1]
    data_reversed = data[::-1]
    colors_reversed = colors[::-1]

    plt.figure(figsize=(10, 6))
    bp = plt.boxplot(data_reversed, patch_artist=True, labels=leagues_reversed, vert=False) 

    for patch, color in zip(bp['boxes'], colors_reversed):
        patch.set_facecolor(color)
        patch.set_linewidth(3)

    for element in ['whiskers', 'caps']:
        plt.setp(bp[element], linewidth=2)
    plt.setp(bp['medians'], linewidth=2, color='black') 

    plt.axvline(0.5, color='black', linestyle='--', linewidth=4)


    plt.xlabel(f"{method_map[method]} Predicted Home Team Win Probability", fontsize=20)
    plt.grid(True, linestyle="--", alpha=0.6)
    xticks = np.arange(0, 1.1, 0.1)
    plt.xticks(xticks, fontsize=15)
    plt.yticks(fontsize=15)
    plt.tight_layout()

    plt.savefig(f"figures/predicted_home_win_prob/{method}.png", dpi=300, bbox_inches='tight')



if __name__ == "__main__":
    methods = ["ml", "elo", "elopoint", "elowin", "keener", "massey", "od", "bt"]

    for method in methods:
        plot_predicted_home_win_prob(method)