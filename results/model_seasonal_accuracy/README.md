# `results/model_seasonal_accuracy/`
This folder contains all the CSV results and PDF/PNG figures of the binary accuracies of various model based probabilistic prediction methods by league and season.




### `{file_name_stem}_fmt.csv`
All files with the suffix `_fmt` in their file name are formatted versions of the file `{file_name_stem}.csv`. In the formatted version, all floating point values are rounded/padded to exactly 3 decimal points after the decimal. All other values are kept the same. If a figure is generated based on a CSV result file, then it is generated based on the original CSV file with full floating point precision. The formatted version of the CSV file is only for user inspection.


### `{league}.csv`
This CSV file contains the Binary accuracy of various model based probabilistic predictions by season for the specified league. The 4 leagues are MLB, NBA, NFL, and NHL. The columns of each results file are below.
- `season`: The season as an integer, representing the year the season ended. 
- `ml_accuracy`: The binary accuracy of moneyline based probabilistic predictions.
- `bt_accuracy`: The binary accuracy of Bradley-Terry based probabilistic predictions.
- `home_bias_accuracy`: The binary accuracy of using the expanding home win rate (the proportion of home wins across all same-season games played prior to the current game) as the predicted probability.
- `coinflip_accuracy`: The binary accuracy of a constant 0.5 prediction for all games. 


### `{league}.pdf`
This PDF file contains a line graph for the specified league. The 4 leagues are MLB, NBA, NFL, and NHL. Each league's line graph displays the binary accuracy of various model's probabilistic predictions by season. The models used in each line graph are below.
- Moneyline: Binary accuracy of the moneyline based probabilistic predictions.
- Bradley-Terry: Binary accuracy of the Bradley-Terry based probabilistic predictions.
- Home Bias Coinflip: Binary accuracy of using the expanding home win rate (the proportion of home wins across all same-season games played prior to the current game) as the predicted probability.
- Coinflip: Binary accuracy of the baseline model that always predicts the home team to win with 0.5 probability.


### `{league}.png`
This PNG file is the same as the previous PDF file, except in PNG format.