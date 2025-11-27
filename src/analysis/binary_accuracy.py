import pandas as pd
from pathlib import Path




def compute_binary_accuracy(data_file: Path, method: str, all_methods: list[str]) -> float:
    """
    Computes the binary accuracy of a prediction method using only the rows where
    all prediction methods have non-missing values.

    Args:
        data_file (Path): CSV file containing game data.
        method (str): Column name of the prediction probability to evaluate.
        all_methods (list[str]): List of all prediction method column names.

    Returns:
        float: Binary accuracy computed only over rows where all methods are present.
    """

    df = pd.read_csv(data_file)

    # keep only rows where all method columns are not NA
    mask = df[all_methods].notna().all(axis=1)

    # compute binary prediction (>= 0.5 means team 1 predicted to win)
    preds = (df.loc[mask, method] >= 0.5).astype(int)

    # compute accuracy
    accuracy = (preds == df.loc[mask, "result"]).mean()

    return accuracy




if __name__ == "__main__":
    output = []
    leagues = ["mlb", "nba", "nfl", "nhl"]
    base_methods = ["ml", "elopoint", "elowin", "keener", "massey", "od"]

    for league in leagues:

        # full list of prediction columns for this league
        all_methods = [f"{m}_prob" for m in base_methods]

        # NFL has one extra method
        if league == "nfl":
            all_methods.append("elo_prob")

        # compute accuracy for each method
        for method in all_methods:
            acc = compute_binary_accuracy(
                data_file=f"processed_data/{league}.csv",
                method=method,
                all_methods=all_methods
            )
            output.append({
                "league": league,
                "method": method,
                "binary_accuracy": acc
            })

    output_df = pd.DataFrame(output)
    output_df = output_df.sort_values(by="binary_accuracy", ascending=False)
    output_df.to_csv("results/binary_accuracy.csv", index=False)
