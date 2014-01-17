#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import sys

connection = None

try:
    # connection = MySQLdb.connect('localhost', 'deifante', 'password', 'Bluesky_Status')
    connection = MySQLdb.connect('reporting2.istockphoto.com', 'maint', 'ngTX6Kupa$c', 'istockphoto')

    for line in sys.stdin:
        iStockId = int(line.strip())
        cursor = connection.cursor()
        cursor.execute('select ID, UserID from AbstractFile where ID = %d' % iStockId)
        data = cursor.fetchone()
        print data
        # #print "Database version: %s" % data
        # print data[0].find('GettyDistribution') != -1

except MySQLdb.Error, e:
    print "Error %d: %s" %(e.args[0], e.args[1])
    sys.exit(1)

finally:
    if connection:
        connection.close()
    
