import string
import sys
broken_local_ids = []
for line in open('all_borked_illustrations.txt'):
    local_id, oracle_id = string.strip(line).split(',')
    broken_local_ids.append(local_id)
    
for line in sys.stdin:
    istock_id, local_id = string.strip(line).split()
    if local_id not in broken_local_ids:
        print '%s,%s' % (istock_id, local_id)
    
    
