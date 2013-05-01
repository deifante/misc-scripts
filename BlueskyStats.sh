#!/bin/bash
DB=bluesky

# See SYSOP-6807 for the logic behind the magic numbers in these mongodb query ranges. Also see US42221
# When people are doing one off's or cute scripts it seems that the priority is usually ~40. 40 is less
# important than the legally binding deactivations and more important than everything else.
UPDATE="\$gte: 0, \$lte: 4"
NEW="\$gte: 10, \$lte: 14"
PULL="\$gte: 50, \$lte: 54"
SPECIAL="\$gte: 40, \$lte: 44"

EXISTS="\$exists:true"

# this function takes a string and runs it as a mongo query against $DB
# escape your quotes
function mongo_query() {
    mongo $DB --quiet --eval "$1"
}

echo -ne "Pending\t\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'pending'});"
echo -ne "  Pulls\t\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'pending', priority : { $PULL }});"
echo -ne "  New Files\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'pending', priority : { $NEW }});"
echo -ne "  Updates\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'pending', priority : { $UPDATE }});"
echo -ne "  Special\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'pending', priority : { $SPECIAL }});"
echo -ne "  Legacy\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'pending', 'partnerData.getty.legacyMigration' : { $EXISTS }});"
echo -ne "  Bulk\t\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'pending', 'partnerData.getty.migrated' : { $EXISTS }});"
echo -ne "  Hand Selected\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'pending', 'partnerData.getty.handSelected' : { $EXISTS }});"

echo -ne "\nProcessing\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'processing'});"
echo -ne "  Oldest\t"
mongo_query "db.assets.find({'partnerData.getty.status' : 'processing'}).limit(1).sort({'version' : 1 }).forEach(function(x) {printjson(x.version) })" | awk '{print strftime("%c", $1)}'
echo -ne "  Newest\t"
mongo_query "db.assets.find({'partnerData.getty.status' : 'processing'}).limit(1).sort({'version' : -1 }).forEach(function(x) {printjson(x.version) })" | awk '{print strftime("%c", $1)}'
echo -ne "  Pulls\t\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'processing', priority : { $PULL }});"
echo -ne "  New\t\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'processing', priority : { $NEW }});"
echo -ne "  Updates\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'processing', priority : { $UPDATE }});"
echo -ne "  Special\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'processing', priority : { $SPECIAL }});"
echo -ne "  Legacy\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'processing', 'partnerData.getty.legacyMigration' : { $EXISTS }});"
echo -ne "  Bulk\t\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'processing', 'partnerData.getty.migrated' : { $EXISTS }});"
echo -ne "  Hand Selected\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'processing', 'partnerData.getty.handSelected' : {$EXISTS}});"

echo -ne "\nCompleted\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'complete'});"
echo -ne "  Pulls\t\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'complete', priority : { $PULL }});"
echo -ne "  New\t\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'complete', priority : { $NEW }});"
echo -ne "  Updates\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'complete', priority : { $UPDATE }});"
echo -ne "  Special\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'complete', priority : { $SPECIAL }});"
echo -ne "  Legacy\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'complete', 'partnerData.getty.legacyMigration' : { $EXISTS }});"
echo -ne "  Bulk\t\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'complete', 'partnerData.getty.migrated' : { $EXISTS }});"
echo -ne "  Hand Selected\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'complete', 'partnerData.getty.handSelected' : { $EXISTS }});"

echo -ne "\nError\t\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'error'} );"
echo -ne "  Pulls\t\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'error', priority: { $PULL }});"
echo -ne "  New\t\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'error', priority: { $NEW }});"
echo -ne "  Updates\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'error', priority: { $UPDATE }});"
echo -ne "  Special\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'error', priority: { $SPECIAL }});"
echo -ne "  Legacy\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'error', 'partnerData.getty.legacyMigration' : { $EXISTS }});"
echo -ne "  Bulk\t\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'error', 'partnerData.getty.migrated' : { $EXISTS }});"
echo -ne "  Hand Selected\t"
mongo_query "db.assets.count({'partnerData.getty.status' : 'error', 'partnerData.getty.handSelected' : { $EXISTS }});"

echo -ne "\nTotal Hand Selected\t"
mongo_query "db.assets.count({'partnerData.getty.handSelected' : { $EXISTS }});"
echo -ne "Total Bulk Migrating\t"
mongo_query "db.assets.count({'partnerData.getty.migrated' : { $EXISTS }});"
echo -ne "Total Legacy\t\t"
mongo_query "db.assets.count({'partnerData.getty.legacyMigration' : { $EXISTS }});"
