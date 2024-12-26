import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class NyTimesSpider(scrapy.Spider):
    name = "nytimes"
    
    start_urls = [
        'https://www.nytimes.com/search?query=port+disruption',
    ]

    def __init__(self):
        self.driver = webdriver.Chrome()
    
    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(3)

        next_button = self.driver.find_element(By.CSS_SELECTOR, '.css-vsuiox button')

        x = 30
        while x != 0:
            next_button.click()
            time.sleep(3)
            x-=1

        html = self.driver.page_source
     
        selenium_response = HtmlResponse(self.driver.current_url, body=html, encoding='utf-8')

        ARTICLE_SELECTOR = '.css-1l4w6pd'
        HEADLINE_SELECTOR = '.css-nsjm9t::text'
        DESCRIPTION_SELECTOR = '.css-16nhkrn::text'
        LINK_SELECTOR = 'a::attr("href")'
        DATE_SELECTOR = '.css-17ubb9w::text'

        for article in selenium_response.css(ARTICLE_SELECTOR):
            yield {
                'headline': article.css(HEADLINE_SELECTOR).extract_first(),
                'description': article.css(DESCRIPTION_SELECTOR).extract_first(),
                'link': "https://www.nytimes.com" + article.css(LINK_SELECTOR).extract_first(),
                'date': article.css(DATE_SELECTOR).extract_first(),
            }

    def close(self, reason):
        self.driver.quit()