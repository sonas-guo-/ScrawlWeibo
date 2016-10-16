# -*- coding: utf-8 -*-
import os
import scrapy
from scrapy.utils.response import get_base_url
from scrapy.spiders import Rule,CrawlSpider
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from scrapy.http import Request,FormRequest
from scrapy.selector import Selector
from ScrawlWeibo.prelogin import PreLogin
import json
import re
import io
import gzip
import lxml
from bs4 import BeautifulSoup
from urllib.parse import urljoin
class Scrawler(CrawlSpider):
    name = 'scrawler'
    start_urls = [
        #'http://newids.seu.edu.cn/authserver/login?goto=http://my.seu.edu.cn/index.portal'
        ]
    rules={
            #Rule(LinkExtractor(allow=('.*')), callback='parse_user')
        }
    headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
            "Referer":"http://weibo.com/",
            "Accept":"*/*",
            "Connection":"keep-alive",
            "Host":"login.sina.com.cn",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding":"gzip, deflate, br",
            "Cookie":"U_TRS1=000000af.b4a63d29.57c7d7f5.e795e0db; UOR=www.baidu.com,blog.sina.com.cn,; SINAGLOBAL=223.3.76.88_1472714742.511501; ULV=1475935395234:14:6:5:223.3.76.88_1475931746.660821:1475931744422; vjuids=-ce103e475.156e4a68a21.0.a40e693838e5e; vjlast=1472714935.1476091377.11; lxlrtst=1475130147_o; lxlrttp=1475130147; SCF=AnJFF8L6wR9zJ4vCHpHt2dHlyIQk6Cyra1AIxugDmi0MJscTImbMappZJyQwTrv_VXpl91bqedD5-wzu9y_uno0.; SUB=_2AkMgorWXdcNhrAJZnPwUyGvgbI9H-jzEiebBAn7tJhMyAhh77lxSqSVFN6emcXZ8gvni6GG9IfWIhtxZxA..; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WFxw.fzHUb0FHrpb-vmMOv35JpV2020SK.RSh27S0z0BGSDdJ2VqcRt; __gads=ID=1a44820a22e8c483:T=1476091387:S=ALNI_MbJQ7RZ0km7VLUYWkUY8Sjs-tRrLg; Apache=223.3.76.88_1476348445.370989"
            }
    formdata={
            "encoding":"UTF-8",
            "weibo":"weibo",
            "from":"",
            "gateway":"1",
            "pagerefer":"",
            "pwencode":"rsa2",
            "returntype":"META",
            "service":"miniblog",
            "sr":"1920*1080",
            "url":"http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "useticket":"1",
            "vsnf":"1",
            "prelt":"176"
            }
    def start_requests(self):
        print("start prelogin")
        prelogin=PreLogin()
        data=prelogin.get_data()
        self.formdata['su']=data['su']
        self.formdata['sp']=data['sp']
        self.formdata['nonce']=data['nonce']
        self.formdata['servertime']=data['servertime']
        self.formdata['rsakv']=data['rsakv']
        yield FormRequest(url='http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)',
                formdata=self.formdata,
                callback=self.redirect)
    def redirect(self,response):
        print("redirect...")
        content=response.body.decode('GBK')
        pattern=r"location\.replace\('(.*?)'\)"
        redirect_url=re.findall(pattern,content)[0]
        print('going to '+redirect_url)
        return Request(url=redirect_url,method='GET',callback=self.after_redirect)
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
        content=response.body.decode('utf8')
        #open('data.html','wb').write(content)
        pattern=r'<li class=\\"member_li S_bg1\\"(.*?)<\\/li>'
        results=re.findall(pattern,content)
        for result in results:
            #匹配follow的用户的<a>标签
            pattern1=r'<div class=\\"title.*?(<a.*?<\\/a>)'
            tag_a=re.findall(pattern1,result)[0]
            if 'usercard' in tag_a:
                href=re.findall(r'href=\\"(.*?)\\"',tag_a)[0]#用户的链接
                title=re.findall(r'title=\\"(.*?)\\"',tag_a)[0]#用户名
                usercard=re.findall(r'usercard=\\"id=(.*?)\\"',tag_a)[0]#用户id
                print(title)
                print(href)
                print(usercard)
                print('分割')
        pass
    def parse_user(self,response):
        print('parse user')
        sel=response.xpath('//div[@id="Pl_Core_T8CustomTriColumn__3"]/div/div/div/table/tbody/tr')
        all_watch_url=sel.xpath('//td[0]/a/@href').extract()
        all_fans_url=sel.xpath('//td[1]/a/@href').extract()
        all_weibo_url=sel.xpath('//td[last()]/a/@href').extract()
        print(all_watch_url)
    #def parse(self,response):
        pass
        '''
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
        '''
