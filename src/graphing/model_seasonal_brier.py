import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path



def plot_brier_scores(league: str, csv_path: Path) -> None:
    """
    Plot Brier score of various models for the NFL as a line graph.
    
    Args:
        league (str): String object of league abbreviation (e.g. "nfl").
        csv_path (Path): Path object of CSV file with Brier scores.

    Returns:
        None
    """

    df = pd.read_csv(csv_path)

    cols_to_labels = {
        "ml_brier": "Moneyline",
        "bt_brier": "Bradley-Terry",
        "home_bias_brier": "Home Bias Coinflip",
        "coinflip_brier": "Coinflip"
    }



    colors = {
        "ml_brier": "green",
        "bt_brier": "red",
        "home_bias_brier": "purple",
        "coinflip_brier": "black",
    }
    line_styles = {
        "ml_brier": "-",
        "bt_brier": ":",
        "home_bias_brier": "--",
        "coinflip_brier": "-.",
    }
    markers = {
        "ml_brier": "o",
        "bt_brier": "s",
        "home_bias_brier": "^",
        "coinflip_brier": "D",
    }

    cols = ["ml_brier", "bt_brier", "home_bias_brier", "coinflip_brier"]

    df = df.dropna(subset=cols)

    plt.figure(figsize=(10, 6))

    for col in cols:
        plt.plot(
            df["season"],
            df[col],
            label=cols_to_labels[col],
            color=colors[col],
            linestyle=line_styles[col],
            marker=markers[col],
            linewidth=2,
            markersize=6,
        )

    plt.xlabel("Season")
    plt.ylabel("Brier Score")
    plt.title(f"{league.upper()} – Brier Scores by Season")
    plt.legend()
    plt.grid(True)
    plt.xticks(df["season"].unique(), rotation=45)

    plt.tight_layout()
    plt.savefig(f"figures/model_seasonal_brier/{league}_seasonal_brier.png")



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        plot_brier_scores(league, f"results/model_seasonal_brier/{league}_seasonal_brier.csv")