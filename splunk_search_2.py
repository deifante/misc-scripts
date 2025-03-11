from time import sleep
import splunklib.client as client
import splunklib.results as results
host     = 'localhost'
username = 'admin'
password = 'changeme'
port     = 8089

# Create a Service instance and log in
service = client.connect(host=host, port=port, username=username, password = password)

# Get the collection of saved searches
error_search = service.saved_searches['Deifante on Blue']

# Run the saved search
job = error_search.dispatch()

while not job.is_done():
    sleep(0.2)
    
results_reader = results.ResultsReader(job.results())
for result in results_reader:
    if isinstance(result, results.Message):
        # Diagnostic messages may be returned in the results
        print '%s: %s' % (result.type, bresult.message)
    elif isinstance(result, dict):
        # Normal events are returned as dicts
        print result
        print 
assert results_reader.is_preview == False
