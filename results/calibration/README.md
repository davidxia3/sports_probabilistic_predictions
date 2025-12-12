# `results/calibration/`
This folder contains all the CSV results and PNG figures of various prediction model calibrations. All results are derived only from games from the second half of each regular season. 




### `{file_name_stem}_fmt.csv`
All files with the suffix `_fmt` in their file name are formatted versions of the file `{file_name_stem}.csv`. In the formatted version, all floating point values are rounded/padded to exactly 3 decimal points after the decimal. All other values are kept the same. If a figure is generated based on a CSV result file, then it is generated based on the original CSV file with full floating point precision. The formatted version of the CSV file is only for user inspection.


### `{league}.csv`
The 4 leagues are MLB, NBA, NFL, and NHL. For each league, there is a corresponding CSV file. Each file has the following columns.
- `bin`: An integer 0-9 inclusive. These represent the 10 equally sized probability bins (e.g. bin 4 are all games in the league with home win probabilistic prediction between 40% and 49.99%).
- `ml_winrate`: The actual home win rate of all games where the moneyline based probabilistic prediction had home team win probability in the bin. (e.g. `ml_winrate` for bin 4 is the actual home winrate of all games where the moneyline predicted the home team to win with probability between 40% and 49.99%). NA value if there were no games where the moneyline's prediction was within the bin.
- `bt_winrate`: The actual home win rate of all games where the Bradley-Terry based probabilistic prediction had home team win probability in the bin. (e.g. `bt_winrate` for bin 4 is the actual home winrate of all games where the Bradley-Terry method predicted the home team to win with probability between 40% and 49.99%). NA value if there were no games where the Bradley-Terry prediction was within the bin.


### `{league}.png`
The 4 leagues are MLB, NBA, NFL, and NHL. For each league, there is a corresponding PNG file. Each file is a calibration plot of the moneyline based probabilistic prediction method and Bradley-Terry probabilistic prediction method against the perfect calibration reference. The horizontal axis represents the 10 equally sized probability bins of predicted home win probability. The vertical axis represents actual home win probability.