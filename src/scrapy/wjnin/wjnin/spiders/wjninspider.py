# -*- coding: utf-8 -*-

from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from wjnin.items import WjninItem

class Wjnin(Spider):
    name = "wjnin"
    allowed_domains = ["bbs.wjnin.cn"]
    start_urls = [
        "http://bbs.wjnin.cn/forum.php?mod=forumdisplay&fid=4"
    ]

    def parse(self, response):
        item = WjninItem()
        sel = Selector(response)
        Posts = sel.xpath('//tr')
        for eachPost in Posts:
            title = eachPost.xpath('th/a[3]/text()').extract()
            type = eachPost.xpath('th/em/a/text()').extract()
            time = eachPost.xpath('td[2]/em/span/text()').extract()
            # 若为几天内的帖子不会在第一个span标签存储年月日信息
            if not time:
                time = eachPost.xpath('td[2]/em/span/span/@title').extract()

            author = eachPost.xpath('td[2]/cite/a/text()').extract()
            reply = eachPost.xpath('td[3]/a/text()').extract()
            read = eachPost.xpath('td[3]/em/text()').extract()
            url = eachPost.xpath('th/a[3]/@href').extract()
            # 公告等非帖子内容同样存储在tr标签内，但无法读取title信息，因此输出前先剔除
            if title:
                item['title'] = title
                item['type'] = type
                item['time'] = time
                item['author'] = author
                item['reply'] = reply
                item['read'] = read
                item['url'] = url
                yield(item)
        # 下一页
        nextLink = sel.xpath('//*[@id="fd_page_bottom"]/div/a[@class="nxt"]/@href').extract()
        if nextLink:
            nextLink = nextLink[0]
            print('NEXTLINK: ' + nextLink)
            # 递归
            yield Request(nextLink, callback=self.parse)
