# encoding: utf-8
import scrapy
from datetime import datetime


class TumblrSpider(scrapy.Spider):
    name = "tumblr"

    def start_requests(self):
        urls = [
            'http://mei-xing.tumblr.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        posts = response.css("div.post")
        for post in posts:
            item = dict()
            item['source'] = response.url
            item['description'] = '\n'.join(post.css("p ::text").extract())
            item['tags'] = post.css("div.tags > a ::text").extract()
            item['date'] = datetime.strptime(post.css("div.date > div.left > a ::attr(href)").extract()[1][5:],
                                             "%Y/%m/%d")

            item['img'] = post.css("div.photo > a.zoom ::attr(href)").extract_first()

            if item['img']:
                yield item

            else:
                iframe_src = post.css("div.html_photoset > iframe.photoset ::attr(src)").extract_first()
                if iframe_src:
                    request = scrapy.Request(url=response.url + iframe_src[1:],
                                             callback=self.parse_iframe)
                    request.meta['item'] = item
                    yield request

    def parse_iframe(self, response):
        item = response.meta['item']
        item['img'] = response.css("div.photoset > div.photoset_row > a.photoset_photo ::attr(href)").extract()
        yield item