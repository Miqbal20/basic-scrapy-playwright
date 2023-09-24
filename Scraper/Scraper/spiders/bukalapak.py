import scrapy
from scrapy_playwright.page import PageMethod


class LazadaSpider(scrapy.Spider):
    name = 'bukalapak'

    def start_requests(self):
        yield scrapy.Request('https://www.bukalapak.com/')
        meta = dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_coroutines=[
                PageMethod('wait_for_selector', "div[class='bl-heading bl-heading--h6']")
            ]
        )

    def parse(self, response, **kwargs):
        yield {
            'text': response.text
        }
