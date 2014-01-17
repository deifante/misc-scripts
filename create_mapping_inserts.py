#!/usr/bin/python
# -*- coding: utf-8 -*-

# Take in lines from a csv and create a insert statement for tbl_GettyIstockAssetMap

import sys

print 'alter table tbl_GettyIstockAssetMap disable keys;'
print 'SET FOREIGN_KEY_CHECKS = 0;'
print 'SET UNIQUE_CHECKS = 0;'
print 'SET AUTOCOMMIT = 0;'
print 'lock tables tbl_GettyIstockAssetMap WRITE;'

accumulator = []
inserts_per_statement = 50000

for line in sys.stdin:
    (istock_id, getty_id) = line.strip().split(',')

    try:
        istock_id = int(istock_id)
        accumulator.append((istock_id, getty_id))
    except ValueError as e:
        sys.stderr.write('Error parsing line: "{0}."({1})\n'.format(line.strip(), str(e)))
        sys.stderr.flush()

    if len(accumulator) > inserts_per_statement:
        sql_statement = 'insert into tbl_GettyIstockAssetMap (AbstractFileID, GettyID) values '
        for id_pair in accumulator:
            sql_statement += '({0},"{1}"),'.format(id_pair[0], id_pair[1])
        accumulator = []
        sql_statement = sql_statement[:-1] + ';'
        print sql_statement

if len(accumulator):
    sql_statement = 'insert into tbl_GettyIstockAssetMap (AbstractFileID, GettyID) values '
    for id_pair in accumulator:
        sql_statement += '({0},{1}),'.format(id_pair[0], id_pair[1])
    accumulator = []
    sql_statement = sql_statement[:-1] + ';'
    print sql_statement
print 'alter table tbl_GettyIstockAssetMap enable keys;'
print 'SET UNIQUE_CHECKS = 1;'
print 'SET FOREIGN_KEY_CHECKS = 1;'
print 'COMMIT;'
print 'unlock tables;'
