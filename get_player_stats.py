import requests
import json

# @param btag: battletag in format Meeow#1317 or Meeow-1317
# @return: dict of json response from api
def get_stats(btag: str) -> dict:
    def format_btag(btag: str) -> str:
        btag = btag.replace('#', '-')
        return btag
    
    # TODO @super
    # @param btag: string that is checked for proper btag format
    # @return: false if not btag, true if possibly a valid btag
    def validate_btag(btag: str) -> bool:
        return True

    api_url_prototype = 'https://ovrstat.com/stats/pc/{}'

    btag = format_btag(btag)

    # Invalid btag
    if not validate_btag(btag):
        return {"error": "invalid btag"}
    
    api_url = api_url_prototype.format(btag)
    response = requests.get(api_url).text
    result = json.loads(response)

    return result

# manual testing
if __name__ == "__main__":
    from pprint import pprint as print
    
    btag = "Meeow#1317"
    test = get_stats(btag)
    print(test)
