#one time use to diff 2 big files and have output I can understand right away. hopefully it's not too slow
#'sorted-cleaned-assets'
mongo = set()
for line in open('2013-12-02-mongo-migrated-assets-sorted.txt'):
    val = int(line)
    mongo.add(val)

inactive = set()
for line in open('2013-12-02-inactive-files-cleaned.txt'):
    val = int(line)
    inactive.add(val)

inactive_mongo = mongo & inactive
for fileId in inactive_mongo:
    print fileId
