import requests
import json
import re
import operator
from datetime import datetime

from discord_globals import STAT_KEYWORDS

# TODO: Historical stats

# @param btag: battletag in format Meeow#1317 or Meeow-1317
# @return: dict of json response from api
# output only meant to be read by machine 
def get_full_stats(btag: str) -> dict:
    def format_btag(btag: str) -> str:
        btag = btag.replace('#', '-')
        return btag
    
    # @param btag: string that is checked for proper btag format
    # @return: false if not btag, true if possibly a valid btag
    # use https://us.battle.net/support/en/article/26963 for BattleTag Naming Policy
    def validate_btag(btag: str) -> bool:
        return True
        # TODO: test this better
        btag_regex = "^([^(.^$*+?(){}\\\\|?`~!@#%&\-_=;:'\"<>,/)0-9]){3,12}\-\d{4,5}$"
        if (re.search(btag_regex, btag) and not btag[0].isdigit()):
            return True
        else:
            return False

    btag = format_btag(btag)

    # invalid btag
    if not validate_btag(btag):
        raise ValueError
    
    api_url_prototype = 'https://ovrstat.com/stats/pc/{}'
    api_url = api_url_prototype.format(btag)

    response = requests.get(api_url).text
    result = json.loads(response)

    return result

# @param btag: battletag in format Meeow#1317 or Meeow-1317
# @param top_heroes: number of most played heroes to return
# @return: SR and stats for top most played heroes
def get_summary_stats(btag: str, top_heroes: int=5) -> dict:

    full_stats = get_full_stats(btag)
    summary_stats = {}
    summary_hero_stats = {}

    # add btag and icon
    summary_stats['name'] = full_stats['name']
    summary_stats['icon'] = full_stats['icon']

    # handle private profile
    if full_stats["private"]:
        summary_stats['error'] = "private profile"
        return summary_stats

    # handle accounts without comp stats
    if not full_stats["ratings"] and full_stats['competitiveStats']['careerStats']:
        summary_stats['error'] = "no competitive stats"
        return summary_stats

    # add sr per role
    ratings = full_stats['ratings']
    summary_stats['ratings'] = {}
    for rating in ratings:
        summary_stats['ratings'][rating['role']] = rating['level']
    
    # add competitive stats 
    hero_stats = full_stats['competitiveStats']['careerStats']
    for hero in hero_stats:
        hero_stat = hero_stats[hero]
        average_stats = hero_stat['average']
        # edge cases
        if not average_stats or hero == 'allHeroes':
            continue
        average_stats.update(hero_stat['game'])
        # only add stats that match keywords
        summary_hero_stats[hero] = {k:(average_stats[k] if k in average_stats else "N/A") for k in STAT_KEYWORDS}

    # find most played heroes
    hero_times = {k: int(summary_hero_stats[k]["timePlayed"].replace(':','')) for k, _ in summary_hero_stats.items()}
    hero_sorted = sorted(hero_times.items(), key=lambda item: item[1], reverse=True)[:top_heroes]
    top_hero_list = [hero[0] for hero in hero_sorted]
    top_hero_stats = [{hero: summary_hero_stats[hero]} for hero in top_hero_list]

    # nest the hero stats dict inside main stats dict
    summary_stats['heroStats'] = top_hero_stats

    return summary_stats


# manual testing
if __name__ == "__main__":
    from pprint import pprint as print
    
    btag = "Mystx#1209" #HachiYuki#4141"
    test = get_summary_stats(btag)
    #test = get_full_stats(btag)
    print(test)
