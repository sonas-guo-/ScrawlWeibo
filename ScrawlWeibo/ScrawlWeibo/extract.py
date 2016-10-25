# -*- encoding:utf-8 -*-
import time
import datetime
class Extract():
    def extract_datetime(self,text):
        text=text.strip()
        l=text.split(' ')
        now=datetime.datetime.now()
        result_datetime=now
        if l:
            if '分钟前' in l[0]:
                minutes=int(l[0][:l[0].find('分钟前')])
                result_datetime=now-datetime.timedelta(minutes=minutes)
            elif '今天' in l[0]:
                hs=datetime.datetime.strptime(l[1],'%H:%M')
                result_datetime=datetime.datetime.combine(now.date,hs.time)
            elif '月' in l[0] and '日' in l[0]:
                mdhs=datetime.datetime.strptime(l[0]+l[1],'%m月%d日%H:%M')
                result_datetime=datetime.datetime(year=now.year,month=mdhs.month,day=mdhs.day,hour=mdhs.hour,minute=mdhs.minute)
            else:
                ymdhms=datetime.datetime.strptime(l[0]+' '+l[1],'%Y-%m-%d %H:%M:%S')
                result_datetime=ymdhms
            return result_datetime
if __name__=='__main__':
    extract=Extract()
    test='10月25日 10:56 来自iPhone 6'
    print(extract.extract_datetime(test))
