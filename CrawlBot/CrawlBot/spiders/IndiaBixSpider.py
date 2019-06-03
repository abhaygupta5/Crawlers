import scrapy
from ..items import QuestionItem
import math
import random
import re
import os

from ..configurations import IndiaBixSingleSpiderConfig, IndiaBixArrangeSpiderConfig


class IndiaBixSingleSpider(scrapy.Spider):
    name = "IndiaBixSingleSpider"
    delimiter = ';'

    conf = IndiaBixSingleSpiderConfig(name).load_configs()
    start_urls = conf.get_starting_urls()

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
            options_A = response.xpath("//*[@id[starts-with(.,'tdOptionDt_A')]]/text()").getall()
            options_B = response.xpath(
                "//*[@id[starts-with(.,'tdOptionDt_B')]]/text() | //*[@id='tdOptionDt_B_387']/i").getall()
            options_C = response.xpath("//*[@id[starts-with(.,'tdOptionDt_C')]]/text()").getall()
            options_D = response.xpath("//*[@id[starts-with(.,'tdOptionDt_D')]]/text()").getall()

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

        for index in range(len(question_numbers)):
            difficulty_index = 0
            item = QuestionItem()
            # item['_id'] = questions[index]
            item['question_text'] = questions[index].strip()
            item['answer_type'] = QuestionItem.ANSWER_TYPE_SINGLE_CORRECT
            item['binary_file_path'] = None
            item['question_type'] = QuestionItem.QUESTION_TYPE_TEXT_BASED
            item['difficulty_level'] = difficulty_level

            random_correct_index = random.choice([1, 2, 3])

            if str(correct_answers[index]) == "A":
                # item['right_answer'] = options_A[index]
                if random_correct_index == 1:
                    item['answer_1'] = options_A[index].strip()
                    item['answer_2'] = options_B[index].strip()
                    item['answer_3'] = options_C[index].strip()
                    item['right_answer'] = "A"
                elif random_correct_index == 2:
                    item['answer_2'] = options_A[index].strip()
                    item['answer_1'] = options_D[index].strip()
                    item['answer_3'] = options_B[index].strip()
                    item['right_answer'] = "B"
                else:
                    item['answer_3'] = options_A[index].strip()
                    item['answer_1'] = options_C[index].strip()
                    item['answer_2'] = options_D[index].strip()
                    item['right_answer'] = "C"
            elif str(correct_answers[index]) == "B":
                # item['right_answer'] = options_B[index]
                if random_correct_index == 1:
                    item['answer_1'] = options_B[index].strip()
                    item['answer_2'] = options_A[index].strip()
                    item['answer_3'] = options_C[index].strip()
                    item['right_answer'] = "A"
                elif random_correct_index == 2:
                    item['answer_2'] = options_B[index].strip()
                    item['answer_1'] = options_D[index].strip()
                    item['answer_3'] = options_A[index].strip()
                    item['right_answer'] = "B"
                else:
                    item['answer_3'] = options_B[index].strip()
                    item['answer_1'] = options_C[index].strip()
                    item['answer_2'] = options_D[index].strip()
                    item['right_answer'] = "C"
            elif str(correct_answers[index]) == "C":
                # item['right_answer'] = options_C[index]
                if random_correct_index == 1:
                    item['answer_1'] = options_C[index].strip()
                    item['answer_2'] = options_B[index].strip()
                    item['answer_3'] = options_A[index].strip()
                    item['right_answer'] = "A"
                elif random_correct_index == 2:
                    item['answer_2'] = options_C[index].strip()
                    item['answer_1'] = options_D[index].strip()
                    item['answer_3'] = options_B[index].strip()
                    item['right_answer'] = "B"
                else:
                    item['answer_3'] = options_C[index].strip()
                    item['answer_1'] = options_A[index].strip()
                    item['answer_2'] = options_D[index].strip()
                    item['right_answer'] = "C"
            else:
                # item['right_answer'] = options_D[index]
                if random_correct_index == 1:
                    item['answer_1'] = options_D[index].strip()
                    item['answer_2'] = options_B[index].strip()
                    item['answer_3'] = options_C[index].strip()
                    item['right_answer'] = "A"
                elif random_correct_index == 2:
                    item['answer_2'] = options_D[index].strip()
                    item['answer_1'] = options_A[index].strip()
                    item['answer_3'] = options_B[index].strip()
                    item['right_answer'] = "B"
                else:
                    item['answer_3'] = options_D[index].strip()
                    item['answer_1'] = options_C[index].strip()
                    item['answer_2'] = options_A[index].strip()
                    item['right_answer'] = "C"

            yield item

        nextPage = response.css('.mx-pager').xpath('./a[last()]/@href').get()
        if nextPage is not None:
            nextPage = response.urljoin(nextPage)
            yield scrapy.Request(nextPage, callback=self.parse)


