import scrapy
from ..items import QuestionItem
import math
import random
import re
import os
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import requests
from ..configurations import AvattoSpiderConf
from ..settings import URL_TO_SEND


class AvattoSpider(scrapy.Spider):
    name = "AvattoSpider"
    base_url = "https://www.avatto.com/general-knowledge/questions/mcqs/kbc/answers/285/"

    def __init__(self, filename='', **kwargs):
        self.fileName = filename
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        super(AvattoSpider, self).__init__(**kwargs)

    def spider_closed(self, spider):
        multipart_form_data = {
            'file': (self.fileName, open(self.fileName, 'rb')),
        }
        response = requests.post(URL_TO_SEND, files=multipart_form_data)
        print(response.text)
        print("ENDING OF SPIDER")

    conf = AvattoSpiderConf(name).load_configs()
    start_urls = conf.get_starting_urls()
    custom_settings = {
        'DOWNLOAD_DELAY': conf.delay,
        'CONCURRENT_REQUESTS': conf.num_of_threads
    }

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

            # question_numbers = len(response.css('.ques p::text').extract())
            questions = response.css('.ques').xpath("string(./p)").extract()
            questions = [re.sub(r"\s+", " ", question.strip().replace('\n', ' ')).replace('\"', '').replace("\'", "\\'")
                         for question in questions]
            options_A = response.css('tr:first_child td:nth-child(2) span p::text').extract()
            options_A = [option.strip().replace('\n', ' ').replace('\"', '').replace("\'", "\\'") for option in
                         options_A]
            options_B = response.css('tr:nth_child(2) td:nth-child(2) span p::text').extract()
            options_B = [option.strip().replace('\n', ' ').replace('\"', '').replace("\'", "\\'") for option in
                         options_B]
            options_C = response.css('tr:nth_child(3) td:nth-child(2) span p::text').extract()
            options_C = [option.strip().replace('\n', ' ').replace('\"', '').replace("\'", "\\'") for option in
                         options_C]
            options_D = response.css('tr:nth_child(4) td:nth-child(2) span p::text').extract()
            options_D = [option.strip().replace('\n', ' ').replace('\"', '').replace("\'", "\\'") for option in
                         options_D]

            # print(len(options_A), len(options_B), len(options_C), len(options_D))
            # print()
            # print(options_A)
            # print(options_B)
            # print(options_C)
            # print(options_D)
            correct_answers = []
            list1 = response.css('.panel-new p:nth-child(1)::text').extract()
            for i in range(len(response.css('.panel-new p:nth-child(1)::text').extract())):
                if(i%2==0):
                    correct_answers.append(list1[i])

            self.number_of_questions = len(response.css('.ques').xpath("string(./p)").extract())
            # print('NUMQUESTION', self.number_of_questions)
            # number_of_easy_questions = math.floor(0.5 * number_of_questions)
            # number_of_medium_questions = math.ceil(0.3 * number_of_questions)
            # number_of_difficult_questions = number_of_questions - number_of_easy_questions - number_of_medium_questions
            # index_of_easy = 0
            # index_of_medium = 0
            # index_of_hard = 0

            self.conf.set_status(response.url,'SUCCESS')
        except Exception,e :
            self.conf.set_status(response.url,'ERROR')
        # logic to filter

        for index in range(self.number_of_questions):
            difficulty_index = 0
            item = QuestionItem()
            # item['_id'] = questions[index]
            # print(item['_id'])
            item['question_text'] = questions[index]
            item['binary_file_path'] = None

            item['question_type'] = question_type
            item['answer_type'] = answer_type
            item['difficulty_level'] = difficulty_level
            item['category'] = category

            random_correct_index = random.choice([1,2,3])

            if str(correct_answers[index]) == "A":
                # item['right_answer'] = options_A[index]
                if random_correct_index == 1:
                    item['answer_1'] = options_A[index]
                    item['answer_2'] = options_B[index]
                    item['answer_3'] = options_C[index]
                    item['right_answer'] = "A"
                elif random_correct_index == 2:
                    item['answer_2'] = options_A[index]
                    item['answer_1'] = options_D[index]
                    item['answer_3'] = options_B[index]
                    item['right_answer'] = "B"
                else:
                    item['answer_3'] = options_A[index]
                    item['answer_1'] = options_C[index]
                    item['answer_2'] = options_D[index]
                    item['right_answer'] = "C"
            elif str(correct_answers[index]) == "B":
                # item['right_answer'] = options_B[index]
                if random_correct_index == 1:
                    item['answer_1'] = options_B[index]
                    item['answer_2'] = options_A[index]
                    item['answer_3'] = options_C[index]
                    item['right_answer'] = "A"
                elif random_correct_index == 2:
                    item['answer_2'] = options_B[index]
                    item['answer_1'] = options_D[index]
                    item['answer_3'] = options_A[index]
                    item['right_answer'] = "B"
                else:
                    item['answer_3'] = options_B[index]
                    item['answer_1'] = options_C[index]
                    item['answer_2'] = options_D[index]
                    item['right_answer'] = "C"
            elif str(correct_answers[index]) == "C":
                # item['right_answer'] = options_C[index]
                if random_correct_index == 1:
                    item['answer_1'] = options_C[index]
                    item['answer_2'] = options_B[index]
                    item['answer_3'] = options_A[index]
                    item['right_answer'] = "A"
                elif random_correct_index == 2:
                    item['answer_2'] = options_C[index]
                    item['answer_1'] = options_D[index]
                    item['answer_3'] = options_B[index]
                    item['right_answer'] = "B"
                else:
                    item['answer_3'] = options_C[index]
                    item['answer_1'] = options_A[index]
                    item['answer_2'] = options_D[index]
                    item['right_answer'] = "C"
            else:
                # item['right_answer'] = options_D[index]
                if random_correct_index == 1:
                    item['answer_1'] = options_D[index]
                    item['answer_2'] = options_B[index]
                    item['answer_3'] = options_C[index]
                    item['right_answer'] = "A"
                elif random_correct_index == 2:
                    item['answer_2'] = options_D[index]
                    item['answer_1'] = options_A[index]
                    item['answer_3'] = options_B[index]
                    item['right_answer'] = "B"
                else:
                    item['answer_3'] = options_D[index]
                    item['answer_1'] = options_C[index]
                    item['answer_2'] = options_A[index]
                    item['right_answer'] = "C"

            print(item)
            yield item

        # nextPage = response.css('.pagination li:last-child a').xpath('@href').get()
        # if nextPage is not None or nextPage != "javascript:void(0);":
        #     nextPage = response.urljoin(nextPage)
        #     yield scrapy.Request(nextPage, callback=self.parse)
