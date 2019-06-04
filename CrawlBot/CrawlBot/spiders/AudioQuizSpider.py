

import scrapy
from ..items import QuestionItem
import random
from ..configurations import AudioQuizSpiderConf, MovieThemeSpiderConf


class AudioQuizSpider(scrapy.Spider):
    name = "AudioQuizSpider"
    conf = AudioQuizSpiderConf(name).load_configs()
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
            self.conf.set_status(response.url, 'SUCCESS')
        except Exception, e:
            self.conf.set_status(response.url, 'ERROR')

        # logic to filter

        for index in range(number_of_questions):
            difficulty_index = 0
            item = QuestionItem()
            item['_id'] = question + str(index)
            item['question_text'] = question.strip()
            item['answer_type'] = QuestionItem.ANSWER_TYPE_SINGLE_CORRECT
            item['binary_file_path'] = response.urljoin(audios[index])
            item['question_type'] = question_type
            item['answer_type'] = answer_type
            item['difficulty_level'] = difficulty_level
            item['category'] = category

            random_correct_index = random.choice([1, 2, 3])

            right_answer = correct_answers[index]
            valid_answers = correct_answers[:]
            valid_answers.remove(right_answer)

            incorrect_answers = random.sample(valid_answers, 2)

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


class MovieThemeSpider(scrapy.Spider):
    name = "MovieThemeSpider"

    conf = MovieThemeSpiderConf(name).load_configs()

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

            self.conf.set_status(response.url, 'STARTED')
            question = response.css('.style112::text').get()

            audios = response.css('.style75 a').xpath('@href').extract()
            correct_answers = response.css('.style75 a font::text').extract()
            number_of_questions = len(response.css('.style75 a font::text').extract())

            print('nm of questions ', number_of_questions)
            print('corr ', len(correct_answers))

            self.conf.set_status(response.url, 'SUCCESS')
        except Exception, e:
            self.conf.set_status(response.url, 'ERROR ' + e.message)

        # logic to filter

        for index in range(number_of_questions):
            item = QuestionItem()
            item['_id'] = question + str(index)
            item['question_text'] = question.strip()
            item['answer_type'] = QuestionItem.ANSWER_TYPE_SINGLE_CORRECT
            item['binary_file_path'] = response.urljoin(audios[index])

            item['question_type'] = question_type
            item['answer_type'] = answer_type
            item['difficulty_level'] = difficulty_level
            item['category'] = category

            random_correct_index = random.choice([1, 2, 3])

            right_answer = correct_answers[index]
            # item['right_answer'] = right_answer
            valid_answers = correct_answers[:]
            valid_answers.remove(right_answer)
            print("Valid answers: ", len(valid_answers))
            print("Correct Answers: ", len(correct_answers))

            incorrect_answers = random.sample(valid_answers, 2)

            # print("incorrect_answers ",incorrect_answers)

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
