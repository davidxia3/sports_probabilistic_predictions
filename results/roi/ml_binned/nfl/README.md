# `results/roi/ml_binned/nfl/`
This folder contains all CSV results and PNG figures of the moneyline based favorite/underdog return on investment for the NFL by bin and season. All results are derived only from games from the second half of each regular season. 




### `bin_{bin}.csv`
This CSV file contains the return on investment of always betting on the favorite vs the return on investment of always betting on the underdog in each bin and by season for the NFL. Games are grouped by prediction into 10 equally sized bins ([0, 0.1), [0,1, 0.2), etc). For each bin, games are grouped by season. The favorite of the game is determined by the moneyline based prediction method. The favorite may disagree with the implied favorite from moneyline scores. However, the ROI is still calculated using the moneyline scores. The columns of the results file are below.
- `season`: The season as an integer, representing the year the season ended.
- `n`: The number of samples (games).
- `favorite_roi`: The ROI percentage of always betting on the favorite according to the moneyline based prediction method. 
- `underdog_roi`: The ROI percentage of always betting on the underdog according to the moneyline based prediction method.


### `bin_{bin}.png`
This PNG file contains a line graph of the moneyline based based prediction for the NFL and for the specified bin. There are 10 bins, and they are all equally sized. The line graph shows the return on investment of always betting on the favorite and the return on investment of always betting on the underdog by season. The favorite of the game is determined by the moneyline based probabilistic prediction method. The ROI is calculated using the moneyline scores. If the figure does not exist, that means there were no games in the NFL where the moneyline based prediction method had a prediction within the bin for any season. 