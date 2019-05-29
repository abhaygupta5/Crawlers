# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuestionItem(scrapy.Item):
    # define the fields for your item here like:
    question_text = scrapy.Field()
    answer_1 = scrapy.Field()
    answer_2 = scrapy.Field()
    answer_3 = scrapy.Field()
    answer_type = scrapy.Field()
    question_type = scrapy.Field()
    right_answer = scrapy.Field()
    difficulty_level = scrapy.Field()
    binary_file_path = scrapy.Field()
