import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



def plot_binary_accuracy_by_model() -> None:
    """
    Plots grouped bar chart of binary accuracy of various leagues by model.

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

    league_colors = {
        "MLB": "#c91f37",
        "NBA": "#ff8936",
        "NFL": "#057748",
        "NHL": "#2e4e7e",
    }

    model_names = {
        "ml": "Moneyline",
        "bt": "Bradley–Terry",
        "home_win_base": "Home Bias Coinflip",
    }


    df = pd.read_csv("results/binary_accuracy.csv")

    df["league"] = df["league"].str.upper()

    models = ["ml", "bt", "home_win_base"]
    leagues = df["league"].tolist()

    x = np.arange(len(models))
    width = 0.18

    plt.figure(figsize=(10,6))
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.axhline(
        y=50,
        color="black",
        linewidth=2,
        linestyle="-"
    )
    for i, league in enumerate(leagues):
        plt.bar(
            x + i * width,
            df.loc[df["league"] == league, models].values.flatten(),
            width,
            label=league,
            color=league_colors[league]        )

    plt.ylabel("Accuracy Rate (%)", fontsize=16)

    plt.yticks([10*i for i in range(11)],fontsize=12)

    plt.xticks(
        x + (len(leagues) - 1) * width / 2,
        [model_names[m] for m in models],fontsize=12
    )

    plt.ylim(0,100)
    plt.legend(fontsize=16)
    plt.tight_layout()
    plt.savefig("results/binary_accuracy_T.pdf")
    plt.savefig("results/binary_accuracy_T.png")
    plt.show()



if __name__ == "__main__":
    plot_binary_accuracy_by_model()