from pathlib import Path
import pandas as pd
import json




def format_date(raw_date_str: str) -> str:
    """
    Converts date from "dd mon yyyy" format to "yyyy-mm-dd".

    Args: 
        raw_date_str (str) : String object of date in "dd mon yyyy" format.

    Returns:
        str: String object of date in "yyyy-mm-dd" format.
    """

    # dictionary that maps month abbreviations to their corresponding number string
    month_abbr_dict = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04",
        "may": "05", "jun": "06", "jul": "07", "aug": "08",
        "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }
    day_str, month_abbr, year_str = raw_date_str.split()
    return f"{year_str}-{month_abbr_dict[month_abbr.lower()]}-{day_str}"




def is_regular(season_type: str) -> int:
    """
    Returns whether the game was played in the regular season or not.
    
    Args:
        season_type (str): String object of the state of the season that the game was played.
    
    Returns:
        int: Integer object that is 1 if season type was regular and 0 otherwise.
    """

    if season_type == "Regular":
        return 1
    return 0




def get_team_abbr(team_name: str, team_abbr_file: Path) -> str:
    """
    Returns the team abbreviation from full team name. Default abbreviation is "unk".
    
    Args:
        team_name (str): String object of full team name.
        team_abbr_file (Path): Path object of file containing dictionary mapping team names to team abbreviations.
    
    Returns:
        str: String object of team abbreviation.
    """

    with open(team_abbr_file, "r") as f:
        team_abbr_dict = json.load(f)
    key = team_name.lower().replace(" ", "_").replace(".","_").replace("__","_")
    if key not in team_abbr_dict:
        return "unk"
    return team_abbr_dict[key]




def format_points(points_str: str) -> int:
    """
    Converts the points string to an integer. Intended to fail and cause error if points not an integer.

    Args: 
        points_str (str): String object of points scored.
    
    Returns:
        int: Integer object of number of points scored. 
    """

    return int(points_str)




def get_result(points_1: int, points_2: int) -> int:
    """
    Determines the winner of the game based on the points scored by the two teams.

    Args:
        points_1 (int): Integer object of number of points scored by team 1.
        points_2 (int): Integer object of number of points scored by team 2. 

    Returns:
        int: Integer object that is 1 if team 1 scored more points and 0 if team 2 scored more points. If there was a tie, return None.
    """

    # ensure the points are valid
    if points_1 == None or points_2 == None:
        return None
    if points_1 > points_2:
        return 1
    if points_2 > points_1:
        return 0
    # in case of tie, return None
    return None




def get_season(game_url: str) -> int:
    """
    Gets the season that the game was played in.

    Args:
        game_url (str): String object of the OddsPortal URL for the game.

    Returns:
        int: Integer object of the year. The year is the year the season ended. (e.g. all games in a 2008-2009 season have season field of 2009, even if they were played in 2008). 
    """

    season_str = game_url.split("/")[5]
    return int(season_str.split("-")[-1])




def format_ml(ml_1_str: str, ml_2_str: str) -> tuple[int, int]:
    """
    Returns integer objects of two-way moneylines.

    Args:
        ml_1_str (str): String object of moneyline of team 1.
        ml_2_str (str): String object of moneyline of team 2.
    
    Returns:
        int: Integer object of moneyline number of team 1. Returns None if either of the two moneylines are not integers.
        int: Integer object of moneyline number of team 2. Returns None if either of the two moneylines are not integers.
    """

    # ensure they are integers
    try:
        ml_1 = int(ml_1_str)
        ml_2 = int(ml_2_str)
    except:
        return None, None
    
    # if both are negative, this is the dual market favorite case
    if ml_1 < 0 and ml_2 < 0:
        return ml_1, ml_2
    
    # otherwise, ensure that the moneyline with greater absolute value is the negative one
    if abs(ml_1) > abs(ml_2):
        ml_1 = -1 * abs(ml_1)
        ml_2 = abs(ml_2)
    else:
        ml_1 = abs(ml_1)
        ml_2 = -1 * abs(ml_2)

    return ml_1, ml_2




def format1x2(ml_1_str: str, ml_x_str: str, ml_2_str: str) -> tuple[int, int, int]:
    """
    Returns integer objet of 1x2 moneylines.

    Args:
        ml_1_str (str): String object of moneyline of team 1 winning.
        ml_x_str (str): String object of moneyline tie happening.
        ml_2_str (str): String object of moneyline of team 2 winning.

    Returns:
        int: Integer object of moneyline number of team 1 winning. Returns None if either of the three moneylines are not integers.
        int: Integer object of moneyline number of tie happening. Returns None if either of the three moneylines are not integers.
        int: Integer object of moneyline number of team 2 winning. Returns None if either of the three moneylines are not integers.      
    """

    try:
        return int(ml_1_str), int(ml_x_str), int(ml_2_str)
    except:
        return None, None, None
    



