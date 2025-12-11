# `results/model_seasonal_brier/`
This folder contains all the CSV results and PNG figures of the Brier scores of various model based probabilistic prediction methods by league and season. All results are derived only from games from the second half of each regular season. 




### `{league}.csv`
This CSV file contains the Brier score of various model based probabilistic predictions by season for the specified league. The 4 leagues are MLB, NBA, NFL, and NHL. The columns of each results file are below.
- `season`: The season as an integer, representing the year the season ended. 
- `ml_brier`: The Brier score of moneyline based probabilistic predictions.
- `bt_brier`: The Brier score of Bradley-Terry based probabilistic predictions.
- `home_bias_brier`: The Brier score of predictions using the home team win probability from the first half of each regular season.
- `coinflip_brier`: The Brier score of a constant 0.5 prediction for all games. 


### `{league}.png`
This PNG file contains a line graph for the specified league. The 4 leagues are MLB, NBA, NFL, and NHL. Each league's line graph displays the Brier score of various model's probabilistic predictions by season. The models used in each line graph are below.
- Moneyline: Brier scores of the moneyline based probabilistic predictions.
- Bradley-Terry: Brier scores of the Bradley-Terry based probabilistic predictions.
- Home Bias Coinflip: Brier scores of the baseline model that predicts the home team to win with the proportion of first half regular season games won by the home team. 
- Coinflip: Brier scores of the baseline model that always predicts the home team to win with 0.5 probability.