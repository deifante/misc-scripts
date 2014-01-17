#!/usr/bin/python

import MySQLdb
import sys

connection = None

try:
    # connection = MySQLdb.connect('localhost', 'deifante', 'password', 'Bluesky_Status')
    connection = MySQLdb.connect('reporting2.istockphoto.com', 'maint', 'ngTX6Kupa$c', 'istockphoto')
    cursor = connection.cursor()
    #cursor.execute("select version()")
    cursor.execute('select Collections from AbstractFile where ID = %d' % 44)
    data = cursor.fetchone()
    #print "Database version: %s" % data
    print data[0].find('GettyDistribution') != -1

except MySQLdb.Error, e:
    print "Error %d: %s" %(e.args[0], e.args[1])
    sys.exit(1)

finally:
    if connection:
        connection.close()
    
