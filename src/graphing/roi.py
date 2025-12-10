import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path



def plot_fav_underdog_roi(csv_path: Path, save_path: Path) -> None:
    """
    Plots line graph of favorite ROI and underdog ROI by bin.

    Args:
        csv_path (Path): Path object of CSV file with favorite ROI and underdog ROI by bin.
        save_path (Path): Path object of PNG file where figure will be saved.

    Retuns:
        None
    """

    df = pd.read_csv(csv_path)

    bins = df["bin"]
    mask = df["n"] > 0

    _, ax = plt.subplots(figsize=(10, 6))

    # horizontal reference line
    ax.axhline(0, color="black", linewidth=2)

    markers = {
        "Favorite ROI": "o",
        "Underdog ROI": "s",
    }
    linestyles = {
        "Favorite ROI": "-",
        "Underdog ROI": ":",
    }



    ax.plot(
        bins[mask] * 10 + 5,
        df.loc[mask, "favorite_roi"],
        color="green",
        marker=markers["Favorite ROI"],
        linestyle=linestyles["Favorite ROI"],
        label="Favorite ROI",
    )

    ax.plot(
        bins[mask] * 10 + 5,
        df.loc[mask, "underdog_roi"],
        color="red",
        marker=markers["Underdog ROI"],
        linestyle=linestyles["Underdog ROI"],
        label="Underdog ROI",
    )



    # label counts (n) for each point
    for _, row in df[mask].iterrows():
        ax.text(
            row["bin"] * 10 + 5,
            row["favorite_roi"],
            str(int(row["n"])),
            color="green",
            fontsize=9,
            ha="center",
            va="bottom",
        )
        ax.text(
            row["bin"] * 10 + 5,
            row["underdog_roi"],
            str(int(row["n"])),
            color="red",
            fontsize=9,
            ha="center",
            va="bottom",
        )

    ax.set_xticks(bins * 10)
    ax.set_ylim(-25, 25)

    methods_dict = {
        "ml": "Moneyline",
        "bt": "Bradley-Terry"
    }

    ax.set_xlabel("Predicted Win Probability Bin")
    ax.set_ylabel("ROI (%)")    
    ax.set_title(f"{methods_dict[method]} Favorite vs Underdog ROI by Bin")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.6)

    plt.savefig(save_path)



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        for method in ["ml", "bt"]:
            plot_fav_underdog_roi(f"results/roi/{method}/{league}.csv", f"results/roi/{method}/{league}.png")