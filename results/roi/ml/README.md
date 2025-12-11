# `results/roi/ml/`
This folder contains all CSV results and PNG figures of the moneyline favorite/underdog return on investment data by bin. All results are derived only from games from the second half of each regular season. 




### `results/roi/ml/{league}.csv`
This CSV file contains the return on investment of always betting on the favorite vs the return on investment of always betting on the underdog by bin for the specified league. The 4 leagues are MLB, NBA, NFL, and NHL. Games are grouped by prediction into 10 equally sized bins ([0, 0.1), [0,1, 0.2), etc). The favorite of the game is determined by the moneyline based prediction method. The ROI is calculated using the moneyline scores. The columns of the results file are below.
- `season`: The season as an integer, representing the year the season ended.
- `n`: The number of samples (games).
- `favorite_roi`: The ROI percentage of always betting on the favorite according to the moneyline based prediction method. 
- `underdog_roi`: The ROI percentage of always betting on the underdog according to the moneyline based prediction method.


### `results/roi/ml/{league}.png`
This PNG file contains a line graph for the moneyline based prediction method on the specified league. The 4 leagues are MLB, NBA, NFL, and NHL. There are 10 bins, and they are all equally sized. Each line graph shows the return on investment of always betting on the favorite and the return on investment of always betting on the underdog by bin. The favorite of the game is determined by the moneyline based probabilistic prediction method. The ROI is calculated using the moneyline scores.