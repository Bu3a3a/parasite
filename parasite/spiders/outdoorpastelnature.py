# encoding: utf-8
from datetime import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class OutdoorPastelNatureSpider(CrawlSpider):
    name = 'outdoorpastelnature'
    allowed_domains = ['outdoorspastelnature.tumblr.com']
    start_urls = ['https://outdoorspastelnature.tumblr.com/page/2']

    rules = (
        Rule(LinkExtractor(allow=('/page/\d+', )), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        posts = response.css("div#posts > ul.post-content")
        for post in posts:
            item = dict()
            item['source'] = response.url
            item['description'] = '\n'.join(post.css("li.caption > p ::text").extract())
            item['tags'] = post.css("ul.tags > li > a ::text").extract()
            item['date'] = datetime.strptime(
                post.css("li.post_info > ul > li.left-control > a ::text").extract_first().strip(), "%B %d, %Y")
            item['img'] = post.css("ul.post > li.photo > a.db ::attr(data-image)").extract_first()
            yield item