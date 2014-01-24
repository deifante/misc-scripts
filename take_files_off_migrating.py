#! /usr/bin/python
# -*- coding: utf-8 -*-
import json
import sys
import pprint

from pymongo import Connection

connection = Connection(host='cf-mongo3.istockphoto.com')
# connection = Connection(host='10.2.241.213')
assets_collection = connection.bluesky.assets

for line in sys.stdin:
    try:
        values = line.strip().split()
        if 2 == len(values):
            iStockId = int(values[0])
            gettyId = int(values[1])
            assets_collection.update({'assetId':iStockId}, {'$unset':{'partnerData.getty.migrated':''},'$set':{'partnerData.getty.partnerId': gettyId}})
        if 1 == len(values):
            iStockId = int(values[0])
            assets_collection.update({'assetId':iStockId}, {'$unset':{'partnerData.getty.migrated':''}})
    except ValueError:
        sys.stderr.write('Value Error on "%s"\n' % line)
        pass
