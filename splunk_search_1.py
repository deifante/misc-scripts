import splunklib.client as client
import sys
from time import sleep
host     = 'localhost'
username = 'admin'
password = 'changeme'
port     = 8089

# Create a Service instance and log in
service = client.connect(host=host, port=port, username=username, password = password)

# Get the collection of saved searches
error_search = service.saved_searches['Errors (Last Month)']

# Run the saved search
job = error_search.dispatch()

# Create a small delay to allow time for the update between server and client
sleep(2)

# Wait for the job to finish -- poll for completion iand display stats
while True:
    job.refresh()
    stats = {"isDone": job["isDone"],
             "doneProgress": float(job["doneProgress"])*100,
             "scanCount": int(job["scanCount"]),
             "eventCount": int(job["eventCount"]),
             "resultCount": int(job["resultCount"])}
    status = ("%(doneProgress)03.1f%%  %(scanCount)d scanned    "
              "%(eventCount)d matched   %(resultCount)d results") % stats
    # sys.stdout.write(status)
    # sys.stdout.flush()
    print status
    if stats["isDone"] == "1":
        break
    sleep(2)

# Display the search results now that the job is done
job_results = job.results()

content = job_results.read(1024)
while len(content) != 0:
    sys.stdout.write(content)
    sys.stdout.flush()
    content = job_results.read(1024)

print
