import sys

from pymongo import Connection

mongo_connection = Connection(host='cf-mongo3.istockphoto.com')
assets_collection = mongo_connection.bluesky.assets

for line in sys.stdin:
    asset_id, getty_id = line.strip().split(',')
    try:
        asset = assets_collection.find_one({'assetId':int(asset_id)})
        assets_collection.update(
            {'assetId':int(asset_id)},
            {'$unset':{'partnerData.getty.migrated':''}, '$set':{'partnerData.getty.partnerId':int(getty_id)}})
    except ValueError:
        sys.stderr.write('Error: %s, %s\n' % (asset_id, getty_id))
        asset = None
print 'done'
