import sys  
from BeautifulSoup import BeautifulSoup
  
def parse(html):  
  
    try:  
        soup = BeautifulSoup(html)
        #print soup.findAll(['title'])
        print soup.findAll('meta', attrs={'name': 'keywords'})[0]["content"]
        print soup.findAll('meta', attrs={'name': 'description'})[0]["content"]
        print soup.findAll(['title'])[0].next
    except Exception, tx:  
        print '%s' % (tx.message)  
  
if __name__ == '__main__':  
    #hiveExe("show tables")
    fp = open("data/part0-out.txt")
    for line in fp:
        line = line.strip()
        if len(line)!=0:
            sections = line.split("")
            print sections[1]
            parse(sections[2])
            #break