def get_implied_prob(ml: int) -> float:
    """
    Convert moneyline to implied probability.

    Args: 
        ml (int): Integer object of moneyline number for event.

    Returns:
        float: Float object of implied probability of event
    """

    if ml == None:
        return None
    if ml < 0:
        return abs(ml) / (abs(ml) + 100)
    else:
        return 100 / (ml + 100)
    



def get_ml_prob(p_1: float, p_2: float) -> float:
    """
    Returns probability of team 1 winning given implied probabilities from two-way moneylines.

    Args:
        p_1 (float): Float object of implied probability that team 1 wins.
        p_2 (float): Float object of implied probability that team 2 wins.

    Returns:
        float: Float object of normalized probability that team 1 wins.
    """

    # ensure both probabilities are valid
    if p_1 == None or p_2 == None:
        return None
    
    # return normalized probability
    return p_1 / (p_1 + p_2)




def get_ml_bookmaker_profit(p_1: float, p_2: float) -> float:
    """
    Gets the bookmaker profit from the implied probabilities of two-way moneyline.

    Args:
        p_1 (float): Float object of implied probability that team 1 wins.
        p_2 (float): Float object of implied probability that team 2 wins.

    Returns:
        float: Float object of bookmaker profit.
    """

    # ensure both probabilities are valid
    if p_1 == None or p_2 == None:
        return None
    
    return p_1 + p_2 - 1





def get_1x2_prob_and_profit(p1: float, px: float, p2: float) -> tuple[float, float]:
    """
    Returns the normalized probability that team 1 wins and the bookmaker profit from 1x2 moneylines.

    Args:
        p1 (float): Float object of implied probability that team 1 wins.
        p2 (float): Float object of implied probability that tie happens.
        p3 (float): Float object of implied probability that team 2 wins.

    Returns:
        float: Float object of bookmaker profit.
        float: Float object of normalized probability that team 1 wins outright.
    """

    # ensure all probabilities are valid
    if p1 == None or px == None or p2 == None:
        return None, None
    
    # calculate bookmaker profit
    total_implied = p1 + px + p2
    bookmaker_profit = total_implied - 1.0
    
    # get normalized probability of team 1 winning outirhgt
    p_1_fair = p1 / total_implied
    p_x_fair = px / total_implied
    p_1_outright = p_1_fair + (p_x_fair * 0.5)
    
    return bookmaker_profit, p_1_outright








