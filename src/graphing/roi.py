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

    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm",
        "axes.unicode_minus": False
    })

    csv_path = Path(f"results/roi/{method}/{league}.csv")
    df = pd.read_csv(csv_path)

    bins = df["bin"]
    mask = df["n"] > 0

    plt.figure(figsize=(10, 6))

    # horizontal reference line
    plt.axhline(0, color="black", linewidth=2, linestyle="-")

    markers = {
        "Bet on favorite": "o",
        "Bet on underdog": "s",
    }
    linestyles = {
        "Bet on favorite": "-",
        "Bet on underdog": ":",
    }

    plt.plot(
        bins[mask] * 10 + 5,
        df.loc[mask, "favorite_roi"],
        color="#0aa344",
        marker=markers["Bet on favorite"],
        linestyle=linestyles["Bet on favorite"],
        label="Bet on favorite",
        markersize=8,
        linewidth=4
    )

    plt.plot(
        bins[mask] * 10 + 5,
        df.loc[mask, "underdog_roi"],
        color="#f05654",
        marker=markers["Bet on underdog"],
        linestyle=linestyles["Bet on underdog"],
        label="Bet on underdog",
        markersize=8,
        linewidth=4
    )

    # label counts (n) for each point
    for _, row in df[mask].iterrows():
        plt.text(
            row["bin"] * 10 + 5,
            row["favorite_roi"],
            str(int(row["n"])),
            color="green",
            fontsize=9,
            ha="center",
            va="bottom",
        )
        plt.text(
            row["bin"] * 10 + 5,
            row["underdog_roi"],
            str(int(row["n"])),
            color="red",
            fontsize=9,
            ha="center",
            va="bottom",
        )

    plt.xticks(bins * 10,fontsize=12)
    plt.ylim(-25, 25)
    plt.yticks(range(-25, 30,5),fontsize=12)
    plt.xlabel("Predicted Win Probability (%)",fontsize=16)
    plt.ylabel("ROI (%)",fontsize=16)
    plt.legend(fontsize=16,loc="upper left")
    plt.grid(True, linestyle="--", alpha=0.5)

    # plt.tight_layout()

    plt.savefig(f"results/roi/{method}/{league}.png")
    plt.savefig(f"results/roi/{method}/{league}.pdf")
    plt.show()



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        for method in ["ml", "bt"]:
            plot_fav_underdog_roi(league, method)