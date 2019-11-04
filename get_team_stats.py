import csv

import scrape_tespa
import get_player_stats

# @return: dict of all teams with format {team_name: {team info}}
def get_teams() -> dict:
    with open(scrape_tespa.teams_path) as f:
        # load csv as list of dicts
        teams = [
                    {k: v for k, v in row.items()}
                    for row in csv.DictReader(f, skipinitialspace=True)
                ]
        # convert into dict of format {team_name: {team info}}
        teams = { team['team_name'][team['team_name'].find(']') + 1:].strip(): team for team in teams }
        return teams

# TODO: fuzzy string matching w/fuzzy wuzzy
# @param team: name of tespa team to fetch
# @return: dict of rank, rating, roster etc of team
def get_team(team: str) -> dict:
    teams = get_teams()
    return teams[team]

# @param team: name of tespa team to fetch
# @return: list of btags of team's roster
def get_btags(team: str) -> list:
    team = get_team(team)
    btags = team['btag']
    return btags.split(',')

# @param team: name of tespa team to fetch
# @return: dict of dicts of each player's summary stats
def get_team_stats(team: str) -> dict:
    btags = get_btags(team)
    result = {}
    for btag in btags:
        result[btag] = get_player_stats.get_summary_stats(btag)
    return result

if __name__ == "__main__":
    import pprint
    pprint.pprint(get_team_stats('UofTears'))
