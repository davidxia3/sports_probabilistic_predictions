import pandas as pd
import matplotlib.pyplot as plt



def plot_home_winrate() -> None:
    """
    Reads previously computed home win percentages and plots a bar chart.

    Args:
        None

    Returns:
        None
    """

    # read home win percentage CSV
    df = pd.read_csv("results/home_win.csv")

    # extract leagues and corresponding percentages
    leagues = ["MLB", "NBA", "NFL", "NHL"]
    averages = [
        df["mlb"].iloc[0],
        df["nba"].iloc[0],
        df["nfl"].iloc[0],
        df["nhl"].iloc[0],
    ]

    colors = ["#c91f37", "#ff8936", "#057748", "#2e4e7e"]

    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm",
        "axes.unicode_minus": False
    })

    plt.figure(figsize=(10, 6))
    plt.bar(leagues, averages, color=colors, width=0.67)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.ylabel("Home Winrate (%)", fontsize=16)

    plt.axhline(
        y=50,
        color="black",
        linewidth=2,
        linestyle="-"
    )

    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.ylim(40, 60)
    plt.tight_layout()
    plt.savefig("results/home_win.pdf")
    plt.savefig("results/home_win.png")
    plt.show()
    plt.close()



if __name__ == "__main__":
    plot_home_winrate()