import pandas as pd
from pathlib import Path

def american_payout(ml, result):
    """
    Computes return (profit) for betting 1 unit on a line with
    American odds ml. result = 1 if the team you bet on wins, else 0.
    """
    if result == 1:  # win
        if ml > 0:
            return ml / 100
        else:
            return 100 / abs(ml)
    else:  # loss
        return -1


def compute_roi(df):
    # Determine favorite by probability
    df["favorite_is_team1"] = df["ml_prob"] >= 0.5

    # Assign ML odds for favorite and underdog
    df["favorite_ml"] = df.apply(
        lambda r: r["home_ml"] if r["favorite_is_team1"] else r["away_ml"],
        axis=1
    )
    df["underdog_ml"] = df.apply(
        lambda r: r["away_ml"] if r["favorite_is_team1"] else r["home_ml"],
        axis=1
    )

    # Compute favorite return
    df["favorite_return"] = df.apply(
        lambda r: american_payout(r["favorite_ml"],
                                  r["result"] if r["favorite_is_team1"] else 1 - r["result"]),
        axis=1
    )

    # Compute underdog return
    df["underdog_return"] = df.apply(
        lambda r: american_payout(r["underdog_ml"],
                                  1 - r["result"] if r["favorite_is_team1"] else r["result"]),
        axis=1
    )

    # ROI = average return per 1-unit bet
    roi = df.groupby("season").agg(
        favorite_roi=("favorite_return", "mean"),
        underdog_roi=("underdog_return", "mean")
    ).reset_index()

    return roi


def create_roi_bins(csv_path: Path, output_dir: Path):
    df = pd.read_csv(csv_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    bins = [(i/10, (i+1)/10) for i in range(10)]

    for low, high in bins:
        bin_df = df[(df["ml_prob"] >= low) & (df["ml_prob"] < high)]

        if bin_df.empty:
            continue

        roi_df = compute_roi(bin_df)
        filename = f"roi_bin_{int(low*100)}_{int(high*100)}.csv"
        roi_df.to_csv(output_dir / filename, index=False)

        print(f"Saved {filename}")


leagues = ["mlb", "nba", "nfl", "nhl"]
for league in leagues:
    csv_path = Path(f"processed_data/{league}.csv")        # Your input CSV
    output_dir = Path(f"results/roi_binned/ml/{league}")       # Output folder
    create_roi_bins(csv_path, output_dir)
