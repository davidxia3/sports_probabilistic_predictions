from pathlib import Path
import pandas as pd
import json
import numpy as np
import ast



# formatting helper functions
def format_date(raw_date_str: str) -> str:
    """
    Converts date from "dd mmm yyyy" format to "yyyy-mm-dd".

    Args: 
        raw_date_str (str) : String object of date in "dd mmm yyyy" format.

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



def parse_moneylines(x):
    if pd.isna(x):
        return []
    return ast.literal_eval(x)



def extract_max_ml(ml_list):
    if not ml_list:
        return pd.NA, pd.NA
    
    home_vals = [t[0] for t in ml_list if t[0] is not None]
    away_vals = [t[1] for t in ml_list if t[1] is not None]
    
    home_max = max(home_vals) if home_vals else pd.NA
    away_max = max(away_vals) if away_vals else pd.NA
    
    return home_max, away_max



def american_to_prob(ml):
    if pd.isna(ml):
        return np.nan
    if ml > 0:
        return 100 / (ml + 100)
    else:
        return -ml / (-ml + 100)



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
def preprocess_league_games(raw_data_file: Path, team_abbr_file: Path, output_save_file: Path) -> None:
    """
    Preproccesses all games for league and saves to CSV file by adding 
    - result of game
    - moneyline based probabilistic predictions
    - Bradley-Terry based probabilistic predictions
    - bookmaker profit.

    Excludes 
    - non-regular season games
    - games at neutral venues
    - games with ties
    - games with invalid moneyline data.

    Args:
        raw_data_file (Path): Path object of league's raw game data.
        team_abbr_file (Path): Path object of file containing dictionary mapping team names to team abbreviations.
        output_save_file (Path): Path object of file where preprocessed data will be saved.

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

    # throw out all non regular season games
    new_df = new_df[new_df["regular"] == 1]


    # determine result of game
    new_df["result"] = new_df.apply(
        lambda row: get_result(row["FTHG"], row["FTAG"]),
        axis=1
    ).astype("Int64")

    # calculate moneyline probabilistic prediction based on home away moneylines
    parsed = raw_df["moneylines"].apply(parse_moneylines)
    ml_df = parsed.apply(lambda x: pd.Series(extract_max_ml(x)))
    ml_df.columns = ["home_ml", "away_ml"]

    new_df["home_ml"] = ml_df["home_ml"].astype("Int64")
    new_df["away_ml"] = ml_df["away_ml"].astype("Int64")

    home_prob = new_df["home_ml"].apply(american_to_prob)
    away_prob = new_df["away_ml"].apply(american_to_prob)
    new_df["bookmaker_profit"] = home_prob + away_prob - 1

    prob_sum = home_prob + away_prob
    normalized_home_prob = home_prob / prob_sum
    new_df["ml_prob"] = normalized_home_prob



    # compute number of invalid games and their reasons and print out the statistics
    total_regular_len = len(new_df)
    neutrals_len = len(new_df[new_df["neutral"] == 1])
    ties_len = len(new_df[new_df["result"].isna()])
    na_team_len = len(new_df[(new_df["HomeTeam"].isna()) | (new_df["AwayTeam"].isna())])
    missing_ml_len = len(new_df[new_df["ml_prob"].isna()])
    mask = (
        (new_df["neutral"] == 0) &
        (new_df["result"].notna()) &
        (new_df["HomeTeam"].notna()) &
        (new_df["AwayTeam"].notna()) &
        (new_df["ml_prob"].notna())
    )
    clean_df = new_df[mask].copy()

    print(f"- {league.upper()}:")
    print(f"    - Total regular season games: {total_regular_len}.")
    print(f"    - Regular season games at neutral venue: {neutrals_len} ({100 * neutrals_len / total_regular_len:.3f}%).")
    print(f"    - Regular season games ending in ties: {ties_len} ({100 * ties_len / total_regular_len:.3f}%).")
    print(f"    - Regular season games with unrecognized teams: {na_team_len} ({100 * na_team_len / total_regular_len:.3f}%).")
    print(f"    - Regular season games with invalid moneyline data: {missing_ml_len} ({100 * missing_ml_len / total_regular_len:.3f}%).")
    print(f"    - Invalid other reason regular season games: {(neutrals_len+ties_len+na_team_len)} ({100 * (neutrals_len+ties_len+na_team_len) / total_regular_len:.3f}%).")
    print(f"    - Clean regular season games: {len(clean_df)} ({100 * len(clean_df) / total_regular_len:.3f}%).")




    # # determine which games occur in second half of regular season for each season
    clean_df = clean_df.sort_values(by=["Season", "Date"])
    season_counts = clean_df.groupby("Season")["Date"].transform("count")
    before_count = clean_df.groupby("Season")["Date"].rank(method="min") - 1
    clean_df["second_half"] = (before_count >= (season_counts + 1) // 2).astype(int)
    clean_df = clean_df.sort_values(by=["Season", "Date"], ascending=[False, False])
    clean_df = clean_df.reset_index(drop=True)



    # compute Bradley Terry Predictions (using code from https://datascience.oneoffcoder.com/btl-model.html)
    clean_df['bt_prob'] = pd.NA
    clean_df['winner'] = clean_df.apply(get_winner, axis=1)
    clean_df['loser'] = clean_df.apply(get_loser, axis=1)
    clean_df = clean_df.reset_index(drop=True)

    
    for index, row in clean_df.iterrows():
        if index % 100 == 0:
            print(f"{index} / {len(clean_df)}")
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
        preprocess_league_games(raw_data_file=Path(f"raw_data/oddsportal_{league}.csv"), 
                            team_abbr_file=Path("utility/team_abbrs.json"), 
                            output_save_file=Path(f"processed_data/{league}.csv"))
        print("-----------\n")