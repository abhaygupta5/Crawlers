import pymongo


class SpiderConfig(object):
    DATABASE_NAME = 'IndiaBix'
    CONFIGURATION_COLLECTION_NAME = 'configuration'

    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        db = self.conn[self.DATABASE_NAME]
        self.collection = db[self.CONFIGURATION_COLLECTION_NAME]

    def save_initial_data(self):
        pass

    def load_configs(self):
        raise Exception("NotImplementedException")


class YoutubePlaylistSpiderConfig(SpiderConfig):

    def __init__(self, spider_name):
        super(YoutubePlaylistSpiderConfig, self).__init__()
        self.categories = []
        self.starting_urls = []
        self.spider_name = spider_name

    def save_initial_data(self):
        # self.collection.create_index([('spider_name', pymongo.TEXT)], name="spider_index")

        data = {
            'spider_name': 'YoutubePlaylistSpider',
            'web_pages': [

                {
                    'url': 'https://www.youtube.com/playlist?list=PL9oqVauEE2LIXtGYECl3wT1f5ae5EwDEZ',
                    'enable_crawling': True,
                    'category': 'Bollywood songs'
                },

                {
                    'url': 'https://www.youtube.com/playlist?list=PLKwnFQ15q7BQYqPTSOU4OjDpMx7xg6ula',
                    'enable_crawling': True,
                    'category': 'Inspiring Movies'
                }

            ],

        }

        self.collection.update({'_id': self.spider_name}, dict(data), upsert=True)

    def load_configs(self):
        self.web_configs = self.collection.find_one({'spider_name': self.spider_name})
        web_url_objects = self.web_configs['web_pages']
        for web_obj in web_url_objects:
            if web_obj['enable_crawling']:
                self.starting_urls.append(web_obj['url'])
                self.categories.append(web_obj['category'])

    def get_starting_urls(self):
        return self.starting_urls

    def get_video_start_time(self):
        return 100;

    def set_status(self, url, status):
        web_url_objects = self.web_configs['web_pages']
        for web_obj in web_url_objects:
            if web_obj['url'] == url:
                web_obj['status'] = status
                break

        self.collection.update({'_id': self.spider_name}, self.web_configs)
        print('--------->UPDATING STATUS')


if __name__ == '__main__':
    conf = YoutubePlaylistSpiderConfig('YoutubePlaylistSpider')
    conf.save_initial_data()
    # print(conf.get_categories())
