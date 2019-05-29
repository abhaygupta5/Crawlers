import scrapy
from scrapy.http import Request

class GeneralIndiabixSpider(scrapy.Spider):
	name = "generalIndiabix"
	start_urls = ['https://www.indiabix.com/general-knowledge/basic-general-knowledge/005001']

	def parse(self, response):
		yield {
			'question_numbers': response.css(".bix-td-qno::text").getall(),
			'questions': response.css(".bix-td-qtxt").xpath("./p/text()").getall(),
			'options_A': response.xpath("//*[@id[starts-with(.,'tdOptionDt_A')]]/text()").getall(),
			'options_B': response.xpath("//*[@id[starts-with(.,'tdOptionDt_B')]]/text()").getall(),
			'options_C': response.xpath("//*[@id[starts-with(.,'tdOptionDt_C')]]/text()").getall(),
			'options_D': response.xpath("//*[@id[starts-with(.,'tdOptionDt_D')]]/text()").getall(),
			'correct_answers': response.css(".jq-hdnakqb::text").getall()
		}
		nextPage = response.css('.mx-pager').xpath('./a[last()]/@href').get()
		if nextPage is not None:
			nextPage = response.urljoin(nextPage)
			yield scrapy.Request(nextPage, callback = self.parse)
