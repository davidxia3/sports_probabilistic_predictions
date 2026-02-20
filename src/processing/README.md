# `src/processing/`
This folder contains all Python scripts that clean, preprocess, and format data.




### `decimal_formatting.py`
This Python script formats floating point data in the `results/` folder. All CSV files in the `results/` folder is duplicated. The duplicate version has all floating point values rounded/padded to have exactly 3 digits after the decimal point. All other values are kept the same. The formatted version of the file `{file_name_stem}.csv` is saved to `{file_name_stem}_fmt.csv`. If a figure is generated based on the CSV result file, then it is generated based on the original CSV file with full floating point precision. The formatted version of the CSV file is only for user inspection.


### `preprocessing.py`
This Python script cleans and processes the raw data for each league. For each league, the final data is saved to `processed_data/{league}.csv`. Each league's data is first cleaned to remove games that do not meet our requirements. Our requirements are below.
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
- `home_ml`: An integer moneyline for the `home_team`, derived by converting the average implied win probability across bookmakers back to American odds.
- `away_ml`: An integer moneyline for the `away_team`, derived by converting the average implied win probability across bookmakers back to American odds.
- `bookmaker_profit`: The bookmaker's built-in margin (vig), calculated by summing the average implied home and away probabilities and subtracting 1.
    - Each bookmaker's moneylines are first converted to implied probabilities, then averaged across bookmakers. For a positive moneyline, the implied probability is 100 / (ML + 100). For a negative moneyline, the implied probability is |ML| / (|ML| + 100).
- `ml_prob`: The normalized probability that `home_team` wins over `away_team`, calculated by dividing the average implied home probability by the sum of the average implied home and away probabilities.
- `bt_prob`: The Bradley-Terry based probabilistic prediction that `home_team` wins over `away_team`. 
    - The probability is calculated by using all previous games in the season to obtain Bradley-Terry ratings for each team. The probability that `home_team` wins over `away_team` is the `home_team`'s rating divided by the sum of the two ratings. 
    - The Bradley-Terry rating estimation process is from this [website](https://datascience.oneoffcoder.com/btl-model.html). A maximum of 100 iterations are used for each game.
    - BRadley-Terry based probabilistic predictions are only computed for second half of season games.
- `game_url`: The URL leading to the game's webpage.