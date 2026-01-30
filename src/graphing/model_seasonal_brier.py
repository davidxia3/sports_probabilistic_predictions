import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path



def plot_brier_scores(league: str) -> None:
    """
    Plot Brier score of various models as a line graph.
    
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

    csv_path = Path(f"results/model_seasonal_brier/{league}.csv")
    df = pd.read_csv(csv_path)

    cols_to_labels = {
        "ml_brier": "Moneyline",
        "bt_brier": "Bradley-Terry",
        "home_bias_brier": "Home Bias Coinflip",
        "coinflip_brier": "Coinflip"
    }



    colors = {
        "ml_brier": "#0aa344",
        "bt_brier": "#f05654",
        "home_bias_brier": "#4a4266",
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

    cols = ["coinflip_brier", "home_bias_brier", "bt_brier", "ml_brier"]


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
            linewidth=4,
            markersize=8,
        )

    plt.ylabel("Brier Score", fontsize=16)
    plt.legend(fontsize=12,loc="upper right")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.xticks(df["season"].unique(), rotation=45,fontsize=12)
    plt.ylim(0.17,0.29)
    plt.xlim(2009,2025)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig(f"results/model_seasonal_brier/{league}.png")
    plt.savefig(f"results/model_seasonal_brier/{league}.pdf")
    plt.show()



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        plot_brier_scores(league)