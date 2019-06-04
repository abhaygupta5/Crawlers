# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import csv
import logging
import requests
from settings import FIELDS_TO_EXPORT, URL_TO_SEND
from custom_csv_class import MyProjectCsvItemExporter

# from .decorators import check_spider_pipeline

DATABASE_NAME = 'IndiaBix'
CONFIGURATION_COLLECTION_NAME = 'Configuration'


class IndiabixPipeline(object):
    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        db = self.conn['IndiaBix']
        self.collection = db['Questions']
        # self.collection.create_index([("question_text", pymongo.TEXT)], name="search_index")

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item


class CsvExporterPipeline(object):
    def open_spider(self, spider):
        print("CsvExporterPipeline called")
        self.filename = spider.conf.get_csv_file_name()
        self.file = open(self.filename, 'wb')
        self.exporter = MyProjectCsvItemExporter(self.file, unicode, quoting=csv.QUOTE_ALL)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class SendCSVFilePipeline(object):

    def close_spider(self, spider):
        file_name = spider.conf.get_csv_file_name()
        print('Sending file : ', str(file_name))
        # multipart_form_data = {
        #     'file': (file_name, open(file_name, 'rb')),
        # }
        # response = requests.post(URL_TO_SEND, files=multipart_form_data)
        # print(response.text)


class CleanDataPipeline(object):
    def open_spider(self, spider):
        logging.debug("CleanDataPipeline called")

    def process_item(self, item, spider):

        SPECIAL_CHARS_TO_REMOVE = ['"']

        for field in FIELDS_TO_EXPORT:
            for special_char in SPECIAL_CHARS_TO_REMOVE:
                if not item[field] is None:
                    item[field] = item[field].replace(special_char, '')

        return item
