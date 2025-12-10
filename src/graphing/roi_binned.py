import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path



def plot_fav_underdog_roi(csv_path: Path, bin: int, save_path: Path) -> None:
    """
    Plots line graph of binned favorite ROI and underdog ROI by season.

    Args:
        csv_path (Path): Path object of CSV file with favorite ROI and underdog ROI by bin.
        bin (int): Integer 0-9 inclusive of bin.
        save_path (Path): Path object of PNG file where figure will be saved.

    Retuns:
        None
    """

    df = pd.read_csv(csv_path)
    # no data, skip
    if len(df) == 0:
        return
    
    seasons = df["season"]
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
        seasons[mask],
        df.loc[mask, "favorite_roi"],
        color="green",
        marker=markers["Favorite ROI"],
        linestyle=linestyles["Favorite ROI"],
        label="Favorite ROI",
    )

    ax.plot(
        seasons[mask],
        df.loc[mask, "underdog_roi"],
        color="red",
        marker=markers["Underdog ROI"],
        linestyle=linestyles["Underdog ROI"],
        label="Underdog ROI",
    )



    # label counts (n) for each point
    for _, row in df[mask].iterrows():
        ax.text(
            row["season"],
            row["favorite_roi"],
            str(int(row["n"])),
            color="green",
            fontsize=9,
            ha="center",
            va="bottom",
        )
        ax.text(
            row["season"],
            row["underdog_roi"],
            str(int(row["n"])),
            color="red",
            fontsize=9,
            ha="center",
            va="bottom",
        )

    ax.set_xticks(range(min(seasons), max(seasons) + 1))
    ax.set_ylim(-50, 50)

    methods_dict = {
        "ml": "Moneyline",
        "bt": "Bradley-Terry"
    }

    ax.set_xlabel("Season")
    ax.set_ylabel("ROI (%)")
    ax.set_title(f"{methods_dict[method]} {bin * 10}-{bin * 10 + 10}% Bin Favorite vs Underdog ROI by Season")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.6)

    # plt.tight_layout()
    plt.savefig(save_path)



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        for method in ["ml", "bt"]:
            for bin in range(10):
                plot_fav_underdog_roi(f"results/roi_binned/{method}/{league}/bin_{bin}.csv", bin, f"figures/roi_binned/{method}/{league}/bin_{bin}.png")