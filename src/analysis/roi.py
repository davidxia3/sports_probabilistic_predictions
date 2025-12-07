import pandas as pd
from pathlib import Path
import numpy as np



def calculate_betting_roi(df: pd.DataFrame, method: str, output_path: Path) -> None:
    """
    Analyzes betting ROI for favorites and underdogs across probability bins.
    
    Args:
        df (pd.DataFrame): DataFrame of specified league games to be considered for calculation.
        method (str): String object of name of prediction method.
        output_path (Path): Path object where ROI results will be saved.

    Returns:
        None
    """
    df = df.dropna(subset=[f"{method}_prob", "home_ml", "away_ml"])

    # drop all first half of regular season games
    df = df[df["second_half"] == 1]

    # calculate payout from single moneyline
    def calculate_payout(odds):
        return np.where(odds > 0, odds / 100.0, 100.0 / np.abs(odds))

    # calculate potential profit for home and away
    df['home_potential_profit'] = calculate_payout(df['home_ml'])
    df['away_potential_profit'] = calculate_payout(df['away_ml'])

    # calculate actual profit and loss for a 1-unit bet on home and away
    df['home_bet_pnl'] = np.where(df['result'] == 1, df['home_potential_profit'], -1.0)
    df['away_bet_pnl'] = np.where(df['result'] == 0, df['away_potential_profit'], -1.0)

    # determine favorite and underdog profit and loss
    is_home_fav = df[f"{method}_prob"] >= 0.5
    
    # sassign favorite profit and loss
    df['favorite_roi'] = np.where(is_home_fav, df['home_bet_pnl'], df['away_bet_pnl'])
    
    # assign underdog profit and loss
    df['underdog_roi'] = np.where(is_home_fav, df['away_bet_pnl'], df['home_bet_pnl'])

    # create 10 equal width bins probability
    bins = np.linspace(0, 1, 11)
    df['bin'] = pd.cut(df[f"{method}_prob"], bins=bins, include_lowest=True, labels=False)

    # group by bin and calculate mean ROI
    analysis = df.groupby('bin', observed=False)[['favorite_roi', 'underdog_roi']].agg(['mean', 'count'])
    
    analysis.columns = ['_'.join(col).strip() for col in analysis.columns.values]
    analysis = analysis.reindex(range(10))  
    analysis.index.name = 'bin'
    analysis = analysis.rename(columns={
        'favorite_roi_mean': 'favorite_roi',
        'favorite_roi_count': 'n',
        'underdog_roi_mean': 'underdog_roi'
    })
    analysis['n'] = analysis['n'].fillna(0).astype(int)
    
    # convert to percentage
    analysis['favorite_roi'] = (analysis['favorite_roi'] * 100).round(4)
    analysis['underdog_roi'] = (analysis['underdog_roi'] * 100).round(4)
    analysis = analysis.reset_index()


    # save results  
    analysis = analysis[["bin", "n", "favorite_roi", "underdog_roi"]]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    analysis.to_csv(output_path, index=False)



if __name__ == "__main__":
    league_files = {
        "mlb": Path("processed_data/mlb.csv"),
        "nba": Path("processed_data/nba.csv"),
        "nfl": Path("processed_data/nfl.csv"),
        "nhl": Path("processed_data/nhl.csv")
    }

    methods = ["ml", "bt"]
    
    for league, path in league_files.items():
            
        df = pd.read_csv(path)
        for method in methods:
            calculate_betting_roi(df, method, Path(f"results/roi/{method}_roi/{league}/{league}.csv"))

            for season in sorted(df["season"].unique()):
                calculate_betting_roi(df[df["season"]==season], method, Path(f"results/roi/{method}_roi/{league}/{league}_{season}.csv"))