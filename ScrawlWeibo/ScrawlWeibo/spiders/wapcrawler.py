# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import get_base_url
from scrapy.spiders import Rule,CrawlSpider
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse,urljoin
from scrapy.http import Request,FormRequest
from scrapy.selector import Selector
from ScrawlWeibo.prelogin import PreLogin
from ScrawlWeibo.extract import Extract
from ScrawlWeibo import UserConfig
import urllib.request
import json
import re
import io
import os
class WapCrawler(CrawlSpider):
    name = 'wapcrawler'
    start_urls = [
        ]
    rules={
        }
    headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
            "Referer":"http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F%3Ffrom%3Dhome&backTitle=%CE%A2%B2%A9&vt=",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Connection":"keep-alive",
            "Host":"login.weibo.cn",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding":"gzip, deflate",
            "Upgrade-Insecure-Requests":'1',
            }
    formdata={
            "backTitle":"微博",
            "remember":"on",
            "submit":"登录",
            "tryCount":"",
            "backURL":"http%3A%2F%2Fweibo.cn%2F%3Ffrom%3Dhome",
            "capId":"",
            "code":"",
            "mobile":"",
            "remember":"on"
            }
    login_url=r'http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F%3Ffrom%3Dhome&backTitle=%CE%A2%B2%A9&vt='
    conf=UserConfig()
    def start_requests(self):
        self.formdata['mobile']=self.conf.username
        print("ready directly login...")
        yield Request(url="http://weibo.cn",cookies=self.conf.cookies,callback=self.login_successful)
    def direct_login(self,response):

        self.can_direct_login=False
        print('request again')
        self.start_requests()
    def prepare_login(self,response):
        current_url=response.url
        match_captcha_url=response.xpath('//div/img[1]/@src').extract()
        print(match_captcha_url)
        if (match_captcha_url):
            captcha_url=match_captcha_url[0]
        else:
            print('Can not find captcha url')
            return
        match_form_action=response.xpath('//div/form/@action').extract()
        match_vk=response.xpath('//div/form/div/input[@name="vk"]/@value').extract()
        match_capId=response.xpath('//div/form/div/input[@name="capId"]/@value').extract()        
        match_password_key=response.xpath("//div/form/div/input[@type='password']/@name").extract()
        match_backurl=response.xpath("//div/form/div/input[@name='backURL']/@value").extract()
        if match_form_action:
            form_action=match_form_action[0]
        if match_vk:
            vk=match_vk[0]
            self.formdata['vk']=vk
        if match_capId:
            capId=match_capId[0]
            self.formdata['capId']=capId
        if match_password_key:
            password_key=match_password_key[0]
            self.formdata[password_key]=self.conf.password
        if match_backurl:
            backurl=match_backurl[0]
            self.formdata['backURL']=backurl
        urllib.request.urlretrieve(captcha_url,'./captcha.jpg')
        print('Please input captcha')
        captcha=input()
        self.formdata['code']=captcha
        full_url=urljoin(current_url,form_action)
        print(self.formdata)
        yield FormRequest(url=full_url,formdata=self.formdata,callback=self.login_successful)
    def login_successful(self,response):
        #先看response的内容，是否是携带cookies登陆成功
        match_detail=response.xpath('//div[@class="u"]/div[@class="ut"]/a/text()').extract()
        login_with_cookies_flag=False
        if (match_detail):
            print(match_detail)
            detail=match_detail[0]
            if detail=='详细资料':
                login_with_cookies_flag=True
        if not login_with_cookies_flag:
                print("login with cookies failed!\nreay login by post formdata...")
                return Request(url=self.login_url,callback=self.prepare_login)
        #登陆成功
        print("login_successful")
        current_url=response.url
        match_follows_url=response.xpath('//div[@class="u"]/div[@class="tip2"]/a/@href').extract()
        if match_follows_url:
            follows_url=match_follows_url[1]
            full_follows_url=urljoin(current_url,follows_url)
            print(full_follows_url)            
            yield Request(url=full_follows_url,callback=self.get_follows)
    def get_follows(self,response):
        #print('getting follows...')
        current_url=response.url
        #open('test.html','wb').write(response.body)
        match_userpages=response.xpath('//table/tr/td[last()]/a[1]/@href').extract()
        match_usernames=response.xpath('//table/tr/td[last()]/a[1]/text()').extract()
        if match_userpages:
            for i in range(len(match_userpages)):
                userpage=match_userpages[i]
                full_userpage=urljoin(current_url,userpage)
                username=match_usernames[i]
                #print(username)
                #print(full_userpage)
                yield Request(url=full_userpage,callback=self.parse_user)
        match_pagenames=response.xpath('//div[@id="pagelist"]/form/div/a/text()').extract()
        match_pageurls=response.xpath('//div[@id="pagelist"]/form/div/a/@href').extract()
        if match_pagenames:
            for i in range(len(match_pagenames)):
                if match_pagenames[i]=="下页":
                    nextpage_url=match_pageurls[i]
                    full_nextpage_url=urljoin(current_url,nextpage_url)
                    yield Request(url=full_nextpage_url,callback=self.get_follows)
    def parse_user(self,response):
        current_url=response.url
        match_follow_url=response.xpath('//div[@class="u"]/div[@class="tip2"]/a[1]/@href').extract()
        if match_follow_url:
            follow_url=match_follow_url[0]
            full_follow_url=urljoin(current_url,follow_url)
            yield Request(url=full_follow_url,callback=self.get_follows)
        match_weibos=response.xpath('//body/div[@class="c"]').extract()
        match_dates=response.xpath('//body/div[@class="c"]/div[last()]/span[@class="ct"]/text()').extract()
        if match_dates:
            extract=Extract()
            for i in range(len(match_dates)):
                raw_date=match_dates[i]
                date=extract.extract_datetime(raw_date)
                raw_weibo=match_weibos[i]
        match_pagenames=response.xpath('//div[@id="pagelist"]/form/div/a/text()').extract()
        match_pageurls=response.xpath('//div[@id="pagelist"]/form/div/a/@href').extract()
        if match_pagenames:
            for i in range(len(match_pagenames)):
                if match_pagenames[i]=="下页":
                    nextpage_url=match_pageurls[i]
                    full_nextpage_url=urljoin(current_url,nextpage_url)
                    yield Request(url=full_nextpage_url,callback=self.parse_user)
        


