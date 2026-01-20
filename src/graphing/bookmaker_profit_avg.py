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

    df = pd.read_csv("results/bookmaker_profit.csv")

    df["league"] = df["league"].str.upper()

    color_map = {
        "MLB": "red",
        "NBA": "orange",
        "NFL": "green",
        "NHL": "blue",
    }

    colors = df["league"].map(color_map)

    plt.figure()
    plt.bar(df["league"], df["average"], color=colors, width=0.5)




    plt.xlabel("League")
    plt.ylabel("Average Bookmaker Profit (%)")
    plt.title("Average Bookmaker Profit by League")

    plt.ylim(3, 5)
    plt.tight_layout()
    plt.savefig("results/bookmaker_profit_avg.pdf")
    plt.savefig("results/bookmaker_profit_avg.png")



if __name__ == "__main__":
    plot_avg_bookmaker_profit()