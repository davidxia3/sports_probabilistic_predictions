import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path



def plot_calibration(league: str, n_bins: int = 10) -> None:
    """
    Plot calibration curves for multiple prediction methods.

    Args:
        league (str): League abbreviation (e.g. "nfl").
        n_bins (int): Number of bins for calibration, default 10.

    Returns:
        None
    """

    df = pd.read_csv(f"processed_data/{league}.csv")

    # keep only second-half games
    df = df[df["second_half"] == 1]

    # prediction methods
    methods = {
        "ML": "ml_prob",
        "Bradley–Terry": "bt_prob",
    }

    # compute calibration curves
    curves = {}
    bins = np.linspace(0, 1, n_bins + 1)
    for label, col in methods.items():
        sub = df[[col, "result"]].dropna().copy()
        sub["bin"] = np.digitize(sub[col], bins) - 1
        calib = sub.groupby("bin").agg(
            predicted=(col, "mean"),
            actual=("result", "mean"),
            count=("result", "size"),
        )
        curves[label] = calib



    plt.figure(figsize=(8, 8))
    plt.plot([0, 1], [0, 1], "k--", linewidth=2, label="Perfect Calibration")

    colors = {
        "ML": "green",
        "Bradley–Terry": "red",
    }
    markers = {
        "ML": "o",
        "Bradley–Terry": "s",
    }
    linestyles = {
        "ML": "-",
        "Bradley–Terry": ":",
    }



    for label, calib in curves.items():
        plt.plot(
            calib["predicted"],
            calib["actual"],
            marker=markers[label],
            linestyle=linestyles[label],
            linewidth=2,
            markersize=7,
            label=label,
            color=colors[label],
        )

    plt.xlabel("Predicted Win Probability", fontsize=14)
    plt.ylabel("Actual Win Rate", fontsize=14)
    plt.title(f"{league.upper()} Calibration Plot", fontsize=16)
    plt.legend()
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    Path("figures/calibration").mkdir(parents=True, exist_ok=True)
    plt.savefig(f"figures/calibration/{league}.png")
    plt.close()



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        plot_calibration(league, 10)