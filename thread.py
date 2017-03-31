import threading
import time

#from crawler import Processor
from crawlerjs import Processor

mutex   = threading.Lock()
mutex2   = threading.Lock()
#fp      = open('data/part0-tb.txt')
fp      = open('data/results-taobao.csv')
#fp      = open('data/results-taobao-10.csv')
#fp      = open('jd.url')
line_no = 0

class Reader(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self) 
        self.num     = num
        #self.process = Processor("ua.txt", "proxy.txt")
        self.process = Processor()

        outfile      = "/data1/songgang/tb-content/mpart0/part0-out-%s.txt" % (num) 
        errfile      = "/data1/songgang/tb-content/mpart0/part0-err-%s.txt" % (num) 
        self.fpout   = open(outfile, "a+")
        self.fperr   = open(errfile, "a+")

    def run(self):
        global line_no
        while True:
            with mutex:
                line = fp.readline()
                if not line:
                    break
                line_no = line_no + 1

            id  = ""
            url = ""
            sections = line.strip().split(",")
            if(len(sections)==4):
                id  = sections[3]
                url = "http://h5.m.taobao.com/awp/core/detail.htm?id=" + id
            else:
                continue


            (ret, html) = self.process.crawl_content_ext(url)

            if ret == 0 :
                #write content
                self.fpout.write(id+""+url+""+html+"\n")
            elif ret == -99:
                self.fperr.write(line+"\n")
                if self.fperr:
                    close(self.fperr)
                return
            else:
                #wrtie err log
                self.fperr.write(line+"\n")
            print('%d->%d:%s' % (line_no, self.num, line))
            time.sleep(0.1)
        if self.fpout:
            self.fpout.close()
        if self.fperr:
            self.fperr.close()


if __name__ == '__main__':
    thread_num  = 50
    thread_list = list();
    for i in range(0, thread_num):
        thread_list.append(Reader(i))
        thread_list[i].start()

    for i in range(0, thread_num):
        thread_list[i].join()

    fp.close()