def preprocess_league_games(league: str, raw_data_file: Path, team_abbr_file: Path, output_save_file: Path, elo_file: Path=None) -> None:
    """
    Preproccesses all games for league and saves to CSV file. 
    Excludes 
    - non-regular season games
    - games at neutral venues
    - games with ties
    - games between unrecognized teams
    - games with invalid moneyline data.

    Args:
        league (str): String object of league abbreviation (e.g. "nfl").
        raw_data_file (Path): Path object of league's raw game data.
        team_abbr_file (Path): Path object of file containing dictionary mapping team names to team abbreviations.
        output_save_file (Path): Path object of file where preprocessed data will be saved.
        elo_file (Path): Path object of file containing of win probabilities based on Elo. Default is None.

    Returns:
        None
    """

    # load raw game dataframe
    raw_df = pd.read_csv(raw_data_file)

    # reformat some of the raw data
    new_df = pd.DataFrame({
        "date": raw_df["date"].apply(format_date),
        "season": raw_df["game_url"].apply(get_season),
        "regular": raw_df["season_type"].apply(is_regular),
        "home_team": raw_df["team_1"].apply(lambda x: get_team_abbr(x, team_abbr_file)),
        "away_team": raw_df["team_2"].apply(lambda x: get_team_abbr(x, team_abbr_file)),
        "points_1": raw_df["points_1"].apply(format_points).astype("Int64"),
        "points_2": raw_df["points_2"].apply(format_points).astype("Int64"),
        "neutral": raw_df["neutral"],
        "game_url": raw_df["game_url"]
    })

    # determine result of game
    new_df["result"] = new_df.apply(
        lambda row: get_result(row["points_1"], row["points_2"]),
        axis=1
    ).astype("Int64")


    # all leagues, except NHL, use home away moneylines, where NHL uses 1x2 moneylines, so the probability logic is slightly different.
    if league != "nhl":
        new_df[["ml_1", "ml_2"]] = raw_df.apply(
            lambda row: format_ml(row["moneyline_1"], row["moneyline_2"]),
            axis=1,
            result_type="expand"
        ).astype("Int64")
        new_df["implied_ml_1"] = new_df["ml_1"].apply(get_implied_prob)
        new_df["implied_ml_2"] = new_df["ml_2"].apply(get_implied_prob)
        new_df["bookmaker_profit"] = new_df.apply(lambda row: get_ml_bookmaker_profit(row["implied_ml_1"], row["implied_ml_2"]), axis=1)
        new_df["ml_prob"] = new_df.apply(lambda row: get_ml_prob(row["implied_ml_1"], row["implied_ml_2"]), axis=1)
    else:
        new_df[["ml_1", "ml_x", "ml_2"]] = raw_df.apply(
            lambda row: format1x2(row["moneyline_1"], row["moneyline_x"], row["moneyline_2"]),
            axis=1,
            result_type="expand"
        ).astype("Int64")
        new_df["implied_ml_1"] = new_df["ml_1"].apply(get_implied_prob)
        new_df["implied_ml_x"] = new_df["ml_x"].apply(get_implied_prob)
        new_df["implied_ml_2"] = new_df["ml_2"].apply(get_implied_prob)
        new_df[["bookmaker_profit", "ml_prob"]] = new_df.apply(
            lambda row: get_1x2_prob_and_profit(row["implied_ml_1"], row["implied_ml_x"], row["implied_ml_2"]),
            axis=1,
            result_type="expand"
        )


    # compute number of invalid games and their reasons and print out the statistics
    total_len = len(new_df)
    non_regular_len = len(new_df[new_df["regular"] == 0])
    neutrals_len = len(new_df[new_df["neutral"] == 1])
    ties_len = len(new_df[new_df["result"].isna()])
    unk_team_len = len(new_df[(new_df["home_team"] == "unk") | (new_df["away_team"] == "unk")])
    missing_ml_len = len(new_df[(new_df["ml_prob"].isna())])
    print(f"total: {total_len}")
    print(f"non regular season: {non_regular_len} ({non_regular_len / total_len})")
    print(f"neutrals: {neutrals_len} ({neutrals_len / total_len})")
    print(f"ties: {ties_len} ({ties_len / total_len})")
    print(f"unk team: {unk_team_len} ({unk_team_len / total_len})")
    print(f"missing ml: {missing_ml_len} ({missing_ml_len / total_len})")

    # exclude invalid games from final result
    mask = (
        (new_df["regular"] == 1) &
        (new_df["neutral"] == 0) &
        (new_df["result"].notna()) &
        (new_df["home_team"] != "unk") &
        (new_df["away_team"] != "unk") &
        (new_df["ml_prob"].notna())
    )
    final_df = new_df[mask].copy()
    print(f"final len {len(final_df)} ({len(final_df) / total_len})")


    # determine which games occur in second half of regular season for each season
    final_df = final_df.sort_values(by=["season", "date"], ascending=[False, False])
    season_counts = final_df.groupby("season")["date"].transform("count")
    reverse_rank = final_df.groupby("season").cumcount()
    final_df["second_half"] = (reverse_rank < (season_counts / 2)).astype(int)


    # if an Elo file was specified, retrieve the probability derived from Elo
    if elo_file != None:
        elo_mapping = {}
        elo_df = pd.read_csv(elo_file)
        for _, row in elo_df.iterrows():
            game_id_str1 = f'{row["date"]}_{row["team1"].lower()}_{row["team2"].lower()}'
            game_id_str2 = f'{row["date"]}_{row["team2"].lower()}_{row["team1"].lower()}'
            elo_mapping[game_id_str1] = row["elo_prob1"]
            elo_mapping[game_id_str2] = 1 - row["elo_prob1"]
        
        for i, row in final_df.iterrows():
            game_id_str = f'{row["date"]}_{row["home_team"]}_{row["away_team"]}'
            if game_id_str in elo_mapping:
                final_df.loc[i, "elo_prob"] = elo_mapping[game_id_str]
            else:
                final_df.loc[i, "elo_prob"] = None



    # save the result
    new_order = [
        "date", "season", "second_half",
        "home_team", "away_team", "result",
        "bookmaker_profit", "ml_prob",
        "game_url"
    ]
    if league == "nfl":
        new_order = [
            "date", "season", "second_half",
            "home_team", "away_team", "result",
            "bookmaker_profit", "ml_prob", "elo_prob",
            "game_url"
        ]
    final_df = final_df[new_order]
    final_df.to_csv(output_save_file, index=False)








if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        print(f"----{league}----")
        preprocess_league_games(league=league, 
                            raw_data_file=f"raw_data/oddsportal_{league}.csv", 
                            team_abbr_file="utility/team_abbrs.json", 
                            output_save_file=f"processed_data/{league}.csv", 
                            elo_file=(f"raw_data/fivethirtyeight_{league}_elo.csv" if league=="nfl" else None))
        print("-----------\n")