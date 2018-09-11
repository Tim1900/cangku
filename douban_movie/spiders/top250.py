# -*- coding: utf-8 -*-
import scrapy
import re

from douban_movie.items import DoubanMovieItem

class Top250Spider(scrapy.Spider):
    name = 'top250'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/top250']
    eval_re = re.compile(r"\d+")

    def parse(self, response):
        movie_blocks = response.xpath('//ol[@class="grid_view"]/li')
        for block in movie_blocks:
            name = block.css('span.title::text').extract_first()
            # name = block.xpath()
            star = block.xpath(".//span[@class='rating_num']/text()").extract_first()
            e =block.xpath(".//div[@class='star']/span[4]/text()").extract_first()
            evaluation = self.eval_re.search(e).group()
            #group（）和groups（），前一个输出字符串，后一个输出元组
            introduction = block.css('span.inq::text').extract_first()
            item = DoubanMovieItem()
            item['name'] = name
            item['star'] = star
            item['evaluation'] = evaluation
            item['introduction'] = introduction
            yield item   #下一次迭代从yield之后开始
        next_url =response.css('span.next > a::attr(href)').extract_first()
        # 注意地址取法，之前都是去text，而这里取的是<>里的，指定attr和对应名称。
        # <a href="?start=25&amp;filter=" style="background: rgb(204, 136, 136); border: 2px solid red;">后页&gt;</a>
        if next_url:
            next_url = response.urljoin(next_url)  # ruljoin创建完整的url
            yield scrapy.Request(next_url, callback=self.parse)
