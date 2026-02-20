# `results/model_seasonal_brier/`
This folder contains all the CSV results and PDF/PNG figures of the Brier scores of various model based probabilistic prediction methods by league and season. 




### `{file_name_stem}_fmt.csv`
All files with the suffix `_fmt` in their file name are formatted versions of the file `{file_name_stem}.csv`. In the formatted version, all floating point values are rounded/padded to exactly 3 decimal points after the decimal. All other values are kept the same. If a figure is generated based on a CSV result file, then it is generated based on the original CSV file with full floating point precision. The formatted version of the CSV file is only for user inspection.


### `{league}.csv`
This CSV file contains the Brier score of various model based probabilistic predictions by season for the specified league. The 4 leagues are MLB, NBA, NFL, and NHL. The columns of each results file are below.
- `season`: The season as an integer, representing the year the season ended. 
- `ml_brier`: The Brier score of moneyline based probabilistic predictions.
- `bt_brier`: The Brier score of Bradley-Terry based probabilistic predictions.
- `home_bias_brier`: Brier scores of using the expanding home win rate (the proportion of home wins across all same-season games played prior to the current game) as the predicted probability.
- `coinflip_brier`: The Brier score of a constant 0.5 prediction for all games. 


### `{league}.pdf`
This PDF file contains a line graph for the specified league. The 4 leagues are MLB, NBA, NFL, and NHL. Each league's line graph displays the Brier score of various model's probabilistic predictions by season. The models used in each line graph are below.
- Moneyline: Brier scores of the moneyline based probabilistic predictions.
- Bradley-Terry: Brier scores of the Bradley-Terry based probabilistic predictions.
- Home Bias Coinflip: Brier scores of using the expanding home win rate (the proportion of home wins across all same-season games played prior to the current game) as the predicted probability.
- Coinflip: Brier scores of the baseline model that always predicts the home team to win with 0.5 probability.


### `{league}.png`
This PNG file is the same as the previous PDF file, except in PNG format.