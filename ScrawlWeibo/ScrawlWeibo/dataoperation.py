# -*- encoding:utf8 -*-
import sqlite3
from __init__ import UserConfig
class DataOperation():
    datapath=''
    def __init__(self):
        config=UserConfig()
        self.datapath=config.get_datapath()
    def create_folders(self):
        pass
    def create_crawlrecords_table(self):
        conn = sqlite3.connect(self.datapath['records']+'/records.db')
        cursor = conn.cursor()
        cursor.execute("create table records(id text,starttime text,endtime text)")
        conn.close()
    def create_id2infomap_table(self):
        conn = sqlite3.connect(self.datapath['id2info']+'/infos.db')
        cursor = conn.cursor()
        cursor.execute("create table infos(id text,name text,birthday text)")
        conn.close()
    def create_userweibos_table(self,userid):
        conn = sqlite3.connect(self.datapath['weibos']+'/'+userid+'.db')
        cursor = conn.cursor()
        cursor.execute("create table weibos(id text,time text,weibo text)")
        conn.close()
    def create_userfollows_table(self):
        conn = sqlite3.connect(self.datapath['follows']+'/follows.db')
        cursor = conn.cursor()
        cursor.execute("create table follows(id text,followid text)")
        conn.close()
    def create_userfans_table(self):
        conn = sqlite3.connect(self.datapath['fans']+'/fans.db')
        cursor = conn.cursor()
        cursor.execute("create table follows(id text,fanid text)")
        conn.close()
    def insert_crawlrecords(self):
        pass
    def insert_id2info(self):
        pass
    def insert_userweibos(self):
        pass
    def insert_userfollows(self,userid,follows):
        pass
    def insert_userfans(self,userid,fans):
        pass
if __name__=='__main__':
    opr=DataOperation()
