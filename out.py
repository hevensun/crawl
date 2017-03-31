import sys

f=open('test.txt','w')
s= '123'
abc= '456'
print >> f, s+""+abc
print >> f, s+""+abc+"2"
print >> open('test.txt', 'w'), s+""+abc+"3"
f.close()
