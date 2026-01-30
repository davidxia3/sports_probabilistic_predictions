import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import linregress



def plot_winrate_vs_brier(league: str) -> None:
    """
    Plots scatterplot of |winrate - 50| vs Brier score and regression line.

    Args:
        league (str): String object of team abbreviation (e.g. "nfl").

    Returns:
        None
    """

    brier_csv = Path(f"results/ml_teamwise_brier/{league}.csv")
    winrate_csv=Path(f"results/ml_teamwise_brier/{league}_winrates.csv")

    df_brier = pd.read_csv(brier_csv)
    df_wr = pd.read_csv(winrate_csv)

    # merge on "team"
    df = pd.merge(df_brier, df_wr, on="team", how="inner")
    df = df.dropna(subset=["brier_score", "winrate"])

    # compute |winrate - 50|
    df["abs_wr_diff"] = (df["winrate"] - 50).abs()

    x = df["abs_wr_diff"]
    y = df["brier_score"]

    # regression
    slope, intercept, _, p_value, _ = linregress(x, y)
    reg_line = slope * x + intercept


    color_map = {
        "mlb": "red",
        "nba": "orange",
        "nfl": "green",
        "nhl": "blue"
    }

    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, color=color_map[league], label=f"{league.upper()} teams")
    plt.plot(x, reg_line, linewidth=2, color="black",
             label=f"y = {slope:.4f}x + {intercept:.4f}\n(p={p_value:.4g})")

    plt.xlabel("|Win Rate - 50%|")
    plt.ylabel("Brier Score")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(f"results/ml_teamwise_brier/{league}_winrates.png")
    plt.savefig(f"results/ml_teamwise_brier/{league}_winrates.pdf")
    plt.show()
    plt.close()



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]

    for league in leagues:
        plot_winrate_vs_brier(league)