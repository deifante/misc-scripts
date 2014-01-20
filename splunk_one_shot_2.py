#! /usr/bin/python
# -*- coding: utf-8 -*-

# This script started off as a splunk one shot example for multiple sources
# now it's an example for fetching multiple searches with threading and pagination.
# Also a tiny example of python regular expressions.
# The code will make a few search requests to splunk in as many threads
# as there are search requests. This code will also determine the # of unique
# id's returned from each search result. If all results are not returned in the
# first result fetch, then the code will retrieve all subsequent batches.
# For unknown reasons using 50 000 as my offest increase caused no results
# to be returned afer the 10th consecutive request.
import json
import re
import pprint
import time
import Queue
import threading
import datetime

import dateutil.parser # cute util for dealing with splunk dates
import splunklib.client as client
import splunklib.results as results
host     = 'localhost'
username = 'admin'
password = 'changeme'
port     = 8089

host     = 'cf-splunk-indexer1.istockphoto.com'
username = 'username'
password = 'password'

class ResultsSpitter(threading.Thread):
    """Threaded Splunk Results Retrieval"""
    def __init__(self, queue, splunk_service):
        """Just get some storage variables and init the threading"""
        threading.Thread.__init__(self)
        self.queue = queue
        self.splunk_service = splunk_service

    def run(self):
        """
        This function is called by the threading library code after start() is
        called on this object. I probably wouldn't need the while loop if I
        loaded the queue before starting the workers.
        """
        while True:
            job_specs = self.queue.get()
            self.search_string = job_specs['search_string']
            # Besides the search_string key, I expect the job to be
            # search parameters for a ResultsSpitter::start_search.
            del job_specs['search_string']
            # This line starts the actual async searching jobs
            self.start_search(**job_specs)
            # Spin while the search job isn't done
            while not self.job.is_done():
                # I'm not super fond of this but total execution
                # times are in minutes right now.
                time.sleep(1)
            self.store_results()
            self.queue.task_done()

    def start_search(self, latest_time = None, earliest_time = None):
        """
        Get splunk started on a search.
        Both dates can be a standard python datetime.datetime or a string in ISO 8601 format

        latest_time: the time closest to now. The higher number.
        earliest_time: the time closest to the start of time. The lower number.
        """
        # Cutting the ttl super low cause I'd been running out of search space
        # on the splunk server and it's not seeming to affect the #'s so far.
        search_kwargs = {'exec_mode':'normal', 'ttl':30}
        if latest_time:
            if type(latest_time) == datetime.datetime:
                search_kwargs['latest_time'] = latest_time.isoformat()
            else:
                search_kwargs['latest_time'] = latest_time

        if earliest_time:
            if type(earliest_time) == datetime.datetime:
                search_kwargs['earliest_time'] = earliest_time.isoformat()
            else:
                search_kwargs['earliest_time'] = earliest_time
        self.job = self.splunk_service.jobs.create(self.search_string, **search_kwargs)

    def store_results(self):
        """
        Fetch the results from splunk

        Fetchs the results from splunk (inlcuding results on multiple pages),
        processes json data into something useful and get a few metrics on the data.
        """
        self.search_results = []
        search_results = []
        # I originally wanted this to be max of the server, but then I found that I would get an empty
        # json response on the 10th consecutive call. I'm still not sure of the reason.
        result_fetch_count = 49123
        result_fetch_offest = 0

        # eventCount should be the total number of matches found on splunk.
        self.total_events = int(self.job['eventCount'])
        # I'm not sure why I got better results using a dictionary to pass the key word args
        kwargs_paginate = {'output_mode':'json', 'ttl':30}

        try:
            # Start retrieving json results from splunk
            while result_fetch_offest < self.total_events:
                kwargs_paginate['count'] = result_fetch_count
                kwargs_paginate['offset'] = result_fetch_offest
                # Not sure why I had to explicitly convert the results to string when
                # the return type was meant to be json. The results are returned as
                # a list of elements so they add together nicely
                search_results += json.loads(str(self.job.results(**kwargs_paginate)))
                result_fetch_offest += result_fetch_count

        except ValueError as e:
            # good chance there's no results
            # probably a 'no JSON object could be decoded' error
            # This was also occuring on the 10th request when paging
            # results with a step of 50 000
            print e
            if len(search_results) == 0:
                return
            print 'Continuing with %d of %d results' % (len(search_results), self.total_events)

        # Now that we have the actual results we have to parse out the event data.
        for search_result in search_results:
            # the _raw element has the actual logged line. Everything
            # after "Change to Bluesky File" has the actual information.
            sub_index = search_result['_raw'].find('Change to Bluesky File')

            # use some regex fun to pull out the data from the surrounding
            # info to make it human readable.
            original_string = search_result['_raw'][sub_index:].strip()
            m = extraction_pattern.search(original_string)

            # _time holds the time when the log message was made
            log_time = dateutil.parser.parse(search_result['_time'])
            self.search_results.append({
                'action':m.group('action').strip(),
                'assetId':int(m.group('assetId')),
                'partner':m.group('partner'),
                'log_time':log_time
                })

    def get_unique_ids(self):
        """
        Get the unique file Id's found in this search.
        """
        # Use the fact that there are no duplicates allowed in sets
        # to make a set comprehension with only unique file ids
        return {int(x['assetId']) for x in self.search_results}

    def get_id_count(self):
        """
        Count how many times every id shows up.
        """
        incident_report = {}
        for x in self.search_results:
            if x['assetId'] in incident_report:
                incident_report[x['assetId']]+=1
            else:
                incident_report[x['assetId']]=1
        return incident_report

    def print_results(self):
        """
        Print the search query and every matching event.
        """
        print self.search_string
        for search_result in self.search_results:
            print '\t%d: %s with %s (@ %s)' % \
            (search_result['assetId'], search_result['action'], search_result['partner'],
             search_result['log_time'].strftime('%A, %B %d %H:%M:%S'))

    def __str__(self):
        """Provide the search query"""
        return self.search_string

    def __len__(self):
        """The total number of matched events"""
        return int(self.total_events)

