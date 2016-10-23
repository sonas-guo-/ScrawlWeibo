# -*- encoding:utf8 -*-
import json
USERNAME='13598410723'
PASSWORD='497932893'
COOKIES='SCF=AnJFF8L6wR9zJ4vCHpHt2dHlyIQk6Cyra1AIxugDmi0MaraSefcPFzEoyu8qyODgVtM4fpt__bA9fdayJg1HSrw.; SUHB=0XDUVwVv5j6mxr; _T_WM=fa6aebdfa9ade0c0133052c1abd777c8; SUB=_2A251DzxBDeTxGedG71YQ9C7Oyz6IHXVW8EQJrDV6PUJbkdAKLRHtkW1TD4LmBAoa8NaA1ULhB1kiD7KaXQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFxw.fzHUb0FHrpb-vmMOv35JpX5o2p5NHD95Qp1hBXeKB7eo5EWs4Dqcj_i--ci-zpi-2Xi--fi-2NiKnci--fiKnfiKyFi--4i-zEiKnpi--ci-20i-88; WEIBOCN_FROM=feed; gsid_CTandWM=4ulIa6911M8dcTKKnXH5Z7JKc3g'
class UserConfig():
    username=''
    password=''
    cookies={}
    def __init__(self):
        self.username=USERNAME
        self.password=PASSWORD
        COOKIES=COOKIES.replace('\n','')
        self.cookies=self.parser_cookies()
    def parser_cookies(self):
        result={}
        items=COOKIES.split(';')
        for item in items:
            key,value=item.split('=')
            result[key]=value
        return result
    def __str__(self):
        return 'username=%s\npassword=%s\ncookies=%s' %(self.username,self.password,json.dumps(self.cookies,indent=1))
if __name__=='__main__':
    conf=UserConfig()
    print(conf)
