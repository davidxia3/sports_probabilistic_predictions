import pandas as pd
from pathlib import Path
import csv








def compute_binary_accuracy(data_file: Path, method: str) -> float:
    """
    Computes the binary accuracy of the prediction method in a file.

    Args:
        data_file (Path): Path object of CSV file with game data.
        method (str): String object of name of column header in file with prediction probability.
    
    Returns:
        float: Float object of binary_accuracy of probabilistic prediction. 
    """

    df = pd.read_csv(data_file)
    mask = df[method].notna()

    # a probabilistic prediction greater than or equal to 0.5 for team 1, indicates team 1 is the binary prediction
    accuracy = ((df.loc[mask, method] >= 0.5).astype(int) == df.loc[mask, 'result']).mean()
    return accuracy







if __name__ == "__main__":
    output = []
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        output.append({'league': league, 'method': "ml_prob", 'binary_accuracy': compute_binary_accuracy(f"processed_data/{league}.csv", "ml_prob")})
        if league == "nfl":
            output.append({'league': league, 'method': "elo_prob", 'binary_accuracy': compute_binary_accuracy(f"processed_data/{league}.csv", "elo_prob")})
    with open("results/binary_accuracy.csv", mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["league", "method", "binary_accuracy"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for game in output:
            writer.writerow(game)
