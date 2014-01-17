#! /usr/bin/python
# -*- coding: utf-8 -*-
import json
import sys
import pprint

from pymongo import Connection
connection = Connection(host='cf-mongo3.istockphoto.com')
assets_collection = connection.bluesky.assets

for line in sys.stdin:
    try:
        fileId = int(line.strip())
        assets_collection.update({'assetId':fileId}, {'$set':{'partnerData.getty.migrated':True}})
    except ValueError:
        sys.stderr.write('Value Error on "%s"\n' % line)
        # usually invalid literal for int cast
        pass
