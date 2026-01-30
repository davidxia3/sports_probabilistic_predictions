import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



def plot_brier_score() -> None:
    """
    Plots grouped bar chart of Brier scores of various models by league.

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

    df = pd.read_csv("results/brier_score.csv")

    df["league"] = df["league"].str.upper()

    leagues = df["league"]
    models = ["home_win_base", "bt", "ml"]

    model_names = {
        "ml": "Moneyline",
        "bt": "Bradley–Terry",
        "home_win_base": "Home Bias Coinflip",
        "coinflip": "Coinflip"
    }

    model_colors = {
        "ml": "#0aa344",
        "bt": "#f05654",
        "home_win_base": "#4a4266",
        "coinflip": "black"
    }

    x = np.arange(len(leagues))
    width = 0.18

    plt.figure(figsize=(10,6))
    plt.grid(True, alpha=0.5)
    

    plt.bar(
        x,
        0.25,
        width,
        label=model_names["coinflip"],
        color=model_colors["coinflip"]
    )

    for i, model in enumerate(models):
        plt.bar(
            x + (i + 1) * width,
            df[model],
            width,
            label=model_names[model],
            color=model_colors[model],
        )

    plt.ylim(0.15,0.30)
    plt.ylabel("Brier Score",fontsize=16)
    plt.xticks(x + width, leagues,fontsize=12)
    plt.legend(fontsize=16,loc="upper right")
    plt.yticks([i/100 for i in range(15,31)],fontsize=12)

    plt.tight_layout()
    plt.savefig("results/brier_score.pdf")
    plt.savefig("results/brier_score.png")
    plt.show()



if __name__ == "__main__":
    plot_brier_score()