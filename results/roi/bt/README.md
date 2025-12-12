# `results/roi/bt/`
This folder contains all CSV results and PNG figures of the Bradley-Terry favorite/underdog return on investment data by bin. All results are derived only from games from the second half of each regular season. 




### `{file_name_stem}_fmt.csv`
All files with the suffix `_fmt` in their file name are formatted versions of the file `{file_name_stem}.csv`. In the formatted version, all floating point values are rounded/padded to exactly 3 decimal points after the decimal. All other values are kept the same. If a figure is generated based on a CSV result file, then it is generated based on the original CSV file with full floating point precision. The formatted version of the CSV file is only for user inspection.


### `{league}.csv`
This CSV file contains the return on investment of always betting on the favorite vs the return on investment of always betting on the underdog by bin for the specified league. The 4 leagues are MLB, NBA, NFL, and NHL. Games are grouped by prediction into 10 equally sized bins ([0, 0.1), [0,1, 0.2), etc). The favorite of the game is determined by the Bradley-Terry prediction method. The favorite may disagree with the implied favorite from moneyline scores. However, the ROI is still calculated using the moneyline scores. The columns of the results file are below.
- `season`: The season as an integer, representing the year the season ended.
- `n`: The number of samples (games).
- `favorite_roi`: The ROI percentage of always betting on the favorite according to the Bradley-Terry prediction method. 
- `underdog_roi`: The ROI percentage of always betting on the underdog according to the Bradley-Terry prediction method.


### `{league}.png`
This PNG file contains a line graph for the Bradley-Terry prediction method on the specified league. The 4 leagues are MLB, NBA, NFL, and NHL. There are 10 bins, and they are all equally sized. Each line graph shows the return on investment of always betting on the favorite and the return on investment of always betting on the underdog by bin. The favorite of the game is determined by the Bradley-Terry probabilistic prediction method. The favorite may disagree with the implied favorite from moneyline scores. However, the ROI is still calculated using the moneyline scores.