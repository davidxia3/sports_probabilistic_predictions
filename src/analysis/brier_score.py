import pandas as pd
from pathlib import Path



def load_filtered_data(data_file: Path, usable_methods: list[str], second_half_only: int) -> pd.DataFrame:
    """
    Load a game-level dataset and return only the rows that satisfy the
    filtering requirements for evaluation.

    Args:
        data_file (Path): Path object of CSV file containing prediction data.
        all_methods (list[str]): List of all prediction method names.
        second_half_only (int): If 1, restrict to games in second half of seasons, otherwise, use the full dataset.

    Returns:
        pd.DataFrame: A filtered DataFrame containing only rows where all required probability columns exist and are non-null.
    """

    df = pd.read_csv(data_file)

    # optional half-season filter
    if second_half_only == 1:
        df = df[df["second_half"] == 1]

    # mask for valid method probabilities
    prob_cols = [f"{m}_prob" for m in usable_methods]
    mask = df[prob_cols].notna().all(axis=1)

    return df.loc[mask]



def compute_brier_score(data_file: Path, method: str, usable_methods: list[str], second_half_only: int) -> float:
    """
    Compute the Brier score for a specified prediction method using only the rows where all prediction method probability columns are present.

    Args:
        data_file (Path): Path object of CSV file containing game data.
        method (str): Name of the prediction method to evaluate (e.g., "ml").
        usable_methods (list[str]): List of all prediction method names.
        second_half_only (int): If 1, restrict to games in second half of seasons, otherwise, use the full dataset.

    Returns:
        float: The Brier score for the specified method.
    """

    df_valid = load_filtered_data(data_file, usable_methods, second_half_only)

    preds = df_valid[f"{method}_prob"].astype(float)
    y = df_valid["result"]

    return ((preds - y) ** 2).mean()



def compute_home_win_probability(data_file: Path) -> float:
    """
    Calculates the proportion of games won by the home team in the entire data set.

    Args:
        data_file (Path): Path object of CSV file containing game data.

    Returns:
        float: Proportion of games won by the home team in the entire data set.
    """

    df = pd.read_csv(data_file)
    return df["result"].mean()


def compute_home_win_brier(data_file: Path, usable_methods: list[str], second_half_only: int) -> float:
    """
    Compute Brier score for baseline method of always predicting the home team to win using the empirical home-team win rate.

    Args:
        data_file (Path): Path object of CSV file containing game data.
        usable_methods (list[str]): List of all prediction method names.
        second_half_only (int): If 1, restrict to games in second half of seasons, otherwise, use the full dataset.

    Returns:
        float: Brier score for home win probability baseline method.
    """

    # baseline probability of overall home win rate
    p_home = compute_home_win_probability(data_file)

    # evaluate accuracy only on valid rows (consistent with methods)
    df_valid = load_filtered_data(data_file, usable_methods, second_half_only)
    y = df_valid["result"]

    return ((p_home - y) ** 2).mean()



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    all_methods = ["ml", "elo", "elopoint", "elowin", "keener", "massey", "od", "bt"]

    results = []

    for league in leagues:
        data_file = Path(f"processed_data/{league}.csv")

        # NFL is the only league with Elo
        usable = all_methods if league == "nfl" else [m for m in all_methods if m != "elo"]

        for second_half_only in [0, 1]:

            row = {
                "league": league,
                "half": second_half_only
            }

            # model Brier scores
            for method in all_methods:
                row[method] = pd.NA
                if method not in usable:
                    continue

                row[method] = compute_brier_score(
                    data_file=data_file,
                    method=method,
                    usable_methods=usable,
                    second_half_only=second_half_only
                )

            # baseline Brier
            row["home_win_base"] = compute_home_win_brier(
                data_file=data_file,
                usable_methods=usable,
                second_half_only=second_half_only
            )

            results.append(row)

    # save results
    output_df = pd.DataFrame(results)
    output_df.to_csv("results/brier_score.csv", index=False)
