#! /usr/bin/python
# -*- coding: utf-8 -*-

# This script will take a list of file ids and produce the error
# that's been stored in mongo for them.
import json
import sys
import pprint

from pymongo import Connection
#from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup

connection = Connection(host='cf-mongo3.istockphoto.com')
assets_collection = connection.bluesky.assets

for line in sys.stdin:
    try:
        fileId = int(line.strip())
    except ValueError:
        #probably not an int
        continue

    asset = assets_collection.find_one({'assetId':fileId})

    if asset and 'partnerData' in asset and 'getty' in asset['partnerData'] and 'message' in asset['partnerData']['getty']:
        try:
            #print '%d\t%s' % (fileId, asset['partnerData']['getty']['message'])
            #print asset['partnerData']['getty']['message']
            y = BeautifulStoneSoup(asset['partnerData']['getty']['message'])
            # print y.message.status.string
            # print y.message.errorcode.string
            # print y.message.partnererrorcode.string
            
            if y.message.errormessage.string:
                error_message = y.message.errormessage.string.replace('&#13;','').replace('null', '').replace("\n",'').strip()
                #error_message = error_message.replace('&#13;','')
                #error_message = error_message.replace('\r','')
                # error_message = error_message.
                if len(error_message):
                    print '%s\t%d' % (error_message, fileId)
        except UnicodeEncodeError:
            pass
        except AttributeError:
            pass

