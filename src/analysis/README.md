# `src/analysis/`
This folder contains all the Python scripts for extracting CSV results from the processed data. All results are derived only from games from the second half of each regular season. 




### `src/analysis/binary_accuracy.py`
This Python script computes the binary accuracy of various model based prediction methods for each league and saves the results to `results/binary_accuracy.csv`. Probabilistic predictions are converted to binary predictions using a 0.5 threshold. The columns of the results file are below.
- `league`: League name. 
- `ml`: Binary accuracy of predictions derived from moneyline scores.
- `bt`: Binary accuracy of predictions derived from Bradley-Terry rating algorithm.
- `hom_win_base`: Binary accuracy of predictions based on if home or away teams won more from first half of each respective regular season.


### `src/analysis/bookmaker_profit.py`
This Python script computes the summary statistics of the bookmaker profit percentages for each league and saves the results to `results/bookmaker_profit.csv`. The columns of the results file are below.
- `league`: League name.
- `min`: Minimum bookmaker profit percentage. 
- `q1`: Quartile 1 of bookmaker profit percentages.
- `median`: Median of bookmaker profit percentages.
- `q3`: Quartile 3 of bookmaker profit percentages.
- `max`: Maximum bookmaker profit percentage. 
- `lower_whisker`: Lower Tukey cutoff (`q1` - 1.5(`q3`-`q1`)) for bookmaker profit percentage outliers.
- `upper_whisker`: Upper Tukey cutoff (`q3` + 1.5(`q3`-`q1`)) for bookmaker profit percentage outliers. 


### `src/analysis/brier_score.py`
This Python script computes the Brier scores of various model based prediction methods for each league and saves the results to `results/brier_score.csv`. The columns of the results file are below.
- `league`: League name.
- `ml`: Brier score of probabilistic predictions derived from moneyline scores.
- `bt`: Brier score of probabilistic predictions derived from Bradley-Terry rating algorithm.
- `hom_win_base`: Brier score of always predicting home team to win with proportion of first half of regular season games won by home team. 


### `src/analysis/calibration.py`
This Python script computes the calibration statistics of the moneyline based and Bradley-Terry based probabilistic prediction methods across each league. Games are grouped by prediction into 10 equally sized bins ([0, 0.1), [0,1, 0.2), etc). For each bin, the average winrate of the home team is calculated. NA values are replace average winrate if there were no games for the bin. For each league, the results are saved to `results/calibration/{league}.csv`. The columns of each results file are below.
- `bin`: Number between 0 and 9, representing the probability bin. 
- `ml_winrate`: Average home team winrate in games where the moneyline based prediction was within the bin.
- `bt_winrate`: Average home team winrate in games where Bradley-Terry based prediction was within the bin. 


### `src/analysis/home_predictions_box.py`
This Python script computes the summary statistics of the moneyline based and Bradley-Terry based probabilistic predictions across each league. For each probabilistic prediciton method, the results are saved to `results/home_predictions/{method}_box.csv`. The columns of each results file are below.
- `league`: League name.
- `min`: Minimum predicted home team win probability. 
- `q1`: Quartile 1 of predicted home team win probabilities.
- `median`: Median of predicted home team win probabilities.
- `q3`: Quartile 3 of predicted home team win probabilities.
- `max`: Maximum predicted home team win probability.
- `lower_whisker`: Lower Tukey cutoff (`q1` - 1.5(`q3`-`q1`)) for predicted home team win probability outliers.
- `upper_whisker`: Upper Tukey cutoff (`q3` + 1.5(`q3`-`q1`)) for predicted home team win probability outliers. 


### `src/analysis/home_predictions_hist.py`
This Python script computes the density histogram statistics of the moneyline based and Bradley-Terry based probabilistic predictions across each league. The histogram is split into 30 equally width bins spanning the entire probability range ([0,1]). The density is used instead of raw counts as different leagues have different total counts. For each probabilistic prediction method and each league, the results are saved to `results/home_predictions/{method}_{league}_hist.csv`. The columns of each results file are below.
- `bin_left`: Left boundary of probability bin.
- `bin_right`: Right boundary of probability bin.
- `bin_center`: Average of `bin_left` and `bin_right`.
- `density`: Density of games with probabilistic prediction between `bin_left` and `bin_right`. 


### `src/analysis/log_loss.py`
This Python script computes the log loss scores of various model based prediction methods for each league and saves the results to `results/log_loss.csv`. The columns of the results file are below.
- `league`: League name.
- `ml`: Log loss score of probabilistic predictions derived from moneyline scores.
- `bt`: Log loss score of probabilistic predictions derived from Bradley-Terry rating algorithm.
- `hom_win_base`: Log loss score of always predicting home team to win with proportion of first half of regular season games won by home team.


### `src/analysis/ml_seasonal_brier.py`
This Python script computes the Brier score of the moneyline based probabilistic predictions by season for each league. The results are saved to `results/ml_seasonal_brier.csv`. The columns of the results file are below.
- `season`: The season as an integer, representing the year the season ended.
- `mlb_brier`: The Brier score of the moneyline based probabilistic predictions for the MLB by season.
- `nba_brier`: The Brier score of the moneyline based probabilistic predictions for the NBA by season.
- `nfl_brier`: The Brier score of the moneyline based probabilistic predictions for the NFL by season.
- `nhl_brier`: The Brier score of the moneyline based probabilistic predictions for the NHL by season.


