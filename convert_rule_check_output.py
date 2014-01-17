#! /usr/bin/python
# -*- coding: utf-8 -*-

# Take the output from RuleEngineCheck.php and make it more csvish

import sys

def collect_entries():
    entries = []
    accumulator = []
    for line in sys.stdin:
        if line[:6] == 'fileId':
            if len(accumulator):
                entries.append(accumulator)
            accumulator = [line]
        else:
            accumulator.append(line)

    if len(accumulator):
        entries.append(accumulator)
    return entries

def print_entry(entry):
    """
    Right now I only care about the failed files.
    """
    if entry[0].find('NOT') > 0:
        sys.stdout.write(entry[0].split()[1] + '\t')
    else:
        return

    for line in entry:
        if line.strip()[:14] == 'Failed Rules: ':
            print line.strip()[14:]

if __name__ == '__main__':
    for entry in collect_entries():
        print_entry(entry)
