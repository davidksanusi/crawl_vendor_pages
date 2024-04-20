import scrapydo
import site_crawler

class CrawlManager:
    def __init__(self, urls, primary_keywords, secondary_keywords):
        self.urls = urls
        self.primary_keywords = primary_keywords
        self.secondary_keywords = secondary_keywords
        scrapydo.setup()  # Setup scrapydo once

    def run_spider(self, url):
        # Use scrapydo to run spiders
        scrapydo.run_spider(site_crawler.KeywordSpider, start_url=url, primary_keywords=self.primary_keywords, secondary_keywords=self.secondary_keywords)

    def control(self):
        for url in self.urls:
            self.run_spider(url)

if __name__ == '__main__':
    primary_keywords = ["supplier", "supplier diversity", "vendor", "sourcing", "supply chain", "procurement", 'vendors']
    secondary_keywords = ["register", "join", "sign", "become", "registration", "submit", "apply", "interested", "fill out", "join",  "becoming", "registered"]
    urls = [
        "https://www.pepsico.com",
        "https://www.tysonfoods.com",
        "https://www.coca-colacompany.com",
        "https://www.generalmills.com",
        "https://www.conagrabrands.com",
        "https://www.jmsmucker.com"
    ]

    manager = CrawlManager(urls, primary_keywords, secondary_keywords)
    manager.control()