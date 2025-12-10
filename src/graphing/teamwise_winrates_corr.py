import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import linregress



def plot_winrate_vs_brier(brier_csv: Path, winrate_csv: Path, league: str, output_path: Path) -> None:
    """
    Plots scatterplot of |winrate - 0.5| vs Brier score and regression line.

    Args:
        brier_csv (Path): Path object of CSV file with team Brier scores.
        winrate_csv (Path): Path object of CSV file team winrates.
        league (str): String object of team abbreviation (e.g. "nfl").
        output_path (Path): Path object of PNG file where figure will be saved.

    Returns:
        None
    """

    df_brier = pd.read_csv(brier_csv)
    df_wr = pd.read_csv(winrate_csv)

    # erge on "team"
    df = pd.merge(df_brier, df_wr, on="team", how="inner")
    df = df.dropna(subset=["brier_score", "win_rate"])

    # compute |winrate - 0.5|
    df["abs_wr_diff"] = (df["win_rate"] - 0.5).abs()

    x = df["abs_wr_diff"]
    y = df["brier_score"]

    # regression
    slope, intercept, _, p_value, _ = linregress(x, y)
    reg_line = slope * x + intercept


    color_map = {
        "mlb": "red",
        "nba": "orange",
        "nfl": "green",
        "nhl": "blue"
    }

    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, color=color_map[league], label=f"{league.upper()} teams")
    plt.plot(x, reg_line, linewidth=2, color="black",
             label=f"y = {slope:.4f}x + {intercept:.4f}\n(p={p_value:.4g})")

    plt.xlabel("|Win Rate - 0.5|")
    plt.ylabel("Brier Score")
    plt.title(f"{league.upper()}: |Win Rate - 0.5| vs Moneyline Brier Score")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    plt.close()



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]

    for league in leagues:
        plot_winrate_vs_brier(
            brier_csv=Path(f"results/ml_teamwise_brier/{league}.csv"),
            winrate_csv=Path(f"results/ml_teamwise_brier/{league}_winrates.csv"),
            league=league,
            output_path=Path(f"results/ml_teamwise_brier/{league}_winrates.png")
        )