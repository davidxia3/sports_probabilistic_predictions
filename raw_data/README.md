# `raw_data/`
This folder contains all the raw data scraped from OddsPortal.




### `raw_data/oddsportal_{league}.csv`
There are 4 leagues: MLB, NBA, NFL, and NHL. Each has a CSV file with game data. All MLB games from the 2008 season to the 2025 season are scraped. All NBA, NFL, and NHL games from the 2008-2009 season to the 2024-2025 season are scraped. The columns of each file are below.
- `date`: The date of the game. OddsPortal formats dates as `dd mmm yyyy`. 
- `season_type`: The season type/stage of the game (e.g. Play Offs, Regular). 
- `neutral`: A 1/0 boolean that represents if the game was played a neutral venue. 
- `team_1`: This value is the home team name if `neutral` is 1. Otherwise, this value is just the name of one of the teams. 
- `team_2`: This value is the away team name if `neutral` is 1. Otherwise, this value is just the name of one of the teams (never the same as `team_1`). 
- `points_1`: The number of points scored by `team_1`. 
- `points_2`: The number of points scored by `team_2`. 
- `moneyline_1`: The average moneyline score for `team_1`.
- `moneyline_2`: The average moneyline score for `team_2`. 
- `game_url`: The URL leading to the game's webpage.