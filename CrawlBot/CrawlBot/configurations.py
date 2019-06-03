import pymongo


class SpiderConfig(object):
    DATABASE_NAME = 'IndiaBix'
    CONFIGURATION_COLLECTION_NAME = 'configuration'

    def __init__(self, spider_name):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        self.spider_name = spider_name
        db = self.conn[self.DATABASE_NAME]
        self.collection = db[self.CONFIGURATION_COLLECTION_NAME]
        self.starting_urls = []

    def save_initial_data(self):
        pass

    def load_configs(self):
        self.web_configs = self.collection.find_one({'spider_name': self.spider_name})
        web_url_objects = self.web_configs['web_pages']
        for web_obj in web_url_objects:
            if web_obj['enable_crawling']:
                self.starting_urls.append(web_obj['url'])
        return self

    def get_starting_urls(self):
        return self.starting_urls

    def set_status(self, url, status):
        web_url_objects = self.web_configs['web_pages']
        for web_obj in web_url_objects:
            if web_obj['url'] == url:
                web_obj['status'] = status
                break

        self.collection.update({'_id': self.spider_name}, self.web_configs)
        print('--------->UPDATING STATUS')


class YoutubePlaylistSpiderConfig(SpiderConfig):

    def __init__(self, spider_name):
        super(YoutubePlaylistSpiderConfig, self).__init__(spider_name)

    def save_initial_data(self):
        # self.collection.create_index([('spider_name', pymongo.TEXT)], name="spider_index")

        data = {
            'spider_name': self.spider_name,
            'web_pages': [

                {
                    'url': 'https://www.youtube.com/playlist?list=PL9oqVauEE2LIXtGYECl3wT1f5ae5EwDEZ',
                    'enable_crawling': True,
                    'category': 'Bollywood songs',
                    'status': 'NOT STARTED'
                },

                {
                    'url': 'https://www.youtube.com/playlist?list=PLKwnFQ15q7BQYqPTSOU4OjDpMx7xg6ula',
                    'enable_crawling': True,
                    'category': 'Inspiring Movies',
                    'status': 'NOT STARTED'
                }

            ],

        }

        self.collection.update({'_id': self.spider_name}, dict(data), upsert=True)

    def get_video_start_time(self):
        return 100;


class JetpunkSpiderConf(SpiderConfig):

    def __init__(self, spider_name):
        super(JetpunkSpiderConf, self).__init__(spider_name)

    def save_initial_data(self):
        # self.collection.create_index([('spider_name', pymongo.TEXT)], name="spider_index")

        data = {
            'spider_name': self.spider_name,
            'web_pages': [

                {
                    'url': 'https://www.jetpunk.com/quizzes/country-flag-1',
                    'enable_crawling': True,
                    'category': '',
                    'status': 'NOT STARTED'
                },

                {
                    'url': 'https://www.jetpunk.com/user-quizzes/139806/brand-logos-quiz-1',
                    'enable_crawling': True,
                    'category': '',
                    'status': 'NOT STARTED'
                },
                {
                    'url': 'https://www.jetpunk.com/user-quizzes/139806/car-logos-quiz',
                    'enable_crawling': True,
                    'category': '',
                    'status': 'NOT STARTED'
                },

                {
                    'url': 'https://www.jetpunk.com/user-quizzes/139806/brand-logos-quiz-2',
                    'enable_crawling': True,
                    'category': '',
                    'status': 'NOT STARTED'
                },

                {
                    'url': 'https://www.jetpunk.com/quizzes/car-logos-quiz-2',
                    'enable_crawling': True,
                    'category': '',
                    'status': 'NOT STARTED'
                },

                {
                    'url': 'https://www.jetpunk.com/quizzes/random-logos-quiz',
                    'enable_crawling': True,
                    'category': '',
                    'status': 'NOT STARTED'
                }

            ]

        }

        self.collection.update({'_id': self.spider_name}, dict(data), upsert=True)


