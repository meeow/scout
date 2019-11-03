import scrapy
import datetime
import logging
from urllib.request import urlopen
from urllib.parse import quote    
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy import Request
from scrapy.spiders import Spider
from twisted.internet import reactor
from twisted.internet.task import deferLater

logging.getLogger('scrapy').propagate = False

# Must be manually updated every season
BASE_URL = 'https://compete.tespa.org'
TOURNAMENT_URL = BASE_URL + '/tournament/145'

leaderboard_path = './scrapes/tespa_leaderboard.csv'
teams_path = './scrapes/tespa_teams.csv'

class CollectLeaderboard(Spider):
    name = "leaderboard"
    allowed_domains = ["tespa.org"]
    start_urls = [TOURNAMENT_URL + "/leaderboard"]
    custom_settings = {
            'DOWNLOAD_DELAY': 0.05,
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'FEED_FORMAT': 'csv',
            'FEED_URI': leaderboard_path
           }

    def parse(self, response):
        names = response.xpath("//table/tbody/tr")
        ans=[]
        for name in names:
            item = {}
            item['rank'] = name.xpath('td[1]/text()').extract()
            item['team_name'] = name.xpath("td/a/span/text()").extract()
            item['team_url'] = name.xpath("td/a/@href").extract()
            item['rating'] = name.xpath("td[3]/text()").extract()
            item['timestamp'] = datetime.datetime.now()
            if item['team_url']:
                item['team_url'] = [item['team_url'][0].replace('../../..', BASE_URL)]
                req = Request((str(item['team_url'][0])), callback=self.parse_team_page)
                req.meta['team_page'] = item
                ans.append(req)
        return ans

    def parse_team_page(self, response):
        it = response.meta['team_page']
        btag = response.xpath('//div/table/tbody/tr/td[3]/text()').extract()
        it['btag'] = btag
        return it   

class CollectTeams(Spider):
    name = "teams"
    allowed_domains = ["tespa.org"]
    # TODO: Do not hardcode the page range
    start_urls = [TOURNAMENT_URL + "/registrants?page={}".format(i) for i in range(1,27)]
    custom_settings = {
            'DOWNLOAD_DELAY': 0.1,
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'FEED_FORMAT': 'csv',
            'FEED_URI': teams_path
           }

    def parse(self, response):
        names = response.xpath('//table/tbody/tr')
        ans=[]
        for name in names:
            item = {}
            item['team_name'] = name.xpath('td/a/text()').extract()
            item['team_school'] = name.xpath("td[4]/text()").extract()
            item['team_link_url'] = name.xpath("td/a/@href").extract()
            item['team_rank'] = name.xpath("td[@class='registrant-ranks']/text()").extract()
            if item['team_link_url']:
                req = Request((str(item['team_link_url'][0])), callback=self.parse_2)
                req.meta['foo'] = item
                ans.append(req)
        return ans

    def parse_2(self, response):
        it = response.meta['foo']
        btag = response.xpath('//div/table/tbody/tr/td[3]/text()').extract()
        it['btag'] = btag
        return it           
    

if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    deferred_leaderboard = process.crawl(CollectLeaderboard)
    #deferred_teams = process.crawl(CollectTeams)
    process.start()
