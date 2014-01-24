#! /usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb
import sys

# Get any previous collections of files

class MySQLAccess(object):

    def __init__(self):
        '''
        Since the purpose of this file is to map collections I'm just gonna get
        the taxonomy mapping table data in the constructor.
        '''
        self.connection = MySQLdb.connect('reporting2.istockphoto.com', 'maint', 'ngTX6Kupa$c', 'istockphoto')

        cursor = self.connection.cursor()
        query = 'select ID, Name from tbl_FileTaxonomy'
        cursor.execute(query)
        data = cursor.fetchall()
        self.taxonomy_mappings = {}
        for mapping in data:
            self.taxonomy_mappings[mapping[0]] = mapping[1]

    def get_previous_collections(self, file_id):
        cursor = self.connection.cursor()
        query = 'select AbstractFileID, OldTaxonomy, NewTaxonomy, DateChanged from tbl_AbstractFileTaxonomyLog where AbstractFileID = %d' % file_id
        cursor.execute(query)
        data = cursor.fetchall()
        accumulator = ''
        for previous_collection in data:
            accumulator += '{0}->{1} at {2},'.format(self.get_collection_name(previous_collection[1]), self.get_collection_name(previous_collection[2]), previous_collection[3])
        return accumulator[:-1]

    def get_collection_name(self, collection_id):
        return self.taxonomy_mappings[collection_id]

if __name__ == '__main__':
    mysql_access = MySQLAccess()

    for line in sys.stdin:
        try:
            file_id = int(line)
            previous_collections = mysql_access.get_previous_collections(file_id)
            print "{0}\t{1}".format(file_id, previous_collections)
        except ValueError:
            sys.stderr.write('Error processing "%s"\n' % line)
