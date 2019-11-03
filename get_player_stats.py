import requests
import json

# TODO 
# Historical stats

# @param btag: battletag in format Meeow#1317 or Meeow-1317
# @return: dict of json response from api
# output only meant to be read by machine 
def get_full_stats(btag: str) -> dict:
    def format_btag(btag: str) -> str:
        btag = btag.replace('#', '-')
        return btag
    
    # TODO @super - try to use regex
    # @param btag: string that is checked for proper btag format
    # @return: false if not btag, true if possibly a valid btag
    def validate_btag(btag: str) -> bool:
        # truncates the btag id number from the btag (i.e. myname#1234 -> myname)
        if re.search("#\d+$", btag):
            name = re.sub("#\d+$", "", btag)
                
            is_within_length_limit = (3 <= len(name) <= 12)                
            starts_with_number = re.search("^\d" ,name)
            banned_characters = "[ .^$*+?(){}\\\\|?`~!@#%&\-_=;:'\"<>,/]"
            contains_banned_characters = re.findall(banned_characters, name)
                
            is_valid = is_within_length_limit and not starts_with_number and not contains_banned_characters
                
            return is_valid
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

# TODO: Implement top_heroes parameter @hachi
# You will need to sort by most played
# @param btag: battletag in format Meeow#1317 or Meeow-1317
# @param top_heroes: number of most played heroes to return
# @return: SR and top most played heroes
def get_summary_stats(btag: str, top_heroes: int=3) -> dict:
    full_stats = get_full_stats(btag)
    summary_stats = {}
    summary_hero_stats = {}

    # add btag
    summary_stats['name'] = full_stats['name']

    # handle private profile
    if full_stats["private"]:
        summary_stats['private'] = full_stats['private']
        return summary_stats

    # add sr per role
    ratings = full_stats['ratings']
    for rating in ratings:
        summary_stats[rating['role']] = rating['level']
    
    # add competitive stats 
    keywords = {
        'deathsAvgPer10Min', 
        'finalBlowsAvgPer10Min', 
        'heroDamageDoneAvgPer10Min',
        "winPercentage", 
        "timePlayed",
    }
    hero_stats = full_stats['competitiveStats']['careerStats']
    for hero in hero_stats:
        hero_stat = hero_stats[hero]
        average_stats = hero_stat['average']
        # edge case
        if not average_stats:
            continue
        average_stats.update(hero_stat['game'])
        # only add stats that match keywords
        summary_hero_stats[hero] = {k:v for k,v in average_stats.items() if k in keywords}
    
    # nest the hero stats dict inside main stats dict
    summary_stats['heroStats'] = summary_hero_stats

    return summary_stats


# manual testing
if __name__ == "__main__":
    from pprint import pprint as print
    
    btag = "Mystx#1209" #HachiYuki#4141"
    test = get_summary_stats(btag)
    test = get_full_stats(btag)
    print(test)

    btag = "Meeow#1317" #HachiYuki#4141"
    test = get_summary_stats(btag)
    #test = get_full_stats(btag)
    print(test)