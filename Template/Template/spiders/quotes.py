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
    name = "quotes"

    def start_requests(self):
        url = 'https://quotes.toscrape.com'
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_methods=[
                PageMethod('wait_for_selector', 'div.quote'),
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

            # Next pages
            next_page = response.css('li.next a::attr(href)').get()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)


if __name__ == '__main__':
    # Attr
    spider = 'quotes'
    output = f'{spider}.json'

    os.system(f'scrapy crawl {spider} -O output/{output}')
