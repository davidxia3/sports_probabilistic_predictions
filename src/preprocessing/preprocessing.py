from pathlib import Path
import pandas as pd
import json

def format_date(raw_date_str: str) -> str:
    month_abbr_dict = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04",
        "may": "05", "jun": "06", "jul": "07", "aug": "08",
        "sep": "09", "oct": "10", "nov": "11", "dec": "12"
    }
    day_str, month_abbr, year_str = raw_date_str.split()
    return f"{year_str}-{month_abbr_dict[month_abbr.lower()]}-{day_str}"

def is_regular(season_type: str) -> int:
    if season_type == "Regular":
        return 1
    return 0

def get_team_abbr(team_name: str, team_abbr_file: Path) -> str:
    with open(team_abbr_file, "r") as f:
        team_abbr_dict = json.load(f)

    key = team_name.lower().replace(" ", "_").replace(".","_").replace("__","_")
    if key not in team_abbr_dict:
        return "unk"
    return team_abbr_dict[key]

def format_points(points_str: str) -> int:
    return int(points_str)
    
def get_result(points_1: int, points_2: int) -> int:
    if points_1 == None or points_2 == None:
        return None
    if points_1 > points_2:
        return 1
    if points_2 > points_1:
        return 0
    return None

def get_season(game_url: str) -> str:
    season_str = game_url.split("/")[5]
    return int(season_str.split("-")[-1])

def format_ml(ml_1_str: str, ml_2_str: str) -> tuple[int, int]:
    try:
        ml_1 = int(ml_1_str)
        ml_2 = int(ml_2_str)
    except:
        return None, None
    if ml_1 < 0 and ml_2 < 0:
        return ml_1, ml_2
    if abs(ml_1) > abs(ml_2):
        ml_1 = -1 * abs(ml_1)
        ml_2 = abs(ml_2)
    else:
        ml_1 = abs(ml_1)
        ml_2 = -1 * abs(ml_2)

    return ml_1, ml_2

def format1x2(ml_1_str: str, ml_x_str: str, ml_2_str: str) -> tuple[int, int, int]:
    try:
        return int(ml_1_str), int(ml_x_str), int(ml_2_str)
    except:
        return None, None, None
    
    
def get_implied_prob(ml: int) -> float:
    if ml == None:
        return None
    if ml < 0:
        return abs(ml) / (abs(ml) + 100)
    else:
        return 100 / (ml + 100)

def get_ml_prob(p_1: float, p_2: float) -> float:
    if p_1 == None or p_2 == None:
        return None
    
    return p_1 / (p_1 + p_2)

def get_ml_bookmaker_profit(p_1: float, p_2: float) -> float:
    if p_1 == None or p_2 == None:
        return None
    
    return p_1 + p_2 - 1

def get_1x2_prob_and_profit(p1: float, px: float, p2: float) -> tuple[float, float]:
    if p1 == None or px == None or p2 == None:
        return None, None
    total_implied = p1 + px + p2
    bookmaker_profit = total_implied - 1.0
    
    p_1_fair = p1 / total_implied
    p_x_fair = px / total_implied
    
    p_1_outright = p_1_fair + (p_x_fair * 0.5)
    
    return bookmaker_profit, p_1_outright



    
def preprocess_league_games(league: str, raw_data_file: Path, team_abbr_file: Path, output_save_file: Path, elo_file: Path=None) -> None:
    
    raw_df = pd.read_csv(raw_data_file)

    new_df = pd.DataFrame({
        "date": raw_df["date"].apply(format_date),
        "season": raw_df["game_url"].apply(get_season),
        "regular": raw_df["season_type"].apply(is_regular),
        "team_1": raw_df["team_1"].apply(lambda x: get_team_abbr(x, team_abbr_file)),
        "team_2": raw_df["team_2"].apply(lambda x: get_team_abbr(x, team_abbr_file)),
        "points_1": raw_df["points_1"].apply(format_points).astype("Int64"),
        "points_2": raw_df["points_2"].apply(format_points).astype("Int64"),
        "neutral": raw_df["neutral"],
        "game_url": raw_df["game_url"]
    })

    new_df["result"] = new_df.apply(
        lambda row: get_result(row["points_1"], row["points_2"]),
        axis=1
    ).astype("Int64")

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


    total_len = len(new_df)
    non_regular_len = len(new_df[new_df["regular"] == 0])
    neutrals_len = len(new_df[new_df["neutral"] == 1])
    ties_len = len(new_df[new_df["result"].isna()])
    unk_team_len = len(new_df[(new_df["team_1"] == "unk") | (new_df["team_2"] == "unk")])
    missing_ml_len = len(new_df[(new_df["ml_prob"].isna())])
    print(f"total: {total_len}")
    print(f"non regular season: {non_regular_len} ({non_regular_len / total_len})")
    print(f"neutrals: {neutrals_len} ({neutrals_len / total_len})")
    print(f"ties: {ties_len} ({ties_len / total_len})")
    print(f"unk team: {unk_team_len} ({unk_team_len / total_len})")
    print(f"missing ml: {missing_ml_len} ({missing_ml_len / total_len})")

    mask = (
        (new_df["regular"] == 1) &
        (new_df["neutral"] == 0) &
        (new_df["result"].notna()) &
        (new_df["team_1"] != "unk") &
        (new_df["team_2"] != "unk") &
        (new_df["ml_prob"].notna())
    )

    final_df = new_df[mask].copy()
    print(f"final len {len(final_df)} ({len(final_df) / total_len})")

    final_df = final_df.sort_values(by=["season", "date"], ascending=[False, False])
    season_counts = final_df.groupby("season")["date"].transform("count")
    reverse_rank = final_df.groupby("season").cumcount()
    final_df["second_half"] = (reverse_rank < (season_counts / 2)).astype(int)


    
    if elo_file != None:
        elo_mapping = {}
        elo_df = pd.read_csv(elo_file)
        for _, row in elo_df.iterrows():
            game_id_str1 = f'{row["date"]}_{row["team1"].lower()}_{row["team2"].lower()}'
            game_id_str2 = f'{row["date"]}_{row["team2"].lower()}_{row["team1"].lower()}'
            elo_mapping[game_id_str1] = row["elo_prob1"]
            elo_mapping[game_id_str2] = 1 - row["elo_prob1"]
        
        for i, row in final_df.iterrows():
            game_id_str = f'{row["date"]}_{row["team_1"]}_{row["team_2"]}'
            if game_id_str in elo_mapping:
                final_df.loc[i, "elo_prob"] = elo_mapping[game_id_str]
            else:
                final_df.loc[i, "elo_prob"] = None



    new_order = [
        "date", "season", "second_half",
        "team_1", "team_2", "result",
        "bookmaker_profit", "ml_prob",
        "game_url"
    ]
    if league == "nfl":
        new_order = [
            "date", "season", "second_half",
            "team_1", "team_2", "result",
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