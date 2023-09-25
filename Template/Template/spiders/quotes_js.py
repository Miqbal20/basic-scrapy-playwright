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
    name = 'quotes_js'

    def start_requests(self):
        url = 'https://quotes.toscrape.com/js'
        yield scrapy.Request(url, meta=dict(
            playwright=True,
            playwright_include_page=True,
            playwright_page_methods=[
                PageMethod('wait_for_selector', 'div.quote')
            ],
            errback=self.errback
        ))

    async def parse(self, response, **kwargs):
        page = response.meta['playwright_page']
        await page.close()

        for quote in response.css('div.quote'):
            quote_item = QuoteItem()
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            quote_item['text'] = quote.css('div.tags a.tag::text').get()

            yield quote_item

        next_page = response.css('.next>a ::attr(href').get()

        if next_page is not None:
            next_page_url = f'http://quotes.toscrape.com{next_page}'
            yield scrapy.Request(next_page_url, meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod('wait_for_selector', 'div.quote')
                ],
                errback=self.errback
            ))

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()


if __name__ == '__main__':
    # Attr
    spider = 'quotes_js'
    output = f'{spider}.json'

    os.system(f'scrapy crawl {spider} -O output/{output}')

