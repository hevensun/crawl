import threading
import time
import os
import sys

#from crawler import Processor
from crawlerjs import Processor

mutex   = threading.Lock()
#fp      = open('data/part0-tb.txt')
fp      = open('../tb-url/part-3-ae')
outfmt  = "/bigdata2/songgang/part-3-ae/%d"
#fp      = open('../tb-url/part2-tb-10.txt')
#fp      = open('data/results-taobao-10.csv')
#fp      = open('jd.url')
line_no = long(0)
class Reader(threading.Thread):
    def __init__(self, num, process_no, process_total):
        threading.Thread.__init__(self) 
        self.num  = num
        self.p_no = process_no
        self.p_total = process_total

        #self.process = Processor("ua.txt", "proxy.txt")
        self.process  = Processor()

        global outfmt
        outdir = outfmt %(process_no)
        print "outdir:", outdir
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        #outfile      = "/data1/songgang/tb-content/mpart2/part2-out-%s.txt" % (num) 
        outfile      =  outdir + "/part-out-%s.txt" % (num) 
        self.errfile =  outdir + "/part-err-%s.txt" % (num) 
        self.fpout   = open(outfile, "a+")
        self.fperr   = None

    def run(self):
        global line_no
        while True:
            with mutex:
                line = fp.readline()
                if not line:
                    break
                line_no = line_no + 1
                if (line_no%self.p_total) != self.p_no :
                    continue

            id  = ""
            url = ""
            line = line.strip()
            sections = line.split("=")
            if(len(sections)==2):
                id  = sections[1]
                url = "http://h5.m.taobao.com/awp/core/detail.htm?id=" + id
            else:
                continue


            (ret, html) = self.process.crawl_content_ext(url)

            if ret == 0 :
                #write content
                self.fpout.write(id+""+url + "" + line+""+html)
            elif ret == -99:
                if self.fperr is None:
                    self.fperr   = open(self.errfile, "a+")
                self.fperr.write(line+"\n")
                if self.fperr:
                    close(self.fperr)
                return
            else:
                #wrtie err log
                if self.fperr is None:
                    self.fperr   = open(self.errfile, "a+")
                self.fperr.write(line+"\n")

            print('%d->%d:%s' % (line_no, self.num, line))
            #time.sleep(0.1)
        if self.fpout:
            self.fpout.close()
        if self.fperr:
            self.fperr.close()


if __name__ == '__main__':
    thread_num  = 20
    #thread_num  = 2
    process_no    = int(sys.argv[1])
    process_total = int(sys.argv[2])
    thread_list = list();
    for i in range(0, thread_num):
        thread_list.append(Reader(i, process_no, process_total))
        thread_list[i].start()

    for i in range(0, thread_num):
        thread_list[i].join()

    fp.close()
