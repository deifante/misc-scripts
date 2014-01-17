messages = ['Queued.', 'Received Error.', 'Received Success.', 'Sent Metadata.', 'Sent Metadata by Id.', 'Sent Uri.', 'Sent Asset.']

for message in messages:
    print "mongo_status/history_snippets/%s.html" % message.strip().lower().replace('.','').replace(' ', '_')

