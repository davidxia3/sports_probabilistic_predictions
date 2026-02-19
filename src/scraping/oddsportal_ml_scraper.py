from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
import pandas as pd



def scrape_ml(input_csv: Path, start_index: int=0) -> None:
    """
    Retrieves average of all bookmaker Home/Away moneylines from OddsPortal for regular season games. 

    Args:
        input_csv (Path): Path object of CSV containing league games.
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
    if "moneylines" not in df.columns:
        df["moneylines"] = [[] for _ in range(len(df))]
        df["moneylines"] = df["moneylines"].astype("object")
    df = df[["date", "season_type", "neutral",
            "team_1", "team_2",
            "points_1", "points_2",
            "moneylines",
            "game_url"]]


    # iterate through each game
    for index, row in df.iterrows():
        if index < start_index:
            # start at start index, skipping all before
            continue


        # optional intermediary save
        if index % 50 == 0:
            print(f"next start index: {index}")
            df.to_csv(input_csv, index=False)
            
            
        # ignore non regular season games for efficiency
        if row["season_type"] != "Regular":
            continue

        # load OddsPortal page and navigate to Home/Away moneyline tab
        driver.get(f"{row['game_url']}#home-away;1")




        # if the game does not have a Home/Away moneyline, OddsPortal will automatically redirect to main 1x2 moneyline tab
        # need to check if we are scraping Home/Away moneyline
        i = 1
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
            if i % 4 == 0:
                driver.refresh()
            if i > 10:
                print(f"invalid: {index}")
                break
            i = i + 1


        # no Home/Away moneyline, only has 1x2 line, skip
        if not has_home_away_line:
            continue

        moneylines = []
        # OddsPortal lists multiple bookmakers and their respective lines
        for ml_row in ml_rows:
            try:
                odds_cells = ml_row.find_elements(By.CLASS_NAME, "odds-cell")
                # ensure exactly 2 moneyline values, indicating Home/Away moneyline
                assert len(odds_cells) == 2

                ml_1 = int(odds_cells[0].text)
                ml_2 = int(odds_cells[1].text)

        
                moneylines.append((ml_1,ml_2))
            except Exception as e:
                print(e)
                print(f"error at index {index}")


        df.at[index, "moneylines"] = moneylines

    



    # final save
    df.to_csv(input_csv, index=False)
    print("scraping complete")



if __name__ == "__main__":
    scrape_ml("", 0)