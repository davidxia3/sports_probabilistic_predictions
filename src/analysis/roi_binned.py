import pandas as pd
from pathlib import Path



def compute_fav_und_roi(row: pd.DataFrame) -> tuple[float, float]:
    """
    Computes ROI for favorite and underdog based on game row.

    Args:
        row (pd.DataFrame): Game data row.

    Returns:
        float: ROI of betting on favorite.
        float: ROI of betting on underdog.
    """

    home_is_fav = row["favorite"]
    home_won = row["result"] == 1

    home_ml = row["home_ml"]
    away_ml = row["away_ml"]

    if home_is_fav:
        fav_ml = home_ml
        dog_ml = away_ml
        fav_won = home_won
    else:
        fav_ml = away_ml
        dog_ml = home_ml
        fav_won = not home_won

    # favorite ROI
    if fav_won:
        if fav_ml < 0:
            favorite_roi = 100 / abs(fav_ml)
        else:
            favorite_roi = fav_ml / 100
    else:
        favorite_roi = -1

    # underdog ROI
    if not fav_won:
        if dog_ml < 0:
            underdog_roi = 100 / abs(dog_ml)
        else:
            underdog_roi = dog_ml / 100
    else:
        underdog_roi = -1

    return favorite_roi, underdog_roi



def compute_binned_roi(league: str, data_file: Path, method: str) -> None:
    """
    Computes and saves the ROI of betting on favorite and underdog determined by prediction method.
    
    Args:
        league (str): String object of league abbreviation (e.g. "nfl").
        data_file (Path): Path object of CSV file containing league game data.
        method (str): String object of name of prediction method.
    
    Returns:
        None
    """
    
    df = pd.read_csv(data_file)

    # drop all first half of regular season games
    df = df[df["second_half"] == 1]

    # home is favorite boolean
    df["favorite"] = df[f"{method}_prob"] >= 0.5

    # ensure directory exists
    output_dir = Path(f"results/roi_binned/{method}/{league}")

    for bin in range(10):
        bin_df = df[
            (df[f"{method}_prob"] >= bin / 10) &
            (df[f"{method}_prob"] < (bin + 1) / 10)
        ]

        if bin_df.empty:
            out_path = output_dir / f"bin_{bin}.csv"
            pd.DataFrame(columns=["season", "n", "favorite_roi", "underdog_roi"]).to_csv(out_path, index=False)
            continue

        # compute ROI for each game
        fav_rois = []
        dog_rois = []
        for _, row in bin_df.iterrows():
            fav_roi, dog_roi = compute_fav_und_roi(row)
            fav_rois.append(fav_roi)
            dog_rois.append(dog_roi)

        bin_df = bin_df.copy()
        bin_df["favorite_roi"] = fav_rois
        bin_df["underdog_roi"] = dog_rois

        # group by season
        grouped = (
            bin_df.groupby("season")
                  .agg(
                      n=("season", "count"),
                      favorite_roi=("favorite_roi", "mean"),
                      underdog_roi=("underdog_roi", "mean")
                  )
                  .reset_index()
        )

        # convert ROI to percentages
        grouped["favorite_roi"] = grouped["favorite_roi"] * 100
        grouped["underdog_roi"] = grouped["underdog_roi"] * 100

        # save CSV
        out_path = output_dir / f"bin_{bin}.csv"
        grouped.to_csv(out_path, index=False)



if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        for method in ["ml", "bt"]:
            compute_binned_roi(league, Path(f"processed_data/{league}.csv"), method)