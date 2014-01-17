import splunklib.client as client
# host     = 'cf-splunk-indexer1.istockphoto.com'
# username = 'dwalters'
# password = 'fyle73aB^'
port     = 8089
# the above settings work. just keeping these local settings so I don't break splunk
host     = 'localhost'
username = 'admin'
password = 'changeme'

# Create a Service instance and log in
service = client.connect(host=host, port=port, username=username, password = password)

# Get the collection of saved searches
savedsearches = service.saved_searches

for s in savedsearches:
    print 'Search Name:%s\n\tSearch Query:%s' % (s.name, s["search"])
    history = s.history()
    if len(history) > 0:
        for job in history:
            print "\t\t%s" % job.name
