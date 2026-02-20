# `results/`
This folder contains all CSV results and PDF/PNG figures from the analysis of processed data.




## `calibration/`
This folder contains all the CSV results and PDF/PNG figures of various prediction model calibrations. All results are derived only from games from the second half of each regular season. 


## `home_predictions/`
This folder contains all the CSV results and PDF/PNG figures of the home team win prediction distributions. All results are derived only from games from the second half of each regular season. 


## `ml_teamwise_brier/`
This folder contains all CSV results and PDF/PNG figures of teamwise Brier scores and team winrates for each league. All results are derived only from games from the second half of each regular season.


## `model_seasonal_accuracy/`
This folder contains all the CSV results and PDF/PNG figures of the binary accuracies of various model based probabilistic prediction methods by league and season. 


## `model_seasonal_brier/`
This folder contains all the CSV results and PDF/PNG figures of the Brier scores of various model based probabilistic prediction methods by league and season.


## `roi/`
This folder contains all the CSV results and PDF/PNG figures of the favorite/underdog return on investment data by prediction method, league, bin, and season. All results are derived only from games from the second half of each regular season. 


### `{file_name_stem}_fmt.csv`
All files with the suffix `_fmt` in their file name are formatted versions of the file `{file_name_stem}.csv`. In the formatted version, all floating point values are rounded/padded to exactly 3 decimal points after the decimal. All other values are kept the same. If a figure is generated based on a CSV result file, then it is generated based on the original CSV file with full floating point precision. The formatted version of the CSV file is only for user inspection.


### `binary_accuracy.csv`
This CSV file contains the binary accuracy of various model based prediction methods for each league. The 4 leagues are MLB, NBA, NFL, and NHL. Probabilistic predictions are converted to binary predictions using a 0.5 threshold. The columns of the results file are below. 
- `league`: League name. 
- `ml`: Binary accuracy of predictions derived from moneyline scores.
- `bt`: Binary accuracy of predictions derived from Bradley-Terry rating algorithm.
- `home_win_base`: Binary accuracy of using the expanding home win rate (the proportion of home wins across all same-season games played prior to the current game) as the predicted probability.


### `binary_accuracy.pdf`
This PDF file contains a grouped bar chart with 4 groups of 4 bars. The groups are the 4 leagues: MLB, NBA, NFL, and NHL. Each league has 4 bars: one for each of the prediction models. The bars display the binary accuracy of the prediction model for by league.


### `binary_accuracy.png`
This PNG file is the same as the previous PDF file, except in PNG format.


### `binary_accuracy_T.pdf`
This PDF file contains a grouped bar chart with 3 groups of 4 bars. The groups are the 3 prediction methods. Each method has 4 bars: one for each of the leagues. The bars display the binary accuracy of the prediction model for by league.


### `binary_accuracy_T.png`
This PNG file is the same as the previous PDF file, except in PNG format.


### `bookmaker_profit.csv`
This CSV file contains the summary statistics of the bookmaker profit percentages for each league. The 4 leagues are MLB, NBA, NFL, and NHL. The columns of the results file are below. Results are derived only from games from the second half of each regular season.
- `league`: League name.
- `min`: Minimum bookmaker profit percentage. 
- `q1`: Quartile 1 of bookmaker profit percentages.
- `median`: Median of bookmaker profit percentages.
- `q3`: Quartile 3 of bookmaker profit percentages.
- `max`: Maximum bookmaker profit percentage. 
- `lower_whisker`: Lower Tukey cutoff (`q1` - 1.5(`q3`-`q1`)) for bookmaker profit percentage outliers.
- `upper_whisker`: Upper Tukey cutoff (`q3` + 1.5(`q3`-`q1`)) for bookmaker profit percentage outliers. 
- `average`: Mean of bookmaker profit percentages.


### `bookmaker_profit_avg.pdf`
This PDF file contains a bar chart with 4 bars. Each bar displays the average moneyline bookamker profit for a sports league. The 4 leagues are MLB, NBA, NFL, and NHL. Results are derived only from games from the second half of each regular season.


### `bookmaker_profit_avg.png`
This PNG file is the same as the previous PDF file, except in PNG format.


