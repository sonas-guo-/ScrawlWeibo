# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import get_base_url
from scrapy.spiders import Rule,CrawlSpider
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse,urljoin
from scrapy.http import Request,FormRequest
from scrapy.selector import Selector
from ScrawlWeibo.prelogin import PreLogin
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
            "Cookie":"SCF=AnJFF8L6wR9zJ4vCHpHt2dHlyIQk6Cyra1AIxugDmi0MaraSefcPFzEoyu8qyODgVtM4fpt__bA9fdayJg1HSrw.; SUHB=0XDUVwVv5j6mxr; _T_WM=fa6aebdfa9ade0c0133052c1abd777c8; SUB=_2AkMvWpo_dcNhrAJZnPwUyGvgbI9H-jzEiebBAn7oJhMyPRgv7lUTqScPRrgu93amHWZ0objca1CgRcUsbg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFxw.fzHUb0FHrpb-vmMOv35JpX5o2p5NHD95Qp1hBXeKB7eo5EWs4Dqcj_i--ci-zpi-2Xi--fi-2NiKnci--fiKnfiKyFi--4i-zEiKnpi--ci-20i-88; WEIBOCN_FROM=home"
            }
    formdata={
            "backTitle":"微博",
            "remember":"on",
            "submit":"登录",
            "tryCount":""
            }
    login_url=r'http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F%3Ffrom%3Dhome&backTitle=%CE%A2%B2%A9&vt='
    def start_requests(self):
        print("ready login...")
        yield Request(url=self.login_url,callback=self.prepare_login)
    def prepare_login(self,response):
        match_captcha_url=response.xpath('//div/img[1]/@src').extract()
        print(match_captcha_url)
        if (match_captcha_url):
            captcha_url=match_captcha_url[0]
        else:
            print('Can not find captcha url')
            return
        urllib.request.urlretrieve(captcha_url,'./captcha.jpg')
        print('Please input captcha')
        captcha=input()
        match_form_action=response.xpath('//div/form/@action').extract()
        match_vk=response.xpath('//div/form/div/input[@name="vk"]/@value').extract()
        match_capId=response.xpath('//div/form/div/input[@name="capId"]/@value').extract()        
        match_password_key=response.xpath("//div/form/div/input[@type='password']/@name").extract()
        match_backurl_key=response.xpath("//div/form/div/input[@name='backURL']/@value").extract()
        print(match_form_action)
        print(match_vk)
        print(match_password_key)
        print(match_backurl_key)
        #return Request(url=redirect_url,method='GET',callback=self.after_redirect)
    def after_redirect(self,response):
        print("redirected")
        content=response.body.decode('utf-8')
        #print(content)
        pattern=r'\"userinfo\":(.*?\})\}'
        userinfo=re.findall(pattern,content)[0]
        info=json.loads(userinfo)
        homepage='http://weibo.com/u/%s/home%s'%(info['uniqueid'],info['userdomain'])
        #print(homepage)
        return Request(url=homepage,headers={
            "Accept-Encoding": "gzip"
            },callback=self.login_successful)
    def login_successful(self,response):
        print("login successful")
        current_url=response.url
        #print(current_url)
        #print(response.body)
        #open("test1.html", 'wb').write(response.body)
        #获取自己的关注用户,粉丝
        content=response.body
        s=content.decode('utf-8','ignore')
        pattern=r'/(\d+?)/'
        usernumber=re.findall(pattern,current_url)[0]
        watch_url=r'/%s/follow?rightmod=1&wvr=6'%(usernumber)
        fan_url=r'/%s/fans?rightmod=1&wvr=6'%(usernumber)
        watch_url=urljoin(current_url,watch_url)
        fan_url=urljoin(current_url,fan_url)
        yield Request(url=watch_url,callback=self.get_my_watches)
    def get_my_watches(self,response):
        print('getting my watches...')
        current_url=response.url
        content=response.body.decode('utf8')
        pattern=r'<li class=\\"member_li S_bg1\\"(.*?)<\\/li>'
        results=re.findall(pattern,content)
        for result in results:
            #匹配follow的用户的<a>标签
            pattern1=r'<div class=\\"title.*?(<a.*?<\\/a>)'
            tag_a=re.findall(pattern1,result)[0]
            if 'usercard' in tag_a:
                raw_href=re.findall(r'href=\\"(.*?)\\"',tag_a)[0]#用户的链接
                title=re.findall(r'title=\\"(.*?)\\"',tag_a)[0]#用户名
                usercard=re.findall(r'usercard=\\"id=(.*?)\\"',tag_a)[0]#用户id
                href=raw_href.replace(r'\/','/')
                full_href=urljoin(current_url,href)
                #print(title)
                #print(full_href)
                yield Request(url=full_href,callback=self.parse_user)
                #print(usercard)
                #print('分割')
        pattern=r'<a bpfilter=\\"page\\" class=\\"page next S_txt1 S_line1\\".*?href=\\"(.*?)\\"><span>'
        result=re.findall(pattern,content)
        if result:
            raw_url=result[0]
            next_url=raw_url.replace(r'\/','/')
            full_next_url=urljoin(current_url,next_url)
            yield Request(url=full_next_url,callback=self.get_my_watches)
    def parse_user(self,response):
        print('parse user')
        current_url=response.url
        content=response.body.decode('utf8')
        pattern=r'<table class=\\"tb_counter\\".*?<tr>.*<\\/tr>.*?<\\/table>'
        match_result=re.findall(pattern,content)
        if match_result:
            result=match_result[0]
            ntag_a=re.findall(r'<a.*?a>',result)
            if ntag_a:
                for tag_a in ntag_a:
                    #print(tag_a)
                    if '微博' in tag_a:
                        #print(tag_a)
                        match_weibo_url=re.findall(r'href=\\"(.*?)\\"',tag_a)
                        if match_weibo_url:
                            url=match_weibo_url[0]
                            url=url.replace(r'\/','/')
                            full_url=urljoin(current_url,url)
                            yield Request(url=full_url,callback=self.get_all_weibos)
                    if '关注' in tag_a:
                        match_follow_url=re.findall(r'href=\\"(.*?)\\"',tag_a)
                        if match_follow_url:
                            url=match_follow_url[0]
                            url=url.replace(r'\/','/')                            
                            full_url=urljoin(current_url,url)
                    if '粉丝' in tag_a:
                        pass
    def get_all_weibos(self,response):
        pass
