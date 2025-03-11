import re

class ClassOne:
    lul_string = 'oh hai'
    extraction_pattern = re.compile(r'^Change to Bluesky File. Action: (?P<action>.+)Asset ID: (?P<assetId>\d+) Partner: (?P<partner>\w+)')
    def __init__(self):
        self.happy_string = 'happy' + ' times'

class ClassTwo:
    extraction_pattern = ClassOne.extraction_pattern
    def __init__(self):
        print 'extraction pattern', 

o = ClassOne()

#print o.lul_string
print ClassOne.lul_string
print ClassTwo.extraction_pattern
