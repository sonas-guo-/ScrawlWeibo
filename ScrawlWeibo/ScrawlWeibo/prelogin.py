# -*- encoding: utf-8 -*-
import execjs
import base64

class PreLogin():
    def __init__(self):
        with open(r'./sinalogin.js','r') as f:
            jscode=f.read()
            jsruntime=execjs.get('JScript')
            self.ctx=jsruntime.compile(jscode)
    def get_username(self,username):
        result=self.ctx.call('get_name',username)
        return result
    def get_password(self,nonce,servertime,rsakey):
        result=self.ctx.call('get_password',nonce,servertime,rsakey)
        return result

if __name__=='__main__':
    pass
