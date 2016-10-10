# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScrawlweiboPipeline(object):
    def process_item(self, item, spider):
        url=item['link']
        downloader=Downloader()
        if url.endswith('.pdf') or  url.endswith('.doc'):
            downloader.download(url)
        return item
