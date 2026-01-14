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

    plt.figure()
    plt.bar(df["league"], df["average"])




    plt.xlabel("League")
    plt.ylabel("Average Bookmaker Profit (%)")
    plt.title("Average Bookmaker Profit by League")

    plt.ylim(3, 5)
    plt.tight_layout()
    plt.savefig("results/bookmaker_profit_avg.pdf")
    plt.savefig("results/bookmaker_profit_avg.png")



if __name__ == "__main__":
    plot_avg_bookmaker_profit()