# Create a Service instance and log in
service = client.connect(host=host, port=port, username=username, password=password)

# The list of searches that we are going to perform.
search_strings = [
    'search "Change to Bluesky File" "Received Error"',
    # 'search "Change to Bluesky File" Queued',
    # 'search "Change to Bluesky File" "Received Success"',
    # 'search "Change to Bluesky File" "Sent Metadata"',
    # 'search "Change to Bluesky File" "Sent Asset"'
    ]

# Use this regular expression to get the action, assetId and partner data out from
# the human readable string.
extraction_string = r'^Change to Bluesky File. Action: (?P<action>.+)Asset ID: (?P<assetId>\d+) Partner: (?P<partner>\w+)'
extraction_pattern = re.compile(extraction_string)

#Spitters... what an unfortunate name.
spitters = []
job_queue = Queue.Queue()

# Spawn the working threads. One for each search string.
# Rotating resources would be cool, but not necessary quite yet.
for i in range(len(search_strings)):
    spitter = ResultsSpitter(job_queue, service)
    spitter.setDaemon(True)
    # Start them spinning right away.
    spitter.start()
    spitters.append(spitter)

# Populate the queue with data
for search_string in search_strings:
    job_queue.put({
            'search_string' :search_string,
            'latest_time'   :datetime.datetime.now(), # This is the bigger number
            'earliest_time' :datetime.datetime.now() - datetime.timedelta(3)  # This is the lower number
            # 'latest_time'   :datetime.datetime(2013, 8, 20), # This is the bigger number
            # 'earliest_time' :datetime.datetime(2013, 8, 19)  # This is the lower number
            })

# wait on the queue until everything has been processed
#print 'job work sent, waiting'
job_queue.join()

# Print out some results for each search query.
for spitter in spitters:
    # print '%s:%d' % (spitter, len(spitter))
    # spitter.print_results()

    #This is the stuff I usually use. just get the unique errors
    unique_ids = spitter.get_unique_ids()
    print '# of Unique Ids: %d' % len(unique_ids)
    for file_id in unique_ids:
        print file_id
    print

    # print 'How many times did each file id show up?'
    # id_count = spitter.get_id_count()
    # for file_id in id_count:
    #     print '%d\t%d' % (id_count[file_id], file_id)