### `bookmaker_profit_dist.pdf`
This PDF file contains 4 box plots. Each box plot displays the summary statistics for the moneyline bookamker profits for a sports league. The 4 leagues are MLB, NBA, NFL, and NHL. The statistics plotted are the min, first quartile, median, third quartile, max, and all outliers are represented as individual points. Results are derived only from games from the second half of each regular season.


### `bookmaker_profit_dist.png`
This PNG file is the same as the previous PDF file, except in PNG format.


### `brier_score.csv`
This CSV file contains the Brier scores of various model based prediction methods for each league. The 4 leagues are MLB, NBA, NFL, and NHL. The columns of the results file are below.
- `league`: League name.
- `ml`: Brier score of probabilistic predictions derived from moneyline scores.
- `bt`: Brier score of probabilistic predictions derived from Bradley-Terry rating algorithm.
- `home_win_base`: Brier score of using the expanding home win rate (the proportion of home wins across all same-season games played prior to the current game) as the predicted probability.


### `brier_score.pdf`
This PDF file contains a grouped bar chart with 4 groups of 4 bars. The groups are the 4 leagues: MLB, NBA, NFL, and NHL. Each league has 4 bars: one for each of the prediction models. The bars display the Brier scores of the prediction model for by league.


### `brier_score.png`
This PNG file is the same as the previous PDF file, except in PNG format.


### `home_win_seasonal.csv`
This CSV file contains the proportion of games won by the home team in each regular season for all leagues. The 4 leagues are MLB, NBA, NFL, and NHL. The columns of the results file are below.
- `season`: The season as an integer, representing the year the season ended. 
- `mlb`: The proportion of games won by the home team in the first half of the regular season for a specified season in the MLB.
- `nba`: The proportion of games won by the home team in the first half of the regular season for a specified season in the NBA.
- `nfl`: The proportion of games won by the home team in the first half of the regular season for a specified season in the NFL.
- `nhl`: The proportion of games won by the home team in the first half of the regular season for a specified season in the NHL.


### `home_win_seasonal.pdf`
This PDF file contains a line graph with a line for each league. Each league's line shows the proportion of games won by the home team in each leagues' regular season. The horizontal axis is the season as an integer representing the year the season ended. The vertical axis is the porbability.


### `home_win_seasonal.png`
This PNG file is the same as the previous PDF file, except in PNG format.


### `home_win.csv`
This CSV file contains the proportion of games won by the home team in each regular season for all leagues. The 4 leagues are MLB, NBA, NFL, and NHL. The columns of the results file are below.


### `home_win.pdf`
This PDF file contains a bar graph with a bar for each league. Each league's bar shows the proportion of games won by the home team in each leagues' regular season.


### `home_win.png`
This PNG file is the same as the previous PDF file, except in PNG format.


### `log_loss.csv`
This CSV file contains the log loss scores of various model based prediction methods for each league. The 4 leagues are MLB, NBA, NFL, and NHL. The columns of the results file are below.
- `league`: League name.
- `ml`: Log loss score of probabilistic predictions derived from moneyline scores.
- `bt`: Log loss score of probabilistic predictions derived from Bradley-Terry rating algorithm.
- `home_win_base`: Log loss of using the expanding home win rate (the proportion of home wins across all same-season games played prior to the current game) as the predicted probability.


### `ml_seasonal_brier.csv`
This CSV file contains the Brier score of the moneyline based probabilistic predictions by season for each league. The 4 leagues are MLB, NBA, NFL, and NHL. The columns of the results file are below. Results are derived only from games from the second half of each regular season.
- `season`: The season as an integer, representing the year the season ended.
- `mlb_brier`: The Brier score of the moneyline based probabilistic predictions for the MLB by season.
- `nba_brier`: The Brier score of the moneyline based probabilistic predictions for the NBA by season.
- `nfl_brier`: The Brier score of the moneyline based probabilistic predictions for the NFL by season.
- `nhl_brier`: The Brier score of the moneyline based probabilistic predictions for the NHL by season.


### `ml_seasonal_brier.pdf`
This PDF file contains a line graph displaying the Brier score of the moneyline based probabilistic prediction for each league by season. The horizontal axis displays the season as an integer representing the year the season ended. The vertical axis is the Brier score. Results are derived only from games from the second half of each regular season.


### `ml_seasonal_brier.png`
This PNG file is the same as the previous PDF file, except in PNG format.