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

    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm",
        "axes.unicode_minus": False
    })

    csv_path = Path(f"results/model_seasonal_accuracy/{league}.csv")
    df = pd.read_csv(csv_path)

    cols_to_labels = {
        "ml_accuracy": "Moneyline",
        "bt_accuracy": "Bradley-Terry",
        "home_bias_accuracy": "Home Bias Coinflip",
        "coinflip_accuracy": "Coinflip"
    }



    colors = {
        "ml_accuracy": "#0aa344",
        "bt_accuracy": "#f05654",
        "home_bias_accuracy": "#4a4266",
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
    plt.grid(True, linestyle="--", alpha=0.5)
    for col in cols:
        plt.plot(
            df["season"],
            df[col],
            label=cols_to_labels[col],
            color=colors[col],
            linestyle=line_styles[col],
            marker=markers[col],
            linewidth=4,
            markersize=8,
        )

    plt.ylabel("Accuracy Rate (%)",fontsize=16)
    plt.legend(loc="upper left",fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.xticks(df["season"].unique(), rotation=45,fontsize=12)
    plt.ylim(50,80)
    plt.xlim(2009,2025)
    plt.yticks([i for i in range(50,80, 5)],fontsize=12)
    plt.tight_layout()
    plt.savefig(f"results/model_seasonal_accuracy/{league}.png")
    plt.savefig(f"results/model_seasonal_accuracy/{league}.pdf")
    plt.show()
    plt.close()



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        plot_binary_accuracy(league)