import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path



def plot_fav_underdog_roi(league: str, method: str) -> None:
    """
    Plots line graph of favorite ROI and underdog ROI by bin.

    Args:
        league (str): String object of league abbreviation (e.g. "nfl").
        method (str): String object of method name.

    Retuns:
        None
    """

    csv_path = Path(f"results/roi/{method}/{league}.csv")
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

    plt.savefig(f"results/roi/{method}/{league}.png")
    plt.savefig(f"results/roi/{method}/{league}.pdf")



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        for method in ["ml", "bt"]:
            plot_fav_underdog_roi(league, method)