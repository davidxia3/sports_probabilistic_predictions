import pandas as pd
import matplotlib.pyplot as plt



def plot_seasonal_home_win_pct() -> None:
    """
    Plots line chart of the seasonal home win percentage of first half of regular season by league.

    Args:
        None

    Returns:
        None
    """

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

    for league in leagues:
        df = pd.read_csv(f"processed_data/{league}.csv")

        overall_win = df["result"].mean()

        # consider only first half of regular season games
        df2 = df[df["second_half"] == 0]
        seasonal = df2.groupby("season")["result"].mean()

        plt.plot(
            seasonal.index,
            seasonal.values,
            label=f"{league.upper()} (overall={overall_win:.3f})",
            color=colors[league],
            linestyle=line_styles[league],
            marker=markers[league],
            markersize=6,
            linewidth=2
        )

    plt.xticks(ticks=range(2008, 2026))
    plt.xlabel("Season")
    plt.ylabel("Home Win %")
    plt.title("Seasonal Home Win Percentage by League")
    plt.legend()
    plt.tight_layout()
    plt.savefig("figures/seasonal_home_win.png")



if __name__ == "__main__":
    plot_seasonal_home_win_pct()