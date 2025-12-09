import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def plot_roi(league, folder: Path):
    files = list(folder.glob("*.csv"))

    for f in files:
        df = pd.read_csv(f)

        # Convert ROI to percentage
        df["favorite_roi_pct"] = df["favorite_roi"] * 100
        df["underdog_roi_pct"] = df["underdog_roi"] * 100

        # Sort by season
        df = df.sort_values("season")

        bin_name = f.stem   # e.g. roi_bin_0_10

        # Plot
        plt.figure(figsize=(12, 6))
        plt.plot(df["season"], df["favorite_roi_pct"], label="Favorite ROI", color="green")
        plt.plot(df["season"], df["underdog_roi_pct"], label="Underdog ROI", color="red")

        plt.xlabel("Season")
        plt.ylabel("ROI (%)")
        plt.title(f"{league.upper()} - Favorite vs Underdog ROI — {bin_name}")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.xticks(rotation=45)

        plt.tight_layout()

        # Save figure
        out_path = Path("figures")
        out_path.mkdir(exist_ok=True)
        plt.savefig(out_path / f"{league}_{bin_name}.png")
        plt.close()


# ---- Run it ----
leagues = ["mlb", "nba", "nfl", "nhl"]
for league in leagues:
    roi_folder = Path(f"results/roi_binned/ml/{league}")
    plot_roi(league, roi_folder)
