import cx_Oracle

print 'cx_Oracle client version:', cx_Oracle.clientversion()

connection = cx_Oracle.connect('gins_user', 'report', '(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=seaputmsdb03.amer.gettywan.com)(PORT=1521)))(CONNECT_DATA=(SERVICE_NAME=TEAMSREP)))')
cursor = connection.cursor()

cursor.execute("""
select ra.*
  from report_asset_alias raa
  left join report_assets ra on
  (raa.UOI_ID = ra.UOI_ID)
  where raa.ALIAS_TYPE='iStockphoto' and raa.PORTAL_ALIAS = 'Y' and raa.ALIAS = :asset_id""",
               {'asset_id': str(44)})
values = list(cursor.fetchone())
columns = [x[0] for x in cursor.description]
pairs = zip(columns, values)
for pair in pairs:
    print pair
#print zip(columns, values)
print 'done'
