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

    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm",
        "axes.unicode_minus": False
    })

    df = pd.read_csv(f"results/calibration/{league}.csv")

    plt.figure(figsize=(7, 6))

    # perfect calibration line
    plt.plot([0, 1], [0, 1], linestyle="--", color="black", linewidth=2, label="Perfect Calibration")

    plt.plot(
        (df["bin"] / 10) + 0.05,
        df["ml_winrate"],
        marker="o",
        linestyle="-",
        color="#0aa344",
        label="Moneyline",
        linewidth=4,
        markersize=8
    )
    plt.plot(
        (df["bin"] / 10) + 0.05,
        df["bt_winrate"],
        marker="s",
        linestyle=":",
        color="#f05654",
        label="Bradley–Terry",
        linewidth=4,
        markersize=8
    )

    plt.xticks([x/10 for x in range(11)],fontsize=12)
    plt.xlabel("Predicted Win Probability", fontsize=16)
    plt.ylabel("Actual Win Rate", fontsize=16)
    plt.yticks([x/10 for x in range(11)],fontsize=12)
    plt.xlim(0,1)
    plt.ylim(0,1)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(f"results/calibration/{league}.png", dpi=300, bbox_inches='tight')
    plt.savefig(f"results/calibration/{league}.pdf", dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        plot_calibration(league)