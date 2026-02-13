import pandas as pd
import matplotlib.pyplot as plt



def plot_avg_bookmaker_profit() -> None:
    """
    Plots bar chart of average moneyline bookmaker profit for each league.

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

    df = pd.read_csv("results/bookmaker_profit.csv")

    df["league"] = df["league"].str.upper()

    color_map = {
        "MLB": "#c91f37",
        "NBA": "#ff8936",
        "NFL": "#057748",
        "NHL": "#2e4e7e"
    }

    colors = df["league"].map(color_map)

    plt.figure(figsize=(10,6))
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.bar(df["league"], df["average"], color=colors, width=0.67)


    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)

    plt.ylabel("Average Bookmaker Profit (%)", fontsize=16)

    plt.ylim(3, 6)
    plt.tight_layout()
    plt.savefig("results/bookmaker_profit_avg.pdf")
    plt.savefig("results/bookmaker_profit_avg.png")
    plt.show()


if __name__ == "__main__":
    plot_avg_bookmaker_profit()