import sys  
sys.path.append("/usr/lib/hive/lib/py")
from hive_service import ThriftHive  
from hive_service.ttypes import HiveServerException  
from thrift import Thrift  
from thrift.transport import TSocket  
from thrift.transport import TTransport  
from thrift.protocol import TBinaryProtocol  
  
def hiveExe(sql):  
  
    try:  
        print "init tsocket"
        transport = TSocket.TSocket('192.168.34.91', 10000)   
        #transport = TSocket.TSocket('localhost', 10000)   
        print "init tbuffer"
        transport = TTransport.TBufferedTransport(transport)  
        protocol = TBinaryProtocol.TBinaryProtocol(transport)  
        print "init thrifthive client"
        client = ThriftHive.Client(protocol)  
        print "transport open ..."
        transport.open()  

        print "execute sql"
        client.execute(sql)  

        print "The return value is : "   
        print client.fetchAll()  
        print "............"  
        transport.close()  
    except Thrift.TException, tx:  
        print '%s' % (tx.message)  
  
if __name__ == '__main__':  
    #hiveExe("show tables")
    hiveExe("select * from jd_id limit 10;")
