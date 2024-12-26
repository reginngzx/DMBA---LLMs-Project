import scrapy

class MarineLogSpider(scrapy.Spider):
    name = "marinelog"
    
    start_urls = [
        'https://www.marinelog.com/category/inland-coastal/ports-terminals/',
        'https://www.marinelog.com/category/legal/regulations/'
    ]
    
    def parse(self, response):
        ARTICLE_SELECTOR = '.article-block'
        HEADLINE_SELECTOR = 'h3 a::text'
        DESCRIPTION_SELECTOR = 'p::text'
        LINK_SELECTOR = 'h3 a::attr("href")'
        DATE_SELECTOR = 'time::text'

        NEXT_SELECTOR = '.load-more::attr("href")' 

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