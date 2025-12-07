import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path



def plot_fav_underdog_roi(csv_path: Path, save_path: Path) -> None:
    """
    Plots line graph of moneyline favorite ROI and underdog ROI by bin.

    Args:
        csv_path (Path): Path object of CSV file with moneyline favorite ROI and underdog ROI by bin.
        save_path (Path): Path object of PNG file where figure will be saved.

    Retuns:
        None
    """

    df = pd.read_csv(csv_path)
    df = df.sort_values("bin")

    bins = df["bin"]
    mask = df["n"] > 0

    _, ax = plt.subplots(figsize=(10, 6))

    # plot horizontal reference line at y=0
    ax.axhline(0, color="black", linewidth=2)

    # plot lines
    ax.plot(
        bins[mask],
        df.loc[mask, "favorite_roi"],
        color="green",
        marker="o",
        label="Favorite ROI"
    )

    ax.plot(
        bins[mask],
        df.loc[mask, "underdog_roi"],
        color="red",
        marker="o",
        label="Underdog ROI"
    )

    # label each bin with count
    for _, row in df[mask].iterrows():
        ax.text(
            row["bin"],
            row["favorite_roi"],
            str(int(row["n"])),
            color="green",
            fontsize=9,
            ha="center",
            va="bottom"
        )
        ax.text(
            row["bin"],
            row["underdog_roi"],
            str(int(row["n"])),
            color="red",
            fontsize=9,
            ha="center",
            va="bottom"
        )

    ax.set_xticks(bins)

    ax.set_xlabel("Bin")
    ax.set_ylabel("ROI (%)")
    ax.set_title("Favorite vs Underdog ROI by Bin")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    plt.savefig(save_path)



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        plot_fav_underdog_roi(f"results/roi/ml_roi/{league}/{league}.csv", f"figures/ml_roi/{league}.png")
