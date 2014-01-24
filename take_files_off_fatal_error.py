#! /usr/bin/python
# -*- coding: utf-8 -*-
import json
import sys
import pprint

from pymongo import Connection

# connection = Connection(host='cf-mongo3.istockphoto.com')
connection = Connection(host='10.2.241.213')
assets_collection = connection.bluesky.assets

for line in sys.stdin:
    try:
        fileId = int(line.strip())
        assets_collection.update({'assetId':fileId}, {'$set':{'partnerData.getty.status':'pending'}})
    except ValueError:
        sys.stderr.write('Value Error on "%s"\n' % line)
        pass
