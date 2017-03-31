#!/usr/bin/env python
# -*- coding: utf-8 -*-
# hive util with hive server2


import pyhs2

class HiveClient:
    def __init__(self, db_host, user, password, database, port=10000, authMechanism="PLAIN"):
        """
        create connection to hive server2
        """
        self.conn = pyhs2.connect(host=db_host,
                                  port=port,
                                  authMechanism=authMechanism,
                                  user=user,
                                  password=password,
                                  database=database,
                                  )

    def runsql(self, sql):
        """
        query
        """
        retList = []
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(sql)
                return cursor.fetch()
            except Exception,e:
                print e
                print "error occured"

    def query(self, sql):
        """
        query
        """
        retList = []
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(sql)
                #return cursor.fetch()
                res = cursor.fetchone()
                retList.append(res)
                print res
                while(res):
                    res = cursor.next()
                    retList.append(res)
                    print res
            except StopIteration,e:
                return retList


    def close(self):
        """
        close connection
        """
        self.conn.close()


def main():
    hive_client = HiveClient(db_host='192.168.34.91', port=10000, user='hdfs', password='mypass',
                             database='default', authMechanism='PLAIN')
    #result = hive_client.query('select * from url_business limit 10')

    fp = open("data/part0-out.txt")
    for line in fp:
        line = line.strip()
        if len(line)!=0:
            sections = line.split("")
            sql = "INSERT INTO TABLE tb_content select '%s', '%s', '%s', '%s', '%s' from jd_id limit 1" %(sections[1],sections[2],"","","")
            #print sql
            hive_client.runsql(sql)
            #break

    hive_client.close()


if __name__ == '__main__':
    main()

