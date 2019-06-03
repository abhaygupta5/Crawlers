from scrapy.statscollectors import StatsCollector


class MyStatsCollector(StatsCollector):
    def _persist_stats(self, stats, spider):
        print("ENDING HERE")