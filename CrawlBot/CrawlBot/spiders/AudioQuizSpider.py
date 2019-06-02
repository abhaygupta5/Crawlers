import scrapy
from ..items import QuestionItem
import math
import random
import re
import os
from ..configurations import AudioQuizSpiderConf


class AudioQuizSpider(scrapy.Spider):
    name = "AudioQuizSpider"
    # f = open(os.getcwd()+"/CrawlBot/spiders/url_audio_single.txt", "r")
    # start_urls = [url.split(" ")[0].strip() for url in f.readlines() if int(url.split(" ")[1]) != 0]
    # f.close()

    conf = AudioQuizSpiderConf(name).load_configs()
    start_urls = conf.get_starting_urls()

    def parse(self, response):
        try:
            temp_ques = response.css('.style110::text').get()
            list1 = list(temp_ques)
            list1.remove('(')
            list1.remove(')')
            question = ''
            for character in list1:
                question += character

            audios = response.css('.style96').xpath('@href').extract()
            correct_answers = response.css('.style96 font::text').extract()
            number_of_questions = len(response.css('.style96 font::text').extract())
            number_of_easy_questions = math.floor(0.5 * number_of_questions)
            number_of_medium_questions = math.ceil(0.3 * number_of_questions)
            number_of_difficult_questions = number_of_questions - number_of_easy_questions - number_of_medium_questions

            self.conf.set_status(response.url,'SUCCESS')
        except Exception,e:
            self.conf.set_status(response.url,'ERROR')


        index_of_easy = 0
        index_of_medium = 0
        index_of_hard = 0

        # logic to filter

        for index in range(number_of_questions):
            difficulty_index = 0
            item = QuestionItem()
            item['_id'] = question + str(index)
            item['question_text'] = question.strip()
            item['answer_type'] = QuestionItem.ANSWER_TYPE_SINGLE_CORRECT
            item['binary_file_path'] = response.urljoin(audios[index])
            item['question_type'] = QuestionItem.QUESTION_TYPE_AUDIO_BASED
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


            right_answer = correct_answers[index]
            # item['right_answer'] = right_answer
            valid_answers = correct_answers[:]
            valid_answers.remove(right_answer)

            incorrect_answers = random.sample(range(0, len(valid_answers)), 2)
            # print("incorrect_answers ",incorrect_answers)

            if random_correct_index == 1:
                item['right_answer'] = 'A'
                item['answer_1'] = right_answer
                item['answer_2'] = correct_answers[incorrect_answers[0]]
                item['answer_3'] = correct_answers[incorrect_answers[1]]
            elif random_correct_index == 2:
                item['right_answer'] = 'B'
                item['answer_2'] = right_answer
                item['answer_1'] = correct_answers[incorrect_answers[0]]
                item['answer_3'] = correct_answers[incorrect_answers[1]]
            else:
                item['right_answer'] = 'C'
                item['answer_3'] = right_answer
                item['answer_1'] = correct_answers[incorrect_answers[0]]
                item['answer_2'] = correct_answers[incorrect_answers[1]]

            print("ITEM", item)
            yield item

        # nextPage = response.css('.mx-pager').xpath('./a[last()]/@href').get()
        # if nextPage is not None:
        #     nextPage = response.urljoin(nextPage)
        #     yield scrapy.Request(nextPage, callback=self.parse)
