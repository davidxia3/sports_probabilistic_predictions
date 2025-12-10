import pandas as pd



def compute_bookmaker_profit_stats() -> None:
    """
    Computes bookmaker profit statistics for all leagues and saves to a CSV file.

    Args:
        None
    
    Returns:
        None
    """

    leagues = ["mlb", "nba", "nfl", "nhl"]
    results = []

    for league in leagues:
        df = pd.read_csv(f"processed_data/{league}.csv")

        # drop all first half of regular season games
        df = df[df["second_half"] == 1]

        profits = df["bookmaker_profit"] * 100

    
        q1 = profits.quantile(0.25)
        median = profits.quantile(0.50)
        q3 = profits.quantile(0.75)
        iqr = q3 - q1

        # Tukey whiskers: 1.5 * IQR rule
        lower_whisker = profits[profits >= (q1 - 1.5 * iqr)].min()
        upper_whisker = profits[profits <= (q3 + 1.5 * iqr)].max()

        stats = {
            "league": league,
            "min": profits.min(),
            "q1": q1,
            "median": median,
            "q3": q3,
            "max": profits.max(),
            "iqr": iqr,
            "lower_whisker": lower_whisker,
            "upper_whisker": upper_whisker,
        }

        results.append(stats)

    # save stats table
    out_df = pd.DataFrame(results)
    out_df.to_csv("results/bookmaker_profit.csv", index=False)



if __name__ == "__main__":
    compute_bookmaker_profit_stats()