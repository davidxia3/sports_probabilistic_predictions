import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path



def plot_calibration(league: str, n_bins) -> None:
    """
    Plot calibration curves for multiple prediction methods.

    Args:
        league (str): League abbreviation (e.g. "nfl").
        n_bins (int): Number of bins for calibration.

    Returns:
        None
    """

    df = pd.read_csv(f"processed_data/{league}.csv")

    # prediction methods
    methods = {
        "ML": "ml_prob",
        "Bradley–Terry": "bt_prob",
    }
    # only NFL has Elo
    if league.lower() == "nfl":
        methods["Elo"] = "elo_prob"

    # RatingsLib columns to average after calibration
    ratingslib_prob_cols = ["elopoint_prob", "elowin_prob", "keener_prob", "massey_prob", "od_prob"]

    # compute calibrations
    curves = {}
    bins = np.linspace(0, 1, n_bins + 1)
    for label, col in methods.items():
        sub = df[[col, "result"]].dropna().copy()
        sub["bin"] = np.digitize(sub[col], bins) - 1
        calib = sub.groupby("bin").agg(
            predicted=(col, "mean"),
            actual=("result", "mean"),
            count=("result", "size")
        )
        curves[label] = calib
    ratingslib_bins = pd.DataFrame(index=range(n_bins), columns=["predicted", "actual", "count"])
    ratingslib_bins["predicted"] = 0.0
    ratingslib_bins["actual"] = 0.0
    ratingslib_bins["count"] = 0

    for col in ratingslib_prob_cols:
        sub = df[[col, "result"]].dropna().copy()
        sub["bin"] = np.digitize(sub[col], bins) - 1
        calib = sub.groupby("bin").agg(
            predicted=(col, "mean"),
            actual=("result", "mean"),
            count=("result", "size")
        )
        for b in calib.index:
            ratingslib_bins.loc[b, "predicted"] += calib.loc[b, "predicted"]
            ratingslib_bins.loc[b, "actual"] += calib.loc[b, "actual"]
            ratingslib_bins.loc[b, "count"] += 1

    ratingslib_bins["predicted"] /= ratingslib_bins["count"]
    ratingslib_bins["actual"] /= ratingslib_bins["count"]

    curves["RatingsLib Average"] = ratingslib_bins



    plt.figure(figsize=(8, 8))
    plt.plot([0, 1], [0, 1], "k--", linewidth=2, label="Perfect Calibration")

    colors = {
        "ML": "green",
        "Elo": "red",
        "Bradley–Terry": "blue",
        "RatingsLib Average": "orange"
    }

    for label, calib in curves.items():
        plt.plot(
            calib["predicted"],
            calib["actual"],
            marker="o",
            linestyle="-",
            linewidth=2,
            markersize=6,
            label=label,
            color=colors[label],
        )

    plt.xlabel("Predicted Win Probability", fontsize=14)
    plt.ylabel("Actual Win Rate", fontsize=14)
    plt.title(f"{league.upper()} Calibration Plot", fontsize=16)
    plt.legend()
    plt.xlim(0,1)
    plt.ylim(0,1)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    # save figure
    Path("figures/calibration").mkdir(parents=True, exist_ok=True)
    plt.savefig(f"figures/calibration/{league}.png")
    plt.close()



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        plot_calibration(league, 10)