# -*- coding: utf-8 -*-
import os
import scrapy
from scrapy.utils.response import get_base_url
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors import LinkExtractor
from urllib.parse import urlparse
from scrapy.http import Request,FormRequest
class Scrawler(scrapy.Spider):
    name = 'scrawler'
    start_urls = [
        'http://newids.seu.edu.cn/authserver/login?goto=http://my.seu.edu.cn/index.portal'
        ]
    rules={
        }
    headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
            "Referer":"http://newids.seu.edu.cn/authserver/login?goto=http://my.seu.edu.cn/index.portal",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Connection":"keep-alive",
            }
    formdata={
            "username":"220161511",
            "password":"guolinsen123"
            }
    def after_login(self,response):
        print('login successful')
        print(response.body)
        open("test.html", 'wb').write(response.body)
        pass
    def parse(self,response):
        print('ready login')
        unready_prams=[
                'lt',
                'dllt',
                'execution',
                '_eventId',
                'rmShown'
                ]
        for item in unready_prams:
            query='//div[@tabid="01"]/form/input[@name=\"'+item+'\"]/@value'
            value=response.xpath(query).extract()
            self.formdata[item]=value
            print('%s=%s'%(item,value))
        yield FormRequest(
                "http://my.seu.edu.cn/index.portal",
                self.headers,
                self.formdata,
                callback=self.after_login)
