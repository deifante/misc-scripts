#! /usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb
import sys

# map Exclusivity IDs to Abstract Type IDs
exclusive_translation_table = {1:1, 2:8, 3:9, 4:4, 5:7}

class MysqlAccess:

    def __init__(self):
        self.connection = MySQLdb.connect('reporting2.istockphoto.com', 'maint', 'ngTX6Kupa$c', 'istockphoto')

    def get_exclusive_types(self, userId):
        cursor = self.connection.cursor()
        query = """select ExclusivityUser.exclusivityID
from ExclusivityUser
  inner join tbl_AbstractFileTypeGroup
    on tbl_AbstractFileTypeGroup.ExclusivityID = ExclusivityUser.ExclusivityID
  inner join AbstractFileType
    on AbstractFileType.AbstractFileTypeGroupID = tbl_AbstractFileTypeGroup.ID
where ExclusivityUser.userID = %d and ExclusivityUser.exclusivityID > 0 and ExclusivityUser.Status = 'Approved'
group by AbstractFileType.ID
""" % userId
        cursor.execute(query)
        all_data = cursor.fetchall()
        return self.translate_exclusive_types_into_abstract_types([x[0] for x in all_data])

    def translate_exclusive_types_into_abstract_types(self, exclusive_types):
        return [exclusive_translation_table[exclusive_type] for exclusive_type in exclusive_types]
        pass

    def get_abstract_type(self, fileId):
        cursor = self.connection.cursor()
        query = 'select AbstractTypeID from AbstractFile where ID = %d' % fileId
        cursor.execute(query)
        return cursor.fetchone()[0]

    def get_contributor(self, fileId):
        cursor = self.connection.cursor()
        query = 'select UserID from AbstractFile where ID = %d' % fileId
        cursor.execute(query)
        return cursor.fetchone()[0]

if __name__ == '__main__':
    access = MysqlAccess()

    for line in sys.stdin:
        try:
            fileId = int(line)
            contributor = access.get_contributor(fileId)
            abstract_type = access.get_abstract_type(fileId)
            exclusive_types = access.get_exclusive_types(contributor)
            is_exclusive = abstract_type in exclusive_types
            print '%s,%d' % (is_exclusive, fileId)
        except Exception:
            sys.stderr.write('Error processing %s\n' % line)
