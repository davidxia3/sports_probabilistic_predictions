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
    - This is used in the script `src/analysis/scraping/oddsportal_ml_scraper.py` to scrape the `moneyline_1` and `moneyline_2` data for each game.
    - It can also used as a unique ID for each game to assist with internal functions like matching.


### `oddsportal_ml_scraper.py`
To obtain the `moneyline_1` and `moneyline_2` values, each game's webpage must be accessed individually and calculated from there. For each league, the scraped data is saved to `raw_data/oddsportal_{league}.csv`.

On each game's individual webpage, OddsPortal only displays the raw moneylines from each bookmaker. The average of moneylines is computed in the following way. Instead of averaging the raw scores, we average the implied probabilities. For a positive moneyline score, the implied probability is 100 / (ML + 100). For a negative moneyline score, the implied probability is abs(ML) / (abs(ML) + 100). The implied probabilities are then averaged together. If the average probability is greater than 0.5, then the average moneyline is -100 * (P / (1 - P)). Otherwise, the average moneyline is 100 * ((1 - P) / P). 

Example:
- Bookmaker 1:
    - Team 1: -300.
    - Team 2: +100.
- Bookmaker 2:
    - Team 1: -400.
    - Team 2: +200.

- Bookmaker 1 implied probabilities:
    - Team 1: abs(-300) / (abs(-300) + 100) = 0.75.
    - Team 2: 100 / (100 + 100) = 0.50.
- Bookmaker 2 implied probabilities:
    - Team 1: abs(-400) / (abs(-400) + 100) = 0.80.
    - Team 2: 100 / (200 + 100) = 0.33

- Average implied probabilities:
    - Team 1: (0.75 + 0.80) / 2 = 0.775.
    - Team 2: (0.50 + 0.33) / 2 = 0.417.
    
- Convert to average moneylines:
    - Team 1: -100 * (0.775 / (1 - 0.775)) = -344.
    - Team 2: 100 ((1 - 0.417) / 0.417) = 140.