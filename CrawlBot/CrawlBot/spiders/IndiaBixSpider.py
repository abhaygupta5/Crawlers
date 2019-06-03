import scrapy
from ..items import QuestionItem
import math
import random
import re
import os
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import requests

from ..configurations import IndiaBixSingleSpiderConfig, IndiaBixArrangeSpiderConfig


class IndiaBixSingleSpider(scrapy.Spider):
    name = "IndiaBixSingleSpider"

    def __init__(self, filename='', **kwargs):
        self.fileName = filename
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        super(IndiaBixSingleSpider, self).__init__(**kwargs)

    def spider_closed(self, spider):
        with open(self.fileName, 'rb') as f:
            r = requests.post('http://httpbin.org/post', files={self.fileName: f})
            print(f.readline())
        print("ENDING OF SPIDER")

    conf = IndiaBixSingleSpiderConfig(name).load_configs()
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

            question_numbers = response.css(".bix-td-qno::text").getall()
            number_of_questions = len(question_numbers)

            print('QUSTION NUM ', question_numbers)
            questions = response.css(".bix-td-qtxt").xpath("./p/text()").getall()
            questions = [re.sub(r"\s+", " ", question.strip().replace('\n', ' ')).replace('\"', '').replace("\'", "\\'") for question in questions]
            options_A = response.xpath("//*[@id[starts-with(.,'tdOptionDt_A')]]/text()").getall()
            options_A = [option.strip().replace('\n', ' ').replace('\"', '').replace("\'", "\\'") for option in options_A]
            options_B = response.xpath(
                "//*[@id[starts-with(.,'tdOptionDt_B')]]/text() | //*[@id='tdOptionDt_B_387']/i").getall()
            options_B = [option.strip().replace('\n', ' ').replace('\"', '').replace("\'", "\\'") for option in
                         options_B]
            options_C = response.xpath("//*[@id[starts-with(.,'tdOptionDt_C')]]/text()").getall()
            options_C = [option.strip().replace('\n', ' ').replace('\"', '').replace("\'", "\\'") for option in
                         options_C]
            options_D = response.xpath("//*[@id[starts-with(.,'tdOptionDt_D')]]/text()").getall()
            options_D = [option.strip().replace('\n', ' ').replace('\"', '').replace("\'", "\\'") for option in
                         options_D]

            # print(len(options_A), len(options_B), len(options_C), len(options_D))
            # print()
            # print(options_A)
            # print(options_B)
            # print(options_C)
            # print(options_D)

            correct_answers = response.css(".jq-hdnakqb::text").getall()
            self.conf.set_status(response.url, 'SUCCESS')
        except Exception, e:
            self.conf.set_status(response.url, 'ERROR')
            number_of_questions = 0

        # logic to filter

        for index in range(number_of_questions):
            difficulty_index = 0
            item = QuestionItem()
            item['_id'] = questions[index]
            item['question_text'] = questions[index]
            item['answer_type'] = QuestionItem.ANSWER_TYPE_SINGLE_CORRECT
            item['binary_file_path'] = None
            item['question_type'] = QuestionItem.QUESTION_TYPE_TEXT_BASED
            item['difficulty_level'] = difficulty_level

            random_correct_index = random.choice([1, 2, 3])

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

            yield item

        nextPage = response.css('.mx-pager').xpath('./a[last()]/@href').get()
        if nextPage is not None:
            nextPage = response.urljoin(nextPage)
            yield scrapy.Request(nextPage, callback=self.parse)


class IndiaBixArrangeSpider(scrapy.Spider):
    name = "IndiaBixArrangeSpider"

    def __init__(self, filename='', **kwargs):
        self.fileName = filename
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        super(IndiaBixArrangeSpider, self).__init__(**kwargs)

    def spider_closed(self, spider):
        with open(self.fileName, 'rb') as f:
            r = requests.post('http://httpbin.org/post', files={self.fileName: f})
            print(f.readline())
        print("ENDING OF SPIDER")

    conf = IndiaBixArrangeSpiderConfig(name).load_configs()
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
        print(self.fileName)
        try:
            difficulty_level = self.conf.get_difficulty_level(response.url, self.default_difficulty_level)
            category = self.conf.get_category(response.url, self.default_category)
            question_type = self.conf.get_question_type(response.url, self.default_question_type)
            answer_type = self.conf.get_answer_type(response.url, self.default_answer_type)

            self.default_difficulty_level = difficulty_level
            self.default_category = category
            self.default_question_type = question_type
            self.default_answer_type = answer_type

            question_numbers = response.css(".bix-td-qno::text").getall()
            number_of_questions = len(question_numbers)
            questions = response.css(".bix-td-qtxt").xpath("./p[2]/text()").getall()
            questions = [re.sub(r"\s+", " ", question.strip().replace('\n', ' ')).replace('\"', '').replace("\'", "\\'")
                         for question in questions]
            responses = response.css(".vr-tbl-lseq-question").xpath("string(./tbody)").getall()
            if len(responses) == 0:
                responses = response.css(".bix-td-qtxt").xpath("./p[3]/text()").getall()
            options_A = response.xpath("//*[@id[starts-with(.,'tdOptionDt_A')]]/text()").getall()
            options_A = [option.strip().replace('\n', ' ').replace('\"', '').replace("\'", "\\'") for option in
                         options_A]
            options_B = response.xpath(
                "//*[@id[starts-with(.,'tdOptionDt_B')]]/text() | //*[@id='tdOptionDt_B_387']/i").getall()
            options_B = [option.strip().replace('\n', ' ').replace('\"', '').replace("\'", "\\'") for option in
                         options_B]
            options_C = response.xpath("//*[@id[starts-with(.,'tdOptionDt_C')]]/text()").getall()
            options_C = [option.strip().replace('\n', ' ').replace('\"', '').replace("\'", "\\'") for option in
                         options_C]
            options_D = response.xpath("//*[@id[starts-with(.,'tdOptionDt_D')]]/text()").getall()
            options_D = [option.strip().replace('\n', ' ').replace('\"', '').replace("\'", "\\'") for option in
                         options_D]

            # print(len(options_A), len(options_B), len(options_C), len(options_D))
            # print()
            # print(questions)
            # print()
            # print(responses)

            correct_answers = response.css(".jq-hdnakqb::text").getall()
            self.conf.set_status(response.url, 'SUCCESS')
        except Exception, e:
            self.conf.set_status(response.url, 'ERROR')
            number_of_questions = 0

        # logic to filter

        for index in range(len(question_numbers)):
            item = QuestionItem()
            item['_id'] = questions[index] + "\n" + re.sub(r'(\d{1})', r' \1', responses[index])
            question_text = questions[index].strip() + re.sub(r'(\d{1})', r' \1', responses[index]).strip()
            question_text = re.sub(r"\s+", " ",question_text.replace('\n', ' ')).replace('\"', '').replace("\'", "\\'")
            item['question_text'] = question_text
            item['answer_type'] = QuestionItem.ANSWER_TYPE_ARRANGE_THE_ORDER
            item['binary_file_path'] = None
            item['question_type'] = QuestionItem.QUESTION_TYPE_TEXT_BASED

            item['question_type'] = question_type
            item['answer_type'] = answer_type
            item['difficulty_level'] = difficulty_level
            item['category'] = category

            random_correct_index = random.choice([1, 2, 3])

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

            yield item

        nextPage = response.css('.mx-pager').xpath('./a[last()]/@href').get()
        if nextPage is not None:
            nextPage = response.urljoin(nextPage)
            yield scrapy.Request(nextPage, callback=self.parse)
