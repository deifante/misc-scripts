#!/usr/bin/python
# -*- coding: utf-8 -*-

# Find out if the .jpg file ids are actually duplicates
# print out the ones that are NOT duplicates

import sys

genuine_ids = {}
duplicate_ids = {}

for line in sys.stdin:
    (iStock_id, thinkstock_id) = line.strip().split(',')
    if line.find('jpg') > 0:
        duplicate_ids[iStock_id] = thinkstock_id
    else:
        genuine_ids[iStock_id] = thinkstock_id

for duplicate_istock_id in duplicate_ids:
    #print duplicate_istock_id[:-4]
    if duplicate_istock_id[:-4] in genuine_ids:
        print '{0},{1}'.format(duplicate_istock_id[:-4], duplicate_ids[duplicate_istock_id])
    
