#http://dev.splunk.com/view/SP-CAAAEE4
import splunklib.client as client

host     = 'cf-splunk-indexer1.istockphoto.com'
username = 'username'
password = 'password'
port     = 8089
# the above settings work. just keeping these local settings so I don't break splunk
# host     = 'localhost'
# username = 'admin'
# password = 'changeme'

# Create a Service instance and log in
service = client.connect(host=host, port=port, username=username, password = password)

# Print installed apps to the console to verify login
for app in service.apps:
    print app.name

# Find out how many results your system is configured to return
maxresultrows = service.confs["limits"]["restapi"]["maxresultrows"]
print "Your system is configured to return a maximum of %s results" % maxresultrows    
print 'done'

