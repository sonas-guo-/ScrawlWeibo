# -*- encoding: utf-8 -*-
import os
import sys
import time
import urllib.request
HIGH_PROGRESSBAR_PRECESION=50
def callbackfunc(blocknum, blocksize, totalsize):
    progressbar(blocknum*blocksize,totalsize,HIGH_PROGRESSBAR_PRECESION)
    
def progressbar(numerator,denominator,precision):
    '''
    @pram precision max basic unit number,namely max '-' number
    '''
    s='['
    percent=numerator/denominator
    for i in range(precision):
        if  i<numerator/denominator*(precision+1):
            s+='-'
        else:
            s+=' '
    s+='] '+str(percent)+'% '
    s+=str(numerator)+' bytes / '+str(denominator)+' bytes\r'
    sys.stdout.write('\r%s Percent:%0.2f % %0.4f bytes / %0.4f bytes'%(percent,numerator,denominator))
    sys.stdout.flush()
class Downloader():
    def __init__(self):
        self.folderpath=r'../tmp'
        if not os.path.exists(self.folderpath):
            os.mkdir(self.folderpath)
    def download(self,url,name=None):
        if name==None:
            name=url[url.rfind('/')+1:]
        print(url,name)
        filename=self.folderpath+'/'+name
        urllib.request.urlretrieve(url,filename,callbackfunc)
