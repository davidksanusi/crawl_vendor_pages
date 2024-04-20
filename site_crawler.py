import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import csv

class KeywordSpider(CrawlSpider):
    name = 'keyword_spider'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'DOWNLOAD_DELAY': 1,
        'AUTOTHROTTLE_ENABLED': True,
        'CLOSESPIDER_PAGECOUNT': 10
    }

    def __init__(self, start_url, primary_keywords, secondary_keywords, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.allowed_domains = [start_url.split("//")[1].strip("www.")]
        self.primary_keywords = primary_keywords
        self.secondary_keywords = secondary_keywords
        self.results = []

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            if 'text' in response.headers.get('Content-Type').decode('utf-8'):
                page_text = response.text.lower()
                primary_found = [keyword for keyword in self.primary_keywords if keyword in page_text]
                secondary_found = [keyword for keyword in self.secondary_keywords if keyword in page_text]

                if primary_found and secondary_found:
                    found_keywords = primary_found + secondary_found
                    self.results.append([self.allowed_domains[0], response.url, ", ".join(found_keywords)])
                    with open('results.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([self.allowed_domains[0], response.url, ", ".join(found_keywords)])
            else:
                self.logger.info(f"Skipped non-text response at {response.url}")
        except Exception as e:
            self.logger.error(f'Crawl Failure: {e}')
