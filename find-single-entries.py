#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys
for line in sys.stdin:
    try:
        values = line.strip().split()
        if not (2 == len(values)):
            print line.strip()
    except ValueError:
        sys.stderr.write('Value Error on "%s"\n' % line)
        
            
