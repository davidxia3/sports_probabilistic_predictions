import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path



def plot_seasonal_home_win() -> None:
    """
    Plots line chart of the seasonal home win percentage of first half of regular season by league.

    Args:
        None

    Returns:
        None
    """

    input_path = Path("results/seasonal_home_win.csv")
    df = pd.read_csv(input_path)

    leagues = ["mlb", "nba", "nfl", "nhl"]

    colors = {
        "mlb": "red",
        "nba": "orange",
        "nfl": "green",
        "nhl": "blue"
    }
    line_styles = {
        "mlb": "-",
        "nba": "--",
        "nfl": ":",
        "nhl": "-."
    }
    markers = {
        "mlb": "o",
        "nba": "s",
        "nfl": "^",
        "nhl": "D"
    }

    plt.figure(figsize=(10, 6))

    # plot each league
    for league in leagues:
        plt.plot(
            df["season"],
            df[league],
            label=league.upper(),
            color=colors[league],
            linestyle=line_styles[league],
            marker=markers[league],
            linewidth=2.5,
            markersize=7,
        )

    plt.xticks(range(2008, 2026))
    plt.xlabel("Season", fontsize=14)
    plt.ylabel("Home Win Percentage", fontsize=14)
    plt.title("Seasonal Home Win Percentage (First Half Only)", fontsize=16)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(fontsize=12)
    plt.savefig("results/seasonal_home_win.png", dpi=300, bbox_inches="tight")
    plt.close()



if __name__ == "__main__":
    plot_seasonal_home_win()