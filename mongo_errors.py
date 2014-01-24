#! /usr/bin/python
# -*- coding: utf-8 -*-
# Used this guy to parse some json records coming out out mongo

import json
import sys
import datetime
import re

def main():
    acc = ''
    for line in sys.stdin:
        acc += line
        if line.rstrip() == '}':
            error_object = json.loads(acc.strip())
            acc = ''
            if 'lastChanged' in error_object['partnerData']['getty'] and \
                    'message' in error_object['partnerData']['getty'] and \
                    'TMS' in error_object['partnerData']['getty']['message']:
                changed_date = datetime.datetime.fromtimestamp(error_object['partnerData']['getty']['lastChanged'])
                match_obj = re.search(r'TMS-\d+', error_object['partnerData']['getty']['message'])
                print '%s\t%s\t%s' % (match_obj.group(0), changed_date.strftime('%Y-%m-%d'), error_object['assetId'])
if __name__ == '__main__':
    main()
