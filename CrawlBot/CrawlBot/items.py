# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuestionItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    question_text = scrapy.Field()
    answer_1 = scrapy.Field()
    answer_2 = scrapy.Field()
    answer_3 = scrapy.Field()
    answer_type = scrapy.Field()
    question_type = scrapy.Field()
    right_answer = scrapy.Field()
    difficulty_level = scrapy.Field()
    binary_file_path = scrapy.Field()
    category = scrapy.Field()

    ANSWER_TYPE_SINGLE_CORRECT = 'Single-Correct'
    ANSWER_TYPE_MULTI_CORRECT = 'Multi-Correct'
    ANSWER_TYPE_ARRANGE_THE_ORDER = 'Arrange the order'

    QUESTION_TYPE_TEXT_BASED = 'Text Based'
    QUESTION_TYPE_IMAGE_BASED = 'Image Based'
    QUESTION_TYPE_AUDIO_BASED = 'Audio Based'
    QUESTION_TYPE_VIDEO_BASED = 'Video Based'

    DIFFICULTY_LEVEL_EASY = 'Easy'
    DIFFICULTY_LEVEL_AVERAGE = 'Medium'
    DIFFICULTY_LEVEL_HARD = 'Hard'
