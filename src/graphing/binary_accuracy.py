import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



def plot_binary_accuracy() -> None:
    """
    Plots grouped bar chart of binary accuracy of various models by league.

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

    df = pd.read_csv("results/binary_accuracy.csv")

    df["league"] = df["league"].str.upper()

    leagues = df["league"]
    models = ["ml", "bt", "home_win_base"]

    model_names = {
        "ml": "Moneyline",
        "bt": "Bradley–Terry",
        "home_win_base": "Home Bias Coinflip"
    }

    model_colors = {
        "ml": "#0aa344",
        "bt": "#f05654",
        "home_win_base": "#4a4266"
    }

    x = np.arange(len(leagues))
    width = 0.25

    plt.figure(figsize=(10,6))
    plt.grid(True, alpha=0.5)
    
    plt.axhline(
        y=50,
        color="black",
        linewidth=2,
        linestyle="-"
    )

    for i, model in enumerate(models):
        plt.bar(
            x + i * width,
            df[model],
            width,
            label=model_names[model],
            color=model_colors[model],
        )

    plt.ylim(0,100)
    plt.ylabel("Binary Accuracy (%)",fontsize=16)
    plt.xticks(x + width, leagues,fontsize=12)
    plt.legend(fontsize=16)
    plt.yticks([10*i for i in range(11)],fontsize=12)

    plt.tight_layout()
    plt.savefig("results/binary_accuracy.pdf")
    plt.savefig("results/binary_accuracy.png")
    plt.show()



if __name__ == "__main__":
    plot_binary_accuracy()