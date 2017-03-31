#/usr/bin/env python
import sys

def main(num):
    """"""
    print "begin"
    fpList = []
    for i in range(8):
        filename = "part-"+ str(i+1)
        fpList.append(open(filename, "a+"))

    #fp = open("tb-100.txt")
    fp = open("tb-all.txt")
    index = long(0)
    done  = False
    while not done:
        line = fp.readline()
        if line != "":
            fpList[ index % num].write(line)
            index = index + 1
            print index
        else:
            done = True

    for i in range(8):
        fpList[i].close()

if __name__ == "__main__":
    print sys.argv
    main(int(sys.argv[1]))
