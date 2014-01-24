import re
import sys


extraction_string = r'^Change to Bluesky File. Action: (?P<action>.+)Asset ID: (?P<assetId>\d+) Partner: (?P<partner>\w+)'

extraction_string = r'Asset ID: (?P<assetId>\d+)'
extraction_pattern = re.compile(extraction_string)
for line in sys.stdin:
    m = extraction_pattern.search(line)
    if m:
        print m.group('assetId')

