# `results/home_predictions/`
This folder contains all the CSV results and PNG figures of the home team win prediction distributions. All results are derived only from games from the second half of each regular season. 




### `bt_box.csv`
This CSV file contains the summary statistics of the Bradley-Terry based home team win probability distribution for each league. The 4 leagues are MLB, NBA, NFL, and NHL. The columns of the CSV file are below.
- `league`: League name.
- `min`: Minimum Bradley-Terry predicted home team win probability. 
- `q1`: Quartile 1 of Bradley-Terry predicted home team win probabilities.
- `median`: Median of Bradley-Terry predicted home team win probabilities.
- `q3`: Quartile 3 of Bradley-Terry predicted home team win probabilities.
- `max`: Maximum Bradley-Terry predicted home team win probability.
- `lower_whisker`: Lower Tukey cutoff (`q1` - 1.5(`q3`-`q1`)) for Bradley-Terry predicted home team win probability outliers.
- `upper_whisker`: Upper Tukey cutoff (`q3` + 1.5(`q3`-`q1`)) for Bradley-Terry predicted home team win probability outliers. 


### `bt_box.png`
This PNG file contains 4 box plots for the Bradley-Terry predicted home team win probability distribution. Each box plot displays the summary statistics for the prediction method's home team win probabilities for a specific league. The 4 leagues are MLB, NBA, NFL, and NHL. The statistics plotted are the min, first quartile, median, third quartile, max, and all outliers are represented as individual points.


### `bt_{league}_hist.csv`
This CSV file contains the density histogram statistics of the Bradley-Terry based probabilistic predictions for the specified league. The 4 leagues are MLB, NBA, NFL, and NHL. The histogram is split into 30 equally width bins spanning the entire probability range ([0,1]). The density is used instead of raw counts as different leagues have different total counts. The columns of each results file are below.
- `bin_left`: Left boundary of probability bin.
- `bin_right`: Right boundary of probability bin.
- `bin_center`: Average of `bin_left` and `bin_right`.
- `density`: Density of league games with probabilistic prediction between `bin_left` and `bin_right`. 


### `bt_{league}_hist.png`
This PNG file contains a histogram for the Bradley-Terry based home team win probability distribution. The 4 leagues are MLB, NBA, NFL, and NHL. There are 30 equal-width bins used for each league's histogram. The density is used instead of the raw counts because each league has a different total count of games.


### `ml_box.csv`
This CSV file contains the summary statistics of the moneyline based home team win probability distribution for each league. The 4 leagues are MLB, NBA, NFL, and NHL. The columns of the CSV file are below.
- `league`: League name.
- `min`: Minimum moneyline predicted home team win probability. 
- `q1`: Quartile 1 of moneyline predicted home team win probabilities.
- `median`: Median of moneyline predicted home team win probabilities.
- `q3`: Quartile 3 of moneyline predicted home team win probabilities.
- `max`: Maximum moneyline predicted home team win probability.
- `lower_whisker`: Lower Tukey cutoff (`q1` - 1.5(`q3`-`q1`)) for moneyline predicted home team win probability outliers.
- `upper_whisker`: Upper Tukey cutoff (`q3` + 1.5(`q3`-`q1`)) for moneyline predicted home team win probability outliers. 


### `ml_box.png`
This PNG file contains 4 box plots for the moneyline predicted home team win probability distribution. Each box plot displays the summary statistics for the prediction method's home team win probabilities for a specific league. The 4 leagues are MLB, NBA, NFL, and NHL. The statistics plotted are the min, first quartile, median, third quartile, max, and all outliers are represented as individual points.


### `ml_{league}_hist.csv`
This CSV file contains the density histogram statistics of the moneyline based probabilistic predictions for the specified league. The 4 leagues are MLB, NBA, NFL, and NHL. The histogram is split into 30 equally width bins spanning the entire probability range ([0,1]). The density is used instead of raw counts as different leagues have different total counts. The columns of each results file are below.
- `bin_left`: Left boundary of probability bin.
- `bin_right`: Right boundary of probability bin.
- `bin_center`: Average of `bin_left` and `bin_right`.
- `density`: Density of league games with probabilistic prediction between `bin_left` and `bin_right`. 


### `ml_{league}_hist.png`
This PNG file contains a histogram for the moneyline based home team win probability distribution. The 4 leagues are MLB, NBA, NFL, and NHL. There are 30 equal-width bins used for each league's histogram. The density is used instead of the raw counts because each league has a different total count of games.