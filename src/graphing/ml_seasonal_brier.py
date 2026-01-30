import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path



def plot_brier_scores() -> None:
    """
    Load a CSV containing the seasonal moneyline based Brier score for each league and plot it as a line graph.
    
    Args:
        None

    Returns:
        None
    """

    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm",
        "axes.unicode_minus": False
    })

    csv_path = Path("results/ml_seasonal_brier.csv")
    df = pd.read_csv(csv_path)

    colors = {
        "mlb_brier": "#c91f37",
        "nba_brier": "#ff8936",
        "nfl_brier": "#057748",
        "nhl_brier": "#2e4e7e"
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


    plt.figure(figsize=(10, 6))

    for col in cols:
        plt.plot(
            df["season"],
            df[col],
            label=col.replace("_brier", "").upper(),
            color=colors[col],
            linestyle=line_styles[col],
            marker=markers[col],
            linewidth=4,
            markersize=8
        )

    plt.ylabel("Brier Score",fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.xticks(df["season"].unique(), rotation=45,fontsize=12)
    plt.yticks([i/100 for i in range(17,26)],fontsize=12)
    plt.xlim(2009,2025)
    plt.tight_layout()
    plt.savefig("results/ml_seasonal_brier.png")
    plt.savefig("results/ml_seasonal_brier.pdf")
    plt.show()
    plt.close()



if __name__ == "__main__":
    plot_brier_scores()