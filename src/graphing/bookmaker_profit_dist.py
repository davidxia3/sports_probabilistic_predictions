import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



def plot_bookmaker_profit_dist() -> None:
    """
    Plots box plot of moneyline bookmaker profit distribution for each league.

    Args:
        None
    
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

    colors = [color_map[league.lower()] for league in leagues]

    dfs = [pd.read_csv(f"processed_data/{league.lower()}.csv") for league in leagues]
    
    # drop all first half of regular season games
    data = [100 * df[df["second_half"]==1]["bookmaker_profit"] for df in dfs]

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


    plt.xlabel(f"Moneyline Bookmaker Profit (%)", fontsize=20)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.xlim(-4,12)
    xticks = np.arange(-4, 13, 2)
    plt.xticks(xticks, fontsize=15)
    plt.yticks(fontsize=15)
    plt.tight_layout()

    # save figure
    plt.savefig(f"results/bookmaker_profit_dist.png", dpi=300, bbox_inches='tight')
    plt.savefig(f"results/bookmaker_profit_dist.pdf", dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()



if __name__ == "__main__":
    plot_bookmaker_profit_dist()