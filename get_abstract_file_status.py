#! /usr/bin/python
# -*- coding: utf-8 -*-
# Get the Status from AbstractFile table based on stdin

import sys
import MySQLdb

connection = MySQLdb.connect('reporting2.istockphoto.com', 'maint', 'ngTX6Kupa$c', 'istockphoto')
cursor = connection.cursor()
for line in sys.stdin:
    # select ID, UserId,  AbstractTypeID, Status from AbstractFile where ID = %d
    cursor.execute('select ID, Status from AbstractFile where ID = %d' % int(line))
    data = cursor.fetchone()
    print '%d,%s' % data






