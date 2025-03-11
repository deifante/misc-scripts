#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys
import string

import cx_Oracle

class TeamsOracle:
    """Quick class to get ids from TEAMS"""
    def __init__(self):
        self.connection = cx_Oracle.connect('gins_user', 'report', '(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=seaputmsdb03.amer.gettywan.com)(PORT=1521)))(CONNECT_DATA=(SERVICE_NAME=TEAMSREP)))')

    def get_teams_id(self, iStockId):
        cursor = self.connection.cursor()
        cursor.execute("""
select ra.ASSET_ID
  from report_asset_alias raa
  left join report_assets ra on
  (raa.UOI_ID = ra.UOI_ID)
  where raa.ALIAS_TYPE='iStockphoto' and raa.PORTAL_ALIAS = 'Y' and raa.ALIAS = :asset_id""",
                       {'asset_id':str(iStockId)})
        value = cursor.fetchone()
        if value:
            return value[0]
        return None

    def get_teams_ids(self, istock_ids):
        cursor = self.connection.cursor()
        statement = """
select raa.ALIAS, ra.ASSET_ID
  from report_asset_alias raa
  left join report_assets ra on
  (raa.UOI_ID = ra.UOI_ID)
  where raa.ALIAS_TYPE='iStockphoto' and raa.PORTAL_ALIAS = 'Y' and raa.ALIAS in """
        statement = statement + str(istock_ids).replace('[', '(').replace(']', ')')
        cursor.execute(statement)
        value = cursor.fetchall()
        return value

def serial_check():
    teams_oracle = TeamsOracle()
    for line in sys.stdin:
        istock_id, local_teams_id = string.split(string.strip(line))
        oracle_teams_id = teams_oracle.get_teams_id(istock_id)
        try:
            if int(local_teams_id) != int(oracle_teams_id):
                print '%s,%s' % (local_teams_id, oracle_teams_id)
        except ValueError:
            sys.stderr.write('Error:%s,%s\n' % (local_teams_id,oracle_teams_id))
        except TypeError:
            sys.stderr.write('Error:%s,%s\n' % (local_teams_id,oracle_teams_id))

if __name__ == '__main__':
    serial_check()
    # teams_oracle  = TeamsOracle()
    # batch_size = 15
    # batch = []
    # for line in sys.stdin:
    #     parts = string.split(string.strip(line))
    #     #batch.append([int(parts[0]), parts[1]])
    #     batch.append([int(parts[0]), int(parts[1])])
    #     batch.sort()
    #     if len(batch) > batch_size:
    #         istock_ids = [str(x[0]) for x in batch]
    #         teams_ids = teams_oracle.get_teams_ids(istock_ids)
    #         print teams_ids
    #         print batch
    #         # print zip([int(x[0]) for x in batch], [int(x[1]) for x in batch], teams_ids)
    #         batch = []
            
                
        # local_id = parts[1]
        # teams_id = to.get_teams_id(parts[0])
        # try:
        #     if int(local_id) != int(teams_id):
        #     #print '%s,%s' % (local_id, teams_id)
        #         print local_id, teams_id
        # except ValueError:
        #     pass
        # print parts
    # val = to.get_teams_id(44)
    # print 'val', val
        
