# -*- encoding:utf8 -*-
import json
import sqlite3
import os
USERNAME='13598410723'
PASSWORD='497932893'
COOKIES='_T_WM=9da107c4d24d9741b24b81ae71783f72; SCF=Ak45nxsfcYhXK2ANTWTDAJGB9Oefvi9HE4z2Wi0HSqpjWxb2ClBWez8zBEx_6VShN1ieO1votN0dOFFKuzWeRLA.; SUHB=0wnEDXJFI2k3ja; WEIBOCN_FROM=home; SUB=_2A251CwuWDeTxGedG71YQ9C7Oyz6IHXVW95XerDV6PUJbkdANLWbgkW2h2104EsFFh9taxHLBBfwOr1R7kw..; gsid_CTandWM=4uYMa6911utmPJxhNutUM7JKc3g'
DATAPATH=r'F:/GitHub/ScrawlWeibo/data'
class UserConfig():
    username=''
    password=''
    cookies={}
    def __init__(self):
        global COOKIES
        self.username=USERNAME
        self.password=PASSWORD
        self.datapath=DATAPATH
        COOKIES=COOKIES.replace('\n','')
        self.cookies=self.parser_cookies()
        self.init_data_warehouse()
    def parser_cookies(self):
        result={}
        items=COOKIES.split(';')
        for item in items:
            key,value=item.split('=')
            result[key]=value
        return result
    def init_data_warehouse(self):
        if not os.path.exists(self.datapath):
            os.makedirs(self.datapath)
        try:
            os.mkdir(self.datapath+'/crawl_record')
        except Exception as e:
            print(e)
        try:
            os.mkdir(self.datapath+'/id2info_map')
        except Exception as e:
            print(e)
        try:
            os.mkdir(self.datapath+'/weibo')
        except Exception as e:
            print(e)
        try:
            os.mkdir(self.datapath+'/follows')
        except Exception as e:
            print(e)
        try:
            os.mkdir(self.datapath+'/fans')
        except Exception as e:
            print(e)
    def get_datapath(self):
        paths={}
        paths['root']=self.datapath
        paths['records']=self.datapath+'/crawl_record'
        paths['id2info']=self.datapath+'/id2info_map'
        paths['weibos']=self.datapath+'/weibo'
        paths['follows']=self.datapath+'/follows'
        paths['fans']=self.datapath+'/fans'
        return paths
    def __str__(self):
        return 'username=%s\npassword=%s\ncookies=%s' %(self.username,self.password,json.dumps(self.cookies,indent=1))
if __name__=='__main__':
    conf=UserConfig()
    print(conf)
