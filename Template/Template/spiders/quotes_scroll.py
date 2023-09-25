import scrapy
import os
from scrapy_playwright.page import PageMethod


class QuoteItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()


class QuoteSpider(scrapy.Spider):
    name = "quotes_scroll"

    def start_requests(self):
        url = 'https://quotes.toscrape.com/scroll'
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_methods=[
                PageMethod('wait_for_selector', 'div.quote'),
                PageMethod('evaluate', 'window.scrollBy(0, document.body.scrollHeight)'),
                PageMethod('wait_for_selector', 'div.quote:nth-child(10)'),
            ],
        ))

    async def parse(self, response, **kwargs):
        all_quotes = response.css('div.quote')
        for quotes in all_quotes:
            quote_item = QuoteItem()
            quote_item['text'] = quotes.css('span.text::text').get()
            quote_item['author'] = quotes.css('small.author::text').get()
            quote_item['tags'] = quotes.css('div.tags a.tag::text').get()

            yield quote_item


if __name__ == '__main__':
    # Attr
    spider = 'quotes_scroll'
    output = f'{spider}.json'

    os.system(f'scrapy crawl {spider} -O output/{output}')
