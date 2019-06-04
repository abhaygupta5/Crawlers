import pymongo

from items import QuestionItem


class SpiderConfig(object):
    DATABASE_NAME = 'IndiaBix'
    CONFIGURATION_COLLECTION_NAME = 'configuration'
    DEFAULT_DIFFICULTY = ''

    def __init__(self, spider_name):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        self.spider_name = spider_name
        db = self.conn[self.DATABASE_NAME]
        self.collection = db[self.CONFIGURATION_COLLECTION_NAME]
        self.starting_urls = []
        self.difficulty_level = {}
        self.question_type = {}
        self.answer_type = {}
        self.category = {}

    def save_initial_data(self):
        pass

    def load_configs(self):
        self.web_configs = self.collection.find_one({'spider_name': self.spider_name})
        self.num_of_threads = self.web_configs['num_of_threads']
        self.delay = self.web_configs['delay']


        web_url_objects = self.web_configs['web_pages']
        for web_obj in web_url_objects:
            self.difficulty_level[web_obj['url']] = web_obj['difficulty_level']
            self.question_type[web_obj['url']] = web_obj['question_type']
            self.answer_type[web_obj['url']] = web_obj['answer_type']
            self.category[web_obj['url']] = web_obj['category']
            if web_obj['enable_crawling']:
                self.starting_urls.append(web_obj['url'])
        return self

    def get_category(self,url,default):
        if url in self.category:
            return self.category[url]
        return default

    def get_num_of_threads(self):
        return self.num_of_threads

    def get_delay(self):
        return self.delay

    def get_starting_urls(self):
        return self.starting_urls

    def get_difficulty_level(self, url,default):
        if url in self.difficulty_level:
            return self.difficulty_level[url]
        return default

    def get_question_type(self, url, default):
        if url in self.question_type:
            return self.question_type[url]
        return default

    def get_answer_type(self, url,default):
        if url in self.answer_type:
            return self.answer_type[url]
        return default


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
            'num_of_threads': 20,
            'delay': 2,
            'web_pages': [

                {
                    'url': 'https://www.youtube.com/playlist?list=PL4BrNFx1j7E6a6IKg8N0IgnkoamHlCHWa',
                    'enable_crawling': True,
                    'category': 'Disney Songs',
                    'status': 'NOT STARTED',
                    'difficulty_level': QuestionItem.DIFFICULTY_LEVEL_EASY,
                    'question_type': QuestionItem.QUESTION_TYPE_VIDEO_BASED,
                    'answer_type': QuestionItem.ANSWER_TYPE_SINGLE_CORRECT
                },

                {
                    'url': 'https://www.youtube.com/playlist?list=PL9oqVauEE2LIXtGYECl3wT1f5ae5EwDEZ',
                    'enable_crawling': True,
                    'category': 'Bollywood songs',
                    'status': 'NOT STARTED',
                    'difficulty_level': QuestionItem.DIFFICULTY_LEVEL_EASY,
                    'question_type': QuestionItem.QUESTION_TYPE_VIDEO_BASED,
                    'answer_type': QuestionItem.ANSWER_TYPE_SINGLE_CORRECT

                },

                {
                    'url': 'https://www.youtube.com/playlist?list=PLKwnFQ15q7BQYqPTSOU4OjDpMx7xg6ula',
                    'enable_crawling': True,
                    'category': 'Inspiring Movies',
                    'status': 'NOT STARTED',
                    'difficulty_level': QuestionItem.DIFFICULTY_LEVEL_EASY,
                    'question_type': QuestionItem.QUESTION_TYPE_VIDEO_BASED,
                    'answer_type': QuestionItem.ANSWER_TYPE_SINGLE_CORRECT

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
            'num_of_threads': 20,
            'delay': 2,
            'web_pages': [

                {
                    'url': 'https://www.jetpunk.com/quizzes/country-flag-1',
                    'enable_crawling': True,
                    'category': 'Country Flag',
                    'status': 'NOT STARTED',
                    'difficulty_level': QuestionItem.DIFFICULTY_LEVEL_EASY,
                    'question_type': QuestionItem.QUESTION_TYPE_IMAGE_BASED,
                    'answer_type': QuestionItem.ANSWER_TYPE_SINGLE_CORRECT

                },

                {
                    'url': 'https://www.jetpunk.com/user-quizzes/139806/brand-logos-quiz-1',
                    'enable_crawling': True,
                    'category': 'Brand',
                    'status': 'NOT STARTED',
                    'difficulty_level': QuestionItem.DIFFICULTY_LEVEL_EASY,
                    'question_type': QuestionItem.QUESTION_TYPE_IMAGE_BASED,
                    'answer_type': QuestionItem.ANSWER_TYPE_SINGLE_CORRECT

                },
                {
                    'url': 'https://www.jetpunk.com/user-quizzes/139806/car-logos-quiz',
                    'enable_crawling': True,
                    'category': 'Cars',
                    'status': 'NOT STARTED',
                    'difficulty_level': QuestionItem.DIFFICULTY_LEVEL_EASY,
                    'question_type': QuestionItem.QUESTION_TYPE_IMAGE_BASED,
                    'answer_type': QuestionItem.ANSWER_TYPE_SINGLE_CORRECT

                },

                {
                    'url': 'https://www.jetpunk.com/user-quizzes/139806/brand-logos-quiz-2',
                    'enable_crawling': True,
                    'category': 'Brand',
                    'status': 'NOT STARTED',
                    'difficulty_level': QuestionItem.DIFFICULTY_LEVEL_EASY,
                    'question_type': QuestionItem.QUESTION_TYPE_IMAGE_BASED,
                    'answer_type': QuestionItem.ANSWER_TYPE_SINGLE_CORRECT
                },

                {
                    'url': 'https://www.jetpunk.com/quizzes/car-logos-quiz-2',
                    'enable_crawling': True,
                    'category': 'Cars',
                    'status': 'NOT STARTED',
                    'difficulty_level': QuestionItem.DIFFICULTY_LEVEL_EASY,
                    'question_type': QuestionItem.QUESTION_TYPE_IMAGE_BASED,
                    'answer_type': QuestionItem.ANSWER_TYPE_SINGLE_CORRECT
                },

                {
                    'url': 'https://www.jetpunk.com/quizzes/random-logos-quiz',
                    'enable_crawling': True,
                    'category': 'Random',
                    'status': 'NOT STARTED',
                    'difficulty_level': QuestionItem.DIFFICULTY_LEVEL_EASY,
                    'question_type': QuestionItem.QUESTION_TYPE_IMAGE_BASED,
                    'answer_type': QuestionItem.ANSWER_TYPE_SINGLE_CORRECT
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
            'num_of_threads': 20,
            'delay': 2,
            'web_pages': [

                {
                    'url': 'https://www.indiabix.com/general-knowledge/basic-general-knowledge/005001',
                    'enable_crawling': True,
                    'category': 'General Knowledge',
                    'status': 'NOT STARTED',
                    'difficulty_level': QuestionItem.DIFFICULTY_LEVEL_EASY,
                    'question_type': QuestionItem.QUESTION_TYPE_TEXT_BASED,
                    'answer_type': QuestionItem.ANSWER_TYPE_SINGLE_CORRECT
                },

                {
                    'url': 'https://www.indiabix.com/general-knowledge/general-science/036001',
                    'enable_crawling': True,
                    'category': 'General Science',
                    'status': 'NOT STARTED',
                    'difficulty_level': QuestionItem.DIFFICULTY_LEVEL_EASY,
                    'question_type': QuestionItem.QUESTION_TYPE_TEXT_BASED,
                    'answer_type': QuestionItem.ANSWER_TYPE_SINGLE_CORRECT
                },
                {
                    'url': 'https://www.indiabix.com/general-knowledge/indian-politics/002001',
                    'enable_crawling': True,
                    'category': 'Indian Politics',
                    'status': 'NOT STARTED',
                    'difficulty_level': QuestionItem.DIFFICULTY_LEVEL_EASY,
                    'question_type': QuestionItem.QUESTION_TYPE_TEXT_BASED,
                    'answer_type': QuestionItem.ANSWER_TYPE_SINGLE_CORRECT
                },

                {
                    'url': 'https://www.indiabix.com/general-knowledge/books-and-authors/031001',
                    'enable_crawling': True,
                    'category': 'Books and Authors',
                    'status': 'NOT STARTED',
                    'difficulty_level': QuestionItem.DIFFICULTY_LEVEL_EASY,
                    'question_type': QuestionItem.QUESTION_TYPE_TEXT_BASED,
                    'answer_type': QuestionItem.ANSWER_TYPE_SINGLE_CORRECT
                },

                {
                    'url': 'https://www.indiabix.com/general-knowledge/sports/012001',
                    'enable_crawling': True,
                    'category': 'Sports',
                    'status': 'NOT STARTED',
                    'difficulty_level': QuestionItem.DIFFICULTY_LEVEL_EASY,
                    'question_type': QuestionItem.QUESTION_TYPE_TEXT_BASED,
                    'answer_type': QuestionItem.ANSWER_TYPE_SINGLE_CORRECT
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
            'num_of_threads': 20,
            'delay': 0,
            'web_pages': [

                {
                    'url': 'https://www.indiabix.com/verbal-reasoning/logical-sequence-of-words/053001',
                    'enable_crawling': True,
                    'category': 'Verbal',
                    'status': 'NOT STARTED',
                    'difficulty_level': QuestionItem.DIFFICULTY_LEVEL_EASY,
                    'question_type': QuestionItem.QUESTION_TYPE_TEXT_BASED,
                    'answer_type': QuestionItem.ANSWER_TYPE_ARRANGE_THE_ORDER
                },

                {
                    'url': 'https://www.indiabix.com/verbal-reasoning/logical-sequence-of-words/070001',
                    'enable_crawling': True,
                    'category': 'Verbal',
                    'status': 'NOT STARTED',
                    'difficulty_level': QuestionItem.DIFFICULTY_LEVEL_EASY,
                    'question_type': QuestionItem.QUESTION_TYPE_TEXT_BASED,
                    'answer_type': QuestionItem.ANSWER_TYPE_ARRANGE_THE_ORDER

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
            'num_of_threads': 20,
            'delay': 2,
            'web_pages': [

                {
                    'url': 'https://www.avatto.com/general-knowledge/questions/mcqs/kbc/answers/285/1.html',
                    'enable_crawling': True,
                    'category': 'Random',
                    'status': 'NOT STARTED',
                    'difficulty_level': QuestionItem.DIFFICULTY_LEVEL_EASY,
                    'question_type': QuestionItem.QUESTION_TYPE_TEXT_BASED,
                    'answer_type': QuestionItem.ANSWER_TYPE_SINGLE_CORRECT
                },
                {
                    'url': 'https://www.avatto.com/general-knowledge/questions/mcqs/countries/answers/282/1.html',
                    'enable_crawling': True,
                    'category': 'Random',
                    'status': 'NOT STARTED',
                    'difficulty_level': QuestionItem.DIFFICULTY_LEVEL_EASY,
                    'question_type': QuestionItem.QUESTION_TYPE_TEXT_BASED,
                    'answer_type': QuestionItem.ANSWER_TYPE_SINGLE_CORRECT
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
            'num_of_threads': 20,
            'delay': 2,
            'web_pages': [

                {
                    'url': 'https://www.quizmasters.biz/DB/Audio/National%20Anthems/National%20Anthems.html',
                    'enable_crawling': True,
                    'category': 'National Anthem',
                    'status': 'NOT STARTED',
                    'difficulty_level': QuestionItem.DIFFICULTY_LEVEL_EASY,
                    'question_type': QuestionItem.QUESTION_TYPE_AUDIO_BASED,
                    'answer_type': QuestionItem.ANSWER_TYPE_SINGLE_CORRECT
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
            'num_of_threads': 20,
            'delay': 2,
            'web_pages': [

                {
                    'url': 'https://www.quizmasters.biz/DB/Audio/Movie%20Themes/Movie%20Themes.html',
                    'enable_crawling': True,
                    'category': 'Movies',
                    'status': 'NOT STARTED',
                    'difficulty_level': QuestionItem.DIFFICULTY_LEVEL_EASY,
                    'question_type': QuestionItem.QUESTION_TYPE_AUDIO_BASED,
                    'answer_type': QuestionItem.ANSWER_TYPE_SINGLE_CORRECT
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
             AvattoSpiderConf('AvattoSpider'), AudioQuizSpiderConf('AudioQuizSpider'),
             MovieThemeSpiderConf('MovieThemeSpider')]

    for conf in confs:
        conf.save_initial_data()
