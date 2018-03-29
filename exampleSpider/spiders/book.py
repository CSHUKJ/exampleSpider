# -*- coding: utf-8 -*-
import scrapy

class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):

        for book in response.css('article.product_pod'):
            name = book.xpath('./h3/a/@title').extract_first()
            price = book.css('p.price_color::text').extract_first()
            yield {
                'name':name,
                'price':price,
            }
        # 提取下页的链接
        next_url = response.css('ul.pager li.next a::attr(href)').extract_first()
        if next_url:
            # 将新的链接加入队列中， 构造新的Request对象
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse)
