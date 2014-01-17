#http://dev.splunk.com/view/SP-CAAAEK2
import splunklib.client as client

host = 'cf-splunk-indexer1.istockphoto.com'
username = 'dwalters'
password = 'fyle73aB!'
port = 8089
# host = 'localhost'
# username = 'admin'
# password = 'changeme'

# Connect to Splunk
service = client.connect(host=host, port=port, username=username, password=password)

# Get the collection of saved searches
savedsearches = service.saved_searches

for savedsearch in savedsearches:
    print " " + savedsearch.name
    print "     Query: " + savedsearch["search"]

