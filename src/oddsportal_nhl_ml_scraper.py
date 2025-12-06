from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
import pandas as pd



def scrape_nhl_ml(input_csv: Path, start_index: int=0) -> None:
    """
    Retrieves average of all bookmaker Home/Away moneylines from OddsPortal for NHL regular season games. 

    Args:
        input_csv (Path): Path object of CSV containing NHL games.
        start_index (int): Optional int object of index in CSV to start scraping at.
    
    Returns:
        None
    """

    # scraper configuration and settings
    chrome_options = Options()
    # chrome_options.add_argument("--headless=new")
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)



    df = pd.read_csv(input_csv)

    # initialize columns
    if "moneyline_1" not in df.columns:
        df["moneyline_1"] = pd.NA
        df["moneyline_1"] = df["moneyline_1"].astype("Int64")
    if "moneyline_2" not in df.columns:
        df["moneyline_2"] = pd.NA
        df["moneyline_2"] = df["moneyline_2"].astype("Int64")
    df = df["date", "season_type",
            "team_1", "team_2",
            "points_1", "points_2",
            "moneyline_1", "moneyline_2",
            "neutral", "game_url"]


    # iterate through each game
    for index, row in df.iterrows():
        if index < start_index:
            # start at start index, skipping all before
            continue

        # ignore non regular season games for efficiency
        if row["season_type"] != "Regular":
            continue

        # load OddsPortal page and navigate to Home/Away moneyline tab
        driver.get(f"{row['game_url']}#home-away;1")


        total_home_prob = 0
        total_away_prob = 0
        count = 0

        i = 1

        # if the game does not have a Home/Away moneyline, OddsPortal will automatically redirect to main 1x2 moneyline tab
        # need to check if we are scraping Home/Away moneyline
        has_home_away_line = False
        while True:
            time.sleep(1)
            try:
                ml_rows = driver.find_elements(By.CSS_SELECTOR, '[data-testid="over-under-expanded-row"]')
            except:
                pass
            
            if len(ml_rows) > 0 and "Home/Away" in driver.page_source:
                has_home_away_line = True
                break
            if i % 20 == 0:
                driver.refresh()
            if i > 60:
                print(f"invalid: {index}")
                break
            i = i + 1


        # no Home/Away moneyline, only has 1x2 line, skip
        if not has_home_away_line:
            continue


        try:
            count = len(ml_rows)
            # OddsPortal lists multiple bookmakers and their respective lines
            # need to calculate average
            for ml_row in ml_rows:
                odds_cells = ml_row.find_elements(By.CLASS_NAME, "odds-cell")
                # ensure exactly 2 moneyline values, indicating Home/Away moneyline
                assert len(odds_cells) == 2

                ml_1 = int(odds_cells[0].text)
                ml_2 = int(odds_cells[1].text)

        
                if ml_1 < 0:
                    prob_1 = abs(ml_1) / (abs(ml_1) + 100)
                else:
                    prob_1 = 100 / (abs(ml_1) + 100)

                if ml_2 < 0:
                    prob_2 = abs(ml_2) / (abs(ml_2) + 100)
                else:
                    prob_2 = 100 / (abs(ml_2) + 100)
            
                total_home_prob += prob_1
                total_away_prob += prob_2


            avg_home_prob = total_home_prob / count
            avg_away_prob = total_away_prob / count

            if avg_home_prob >= 0.5:
                avg_home_ml = -100 * (avg_home_prob / (1 - avg_home_prob))
            else:
                avg_home_ml = 100 * ((1 - avg_home_prob) / avg_home_prob)
            
            if avg_away_prob >= 0.5:
                avg_away_ml = -100 * (avg_away_prob / (1 - avg_away_prob))
            else:
                avg_away_ml = 100 * ((1 - avg_away_prob) / avg_away_prob)

            
            df.loc[index, "moneyline_1"] = round(avg_home_ml)
            df.loc[index, "moneyline_2"] = round(avg_away_ml)
        except Exception as e:
            print(e)
            print(f"error at index {index}")
            # save results from before fail
            df
            df.to_csv(input_csv,index=False)
            print(f"next start index: {index}")
            exit(1)

    
        # optional intermediary save
        if index % 100 == 0:
            print(f"next start index: {index}")
            df.to_csv(input_csv, index=False)



    # final save
    df.to_csv(input_csv, index=False)
    print("scraping complete")



if __name__ == "__main__":
    scrape_nhl_ml("raw_data/oddsportal_nhl.csv", 0)