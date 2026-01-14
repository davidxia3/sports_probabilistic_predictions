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

    df = pd.read_csv("results/binary_accuracy.csv")

    leagues = df["league"]
    models = ["ml", "bt", "home_win_base"]

    x = np.arange(len(leagues))
    width = 0.25

    plt.figure()

    for i, model in enumerate(models):
        plt.bar(x + i * width, df[model], width, label=model)

    plt.xlabel("League")
    plt.ylabel("Binary Accuracy (%)")
    plt.title("Binary Accuracy by League and Model")
    plt.xticks(x + width, leagues)
    plt.legend()

    plt.tight_layout()
    plt.savefig("results/binary_accuracy.pdf")
    plt.savefig("results/binary_accuracy.png")



if __name__ == "__main__":
    plot_binary_accuracy()