# `processed_data/`
This folder contains all the cleaned and processed game data for each league.




### `{league}.csv`
There are 4 leagues: MLB, NBA, NFL, and NHL. Each has a CSV file with game data. The MLB file contains games from the 2009 season to the 2025 season. The NBA, NFL, and NHL files contain games from the 2008-2009 season to the 2024-2025 season. Each league's data is first cleaned to remove games that do not meet our requirements. Our requirements are below.
- Regular season: The game must be played during the regular season. This is to ensure all team's play the same number of games and at a consistent competitive level.
- Non-neutral: We intend to investigate the effects of home field/court advantage in our analysis, so we restrict our dataset to games where there is a home team and an away team.
- No ties: The game must end with a winner (no ties).
- No unrecognized teams: The game must be between two teams within the league. This is to exclude exhibition games, friendly games, all-star games, etc. that may not be held at a competitive level.
- Valid moneyline data: The game must have a moneylin score for the home team and a moneyline score for the away team. The moneyline scores are the primary probabilistic prediction method investigated in our analysis, so all games must have valid and non-missing moneyline data.

Below are the statistics behind the cleaning process.
| League | Total Regular Games | Neutral Regular Games | Regular Games w/ Ties | Regular Games w/ Unrecognized Teams | Regular Games w/ Invalid Moneyline | Clean Regular Games |
|--------|--------------------|----------------------|----------------------|-------------------------------------|------------------------------------|--------------------|
| MLB | 39,714 | 59 (0.149%) | 1 (0.003%) | 0 (0.000%) | 850 (2.140%) | 38,805 (97.711%) |
| NBA | 20,311 | 10 (0.049%) | 0 (0.000%) | 0 (0.000%) | 789 (3.885%) | 19,512 (96.066%) |
| NFL | 4,403 | 25 (0.568%) | 13 (0.295%) | 2 (0.045%) | 3 (0.068%) | 4,360 (99.023%) |
| NHL | 20,300 | 6 (0.030%) | 1 (0.005%) | 1 (0.005%) | 1,129 (5.562%) | 19,164 (94.404%) |

The regular season games that were discarded due to invalid moneyline were from the early seasons of each league (~ 2009-2010) where OddsPortal had less archived betting data.

After cleaning, the script then formats and processes the data to be be more convenient. The columns of each processed data file are below.
- `date`: Date of the game into `yyyy-mm-dd` format.
- `season`: The season as an integer, representing the year the season ended. 
- `second_half`: A 1/0 boolean representing if the game is in the second half of its respective regular season. This is determined by if more than half of the valid regular season games are chronologically before the game. 
- `home_team`: The home team's abbreviation.
- `away_team`: The away team's abbreviation.
- `result`: A 1/0 boolean representing who won the game. 1 if the home team won and 0 if the away team won. Determined by comparing the number of points the two teams scored.
- `home_ml`: An integer representing the average of raw moneyline scores for the `home_team`.
- `away_ml`: An integer representing the average of raw moneyline scores for the `away_team`.
- `bookmaker_profit`: The profit the bookmaker makes on the game's `home_ml` and `away_ml`.
- `ml_prob`: The moneyline based probabilistic prediction that `home_team` wins over `away_team`. 
- `bt_prob`: The Bradley-Terry based probabilistic prediction that `home_team` wins over `away_team`. Only computed for second half of season games.
- `game_url`: The URL leading to the game's webpage.