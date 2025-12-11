# `src/graphing/`
This folder contains all the scripts for graphing and plotting the results into figures. All figures show results only from games from the second half of each regular season. 




### `src/graphing/bookmaker_profit.py`
This Python script plots 4 box plots. Each box plot displays the summary statistics for the moneyline bookamker profits for a sports league. The 4 leagues are MLB, NBA, NFL, and NHL. The statistics plotted are the min, first quartile, median, third quartile, max, and all outliers are represented as individual points. The figure is saved to `results/bookmaker_profit.png`. 


### `src/graphing/calibration.py`
This Python script plots the calibration plot displaying the adequecy of moneyline based and Bradley-Terry based probabilistic predictions. The horizontal axis shows 10 equal-width home probabilitistic prediction bins. The vertical axis is the actual home win rate of games in those bins. Points close to each horizontal side may be missing, which indicate no games the home team predicted with probability in that bin. For each league, the figure is saved to `results/calibration/{league}.png`. 


### `src/graphing/home_predictions_box.py`
This Python script plots 4 box plots for each specified prediction method. The two prediction methods are moneyline based and Bradley-Terry based. Each box plot displays the summary statistics for the prediction method's home team win probabilities for a specific league. The 4 leagues are MLB, NBA, NFL, and NHL. The statistics plotted are the min, first quartile, median, third quartile, max, and all outliers are represented as individual points. For each prediction method, the figure is saved to `results/home_predictions/{method}_box.png`. 


### `src/graphing/home_predictions_hist.py`
This Python script plots 4 histograms for each specified prediction method. The two prediction methods are moneyline based and Bradley-Terry based. Each histogram displays the distribution of the prediction method's home team win probabilities for a specific league. The 4 leagues are MLB, NBA, NFL, and NHL. There are 30 equal-width bins used for each league's histogram. The density is used instead of the raw counts because each league has a different total count of games. For each prediction method and league, the figure is saved to `results/home_predictions/{method}_{league}_hist.png`. 


### `src/graphing/ml_seasonal_brier.py`
This Python script plots a line graph displaying the Brier score of the moneyline based probabilistic prediction for each league by season. The horizontal axis displays the season as an integer representing the year the season ended. The vertical axis is the Brier score. The figure is saved to `results/ml_seasonal_brier.png`. 


### `src/ml_teamwise_brier.py`
This Python script plots a bar chart for each league. Each league's bar chart displays the Brier score of the moneyline based probabilistic predictions for each team in the league. The Brier score of a team is the Brier score of all games involving the team. The bars are sorted in ascending order. For each league, the figure is saved to `results/ml_teamwise_brier/{league}.png`.


### `src/model_seasonal_brier.py`
This Python script plots a line graph for each league. Each league's line graph displays the Brier score of various model's probabilistic predictions by season. For each league, the figure is saved to `results/model_seasonal_brier/{league}.png`. The models used in each line graph are below.
- Moneyline: Brier scores of the moneyline based probabilistic predictions.
- Bradley-Terry: Brier scores of the Bradley-Terry based probabilistic predictions.
- Home Bias Coinflip: Brier scores of the baseline model that predicts the home team to win with the proportion of first half regular season games won by the home team. 
- Coinflip: Brier scores of the baseline model that always predicts the home team to win with 0.5 probability. 


### `src/roi_binned.py`
This Python script produces a line graph for each prediction method, league, and bin. The two prediction methods are moneyline based and Bradley-Terry based. The 4 leagues are MLB, NBA, NFL, and NHL. There are 10 bins for each prediction method and league, and they are all equally sized. Each line graph shows the return on investment of always betting on the favorite and the return on investment of always betting on the underdog by season. The favorite of the game is determined by the specified probabilistic prediction method. If the specified probabilistic prediction method is not the moneyline, then the favorite may disagree with the implied favorite from moneyline scores. However, the ROI is always calculated using the moneyline scores, regardless of specified prediction method.

Example:
- Home team: ML = -250.
- Away team: ML = +200.
- Bradley-Terry prediction: 0.4.
The moneyline scores states that the home team is the favorite. However, because the Bradley-Terry based prediction is less than 0.5, the favorite according to Bradley-Terry is the away team. If the game resulted in the home team winning, the ROI of betting on the favorite would be -100% (all investment lost). If the game resulted in the away team winning, the ROI of betting on the favorite would be 200%.

For each prediction method, league, and bin, the figure is saved to `results/roi/{method}_binned/{league}/bin_{bin}.png`. If the figure does not exist, that means there were no games in the league where the prediction method had a prediction within the bin for any season. 


### `src/roi.py`
This Python script produces a line graph for each prediction method and league. The two prediction methods are moneyline based and Bradley-Terry based. The 4 leagues are MLB, NBA, NFL, and NHL. There are 10 bins for each prediction method and league, and they are all equally sized. Each line graph shows the return on investment of always betting on the favorite and the return on investment of always betting on the underdog by bin. The favorite of the game is determined by the specified probabilistic prediction method. If the specified probabilistic prediction method is not the moneyline, then the favorite may disagree with the implied favorite from moneyline scores. However, the ROI is always calculated using the moneyline scores, regardless of specified prediction method.

Example:
- Home team: ML = -250.
- Away team: ML = +200.
- Bradley-Terry prediction: 0.4.
The moneyline scores states that the home team is the favorite. However, because the Bradley-Terry based prediction is less than 0.5, the favorite according to Bradley-Terry is the away team. If the game resulted in the home team winning, the ROI of betting on the favorite would be -100% (all investment lost). If the game resulted in the away team winning, the ROI of betting on the favorite would be 200%.

For each prediction method and league, the figure is saved to `results/roi/{method}/{league}.png`.


### `src/graphing/seasonal_home_win.py`
This Python script plots a line graph with a line for each league. Each league's line shows the proportion of games won by the home team in the first half of each leagues' regular season. The horizontal axis is the season as an integer representing the year the season ended. The vertical axis is the porbability. The figure is saved to `results/seasonal_home_win.png`.


### `src/graphing/teamwise_winrates_corr.py`
This Python script plots the scatter plot of teams for each league. For the teams in each league, the horizontal axis represents the absolute difference between the team's winrate and 50%. Team's on the left had winrates close to 50% and teams on the right had winrates much lower than 50% or winrates much higher than 50%. The vertical axis represents the Brier score of all games involving the team. The script also plots the least squares line with its equation, as well as the p-value of the linear relationship between the absolute difference between a team's winrate and 50% with the Brier score. For each league, the figure is saved to `results/ml_teamwise_brier/{league}_winrates.png`.