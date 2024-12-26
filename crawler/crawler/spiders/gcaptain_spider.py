import scrapy

class GcaptainSpider(scrapy.Spider):
    name = "gcaptain"
    
    start_urls = [
        'https://gcaptain.com/category/ports/',
    ]
    
    def parse(self, response):
        ARTICLE_SELECTOR = '.article'
        HEADLINE_SELECTOR = '.headline h3::text'
        DESCRIPTION_SELECTOR = 'p::text'
        LINK_SELECTOR = '.headline::attr("href")'
        DATE_SELECTOR = '.date::text'

        NEXT_SELECTOR = '.next.page-numbers::attr("href")' 

        for article in response.css(ARTICLE_SELECTOR):
            yield {
                'headline': article.css(HEADLINE_SELECTOR).extract_first(),
                'description': article.css(DESCRIPTION_SELECTOR).extract_first(),
                'link': article.css(LINK_SELECTOR).extract_first(),
                'date': article.css(DATE_SELECTOR).extract_first(),
            }

        next_page = response.css(NEXT_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page))