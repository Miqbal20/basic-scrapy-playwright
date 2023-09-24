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
```

### Start Project
```commandline
scrapy startproject Scraper
```

### Create Folder
```commandline
spiders/quotes.py
```
### quotes.py
```commandline
import scrapy

class QuoteSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://quotes.toscrape.com/'
    ]
    
    title = response.css('title::text').extract()
        yield {
            'title': title
        }
```

### Basic command
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