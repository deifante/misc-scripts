#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import sys

connection = MySQLdb.connect('reporting2.istockphoto.com', 'maint', 'ngTX6Kupa$c', 'istockphoto')
cursor = connection.cursor()
print 'FileId,Priority,Collection'
for line in sys.stdin:
    (fileId, priority) = line.strip().split(',')
    fileId = int(fileId)
    priority = int(priority)
    #print '{0},{1}'.format(fileId, priority)
    cursor.execute('select FileTaxonomyID from tbl_AbstractFileTaxonomy where AbstractFileID = %d' % fileId)
    data = cursor.fetchone()
    collection = None
    if None == data:
        collection = 'Main'
    else:
        #tbl_FileTaxonomy
        cursor.execute('select Name from tbl_FileTaxonomy where ID = %d' % int(data[0]))
        data = cursor.fetchone()
        collection = data[0]
    print '{0},{1},{2}'.format(fileId, priority, collection)
    
