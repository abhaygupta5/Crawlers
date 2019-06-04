
'''
Run this file to start all the spiders.

TODO : bug : csv files are not getting created

'''

#
# import scrapy
# from twisted.internet import reactor
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
#
# from CrawlBot.CrawlBot.spiders.AudioQuizSpider import AudioQuizSpider
# from CrawlBot.CrawlBot.spiders.AvattoSpider import AvattoSpider
# from CrawlBot.CrawlBot.spiders.IndiaBixSpider import IndiaBixSingleSpider
#
# from CrawlBot.CrawlBot.spiders.JetpunkSpider import JetpunkSpider
# from CrawlBot.CrawlBot.spiders.YoutubePlaylistScrapper import YoutubePlaylistSpider
#
#
#
#
# configure_logging()
# runner = CrawlerRunner()
# runner.crawl(IndiaBixSingleSpider)
# runner.crawl(JetpunkSpider)
# runner.crawl(AvattoSpider)
# runner.crawl(AudioQuizSpider)
# runner.crawl(YoutubePlaylistSpider)
#
# d = runner.join()
# d.addBoth(lambda _: reactor.stop())
#
# reactor.run() # the script will block here until all crawling jobs are finished