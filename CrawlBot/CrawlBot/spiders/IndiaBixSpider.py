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
    # f = open(os.getcwd()+"/CrawlBot/spiders/url_indiabix_single.txt", "r")
    # start_urls = [url.split(" ")[0].strip() for url in f.readlines() if int(url.split(" ")[1]) != 0]
    # f.close()

    conf = IndiaBixSingleSpiderConfig(name).load_configs()
    start_urls = conf.get_starting_urls()

    def parse(self, response):
        try:
            difficulty_level = self.conf.get_difficulty_level(response.url)
            question_numbers = response.css(".bix-td-qno::text").getall()
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
        number_of_questions = len(question_numbers)
        number_of_easy_questions = math.floor(0.5 * number_of_questions)
        number_of_medium_questions = math.ceil(0.3 * number_of_questions)
        number_of_difficult_questions = number_of_questions - number_of_easy_questions - number_of_medium_questions
        index_of_easy = 0
        index_of_medium = 0
        index_of_hard = 0

        # logic to filter

        for index in range(len(question_numbers)):
            difficulty_index = 0
            item = QuestionItem()
            item['_id'] = questions[index]
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
    # f = open(os.getcwd()+"/CrawlBot/spiders/url_indiabix_arrange.txt", "r")
    # start_urls = [url.split(" ")[0].strip() for url in f.readlines() if int(url.split(" ")[1]) != 0]
    # f.close()

    conf = IndiaBixArrangeSpiderConfig(name).load_configs()
    start_urls = conf.get_starting_urls()

    def parse(self, response):

        try:
            difficulty_level = self.conf.get_difficulty_level(response.url)
            question_numbers = response.css(".bix-td-qno::text").getall()
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

        number_of_questions = len(question_numbers)
        number_of_easy_questions = math.floor(0.5 * number_of_questions)
        number_of_medium_questions = math.ceil(0.3 * number_of_questions)
        number_of_difficult_questions = number_of_questions - number_of_easy_questions - number_of_medium_questions
        index_of_easy = 0
        index_of_medium = 0
        index_of_hard = 0

        # logic to filter

        for index in range(len(question_numbers)):
            difficulty_index = 0
            item = QuestionItem()
            item['_id'] = questions[index] + "\n" + re.sub(r'(\d{1})', r' \1', responses[index])
            item['question_text'] = questions[index].strip() + re.sub(r'(\d{1})', r' \1', responses[index]).strip()
            item['answer_type'] = QuestionItem.ANSWER_TYPE_ARRANGE_THE_ORDER
            item['binary_file_path'] = None
            item['question_type'] = QuestionItem.QUESTION_TYPE_TEXT_BASED
            if index_of_easy < number_of_easy_questions:
                item['difficulty_level'] = QuestionItem.DIFFICULTY_LEVEL_EASY
                index_of_easy += 1
            elif index_of_medium < number_of_medium_questions:
                item['difficulty_level'] = QuestionItem.DIFFICULTY_LEVEL_AVERAGE
                index_of_medium += 1
            else:
                item['difficulty_level'] = QuestionItem.DIFFICULTY_LEVEL_HARD
                index_of_hard += 1

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
