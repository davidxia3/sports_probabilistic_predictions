import pandas as pd



def compute_home_prediction_stats(method: str) -> None:
    """
    Computes home prediction statistics for all leagues and saves to a CSV file.

    Args:
        method (str): String object of name of prediction method.
    
    Returns:
        None
    """

    leagues = ["mlb", "nba", "nfl", "nhl"]
    results = []

    for league in leagues:
        df = pd.read_csv(f"processed_data/{league}.csv")

        # drop all first half of regular season games
        df = df[df["second_half"] == 1]

        predictions = df[f"{method}_prob"] * 100

    
        q1 = predictions.quantile(0.25)
        median = predictions.quantile(0.50)
        q3 = predictions.quantile(0.75)
        iqr = q3 - q1

        # Tukey whiskers: 1.5 * IQR rule
        lower_whisker = predictions[predictions >= (q1 - 1.5 * iqr)].min()
        upper_whisker = predictions[predictions <= (q3 + 1.5 * iqr)].max()

        stats = {
            "league": league,
            "min": predictions.min(),
            "q1": q1,
            "median": median,
            "q3": q3,
            "max": predictions.max(),
            "iqr": iqr,
            "lower_whisker": lower_whisker,
            "upper_whisker": upper_whisker,
        }

        results.append(stats)

    # save stats table
    out_df = pd.DataFrame(results)
    out_df.to_csv(f"results/home_predictions/{method}_box.csv", index=False)



if __name__ == "__main__":
    methods = ["ml", "bt"]
    for method in methods:
        compute_home_prediction_stats(method)