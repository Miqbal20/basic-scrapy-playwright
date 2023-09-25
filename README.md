# Basis Scrapy
## Tutorial
### Target
https://quotes.toscrape.com
```commandline
scrapy shell 'https://quotes.toscrape.com/'
```
### Library

```
pip install scrapy
pip install pyopenssl
pip install pywin32
pip install scrapy_playwright
```

### Start Project
```commandline
scrapy startproject Scraper
```

### Create file Crawler
```commandline
spiders/quotes.py
```

### settings.py
```commandline
DOWNLOAD_HANDLERS = {
    "http": 'scrapy_playwright.handler.ScrapyPlayWrightDownloadHandler',
    "https": 'scrapy_playwright.handler.ScrapyPlayWrightDownloadHandler',
}
```

### Basic shell command
```commandline
response
response.css("title")
response.css("title::text").get()
response.css("title::text").extract()
response.css(".text::text").get()
response.css(".text::text")[2].get()
response.css(".text::text").getall()
response.css(".author::text").getall()
```

### quotes.py
```commandline
import scrapy

class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://quotes.toscrape.com/'
    ]
    
        def parse(self, response):
        all_quotes = response.css('div.quote')
        for quotes in all_quotes:
            content = quotes.css('.text::text').get()
            author = quotes.css('.author::text').get()
            tag = quotes.css('.tag::text').getall()

            yield {
                'content': content,
                'author': author,
                'tag': tag,
            }

            # Next pages
            next_page = response.css('li.next a::attr(href)').get()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
```
### Start Crawl
```commandline
scrapy crawl quotes
```

### Output 
```commandline
scrapy crawl quotes -o quotes.json
scrapy crawl quotes -O quotes.json

scrapy crawl quotes -o quotes.csv
scrapy crawl quotes -O quotes.csv
```