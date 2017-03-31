#!/usr/bin/env python
import sys
import random
import time
import subprocess

CASPERPATH="/usr/bin/casperjs"

class  Processor:
    # load user agent
    def __init__(self):
        """"""
        self.casperpath = CASPERPATH

        pass
    def crawl_content(self, url):
        retCode = -1
        html    = ""
        #crawl url
        try:
            cmd = CASPERPATH + " mini.js --url=" + url
            print cmd
            ret = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE,\
                    stderr = subprocess.STDOUT)
            if ret:
                for line in iter(ret.stdout.readline, b''):
                    if line.startswith('content:'):
                        html = line[8:]
                        retCode = 0
                        return (retCode,html)
        except Exception,e:
            print "some error/exception occured"
            print e
            #print >> self.errfp,  "%d%s" %(cnt, url)
            # connection refused or return badstatus
        finally:
            return (retCode,html)
        
    def crawl_content_ext(self, url):
        """craw url 3 times"""
        tryTimes = 3
        ret  = -1
        html = ""

        # -99 means no proxy to use
        while (tryTimes>0) and (ret != 0):
            (ret,html) = self.crawl_content(url)
            tryTimes = tryTimes - 1
        return (ret,html)


if __name__ == "__main__":
    p = Processor()
    #fp = open("tb-1.url")
    #fp = open("jd-10.url")
    #fp = open("data/part0-tb.txt")
    #cnt = 0
    #for line in fp:
    #    line = line.strip()
    #    (ret, html) = p.crawl_content_ext(line)
    #    print line,ret,len(html)
    #    cnt = cnt + 1
    #    time.sleep(0.5)
    #p.close_fp()
    #exit(0)

    fp = open("mtb.out","a+")
    #(ret, html) = p.crawl_content_ext("http://detail.m.tmall.com/item.html?id=7679214500")
    (ret, html) = p.crawl_content_ext("http://h5.m.taobao.com/awp/core/detail.htm?id=10314043465")
    if ret == 0:
        fp.write(html)
        fp.close()
    else:
        print "craw error"
    exit(0)

