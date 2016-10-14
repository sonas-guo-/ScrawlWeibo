# -*- encoding: utf-8 -*-
import execjs
import base64
import json
import time
import binascii
import rsa
from urllib import request
class PreLogin():
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
    def __init__(self):
        '''
        with open(r'./sinalogin.js','r') as f:
            jscode=f.read()
            jsruntime=execjs.get('JScript')
            self.ctx=jsruntime.compile(jscode)
        '''
        preUrl='https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.18)&_='
        preUrl+=str(int(time.time() * 1000))
        result=request.urlopen(preUrl)
        content=result.read()
        s=str(content,encoding='utf-8')
        sjson=s[s.find('{'):s.rfind('}')+1]
        self.data=json.loads(sjson)
        su=self.get_username('13598410723')
        sp=self.get_password('497932893',self.data['nonce'],self.data['servertime'],self.data['pubkey'])
        self.data['su']=su
        self.data['sp']=sp
        for key,value in self.data.items():
            if type(value)==int:
                self.data[key]=str(value)
    def get_username(self,username):
        su=base64.b64encode(username.encode("utf-8"))
        return su
    def get_password(self,password,nonce,servertime,rsakey):
        rsaPublickey = int(rsakey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537)
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
        message = message.encode("utf-8")
        sp=rsa.encrypt(message, key).hex()
        return sp
    def get_data(self):
        return self.data
if __name__=='__main__':
    prelogin=PreLogin()
