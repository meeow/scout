import requests
import json

# @param btag: battletag in format Meeow#1317 or Meeow-1317
# @return: dict of json response from api
def get_full_stats(btag: str) -> dict:
    def format_btag(btag: str) -> str:
        btag = btag.replace('#', '-')
        return btag
    
    # TODO @super - try to use regex
    # @param btag: string that is checked for proper btag format
    # @return: false if not btag, true if possibly a valid btag
    def validate_btag(btag: str) -> bool:
        return True

    btag = format_btag(btag)
    # Invalid btag
    if not validate_btag(btag):
        raise ValueError
    
    api_url_prototype = 'https://ovrstat.com/stats/pc/{}'
    api_url = api_url_prototype.format(btag)

    response = requests.get(api_url).text
    result = json.loads(response)

    return result

# @param btag: battletag in format Meeow#1317 or Meeow-1317
# @return: SR and top 3 most played heroes
def get_summary_stats(btag: str) -> dict:
    full_stats = get_full_stats(btag)
    if full_stats["private"]:
        return {"error": "private profile"}
    else:
        summary_stats = {}
        ratings = full_stats['ratings']
        for rating in ratings:
            summary_stats[rating['role']] = rating['level']
        return summary_stats

# manual testing
if __name__ == "__main__":
    from pprint import pprint as print
    
    btag = "Mystx#1209" #HachiYuki#4141"
    test = get_summary_stats(btag)
    print(test)
