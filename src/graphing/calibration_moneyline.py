import pandas as pd
import matplotlib.pyplot as plt



def plot_moneyline_calibration() -> None:
    """
    Plots all league's calibration curves for ML prediction methods.

    Args:
        None
    
    Returns:
        None
    """

    df = pd.read_csv(f"results/calibration/moneyline.csv")

    plt.figure(figsize=(7, 6))

    # perfect calibration line
    plt.plot([0, 1], [0, 1], linestyle="--", color="black", linewidth=2, label="Perfect Calibration")

    plt.plot(
        (df["bin"] / 10) + 0.05,
        df["mlb"],
        marker="o",
        linestyle="-",
        color="red",
        label="MLB",
        linewidth=2,
        markersize=4
    )
    plt.plot(
        (df["bin"] / 10) + 0.05,
        df["nba"],
        marker="o",
        linestyle="-",
        color="orange",
        label="NBA",
        linewidth=2,
        markersize=4
    )
    plt.plot(
        (df["bin"] / 10) + 0.05,
        df["nfl"],
        marker="o",
        linestyle="-",
        color="green",
        label="NFL",
        linewidth=2,
        markersize=4
    )
    plt.plot(
        (df["bin"] / 10) + 0.05,
        df["nhl"],
        marker="o",
        linestyle="-",
        color="blue",
        label="NHL",
        linewidth=2,
        markersize=4
    )

    plt.xticks([x/10 for x in range(11)])
    plt.xlabel("Predicted Win Probability", fontsize=14)
    plt.ylabel("Actual Win Rate", fontsize=14)
    plt.xlim(0,1)
    plt.ylim(0,1)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.savefig("results/calibration/moneyline.png", dpi=300, bbox_inches='tight')
    plt.savefig("results/calibration/moneyline.pdf", dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()



if __name__ == "__main__":
    plot_moneyline_calibration()