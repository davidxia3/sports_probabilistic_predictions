from pathlib import Path
import pandas as pd
import json
import numpy as np
from ratingslib.ratings.elo import Elo
from ratingslib.ratings.keener import Keener
from ratingslib.ratings.massey import Massey
from ratingslib.ratings.od import OffenseDefense
from ratingslib.utils.enums import ratings
from ratingslib.ratings.methods import normalization_rating



# formatting helper functions
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
    Returns the team abbreviation from full team name. Default if key not found is NA.
    
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
        return pd.NA
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
        int: Integer object that is 1 if team 1 scored more points and 0 if team 2 scored more points. If there was a tie, return NA.
    """

    # ensure the points are valid
    if pd.isna(points_1) or pd.isna(points_2):
        return pd.NA
    if points_1 > points_2:
        return 1
    if points_2 > points_1:
        return 0
    
    # in case of tie, return NA
    return pd.NA



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
        int: Integer object of moneyline number of team 1. Returns NA if either of the two moneylines are not integers.
        int: Integer object of moneyline number of team 2. Returns NA if either of the two moneylines are not integers.
    """

    # ensure they are integers
    try:
        ml_1 = int(ml_1_str)
        ml_2 = int(ml_2_str)
    except:
        return pd.NA, pd.NA

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
        int: Integer object of moneyline number of team 1 winning. Returns NA if either of the three moneylines are not integers.
        int: Integer object of moneyline number of tie happening. Returns NA if either of the three moneylines are not integers.
        int: Integer object of moneyline number of team 2 winning. Returns NA if either of the three moneylines are not integers.      
    """

    try:
        return int(ml_1_str), int(ml_x_str), int(ml_2_str)
    except:
        return pd.NA, pd.NA, pd.NA



def get_implied_prob(ml: int) -> float:
    """
    Convert moneyline to implied probability.

    Args: 
        ml (int): Integer object of moneyline number for event.

    Returns:
        float: Float object of implied probability of event.
    """

    if pd.isna(ml):
        return pd.NA
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
    if pd.isna(p_1) or pd.isna(p_2):
        return pd.NA
    
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
    if pd.isna(p_1) or pd.isna(p_2):
        return pd.NA
    
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
    if pd.isna(p1) or pd.isna(px) or pd.isna(p2):
        return pd.NA, pd.NA

    # calculate bookmaker profit
    total_implied = p1 + px + p2
    bookmaker_profit = total_implied - 1.0

    # get normalized probability of team 1 winning outirhgt
    p_1_fair = p1 / total_implied
    p_x_fair = px / total_implied
    p_1_outright = p_1_fair + (p_x_fair * 0.5)

    return bookmaker_profit, p_1_outright







# Bradley Terry helper functions
def bt_get_estimate(i: int, p: pd.Series, df: pd.DataFrame) -> float:
    """
    Compute the Bradley–Terry updated strength estimate for a single item.
        p_i_new = n_i / Σ_j ( (w_ij + w_ji) / (p_i + p_j) )
        where:
            - n_i is the total number of comparisons involving item i
            - w_ij is the number of wins of item i over j (df.iloc[i, j])
            - w_ji is the number of wins of item j over i (df.iloc[j, i])
            - p_i, p_j are current strength estimates

    Args:
        i (int): Index of the item whose strength is being updated.
        p (pd.Series): Current strength estimates for all items.
        df (pd.DataFrame): Square comparison matrix where df.iloc[i, j] represents the number of wins of item i over item j.

    Returns:
        float: The updated Bradley Terry strength estimate for item i.
    """
    get_prob = lambda i, j: np.nan if i == j else p.iloc[i] + p.iloc[j]
    n = df.iloc[i].sum()

    d_n = df.iloc[i] + df.iloc[:, i]
    d_d = pd.Series([get_prob(i, j) for j in range(len(p))], index=p.index)
    d = (d_n / d_d).sum()

    return n / d



def bt_estimate_p(p: pd.Series, df: pd.DataFrame) -> pd.Series:
    """
    Perform a single Bradley Terry strength update step.

    Args:
        p (pd.Series): Current strength estimates for each item/team.
        df (pd.DataFrame): A comparison or results matrix used by "bt_get_estimate" to compute updated strength values.

    Returns:
        pd.Series: A new Series of updated Bradley Terry strength estimates.
    """
    return pd.Series([bt_get_estimate(i, p, df) for i in range(df.shape[0])], index=p.index)



def bt_iterate(df: pd.DataFrame, p: pd.Series = None, n: int = 100, sorted: bool = True) -> tuple[pd.Series, pd.DataFrame]:
    """
    Perform iterative Bradley Terry probability estimation.

    Args:
        df (pd.DataFrame): A square comparison matrix or results DataFrame used by "bt_estimate_p" to update strength estimates.
        p (pd.Series, optional): Initial strength estimates indexed by the same labels as `df.columns`. If None, all strengths start equal. Defaults to None.
        n (int, optional): Number of iteration steps to perform. Defaults to 100.
        sorted (bool, optional): If True, returns the final strength vector sorted in descending order. Defaults to True.

    Returns:
        pd.Series: Final strength estimates.
        pd.DataFrame: Each row contains the strength estimates from one iteration.
    """
    if p is None:
        p = pd.Series([1 for _ in range(df.shape[0])], index=list(df.columns))

    estimates = [p]

    for _ in range(n):
        p = bt_estimate_p(p, df)
        p = p / p.sum()
        estimates.append(p)

    p = p.sort_values(ascending=False) if sorted else p
    return p, pd.DataFrame(estimates)



def get_winner(row: pd.Series) -> str:
    """
    Determine the winner of a match from a DataFrame row.

    Args:
        row (pd.Series): A pandas Series representing a single match.
            - 'FTHG' (int): Full-time home goals.
            - 'FTAG' (int): Full-time away goals.
            - 'HomeTeam' (str): Name of the home team.
            - 'AwayTeam' (str): Name of the away team.

    Returns:
        str: The name of the winning team, or `pd.NA` if the match is a draw or if score data is missing.
    """
    if pd.isna(row.FTHG) or pd.isna(row.FTAG):
        return pd.NA
    if row.FTHG > row.FTAG:
        return row.HomeTeam
    elif row.FTHG < row.FTAG:
        return row.AwayTeam
    else:
        return pd.NA
    


def get_loser(row: pd.Series) -> str:
    """
    Determine the loser of a match from a DataFrame row.

    Args:
        row (pd.Series): A pandas Series representing a single match.
            - 'FTHG' (int): Full-time home goals.
            - 'FTAG' (int): Full-time away goals.
            - 'HomeTeam' (str): Name of the home team.
            - 'AwayTeam' (str): Name of the away team.

    Returns:
        str: The name of the losing team, or `pd.NA` if the match is a draw
        or if score data is missing.
    """
    if pd.isna(row.FTHG) or pd.isna(row.FTAG):
        return pd.NA
    if row.FTHG > row.FTAG:
        return row.AwayTeam
    elif row.FTHG < row.FTAG:
        return row.HomeTeam
    else:
        return pd.NA







# main processing function
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
        "Date": raw_df["date"].apply(format_date),
        "Season": raw_df["game_url"].apply(get_season),
        "regular": raw_df["season_type"].apply(is_regular),
        "HomeTeam": raw_df["team_1"].apply(lambda x: get_team_abbr(x, team_abbr_file)),
        "AwayTeam": raw_df["team_2"].apply(lambda x: get_team_abbr(x, team_abbr_file)),
        "FTHG": raw_df["points_1"].apply(format_points).astype("Int64"),
        "FTAG": raw_df["points_2"].apply(format_points).astype("Int64"),
        "neutral": raw_df["neutral"],
        "game_url": raw_df["game_url"]
    })

    # determine result of game
    new_df["result"] = new_df.apply(
        lambda row: get_result(row["FTHG"], row["FTAG"]),
        axis=1
    ).astype("Int64")

    # all leagues, except NHL, use home away moneylines, where NHL uses 1x2 moneylines, so the probability logic is slightly different
    if league != "nhl":
        new_df[["home_ml", "away_ml"]] = raw_df.apply(
            lambda row: format_ml(row["moneyline_1"], row["moneyline_2"]),
            axis=1,
            result_type="expand"
        ).astype("Int64")
        new_df["implied_ml_1"] = new_df["home_ml"].apply(get_implied_prob)
        new_df["implied_ml_2"] = new_df["away_ml"].apply(get_implied_prob)
        new_df["bookmaker_profit"] = new_df.apply(lambda row: get_ml_bookmaker_profit(row["implied_ml_1"], row["implied_ml_2"]), axis=1)
        new_df["ml_prob"] = new_df.apply(lambda row: get_ml_prob(row["implied_ml_1"], row["implied_ml_2"]), axis=1)
    else:
        new_df[["home_ml", "tie_ml", "away_ml"]] = raw_df.apply(
            lambda row: format1x2(row["moneyline_1"], row["moneyline_x"], row["moneyline_2"]),
            axis=1,
            result_type="expand"
        ).astype("Int64")
        new_df["implied_ml_1"] = new_df["home_ml"].apply(get_implied_prob)
        new_df["implied_ml_x"] = new_df["tie_ml"].apply(get_implied_prob)
        new_df["implied_ml_2"] = new_df["away_ml"].apply(get_implied_prob)
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
    na_team_len = len(new_df[(new_df["HomeTeam"].isna()) | (new_df["AwayTeam"].isna())])
    missing_ml_len = len(new_df[(new_df["ml_prob"].isna())])
    print(f"total: {total_len}")
    print(f"non regular season: {non_regular_len} ({non_regular_len / total_len})")
    print(f"neutrals: {neutrals_len} ({neutrals_len / total_len})")
    print(f"ties: {ties_len} ({ties_len / total_len})")
    print(f"na team: {na_team_len} ({na_team_len / total_len})")
    print(f"missing ml: {missing_ml_len} ({missing_ml_len / total_len})")



    # exclude invalid games from final result
    mask = (
        (new_df["regular"] == 1) &
        (new_df["neutral"] == 0) &
        (new_df["result"].notna()) &
        (new_df["HomeTeam"].notna()) &
        (new_df["AwayTeam"].notna()) &
        (new_df["ml_prob"].notna())
    )
    clean_df = new_df[mask].copy()
    print(f"final len {len(clean_df)} ({len(clean_df) / total_len})")



    # determine which games occur in second half of regular season for each season
    clean_df = clean_df.sort_values(by=["Season", "Date"], ascending=[False, False])
    season_counts = clean_df.groupby("Season")["Date"].transform("count")
    reverse_rank = clean_df.groupby("Season").cumcount()
    clean_df["second_half"] = (reverse_rank < (season_counts / 2)).astype(int)

    clean_df = clean_df.reset_index(drop=True)

    # if an Elo file was specified, retrieve the probability derived from Elo
    if elo_file is not None:
        elo_mapping = {}
        elo_df = pd.read_csv(elo_file)
        for _, row in elo_df.iterrows():
            game_id_str1 = f'{row["date"]}_{row["team1"].lower()}_{row["team2"].lower()}'
            game_id_str2 = f'{row["date"]}_{row["team2"].lower()}_{row["team1"].lower()}'
            elo_mapping[game_id_str1] = row["elo_prob1"]
            elo_mapping[game_id_str2] = 1 - row["elo_prob1"]
        
        for index, row in clean_df.iterrows():
            game_id_str = f'{row["Date"]}_{row["HomeTeam"]}_{row["AwayTeam"]}'
            if game_id_str in elo_mapping:
                clean_df.loc[index, "elo_prob"] = elo_mapping[game_id_str]
            else:
                clean_df.loc[index, "elo_prob"] = pd.NA


    
    # compute RatingsLib probabilistic predictions
    clean_df["elopoint_prob"] = pd.NA
    clean_df["elowin_prob"] = pd.NA
    clean_df["keener_prob"] = pd.NA
    clean_df["massey_prob"] = pd.NA
    clean_df["od_prob"] = pd.NA

    for index, row in clean_df.iterrows():
        past_games = clean_df[
            (clean_df['Season'] == row['Season']) & 
            (pd.to_datetime(clean_df['Date'], format="%Y-%m-%d") < pd.to_datetime(row['Date'], format="%Y-%m-%d"))
        ]

        unique_teams = pd.unique(past_games[['HomeTeam', 'AwayTeam']].values.ravel())
        unique_teams_df = pd.DataFrame(unique_teams, columns=['Item'])

        home = row['HomeTeam']
        away = row['AwayTeam']

        try:
            elopoint = Elo(version=ratings.ELOPOINT, starting_point=0).rate(past_games, unique_teams_df)
            elopoint['rating'] = normalization_rating(elopoint, "rating")
            elopoint['rating'] = normalization_rating(elopoint, "rating")
            ep_home = elopoint[elopoint["Item"] == home].iloc[0]["rating"]
            ep_away = elopoint[elopoint["Item"] == away].iloc[0]["rating"]
            clean_df.at[index, "elopoint_prob"] = ep_home / (ep_home + ep_away)
        except:
            clean_df.at[index, "elopoint_prob"] = pd.NA

        try:
            elowin = Elo(version=ratings.ELOWIN, starting_point=0).rate(past_games, unique_teams_df)
            elowin['rating'] = normalization_rating(elowin, "rating")
            ew_home = elowin[elowin["Item"] == home].iloc[0]["rating"]
            ew_away = elowin[elowin["Item"] == away].iloc[0]["rating"]
            clean_df.at[index, "elowin_prob"] = ew_home / (ew_home + ew_away)
        except:
            clean_df.at[index, "elowin_prob"] = pd.NA

        try:
            keener = Keener(normalization=False).rate(past_games, unique_teams_df)
            keener['rating'] = normalization_rating(keener, "rating")
            keener_home = keener[keener["Item"] == home].iloc[0]["rating"]
            keener_away = keener[keener["Item"] == away].iloc[0]["rating"]
            clean_df.at[index, "keener_prob"] = keener_home / (keener_home + keener_away)
        except:
            clean_df.at[index, "keener_prob"] = pd.NA


        try:
            massey = Massey().rate(past_games, unique_teams_df)
            massey['rating'] = normalization_rating(massey, "rating")
            massey_home = massey[massey["Item"] == home].iloc[0]["rating"]
            massey_away = massey[massey["Item"] == away].iloc[0]["rating"]
            clean_df.at[index, "massey_prob"] = massey_home / (massey_home + massey_away)
        except:
            clean_df.at[index, "massey_prob"] = pd.NA


        try:    
            od = OffenseDefense(tol=0.0001).rate(past_games, unique_teams_df)
            od['rating'] = normalization_rating(od, "rating")
            od_home = od[od["Item"] == home].iloc[0]["rating"]
            od_away = od[od["Item"] == away].iloc[0]["rating"]
            clean_df.at[index, "od_prob"] = od_home / (od_home + od_away)
        except:
            clean_df.at[index, "od_prob"] = pd.NA



    # compute Bradley Terry Predictions (https://datascience.oneoffcoder.com/btl-model.html)
    clean_df['bt_prob'] = pd.NA
    clean_df['winner'] = clean_df.apply(get_winner, axis=1)
    clean_df['loser'] = clean_df.apply(get_loser, axis=1)
    clean_df = clean_df.reset_index(drop=True)

    
    for index, row in clean_df.iterrows():
            
        past_games = clean_df[
            (clean_df['Season'] == row['Season']) & 
            (pd.to_datetime(clean_df['Date'], format="%Y-%m-%d") < pd.to_datetime(row['Date'], format="%Y-%m-%d"))
        ]

        teams = sorted(list(set(past_games.HomeTeam) | set(past_games.AwayTeam)))
        t2i = {t: i for i, t in enumerate(teams)}

        df = past_games\
            .groupby(['winner', 'loser'])\
            .agg('count')\
            .drop(columns=['AwayTeam', 'FTHG', 'FTAG'])\
            .rename(columns={'HomeTeam': 'n'})\
            .reset_index()
        df['r'] = df['winner'].apply(lambda t: t2i[t])
        df['c'] = df['loser'].apply(lambda t: t2i[t])

        n_teams = len(teams)
        mat = np.zeros([n_teams, n_teams])

        for _, r in df.iterrows():
            mat[r.r, r.c] = r.n

        iterate_df = pd.DataFrame(mat, columns=teams, index=teams)

        # max 100 iterations
        p, _ = bt_iterate(iterate_df, n=100)
        home_team, away_team = row['HomeTeam'], row['AwayTeam']

        if home_team in p and away_team in p:
            if (p[home_team] + p[away_team]) != 0:
                clean_df.at[index, 'bt_prob'] = p[home_team] / (p[home_team] + p[away_team])
            else:
                clean_df.at[index, 'bt_prob'] = pd.NA



    # save the result
    new_order = [
        "Date", "Season", "second_half",
        "HomeTeam", "AwayTeam", "result",
        "home_ml", "away_ml",
        "bookmaker_profit", "ml_prob",
        "elopoint_prob", "elowin_prob", "keener_prob", "massey_prob", "od_prob",
        "bt_prob",
        "game_url"
    ]
    if league == "nfl":
        new_order = [
            "Date", "Season", "second_half",
            "HomeTeam", "AwayTeam", "result",
            "home_ml", "away_ml",
            "bookmaker_profit", "ml_prob", "elo_prob",
            "elopoint_prob", "elowin_prob", "keener_prob", "massey_prob", "od_prob",
            "bt_prob",
            "game_url"
        ]
    elif league == "nhl":
        new_order = [
            "Date", "Season", "second_half",
            "HomeTeam", "AwayTeam", "result",
            "home_ml", "tie_ml", "away_ml",
            "bookmaker_profit", "ml_prob",
            "elopoint_prob", "elowin_prob", "keener_prob", "massey_prob", "od_prob",
            "bt_prob",
            "game_url"
        ]
    clean_df = clean_df[new_order]
    clean_df = clean_df.rename(columns={
        "Date": "date",
        "Season": "season",
        "HomeTeam": "home_team",
        "AwayTeam": "away_team"
    })
    clean_df.to_csv(output_save_file, index=False)







if __name__ == "__main__":
    leagues = ["mlb", "nba", "nfl", "nhl"]
    for league in leagues:
        print(f"----{league}----")
        preprocess_league_games(league=league, 
                            raw_data_file=Path(f"raw_data/oddsportal_{league}.csv"), 
                            team_abbr_file=Path("utility/team_abbrs.json"), 
                            output_save_file=Path(f"processed_data/{league}.csv"), 
                            elo_file=(Path(f"raw_data/fivethirtyeight_{league}_elo.csv") if league=="nfl" else None))
        print("-----------\n")