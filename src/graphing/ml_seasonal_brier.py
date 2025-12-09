import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path



def plot_brier_scores(csv_path: Path) -> None:
    """
    Load a CSV containing the seasonal moneyline based Brier score for each league and plot it as a line graph.
    
    Args:
        csv_path (Path): Path object of CSV file with Brier scores.

    Returns:
        None
    """

    df = pd.read_csv(csv_path)

    colors = {
        "mlb_brier": "red",
        "nba_brier": "orange",
        "nfl_brier": "green",
        "nhl_brier": "blue",
    }
    line_styles = {
        "mlb_brier": "-",
        "nba_brier": "--",
        "nfl_brier": ":",
        "nhl_brier": "-.",
    }
    markers = {
        "mlb_brier": "o",
        "nba_brier": "s",
        "nfl_brier": "^",
        "nhl_brier": "D",
    }

    cols = ["mlb_brier", "nba_brier", "nfl_brier", "nhl_brier"]

    df = df.dropna(subset=cols)

    plt.figure(figsize=(10, 6))

    for col in cols:
        plt.plot(
            df["season"],
            df[col],
            label=col.replace("_brier", "").upper(),
            color=colors[col],
            linestyle=line_styles[col],
            marker=markers[col],
            linewidth=2,
            markersize=6
        )

    plt.xlabel("Season")
    plt.ylabel("Brier Score")
    plt.title("Moneyline Brier Scores by Season")
    plt.legend()
    plt.grid(True)
    plt.xticks(df["season"].unique(), rotation=45)

    plt.tight_layout()
    plt.savefig("figures/ml_seasonal_brier.png")



if __name__ == "__main__":
    plot_brier_scores("results/ml_seasonal_brier.csv")