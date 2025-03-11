#! /usr/bin/python
# -*- coding: utf-8 -*-
import json
import sys

from pymongo import Connection, ASCENDING, DESCENDING

connection = Connection(host='10.2.106.180')

assets_collection = connection.bluesky.assets

asset_ids = []

for line in sys.stdin:
    asset_id = int(line.strip())
    if asset_id:
        asset_ids.append(asset_id)

results = assets_collection.find({'assetId':{'$in':asset_ids}}, {'_id':False, 'partnerData.getty.lastChanged':True, 'assetId':True})
for r in results:
    try:
        print '%d %d' % (r['assetId'], r['partnerData']['getty']['lastChanged'])
    except KeyError:
        pass
    

