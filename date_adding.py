import datetime
date_one = datetime.datetime(2013, 7, 31)

date_two = date_one + datetime.timedelta(1)

print 'date_one:%s, date_two:%s' % (str(date_one), str(date_two))
