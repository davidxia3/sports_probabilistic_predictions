import pandas as pd
from pathlib import Path



def compute_teamwise_winrate(csv_path: Path) -> pd.DataFrame:
    """
    Computes winrate for each team in the league.

    Args:
        csv_path (Path): Path object of CSV file with league game data.

    Returns:
        pd.DataFrame: DataFrame with 2 columns: team and winrate.
    """

    df = pd.read_csv(csv_path)

    team_1_wins = df[['home_team', 'result']].copy()
    team_1_wins.columns = ['team', 'win']
    team_1_wins['win'] = team_1_wins['win']

    team_2_wins = df[['away_team', 'result']].copy()
    team_2_wins.columns = ['team', 'win']
    team_2_wins['win'] = 1 - team_2_wins['win']

    all_teams = pd.concat([team_1_wins, team_2_wins])

    win_rates = all_teams.groupby('team')['win'].mean()

    win_rates_df = win_rates.reset_index().rename(columns={'win': 'win_rate'}).sort_values(by='win_rate', ascending=False)

    return win_rates_df



if __name__ == "__main__":
    league_files = {
        "mlb": Path("processed_data/mlb.csv"),
        "nba": Path("processed_data/nba.csv"),
        "nfl": Path("processed_data/nfl.csv"),
        "nhl": Path("processed_data/nhl.csv")
    }
    
    for league, path in league_files.items():
        league_df = compute_teamwise_winrate(path)
        league_df.to_csv(f"results/ml_teamwise_brier/{league}_winrates.csv", index=False)
