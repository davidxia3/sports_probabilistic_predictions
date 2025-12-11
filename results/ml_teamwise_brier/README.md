# `results/ml_teamwise_brier/`
This folder contains all CSV results and PNG figures of teamwise Brier scores and team winrates for each league. All results are derived only from games from the second half of each regular season. 




### `{league}_winrates.csv`
This CSV file contains the winrates for each team in the specified league. The 4 leagues are MLB, NBA, NFL, and NHL. The columns of the results file are below.
- `team`: Team abbreviation.
- `winrate`: Team's winrate as a percentage.  


### `{league}_winrates.png`
This PNG file contains the scatter plot of teams for the specified league. For the teams in the league, the horizontal axis represents the absolute difference between the team's winrate and 50%. Team's on the left had winrates close to 50% and teams on the right had winrates much lower than 50% or winrates much higher than 50%. The vertical axis represents the Brier score of all games involving the team. The script also plots the least squares line with its equation, as well as the p-value of the linear relationship between the absolute difference between a team's winrate and 50% with the Brier score.


### `{league}.csv`
This CSV file contains the Brier score of the moneyline based probabilistic predictions by team for the specified league. The 4 leagues are MLB, NBA, NFL, and NHL. A team's Brier score is the Brier score the moneyline based prediction for all games involving the team, regardless if the team is home or away. The columns of each results file are below.
- `team`: The team's abbreviation.
- `brier_score`: The moneyline based Brier score of all games involving the team.


### `{league}.png`
This PNG file plots a bar chart for the specified league. The bar chart displays the Brier score of the moneyline based probabilistic predictions for each team in the league. The Brier score of a team is the Brier score of all games involving the team. The bars are sorted in ascending order.