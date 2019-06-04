#!/bin/bash
scrapy crawl IndiaBixArrangeSpider -o IndiaBixArrange.csv -a filename=IndiaBixArrange.csv -t csv
scrapy crawl IndiaBixSingleSpider -o IndiaBixSingle.csv -a filename=IndiaBixSingle.csv -t csv
scrapy crawl AvattoSpider -o AvattoSingle.csv -a filename=AvattoSingle.csv -t csv
scrapy crawl AudioQuizSpider -o AudioSingle.csv -a filename=AudioSingle.csv -t csv
scrapy crawl MovieThemeSpider -o MovieThemeSingle.csv -a filename=MovieThemeSingle.csv -t csv
scrapy crawl JetpunkSpider -o ImageSingle.csv -a filename=ImageSingle.csv -t csv
scrapy crawl YoutubePlaylistSpider -o VideoSingle.csv -a filename=VideoSingle.csv -t csv