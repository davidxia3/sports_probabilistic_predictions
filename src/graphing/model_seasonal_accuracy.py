import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path



def plot_binary_accuracy(league: str) -> None:
    """
    Plot binary accuracy of various models as a line graph.
    
    Args:
        league (str): String object of league abbreviation (e.g. "nfl").

    Returns:
        None
    """

    csv_path = Path(f"results/model_seasonal_accuracy/{league}.csv")
    df = pd.read_csv(csv_path)

    cols_to_labels = {
        "ml_accuracy": "Moneyline",
        "bt_accuracy": "Bradley-Terry",
        "home_bias_accuracy": "Home Bias Coinflip",
        "coinflip_accuracy": "Coinflip"
    }



    colors = {
        "ml_accuracy": "green",
        "bt_accuracy": "red",
        "home_bias_accuracy": "purple",
        "coinflip_accuracy": "black",
    }
    line_styles = {
        "ml_accuracy": "-",
        "bt_accuracy": ":",
        "home_bias_accuracy": "--",
        "coinflip_accuracy": "-.",
    }
    markers = {
        "ml_accuracy": "o",
        "bt_accuracy": "s",
        "home_bias_accuracy": "^",
        "coinflip_accuracy": "D",
    }

    cols = ["ml_accuracy", "bt_accuracy", "home_bias_accuracy", "coinflip_accuracy"]

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
    plt.ylabel("Binary Accuracy")
    plt.title(f"{league.upper()} – Binary Accuracy by Season")
    plt.legend()
    plt.grid(True)
    plt.xticks(df["season"].unique(), rotation=45)

    plt.tight_layout()
    plt.savefig(f"results/model_seasonal_accuracy/{league}.png")
    plt.savefig(f"results/model_seasonal_accuracy/{league}.pdf")



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        plot_binary_accuracy(league)