#!/usr/bin/python
# -*- coding: utf-8 -*-

# Take in a file id from stdin and provide it's iStock license type

import MySQLdb
import sys

print 'FileId,iStockLicense'

connection = MySQLdb.connect('reporting2.istockphoto.com', 'maint', 'ngTX6Kupa$c', 'istockphoto')
cursor = connection.cursor()

for line in sys.stdin:
    try:
        iStockId = int(line.strip())
    except ValueError:
        sys.stderr.write('ValueError "{0}"\n'.format(line.strip()))
        sys.stderr.flush()
        continue
    cursor.execute('select LicenseTypeID from tbl_AbstractFileLicense where AbstractFileID = %d' % iStockId)
    data = cursor.fetchone()
    license = 'Creative'
    if data != None:
        license = 'Editorial'

    print '{0},{1}'.format(iStockId, license)
