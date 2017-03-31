#!/usr/bin/env python
import sys
import mechanize
import cookielib
import random
import time
import urllib2

class Crawler:
    def __init__(self):
        #Browser
        self.br = mechanize.Browser()
        
        #set cookie
        cj = cookielib.LWPCookieJar()
        self.br.set_cookiejar(cj)
        
        #options
        self.br.set_handle_equiv(True)
        #self.br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        
        #Follows refresh 0 but not hangs on refresh > 0
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        
        #debugging?
        self.br.set_debug_http(True)
        self.br.set_debug_redirects(True)
        self.br.set_debug_responses(True)
    
    def set_ua(self, useragent=""):
        #User-Agent (this is cheating, ok?)
        if useragent != "":
            self.br.addheaders = [('User-agent', useragent)]
        else:
            self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    def set_proxy(self, ipport, type="http", user="", passwd=""):
        #Proxy
        #self.br.set_proxies({"http": ipport})
        self.br.set_proxies({type: ipport})
        if user!="":
            self.br.add_proxy_password(user, passwd)
        
        #Proxy and usrer/password
        #self.br.set_proxies({"http":"username:password@proxy.com:8888"})

    def get_content(self, url):
        #self.br.add_password('http://www.taobao.com', 'sone', '1985')
        r = self.br.open(url)
        html = r.read()
        #print html
        #print br.response().read()
        #print self.br.title().decode("gbk").encode("utf-8") 
        #print self.br.title()
        print r.info()
        return html

class  Processor:
    # load user agent
    def __init__(self, ua, proxy, outfile="", errfile=""):
        if len(outfile)!=0:
            self.outfp = open(outfile, "a+")
        else:
            self.outfp = sys.stdout
        if len(errfile)!=0:
            self.errfp = open(errfile, "a+")
        else:
            self.errfp = sys.stderr
        self.ua_list    = list()
        self.proxy_list = list()
        #load ua
        fp = open(ua)
        for line in fp:
            line = line.strip()
            if len(line)!=0:
                self.ua_list.append(line)

        #load proxy
        fp = open(proxy)
        for line in fp:
            line = line.strip()
            if len(line)!=0:
                sections = line.split("\t")
                if len(sections) == 7:
                    self.proxy_list.append((sections[1]+":"+sections[2], sections[5].lower()))

        print "ua_list:",len(self.ua_list),"proxy_list",len(self.proxy_list)

        self.crawler = Crawler()

    def _delete_proxy(self, proxy):
        """delete proxy in proxy_list"""
        print "except, remove proxy: ", proxy 
        new_set  = set(self.proxy_list)
        new_set.remove(proxy)
        self.proxy_list = list(new_set)

    def crawl_content(self, url):
        retCode = -1
        html    = ""
        # random get useragent/proxy to use
        ua    = self.ua_list[random.randrange(0,len(self.ua_list))]
        proxy = self.proxy_list[random.randrange(0,len(self.proxy_list))]
        
        #set ua,proxy
        print ua,proxy
        self.crawler.set_ua(ua)
        self.crawler.set_proxy(proxy[0], proxy[1])
        
        #crawl url
        try:
            html = self.crawler.get_content(url)
            html = html.decode("gbk").encode("utf-8")
            html = html.replace("\r", "")
            html = html.replace("\n", "")
            #html.replace("\n","")
            #print >> self.outfp, "%d%s%s" % (cnt,url,html)
            retCode = 0
        #except urllib2.HTTPError,e:
        except urllib2.URLError,e:
            print >> self.errfp,  "%d%s" %(cnt, url)
            if hasattr(e,"code") and (-2 == e.code):
                #urllib2.URLError: <urlopen error [Errno -2] Name or service not known>, not exist
                pass
            else:
                self._delete_proxy(proxy)
        except:
            print "some error/exception occured"
            #print >> self.errfp,  "%d%s" %(cnt, url)
            # connection refused or return badstatus
            self._delete_proxy(proxy)
        finally:
            return (retCode,html)
        
    def crawl_content_ext(self, url):
        """craw url 3 times"""
        tryTimes = 3
        ret  = -1
        html = ""

        # -99 means no proxy to use
        if len(self.proxy_list) == 0:
            return (-99, html)
        while (tryTimes>0) and (ret != 0):
            (ret,html) = self.crawl_content(url)
            tryTimes = tryTimes - 1
        return (ret,html)

    def close_fp(self):
        if self.errfp and (self.errfp != sys.stderr):
            close(self.errfp)
        if self.outfp and (self.outfp != sys.stdout):
            close(sefl.outfp)

if __name__ == "__main__":
    p = Processor("ua.txt", "proxy.txt")
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
    (ret, html) = p.crawl_content("http://detail.m.tmall.com/item.html?id=7679214500")
    if ret == 0:
        fp.write(html)
        fp.close()
    else:
        print "craw error"
    exit(0)
    crawler = Crawler()
    crawler.set_ua("")
    #crawler.set_proxy("202.171.253.84:86")
    #crawler.set_proxy("115.124.75.148:80", "https")
    #crawler.set_proxy("49.1.245.235:3128", "https")
    crawler.set_proxy("49.1.245.235:3128", "https")
    crawler.get_content("http://www.sina.com")

