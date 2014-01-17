#! /usr/bin/python
# -*- coding: utf-8 -*-

# Determine if iStock ids from standard in are valid for Bluesky

import sys
from optparse import OptionParser
import pprint

import bluesky

if __name__ ==  '__main__':
    fileId = 0
    parser = bluesky.create_bluesky_option_parser()
    #live
    pre_defined_args = ['-r', 'bluesky-api.istockphoto.com', '-c', 'https', '-k', 'e5adb70ecb2ce9db3589197a756e9197', '-u', 'deifante', '-q', '-pfyle73a', '-m', '7']
    #dev
    #pre_defined_args = ['-q', '-m', '7']
    for line in sys.stdin:
        try:
            fileId = int(line.strip())
            (options, args) = parser.parse_args(pre_defined_args + ['-i', fileId])
            bluesky_api = bluesky.BlueSkyApiTest(options)
            bluesky_api.login()
            bluesky_api.get_methods_available()
            bluesky_api.choose_method()
            result = bluesky_api.run()
            if None != result and result['getAssetDataByIdResult']['shareable'] == True:
                print fileId, 'valid'
            else:
                print fileId, 'invalid'
        except ValueError:
            sys.stdout.write('Error parsing integer file id from "{0}".\n'.format(line.strip()))