### `src/analysis/ml_teamwise_brier.py`
This Python script computes the Brier score of the moneyline based probabilistic predictions by team for each league. A team's Brier score is the Brier score the moneyline based prediction for all games involving the team, regardless if the team is home or away. For each league, the results are saved to `results/ml_teamwise_brier/{league}.csv`. The columns of each results file are below.
- `team`: The team's abbreviation.
- `brier_score`: The Brier score of all games involving the team.


### `src/analysis/model_seasonal_brier.py`
This Python script computes the Brier score of various model based probabilistic predictions by season for each league. For each league, the results are saved to `results/model_seasonal_brier/{league}.csv`. The columns of each results file are below.
- `season`: The season as an integer, representing the year the season ended. 
- `ml_brier`: The Brier score of moneyline based probabilistic predictions.
- `bt_brier`: The Brier score of Bradley-Terry based probabilistic predictions.
- `home_bias_brier`: The Brier score of predictions using the home team win probability from the first half of each regular season.
- `coinflip_brier`: The Brier score of a constant 0.5 prediction for all games. 


### `src/analysis/roi_binned.py`
This Python script computes the return on investment of always betting on the favorite vs the return on investment of always betting on the underdog in each bin and by season. Games are grouped by prediction into 10 equally sized bins ([0, 0.1), [0,1, 0.2), etc). For each bin, games are grouped by season. The favorite of the game is determined by the specified probabilistic prediction method. If the specified probabilistic prediction method is not the moneyline, then the favorite may disagree with the implied favorite from moneyline scores. However, the ROI is always calculated using the moneyline scores, regardless of specified prediction method.

Example:
- Home team: ML = -250.
- Away team: ML = +200.
- Bradley-Terry prediction: 0.4.
The moneyline scores states that the home team is the favorite. However, because the Bradley-Terry based prediction is less than 0.5, the favorite according to Bradley-Terry is the away team. If the game resulted in the home team winning, the ROI of betting on the favorite would be -100% (all investment lost). If the game resulted in the away team winning, the ROI of betting on the favorite would be 200%.

For each probabilistic prediction method, league, and bin (0-9), the results are saved to `results/roi/{method}_binned/{league}/bin_{bin}.csv`. The columns of each results file are below.
- `season`: The season as an integer, representing the year the season ended.
- `n`: The number of samples (games).
- `favorite_roi`: The ROI percentage of always betting on the favorite according to the specified prediction method. 
- `underdog_roi`: The ROI percentage of always betting on the underdog according to the specified prediction method.


### `src/analysis/roi.py`
This Python script computes the return on investment of always betting on the favorite vs the return on investment of always betting on the underdog by bin for each league. For each league, games are grouped by prediction into 10 equally sized bins ([0, 0.1), [0,1, 0.2), etc). The favorite of the game is determined by the specified probabilistic prediction method. If the specified probabilistic prediction method is not the moneyline, then the favorite may disagree with the implied favorite from moneyline scores. However, the ROI is always calculated using the moneyline scores, regardless of specified prediction method.

Example:
- Home team: ML = -250.
- Away team: ML = +200.
- Bradley-Terry prediction: 0.4.
The moneyline scores states that the home team is the favorite. However, because the Bradley-Terry based prediction is less than 0.5, the favorite according to Bradley-Terry is the away team. If the game resulted in the home team winning, the ROI of betting on the favorite would be -100% (all investment lost). If the game resulted in the away team winning, the ROI of betting on the favorite would be 200%.

For each probabilistic prediction method and league, the results are saved to `results/roi/{method}/{league}.csv`. The columns of each results file are below.
- `season`: The season as an integer, representing the year the season ended.
- `n`: The number of samples (games).
- `favorite_roi`: The ROI percentage of always betting on the favorite according to the specified prediction method. 
- `underdog_roi`: The ROI percentage of always betting on the underdog according to the specified prediction method.


### `src/analysis/seasonal_home_win.py`
This Python script computes the proportion of games won by the home team in the first half of each regular season for all leagues. The results are saved to `results/seasonal_home_win.csv`. The columns of the results file are below.
- `season`: The season as an integer, representing the year the season ended. 
- `mlb`: The proportion of games won by the home team in the first half of the regular season for a specified season in the MLB.
- `nba`: The proportion of games won by the home team in the first half of the regular season for a specified season in the NBA.
- `nfl`: The proportion of games won by the home team in the first half of the regular season for a specified season in the NFL.
- `nhl`: The proportion of games won by the home team in the first half of the regular season for a specified season in the NHL.


### `src/analysis/teamwise_winrates.py`
This Python script computes the winrates for each team. For every league, the results are saved to `results/ml_teamwise_brier/{league}_winrates.csv`. The columns of the results file are below.
- `team`: Team abbreviation.
- `winrate`: Team's winrate as a percentage.  