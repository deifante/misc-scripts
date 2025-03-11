import json
import re
import pprint

import dateutil.parser
import splunklib.client as client
import splunklib.results as results
host     = 'localhost'
username = 'admin'
password = 'changeme'
port     = 8089

assetId = 11604984

# Create a Service instance and log in
service = client.connect(host=host, port=port, username=username, password = password)

kwargs_oneshot = {'output_mode':'json'}
search_query_oneshot = 'search "Change to Bluesky File" "Asset ID: %d" | head 1' % assetId
oneshot_results = service.jobs.oneshot(search_query_oneshot, **kwargs_oneshot)
temp = str(oneshot_results)
oneshot_json = json.loads(temp.strip())

#print pprint.pprint(oneshot_json)
sub_index = oneshot_json[0]['_raw'].find('Change to Bluesky File')
original_string  = oneshot_json[0]['_raw'][sub_index:].strip()
extraction_string = r'^Change to Bluesky File. Action: (?P<action>[\w\s]+). Asset ID: (?P<assetId>\d+) Partner: (?P<partner>\w+)'
extraction_pattern = re.compile(extraction_string)
m = extraction_pattern.search(original_string)
log_time = dateutil.parser.parse(oneshot_json[0]['_time'])
extracted_data_string = 'Extracted values: Action "%s"; Asset Id "%s"; Partner "%s" (Logged @ %s)' % (m.group('action'), m.group('assetId'), m.group('partner'), log_time.strftime('%A, %B %d %H:%M:%S'))
print extracted_data_string
