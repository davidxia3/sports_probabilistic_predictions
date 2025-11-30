import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path



def plot_brier_scores(csv_path: Path) -> None:
    """
    Plot Brier score of various models for the NFL as a line graph.
    
    Args:
        csv_path (Path): Path object of CSV file with Brier scores.

    Returns:
        None
    """

    df = pd.read_csv(csv_path)

    cols_to_labels = {
        "ml_brier": "Moneyline",
        "elo_brier": "Elo",
        "home_bias_brier": "Home Bias Coinflip",
        "coinflip_brier": "Coinflip"
    }
    cols_to_colors = {
        "ml_brier": "green",
        "elo_brier": "red",
        "coinflip_brier": "black",
        "home_bias_brier": "blue",
    }

    cols = ["ml_brier", "elo_brier", "home_bias_brier", "coinflip_brier"]

    df = df.dropna(subset=cols)

    plt.figure(figsize=(10, 6))
    for col in cols:
        plt.plot(
            df["season"],
            df[col],
            marker="o",
            label=cols_to_labels[col],
            color=cols_to_colors[col],
        )

    plt.xlabel("Season")
    plt.ylabel("Brier Score")
    plt.title("Brier Scores by Season")
    plt.legend()
    plt.grid(True)
    plt.xticks(df["season"].unique(), rotation=45)

    plt.tight_layout()

    plt.savefig("figures/nfl_seasonal_brier.png")



if __name__ == "__main__":
    plot_brier_scores("results/nfl_seasonal_brier.csv")