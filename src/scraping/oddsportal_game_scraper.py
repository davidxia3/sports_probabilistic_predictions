from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv
import time
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path




def scrape_league_games(sport: str, seasons: list[str], output_file: Path) -> None:
    """
    Scrapes all game data for league from OddsPortal.

    Args:
        sport (str): String object of sport name compatible with OddsPortal (e.g. "american-football").
        seasons (list[str]): List object of strings of season names compatible with OddsPortal (e.g. "nfl-2024-2025).
        output_file (Path): Path object of CSV file where game data will be saved.

    Returns
        None
    """

    # scraper configuration and settings
    chrome_options = Options()
    # chrome_options.add_argument("--headless=new")
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    total_data = []




    # default values
    date = "31 Dec 1999"
    season_type = "Regular"




    # iterate through each season
    for season in seasons:
        print(f"scraping season {season}")
        driver.get(f"https://www.oddsportal.com/{sport}/usa/{season}/results")
        
        
        
        
        # find number of pages for each season
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "pagination-link"))
        )
        pagination = driver.find_elements(By.CLASS_NAME, "pagination-link")
        last_page = int(pagination[-2].text)




        # iterate through each page for league
        curr_page = 1
        while True:
            print(f"scraping page {curr_page}")
            # reset by scrolling to top and ensure top of webpage is loaded
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(4)




            # scroll to bottom to load all rows
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height



            # determine number of event rows on page, should be 50 for all pages except last    
            if curr_page != last_page:
                for i in range(50):
                    try:
                        events = driver.find_elements(By.CLASS_NAME, "eventRow")
                        if len(events) == 50:
                            print(i)
                            break
                        time.sleep(2)
                    except:
                        pass
                    if i == 49:
                        print(f"ERROR: only {len(events)} on page {curr_page}")
                        exit(1)
            else:
                time.sleep(15)
                events = driver.find_elements(By.CLASS_NAME, "eventRow")




            # iterate through event rows
            for event in events:
                # load new values of date and header if they exist
                try:
                    # presence of date header means new date
                    date_header = event.find_element(By.CSS_SELECTOR, '[data-testid="date-header"]')
                    try:
                        date = date_header.text.split("-")[0].strip()
                    except:
                        date = "31 Dec 1999"
                    
                    # date header can also contain season type, but if not, it is regular season
                    try:
                        season_type = date_header.text.split("-", 1)[1].strip()
                    except:
                        season_type = "Regular"
                except:
                    # no date header, so same date and season type as last row
                    pass



                # load game data from event row
                game_data = {}
                game = event.find_element(By.CSS_SELECTOR, '[data-testid="game-row"]')
                game_info = game.text.splitlines()




                if "canc." in game_info:
                    # game was cancelled, skip
                    continue




                # check if game is played at neutral location
                neutral = False
                try:
                    # check if has exclamation warning
                    exclamation = event.find_element(By.CSS_SELECTOR, "div.bg-event-exclamation")
                    html_before = exclamation.get_attribute("outerHTML")

                    # execute java script to hover
                    java_script = """
                    var evObj = document.createEvent('MouseEvents');
                    evObj.initMouseEvent(\"mouseover\",true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
                    arguments[0].dispatchEvent(evObj);
                    """
                    driver.execute_script(java_script, exclamation)

                    # make sure hover was successful
                    html_after = exclamation.get_attribute("outerHTML")
                    if html_before == html_after:
                        print("ERROR: hover not working")
                        exit(1)

                    if "Neutral location" in html_after:
                        neutral = True
                except:
                    # no exclamation warning, not at neutral location
                    pass




                # isolate and split info in each row
                team_1_idx = 1
                team_2_idx = 5
                points_1_idx = 2
                points_2_idx = 4
                moneyline_1_idx = 6
                moneyline_2_idx = 7
                if game_info[moneyline_1_idx] == "OT" or game_info[moneyline_1_idx] == "pen.":
                    moneyline_1_idx += 1
                    moneyline_2_idx += 1
                if game_info[moneyline_1_idx] == "FRO":
                    moneyline_1_idx += 1
                    moneyline_2_idx += 1
                if moneyline_2_idx >= len(game_info):
                    print(f"ERROR: game data unaligned")
                    continue



                # store data
                game_data["date"] = date
                game_data["season_type"] = season_type
                game_data["neutral"] = 1 if neutral else 0
                game_data["team_1"] = game_info[team_1_idx]
                game_data["team_2"] = game_info[team_2_idx]
                game_data["points_1"] = game_info[points_1_idx]
                game_data["points_2"] = game_info[points_2_idx]

                # oddsportal default line for hockey games is 1x2 not home/away
                # home/away lines need to be scraped separately
                if sport != "hockey":
                    game_data["moneyline_1"] = game_info[moneyline_1_idx]
                    game_data["moneyline_2"] = game_info[moneyline_2_idx]
                try:
                    game_data["game_url"] = game.find_elements(By.TAG_NAME, "a")[-4].get_attribute("href")
                except Exception as e:
                    print(f"ERROR: game_url: {e}")
                    pass
                total_data.append(game_data)




            # finished with season
            if curr_page == last_page:
                break




            # not finished, so click next button to go to next page
            try:
                next_btn = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//a[contains(@class, 'pagination-link') and text()='Next']")
                    )
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
                driver.execute_script("window.scrollBy(0, -1000);")
                time.sleep(4)
                next_btn.click()
                curr_page += 1
                time.sleep(8)
            except TimeoutException:
                # no next button found
                print(f"ERROR: no next button found on page {curr_page}")
                exit(1)



        # optional intermediary save point
        # with open(f"{season.replace('-', '_')}.csv", mode='w', newline='', encoding='utf-8') as csv_file:
        #     fieldnames = ["date", "season_type", "team_1", "team_2", "points_1", "points_2", "moneyline_1", "moneyline_2", "neutral", "game_url"]
        #     
        #     # oddsportal default line for hockey games is 1x2 not home/away
        #     # home/away lines need to be scraped separately
        #     if sport == "hockey":
        #         field_names = ["date", "season_type", "team_1", "team_2", "points_1", "points_2", "neutral", "game_url"]
        #     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        #     writer.writeheader()
        #     for game in total_data:
        #         writer.writerow(game)








    # save final data
    with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ["date", "season_type", "neutral", "team_1", "team_2", "points_1", "points_2", "moneyline_1", "moneyline_2", "game_url"]
        
        # oddsportal default line for hockey games is 1x2 not home/away
        # home/away lines need to be scraped separately
        if sport == "hockey":
            fieldnames = ["date", "season_type", "neutral", "team_1", "team_2", "points_1", "points_2", "game_url"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for game in total_data:
            writer.writerow(game)








if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        league_to_sport_dict = {
            "mlb": "baseball",
            "nba": "basketball",
            "nfl": "american-football",
            "nhl": "hockey"
        }
        league_to_seasons_dict = {
            "mlb": [f"{league}-{year}" for year in range(2025, 2007, -1)],
            "nba": [f"{league}-{year}-{year+1}" for year in range(2024, 2007, -1)],
            "nfl": [f"{league}-{year}-{year+1}" for year in range(2024, 2007, -1)],
            "nhl": [f"{league}-{year}-{year+1}" for year in range(2024, 2007, -1)]
        }
        scrape_league_games(sport=league_to_sport_dict[league],
                            seasons=league_to_seasons_dict[league],
                            output_file=f"raw_data/oddsportal_{league}.csv")