# -*- coding: utf-8 -*-
import os
import scrapy
from scrapy.utils.response import get_base_url
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors import LinkExtractor
from urllib.parse import urlparse
from scrapy.http import Request,FormRequest
from ScrawlWeibo.prelogin import PreLogin
import json
import re
class Scrawler(scrapy.Spider):
    name = 'scrawler'
    start_urls = [
        #'http://newids.seu.edu.cn/authserver/login?goto=http://my.seu.edu.cn/index.portal'
        "http://weibo.com/"
        ]
    rules={
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
        print(content)
        pattern=r'\"userinfo\":(.*?\})\}'
        userinfo=re.findall(pattern,content)[0]
        info=json.loads(userinfo)
        homepage='http://weibo.com/u/%s/home%s'%(info['uniqueid'],info['userdomain'])
        #print(homepage)
        return Request(url=homepage,callback=self.login_successful)
    def login_successful(self,response):
        print("login successful")
        open("test1.html", 'wb').write(response.body)
    def parse(self,response):
        print(response.url)
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
