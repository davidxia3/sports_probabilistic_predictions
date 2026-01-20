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

    league_colors = {
        "MLB": "red",
        "NBA": "orange",
        "NFL": "green",
        "NHL": "blue",
    }

    model_names = {
        "ml": "Moneyline",
        "bt": "Bradley–Terry",
        "home_win_base": "Home Win Baseline",
    }


    df = pd.read_csv("results/binary_accuracy.csv")

    df["league"] = df["league"].str.upper()

    models = ["ml", "bt", "home_win_base"]
    leagues = df["league"].tolist()

    x = np.arange(len(models))
    width = 0.18

    plt.figure()

    for i, league in enumerate(leagues):
        plt.bar(
            x + i * width,
            df.loc[df["league"] == league, models].values.flatten(),
            width,
            label=league,
            color=league_colors[league],
        )

    plt.xlabel("Model")
    plt.ylabel("Binary Accuracy (%)")
    plt.title("Binary Accuracy by Model and League")

    plt.xticks(
        x + (len(leagues) - 1) * width / 2,
        [model_names[m] for m in models],
    )

    plt.ylim(0,100)

    plt.legend(title="League")
    plt.tight_layout()
    plt.savefig("results/binary_accuracy_T.pdf")
    plt.savefig("results/binary_accuracy_T.png")



if __name__ == "__main__":
    plot_binary_accuracy_by_model()