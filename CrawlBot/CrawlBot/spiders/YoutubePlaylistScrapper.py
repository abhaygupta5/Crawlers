from ..items import QuestionItem

import scrapy
import random
import re

from selenium import webdriver


class YoutubePlaylistSpider(scrapy.Spider):
    name = "YoutubePlaylistSpider"
    start_urls = ['https://www.youtube.com/playlist?list=PL9oqVauEE2LIXtGYECl3wT1f5ae5EwDEZ']
    path = "/Users/abhaygupta/Desktop/chromedriver"


    def parse(self, response):
        selenium_options = webdriver.ChromeOptions()
        selenium_options.add_argument('headless')
        driver = webdriver.Chrome(self.path, chrome_options=selenium_options)

        try:
            driver.get(response.url)
            links = driver.find_elements_by_xpath('//*[@id="content"]/a')
            titles = driver.find_elements_by_xpath('//*[@id="video-title"]')

            titles = [re.split('[|-]', t.text)[0] for t in titles]
            # titles = [t.text.split('|')[0] for t in titles]
            links = [l.get_attribute('href') for l in links]
            driver.close()

        except Exception, e:
            print('Error occured', e.message)
            driver.close()

        NUM_OF_SONGS = len(titles)
        option_a_list = titles
        option_b_list = titles[1:] + titles[:1]
        option_c_list = titles[2:] + titles[:2]

        print(option_a_list)
        print(option_b_list)
        print(option_c_list)

        correct_answer_index_list = [0 for i in range(NUM_OF_SONGS)]

        for i in range(NUM_OF_SONGS):

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
            correct_answer_index_list[i] = correct_answer_index_list[
                                               i] + 1  # index starts with 0 here...changing it to start at 1
            question_item = QuestionItem()

            question_item['question_text'] = 'Identify the song ?'
            question_item['answer_1'] = option_a_list[i]
            question_item['answer_2'] = option_b_list[i]
            question_item['answer_3'] = option_c_list[i]
            question_item['answer_type'] = QuestionItem.ANSWER_TYPE_SINGLE_CORRECT
            question_item['question_type'] = QuestionItem.QUESTION_TYPE_VIDEO_BASED
            if correct_answer_index_list[i] == 1:
                question_item['right_answer'] = "A"
            elif correct_answer_index_list[i] == 2:
                question_item['right_answer'] = "B"
            elif correct_answer_index_list[i] == 3:
                question_item['right_answer'] = "C"
            question_item['difficulty_level'] = QuestionItem.DIFFICULTY_LEVEL_EASY
            question_item['binary_file_path'] = links[i]

            yield question_item
