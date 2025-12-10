import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json



def plot_team_brier_bar(csv_path: Path, color_map: dict, output_path: Path) -> None:
    """
    Plot a bar chart of the teamwise moneyline Brier score.

    Args:
        csv_path (Path): Path object to the CSV file.
        color_map (dict): Dictionary mapping team to color.
        output_path (Path): Path object of PNG file where the figure is saved.

    Returns:
        None
    """
    df = pd.read_csv(csv_path)

    # sort ascending by brier score
    df = df.sort_values("brier_score", ascending=True)

    # determine bar colors
    colors = [color_map[team] for team in df["team"]]
    normalized_colors = []
    for color in colors:
        normalized_color = [val / 255.0 for val in color]
        normalized_colors.append(normalized_color)

    plt.figure(figsize=(12, 6))
    plt.bar(df["team"], df["brier_score"], color=normalized_colors)
    ymin = df["brier_score"].min()
    ymax = df["brier_score"].max()
    padding = (ymax - ymin) * 0.1
    plt.ylim(ymin - padding, ymax + padding)
    plt.xlabel("Team")
    plt.ylabel("Brier Score")
    plt.title(f"{league.upper()} Moneyline Brier Scores by Team")
    plt.xticks(rotation=270, ha="right")
    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    plt.close()



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        with open(f"utility/{league}_team_colors.json") as f:
            color_map = json.load(f)

        plot_team_brier_bar(
            csv_path=Path(f"results/ml_teamwise_brier/{league}.csv"),
            color_map=color_map,
            output_path=Path(f"results/ml_teamwise_brier/{league}.png")
        )