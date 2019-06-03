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
    # f = open(os.getcwd()+"/CrawlBot/spiders/url_jetpunk_images.txt", "r")
    # start_urls = [url.split(" ")[0].strip() for url in f.readlines() if int(url.split(" ")[1]) != 0]
    # f.close()
    path = "chromedriver"

    def parse(self, response):

        try:
            selenium_options = webdriver.ChromeOptions()
            selenium_options.add_argument('headless')
            driver = webdriver.Chrome(self.path, chrome_options=selenium_options)
            driver.get(response.url)
            take_quiz = driver.find_element_by_xpath('//*[(@id = "start-button")]')
            take_quiz.click()

            give_up = driver.find_element_by_xpath(
                '//*[contains(concat( " ", @class, " " ), concat( " ", "link-like", " " ))]')
            give_up.click()

            time.sleep(2)
            # print("page source",self.driver.getPageSource())
            html_response = HtmlResponse(url=response.url, body=driver.page_source, encoding='utf-8')

            page = Selector(response=html_response)

            print(page.css('title::text').extract())

            number_of_questions = len(page.css(".photo-img").xpath('@src').extract())
            print("number_of_questions ", number_of_questions)

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
            self.conf.set_status(response.url,'ERROR '+e.message)
            driver.close()

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
            item['question_text'] = question.strip()
            item['answer_type'] = QuestionItem.ANSWER_TYPE_SINGLE_CORRECT
            item['binary_file_path'] = self.base_url + images[index]
            item['question_type'] = QuestionItem.QUESTION_TYPE_IMAGE_BASED
            item['_id'] = question+str(index)+images[index]
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

            right_answer = correct_answers[index]
            # item['right_answer'] = right_answer
            valid_answers = correct_answers[:]
            valid_answers.remove(right_answer)

            incorrect_answers = []
            num = random.randint(0, len(valid_answers))
            print("RANDOM CHOSEN ", num)
            incorrect_answers.append(num)

            num1 = random.randint(0, len(valid_answers))
            while num1 == num:
                num1 = random.randint(0, len(valid_answers))
            print("RANDOM CHOSEN 2 ", num1)
            incorrect_answers.append(num1)
            print("INCORRECT ", incorrect_answers)

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