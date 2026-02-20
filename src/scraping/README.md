# `src/analysis/scraping/`
This folder contains all the Python scripts for scraping raw data from OddsPortal website. OddsPortal is a website with archived games and betting results.




### `oddsportal_scraper.py`
This Python script scrapes game data from OddsPortal. All MLB games from the 2009 season to the 2025 season are scraped. All NBA, NFL, and NHL games from the 2008-2009 season to the 2024-2025 season are scraped. For each league, the scraped raw data is saved to `raw_data/oddsportal_{league}.csv`. For each game, the script scrapes the following features.
- `date`: The date of the game. OddsPortal formats dates as `dd mmm yyyy`. 
- `season_type`: The season type/stage of the game (e.g. Play Offs, Regular). 
- `neutral`: A 1/0 boolean that represents if the game was played a neutral venue. 
- `team_1`: This value is the home team name if `neutral` is 1. Otherwise, this value is just the name of one of the teams. 
- `team_2`: This value is the away team name if `neutral` is 1. Otherwise, this value is just the name of one of the teams (never the same as `team_1`). 
- `points_1`: The number of points scored by `team_1`. 
- `points_2`: The number of points scored by `team_2`. 
- `game_url`: The URL leading to the game's webpage.
    - This is used in the script `src/analysis/scraping/oddsportal_ml_scraper.py` to scrape the `moneylines` data for each game.
    - It can also used as a unique ID for each game to assist with internal functions like matching.


### `oddsportal_ml_scraper.py`
A game's `moneylines` value is a list of pairs. Each pair represents a bookmaker's moneyline for the game. The first value in each pair is the home moneyline. The second value in each pair is the away moneyline. To fit a list into a CSV cell, the list is converted and stored as a string object. To obtain the `moneylines` column values, each game's webpage must be accessed individually and calculated from there. For each league, the scraped data is saved to `raw_data/oddsportal_{league}.csv`.