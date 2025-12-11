import pandas as pd
import matplotlib.pyplot as plt



def plot_calibration(league: str) -> None:
    """
    Plot calibration curves for ML and Bradley–Terry prediction methods.

    Args:
        league (str): League abbreviation (e.g., "nfl").

    Returns:
        None
    """

    df = pd.read_csv(f"results/calibration/{league}.csv")

    plt.figure(figsize=(7, 6))

    # perfect calibration line
    plt.plot([0, 1], [0, 1], linestyle="--", color="black", linewidth=2, label="Perfect Calibration")

    plt.plot(
        (df["bin"] / 10) + 0.05,
        df["ml_winrate"],
        marker="o",
        linestyle="-",
        color="green",
        label="ML",
        linewidth=4,
        markersize=8
    )
    plt.plot(
        (df["bin"] / 10) + 0.05,
        df["bt_winrate"],
        marker="s",
        linestyle=":",
        color="red",
        label="Bradley–Terry",
        linewidth=4,
        markersize=8
    )

    plt.xticks([x/10 for x in range(11)])
    plt.xlabel("Predicted Win Probability", fontsize=14)
    plt.ylabel("Actual Win Rate", fontsize=14)
    plt.title(f"{league.upper()} Calibration Plot", fontsize=16)
    plt.xlim(0,1)
    plt.ylim(0,1)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.savefig(f"results/calibration/{league}.png", dpi=300, bbox_inches='tight')
    plt.close()



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        plot_calibration(league)