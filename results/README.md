# `results/`
This folder contains all CSV results and PNG figures from the analysis of processed data. All results are derived only from games from the second half of each regular season. 




## `results/calibration/`
This folder contains all the CSV results and PNG figures of various prediction model calibrations. All results are derived only from games from the second half of each regular season. 


## `results/home_predictions/`
This folder contains all the CSV results and PNG figures of the home team win prediction distributions. All results are derived only from games from the second half of each regular season. 


## `results/ml_teamwise_brier/`
This folder contains all CSV results and PNG figures of teamwise Brier scores and team winrates for each league. All results are derived only from games from the second half of each regular season.


## `results/model_seasonal_brier/`
This folder contains all the CSV results and PNG figures of the Brier scores of various model based probabilistic prediction methods by league and season. All results are derived only from games from the second half of each regular season. 


## `results/roi/`
This folder contains all the CSV results and PNG figures of the favorite/underdog return on investment data by prediction method, league, bin, and season. All results are derived only from games from the second half of each regular season. 


### `results/binary_accuracy.csv`
This CSV file contains the binary accuracy of various model based prediction methods for each league. The 4 leagues are MLB, NBA, NFL, and NHL. Probabilistic predictions are converted to binary predictions using a 0.5 threshold. The columns of the results file are below.
- `league`: League name. 
- `ml`: Binary accuracy of predictions derived from moneyline scores.
- `bt`: Binary accuracy of predictions derived from Bradley-Terry rating algorithm.
- `hom_win_base`: Binary accuracy of predictions based on if home or away teams won more from first half of each respective regular season.


### `results/bookmaker_profit.csv`
This CSV file contains the summary statistics of the bookmaker profit percentages for each league. The 4 leagues are MLB, NBA, NFL, and NHL. The columns of the results file are below.
- `league`: League name.
- `min`: Minimum bookmaker profit percentage. 
- `q1`: Quartile 1 of bookmaker profit percentages.
- `median`: Median of bookmaker profit percentages.
- `q3`: Quartile 3 of bookmaker profit percentages.
- `max`: Maximum bookmaker profit percentage. 
- `lower_whisker`: Lower Tukey cutoff (`q1` - 1.5(`q3`-`q1`)) for bookmaker profit percentage outliers.
- `upper_whisker`: Upper Tukey cutoff (`q3` + 1.5(`q3`-`q1`)) for bookmaker profit percentage outliers. 


### `results/bookmaker_profit.png`
This PNG file contains 4 box plots. Each box plot displays the summary statistics for the moneyline bookamker profits for a sports league. The 4 leagues are MLB, NBA, NFL, and NHL. The statistics plotted are the min, first quartile, median, third quartile, max, and all outliers are represented as individual points.


### `results/brier_score.csv`
This CSV file contains the Brier scores of various model based prediction methods for each league. The 4 leagues are MLB, NBA, NFL, and NHL. The columns of the results file are below.
- `league`: League name.
- `ml`: Brier score of probabilistic predictions derived from moneyline scores.
- `bt`: Brier score of probabilistic predictions derived from Bradley-Terry rating algorithm.
- `hom_win_base`: Brier score of always predicting home team to win with proportion of first half of regular season games won by home team.


### `results/log_loss.csv`
This CSV file contains the log loss scores of various model based prediction methods for each league. The 4 leagues are MLB, NBA, NFL, and NHL. The columns of the results file are below.
- `league`: League name.
- `ml`: Log loss score of probabilistic predictions derived from moneyline scores.
- `bt`: Log loss score of probabilistic predictions derived from Bradley-Terry rating algorithm.
- `hom_win_base`: Log loss score of always predicting home team to win with proportion of first half of regular season games won by home team.


### `results/ml_seasonal_brier.csv`
This CSV file contains the Brier score of the moneyline based probabilistic predictions by season for each league. The 4 leagues are MLB, NBA, NFL, and NHL. The columns of the results file are below.
- `season`: The season as an integer, representing the year the season ended.
- `mlb_brier`: The Brier score of the moneyline based probabilistic predictions for the MLB by season.
- `nba_brier`: The Brier score of the moneyline based probabilistic predictions for the NBA by season.
- `nfl_brier`: The Brier score of the moneyline based probabilistic predictions for the NFL by season.
- `nhl_brier`: The Brier score of the moneyline based probabilistic predictions for the NHL by season.


### `results/ml_seasonal_brier.png`
This PNG file contains a line graph displaying the Brier score of the moneyline based probabilistic prediction for each league by season. The horizontal axis displays the season as an integer representing the year the season ended. The vertical axis is the Brier score.


### `results/seasonal_home_win.csv`
This CSV file contains the proportion of games won by the home team in the first half of each regular season for all leagues. The 4 leagues are MLB, NBA, NFL, and NHL. The columns of the results file are below.
- `season`: The season as an integer, representing the year the season ended. 
- `mlb`: The proportion of games won by the home team in the first half of the regular season for a specified season in the MLB.
- `nba`: The proportion of games won by the home team in the first half of the regular season for a specified season in the NBA.
- `nfl`: The proportion of games won by the home team in the first half of the regular season for a specified season in the NFL.
- `nhl`: The proportion of games won by the home team in the first half of the regular season for a specified season in the NHL.


### `results/seasonal_home_win.png`
This PNG file contains a line graph with a line for each league. Each league's line shows the proportion of games won by the home team in the first half of each leagues' regular season. The horizontal axis is the season as an integer representing the year the season ended. The vertical axis is the porbability.