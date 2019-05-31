import scrapy
from ..items import QuestionItem
import math
import random
import re
import os


class AvattoSpider(scrapy.Spider):
    name = "AvattoSpider"
    base_url = "https://www.avatto.com/general-knowledge/questions/mcqs/kbc/answers/285/"
    f = open(os.getcwd()+"/CrawlBot/spiders/url_avatto_single.txt", "r")
    start_urls = [url.split(" ")[0].strip() for url in f.readlines() if int(url.split(" ")[1]) != 0]
    f.close()

    def parse(self, response):
        # question_numbers = len(response.css('.ques p::text').extract())
        questions = response.css('.ques').xpath("string(./p)").extract()
        options_A = response.css('tr:first_child td:nth-child(2) span p::text').extract()
        options_B = response.css('tr:nth_child(2) td:nth-child(2) span p::text').extract()
        options_C = response.css('tr:nth_child(3) td:nth-child(2) span p::text').extract()
        options_D = response.css('tr:nth_child(4) td:nth-child(2) span p::text').extract()

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

        number_of_questions = len(response.css('.ques').xpath("string(./p)").extract())
        number_of_easy_questions = math.floor(0.5 * number_of_questions)
        number_of_medium_questions = math.ceil(0.3 * number_of_questions)
        number_of_difficult_questions = number_of_questions - number_of_easy_questions - number_of_medium_questions
        index_of_easy = 0
        index_of_medium = 0
        index_of_hard = 0

        # logic to filter

        for index in range(number_of_questions):
            difficulty_index = 0
            item = QuestionItem()
            item['_id'] = questions[index]
            print(item['_id'])
            item['question_text'] = questions[index].strip()
            item['answer_type'] = QuestionItem.ANSWER_TYPE_SINGLE_CORRECT
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

            random_correct_index = random.choice([1,2,3])

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

            print(item)
            yield item

        nextPage = response.css('.pagination li:last-child a').xpath('@href').get()
        if nextPage is not None or nextPage != "javascript:void(0);":
            nextPage = response.urljoin(nextPage)
            yield scrapy.Request(nextPage, callback=self.parse)
