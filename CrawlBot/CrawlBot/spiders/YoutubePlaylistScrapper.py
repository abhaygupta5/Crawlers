from ..items import QuestionItem
from ..configurations import YoutubePlaylistSpiderConfig
import scrapy
import random
import re
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import requests
from selenium import webdriver
from ..settings import URL_TO_SEND


class YoutubePlaylistSpider(scrapy.Spider):
    name = "YoutubePlaylistSpider"

    def __init__(self, filename='', **kwargs):
        self.fileName = filename
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        super(YoutubePlaylistSpider, self).__init__(**kwargs)

    def spider_closed(self, spider):
        multipart_form_data = {
            'file': (self.fileName, open(self.fileName, 'rb')),
        }
        response = requests.post(URL_TO_SEND, files=multipart_form_data)
        print(response.text)
        print("ENDING OF SPIDER")

    conf = YoutubePlaylistSpiderConfig(name).load_configs()
    start_urls = conf.get_starting_urls()
    custom_settings = {
        'DOWNLOAD_DELAY': conf.delay,
        'CONCURRENT_REQUESTS': conf.num_of_threads
    }
    path = 'chromedriver'
    XPATH_LINKS = '//*[@id="content"]/a'
    XPATH_TITLES = '//*[@id="video-title"]'
    XPATH_CATEGORY = '//*[(@id = "title")]//*[contains(concat( " ", @class, " " ), concat( " ", "yt-formatted-string", " " ))]'


    default_difficulty_level = ''
    default_category = ''
    default_question_type = ''
    default_answer_type = ''

    def parse(self, response):
        selenium_options = webdriver.ChromeOptions()
        selenium_options.add_argument('headless')
        driver = webdriver.Chrome(executable_path=self.path, chrome_options=selenium_options)

        try:
            difficulty_level = self.conf.get_difficulty_level(response.url, self.default_difficulty_level)
            category = self.conf.get_category(response.url, self.default_category)
            question_type = self.conf.get_question_type(response.url, self.default_question_type)
            answer_type = self.conf.get_answer_type(response.url, self.default_answer_type)

            self.default_difficulty_level = difficulty_level
            self.default_category = category
            self.default_question_type = question_type
            self.default_answer_type = answer_type

            driver.get(response.url)
            self.conf.set_status(response.url, 'STARTED')
            links = driver.find_elements_by_xpath(self.XPATH_LINKS)
            titles = driver.find_elements_by_xpath(self.XPATH_TITLES)
            category = driver.find_element_by_xpath(self.XPATH_CATEGORY).text
            category = re.split('[|]', category)[0]

            titles = [re.split('[|-]', t.text)[0] for t in titles]
            titles = [t.replace('"', '') for t in titles]
            # titles = [t.text.split('|')[0] for t in titles]
            links = [l.get_attribute('href') for l in links]

            self.conf.set_status(response.url, 'SUCCESS')
            driver.close()

        except Exception, e:
            print('Error occured', e.message)
            self.conf.set_status(response.url, 'ERROR ' + e.message)
            driver.close()

        num_of_songs = len(titles)
        option_a_list = titles
        option_b_list = titles[1:] + titles[:1]
        option_c_list = titles[2:] + titles[:2]

        print(option_a_list)
        print(option_b_list)
        print(option_c_list)

        correct_answer_index_list = [0 for i in range(num_of_songs)]

        for i in range(num_of_songs):

            '''
            shuffling the answers keeping track of the correct answer in the correct_answer_index_list
            '''

            random_index = random.randint(0, 3)

            if random_index == 1:
                option_a_list[i], option_b_list[i] = option_b_list[i], option_a_list[i]
                correct_answer_index_list[i] = 1

            elif random_index == 2:
                option_a_list[i], option_c_list[i] = option_c_list[i], option_a_list[i]
                correct_answer_index_list[i] = 2

            '''
            Wrapping into item container

            '''

            question_item = QuestionItem()

            question_item['question_text'] = 'Identify : ' + category
            question_item['answer_1'] = option_a_list[i]
            question_item['answer_2'] = option_b_list[i]
            question_item['answer_3'] = option_c_list[i]

            question_item['right_answer'] = chr(ord('A') + correct_answer_index_list[i])
            question_item['binary_file_path'] = links[i]

            question_item['question_type'] = question_type
            question_item['answer_type'] = answer_type
            question_item['difficulty_level'] = difficulty_level
            question_item['category'] = category

            yield question_item
