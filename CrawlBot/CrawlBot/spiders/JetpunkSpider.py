import scrapy
from ..items import QuestionItem
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import math
import random
import time
import os

from ..configurations import JetpunkSpiderConf


class JetpunkSpider(scrapy.Spider):
    name = "JetpunkSpider"
    base_url = "https://www.jetpunk.com"
    conf = JetpunkSpiderConf(name).load_configs()
    start_urls = conf.get_starting_urls()
    path = "chromedriver"

    default_difficulty_level = ''
    default_category = ''
    default_question_type = ''
    default_answer_type = ''

    def parse(self, response):

        try:
            difficulty_level = self.conf.get_difficulty_level(response.url, self.default_difficulty_level)
            category = self.conf.get_category(response.url, self.default_category)
            question_type = self.conf.get_question_type(response.url, self.default_question_type)
            answer_type = self.conf.get_answer_type(response.url, self.default_answer_type)

            self.default_difficulty_level = difficulty_level
            self.default_category = category
            self.default_question_type = question_type
            self.default_answer_type = answer_type

            selenium_options = webdriver.ChromeOptions()
            selenium_options.add_argument('headless')
            driver = webdriver.Chrome(self.path, chrome_options=selenium_options)
            driver.get(response.url)
            difficulty_level = self.conf.get_difficulty_level(response.url)
            take_quiz = driver.find_element_by_xpath('//*[(@id = "start-button")]')
            take_quiz.click()

            number_of_questions = 0
            give_up = driver.find_element_by_xpath(
                '//*[contains(concat( " ", @class, " " ), concat( " ", "link-like", " " ))]')
            give_up.click()

            time.sleep(2)
            # print("page source",self.driver.getPageSource())
            html_response = HtmlResponse(url=response.url, body=driver.page_source, encoding='utf-8')

            page = Selector(response=html_response)

            print(page.css('title::text').extract())

            number_of_questions = len(page.css(".photo-img").xpath('@src').extract())
            # print("number_of_questions ", number_of_questions)

            question = response.css(".instructions::text").get()

            correct_answers = page.css('.answer-display::text').extract()

            print("correct ", correct_answers)
            # print("length of correct_answers ",len(correct_answers))

            # for answer in correct_answers:
            #     print(answer)

            # images
            images = page.css('.photo-img').xpath('@src').extract()
            for image in page.css('.photo-img').xpath('@src').extract():
                link = self.base_url + image
                # print(link)

            driver.close()
            self.conf.set_status(response.url,'SUCCESS')
        except Exception,e :
            number_of_questions = 0
            self.conf.set_status(response.url,'ERROR '+e.message)
            driver.close()

        # logic to filter

        for index in range(number_of_questions):
            difficulty_index = 0
            item = QuestionItem()
            item['question_text'] = question.strip()
            item['binary_file_path'] = self.base_url + images[index]
            item['_id'] = question+str(index)+images[index]

            item['question_type'] = question_type
            item['answer_type'] = answer_type
            item['difficulty_level'] = difficulty_level
            item['category'] = category

            random_correct_index = random.choice([1, 2, 3])

            right_answer = correct_answers[index]
            valid_answers = correct_answers[:]
            valid_answers.remove(right_answer)

            incorrect_answers = random.sample(valid_answers,2)

            if random_correct_index == 1:
                item['right_answer'] = 'A'
                item['answer_1'] = right_answer
                item['answer_2'] = incorrect_answers[0]
                item['answer_3'] = incorrect_answers[1]
            elif random_correct_index == 2:
                item['right_answer'] = 'B'
                item['answer_2'] = right_answer
                item['answer_1'] = incorrect_answers[0]
                item['answer_3'] = incorrect_answers[1]
            else:
                item['right_answer'] = 'C'
                item['answer_3'] = right_answer
                item['answer_1'] = incorrect_answers[0]
                item['answer_2'] = incorrect_answers[1]

            print("ITEM", item)
            yield item

        # nextPage = response.css('.mx-pager').xpath('./a[last()]/@href').get()
        # if nextPage is not None:
        #     nextPage = response.urljoin(nextPage)
        #     yield scrapy.Request(nextPage, callback=self.parse)