class IndiaBixArrangeSpider(scrapy.Spider):
    name = "IndiaBixArrangeSpider"

    conf = IndiaBixArrangeSpiderConfig(name).load_configs()
    start_urls = conf.get_starting_urls()

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
            questions = response.css(".bix-td-qtxt").xpath("./p[2]/text()").getall()
            responses = response.css(".vr-tbl-lseq-question").xpath("string(./tbody)").getall()
            if len(responses) == 0:
                responses = response.css(".bix-td-qtxt").xpath("./p[3]/text()").getall()
            options_A = response.xpath("//*[@id[starts-with(.,'tdOptionDt_A')]]/text()").getall()
            options_B = response.xpath(
                "//*[@id[starts-with(.,'tdOptionDt_B')]]/text() | //*[@id='tdOptionDt_B_387']/i").getall()
            options_C = response.xpath("//*[@id[starts-with(.,'tdOptionDt_C')]]/text()").getall()
            options_D = response.xpath("//*[@id[starts-with(.,'tdOptionDt_D')]]/text()").getall()

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
            item['question_text'] = questions[index].strip() + re.sub(r'(\d{1})', r' \1', responses[index]).strip()
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
                    item['answer_1'] = options_A[index].strip()
                    item['answer_2'] = options_B[index].strip()
                    item['answer_3'] = options_C[index].strip()
                    item['right_answer'] = "A"
                elif random_correct_index == 2:
                    item['answer_2'] = options_A[index].strip()
                    item['answer_1'] = options_D[index].strip()
                    item['answer_3'] = options_B[index].strip()
                    item['right_answer'] = "B"
                else:
                    item['answer_3'] = options_A[index].strip()
                    item['answer_1'] = options_C[index].strip()
                    item['answer_2'] = options_D[index].strip()
                    item['right_answer'] = "C"
            elif str(correct_answers[index]) == "B":
                if random_correct_index == 1:
                    item['answer_1'] = options_B[index].strip()
                    item['answer_2'] = options_A[index].strip()
                    item['answer_3'] = options_C[index].strip()
                    item['right_answer'] = "A"
                elif random_correct_index == 2:
                    item['answer_2'] = options_B[index].strip()
                    item['answer_1'] = options_D[index].strip()
                    item['answer_3'] = options_A[index].strip()
                    item['right_answer'] = "B"
                else:
                    item['answer_3'] = options_B[index].strip()
                    item['answer_1'] = options_C[index].strip()
                    item['answer_2'] = options_D[index].strip()
                    item['right_answer'] = "C"
            elif str(correct_answers[index]) == "C":
                if random_correct_index == 1:
                    item['answer_1'] = options_C[index].strip()
                    item['answer_2'] = options_B[index].strip()
                    item['answer_3'] = options_A[index].strip()
                    item['right_answer'] = "A"
                elif random_correct_index == 2:
                    item['answer_2'] = options_C[index].strip()
                    item['answer_1'] = options_D[index].strip()
                    item['answer_3'] = options_B[index].strip()
                    item['right_answer'] = "B"
                else:
                    item['answer_3'] = options_C[index].strip()
                    item['answer_1'] = options_A[index].strip()
                    item['answer_2'] = options_D[index].strip()
                    item['right_answer'] = "C"
            else:
                if random_correct_index == 1:
                    item['answer_1'] = options_D[index].strip()
                    item['answer_2'] = options_B[index].strip()
                    item['answer_3'] = options_C[index].strip()
                    item['right_answer'] = "A"
                elif random_correct_index == 2:
                    item['answer_2'] = options_D[index].strip()
                    item['answer_1'] = options_A[index].strip()
                    item['answer_3'] = options_B[index].strip()
                    item['right_answer'] = "B"
                else:
                    item['answer_3'] = options_D[index].strip()
                    item['answer_1'] = options_C[index].strip()
                    item['answer_2'] = options_A[index].strip()
                    item['right_answer'] = "C"

            yield item

        nextPage = response.css('.mx-pager').xpath('./a[last()]/@href').get()
        if nextPage is not None:
            nextPage = response.urljoin(nextPage)
            yield scrapy.Request(nextPage, callback=self.parse)