class IndiaBixSingleSpiderConfig(SpiderConfig):

    def __init__(self, spider_name):
        super(IndiaBixSingleSpiderConfig, self).__init__(spider_name)

    def save_initial_data(self):
        # self.collection.create_index([('spider_name', pymongo.TEXT)], name="spider_index")
        data = {
            'spider_name': self.spider_name,
            'web_pages': [

                {
                    'url': 'https://www.indiabix.com/general-knowledge/basic-general-knowledge/005001',
                    'enable_crawling': True,
                    'category': '',
                    'status': 'NOT STARTED'
                },

                {
                    'url': 'https://www.indiabix.com/general-knowledge/general-science/036001',
                    'enable_crawling': True,
                    'category': '',
                    'status': 'NOT STARTED'
                },
                {
                    'url': 'https://www.indiabix.com/general-knowledge/indian-politics/002001',
                    'enable_crawling': True,
                    'category': '',
                    'status': 'NOT STARTED'
                },

                {
                    'url': 'https://www.indiabix.com/general-knowledge/books-and-authors/031001',
                    'enable_crawling': True,
                    'category': '',
                    'status': 'NOT STARTED'
                },

                {
                    'url': 'https://www.indiabix.com/general-knowledge/sports/012001',
                    'enable_crawling': True,
                    'category': '',
                    'status': 'NOT STARTED'
                }

            ]

        }

        self.collection.update({'_id': self.spider_name}, dict(data), upsert=True)


class IndiaBixArrangeSpiderConfig(SpiderConfig):

    def __init__(self, spider_name):
        super(IndiaBixArrangeSpiderConfig, self).__init__(spider_name)

    def save_initial_data(self):
        # self.collection.create_index([('spider_name', pymongo.TEXT)], name="spider_index")
        data = {
            'spider_name': self.spider_name,
            'web_pages': [

                {
                    'url': 'https://www.indiabix.com/verbal-reasoning/logical-sequence-of-words/053001',
                    'enable_crawling': True,
                    'category': '',
                    'status': 'NOT STARTED'
                },

                {
                    'url': 'https://www.indiabix.com/verbal-reasoning/logical-sequence-of-words/070001',
                    'enable_crawling': True,
                    'category': '',
                    'status': 'NOT STARTED'

                }

            ]

        }

        self.collection.update({'_id': self.spider_name}, dict(data), upsert=True)


class AvattoSpiderConf(SpiderConfig):

    def __init__(self, spider_name):
        super(AvattoSpiderConf, self).__init__(spider_name)

    def save_initial_data(self):
        # self.collection.create_index([('spider_name', pymongo.TEXT)], name="spider_index")
        data = {
            'spider_name': self.spider_name,
            'web_pages': [

                {
                    'url': 'https://www.avatto.com/general-knowledge/questions/mcqs/kbc/answers/285/1.html',
                    'enable_crawling': True,
                    'category': '',
                    'status': 'NOT STARTED'
                },
                {
                    'url': 'https://www.avatto.com/general-knowledge/questions/mcqs/countries/answers/282/1.html',
                    'enable_crawling': True,
                    'category': '',
                    'status': 'NOT STARTED'
                }

            ]

        }

        self.collection.update({'_id': self.spider_name}, dict(data), upsert=True)


class AudioQuizSpiderConf(SpiderConfig):

    def __init__(self, spider_name):
        super(AudioQuizSpiderConf, self).__init__(spider_name)

    def save_initial_data(self):
        # self.collection.create_index([('spider_name', pymongo.TEXT)], name="spider_index")
        data = {
            'spider_name': self.spider_name,
            'web_pages': [

                {
                    'url': 'https://www.quizmasters.biz/DB/Audio/National%20Anthems/National%20Anthems.html',
                    'enable_crawling': True,
                    'category': '',
                    'status': 'NOT STARTED'
                }

            ]

        }

        self.collection.update({'_id': self.spider_name}, dict(data), upsert=True)


class MovieThemeSpiderConf(SpiderConfig):

    def __init__(self, spider_name):
        super(MovieThemeSpiderConf, self).__init__(spider_name)

    def save_initial_data(self):
        # self.collection.create_index([('spider_name', pymongo.TEXT)], name="spider_index")
        data = {
            'spider_name': self.spider_name,
            'web_pages': [

                {
                    'url': 'https://www.quizmasters.biz/DB/Audio/Movie%20Themes/Movie%20Themes.html',
                    'enable_crawling': True,
                    'category': '',
                    'status': 'NOT STARTED'
                }

            ]

        }

        self.collection.update({'_id': self.spider_name}, dict(data), upsert=True)



if __name__ == '__main__':

    '''
    Run this program to save the initial configurations to a fresh database
    
    '''

    confs = [IndiaBixArrangeSpiderConfig('IndiaBixArrangeSpider'), IndiaBixSingleSpiderConfig('IndiaBixSingleSpider'),
             YoutubePlaylistSpiderConfig('YoutubePlaylistSpider'), JetpunkSpiderConf('JetpunkSpider'),
             AvattoSpiderConf('AvattoSpider'), AudioQuizSpiderConf('AudioQuizSpider'), MovieThemeSpiderConf('MovieThemeSpider')]

    for conf in confs:
        conf.save_initial_data()
