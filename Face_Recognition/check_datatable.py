import pyodbc
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-o", "--operation", required=False, help="operation to be performed", default='select')
ap.add_argument("-u", "--userid", required=False, help="userid to be deleted", nargs='+')

args = vars(ap.parse_args())

op = args['operation']
# print(args['userid'])

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=172.16.1.72;DATABASE=Automate_Fulfilment;UID=steeplap_sa;PWD=St33p@12345')
cursor = cnxn.cursor()

if op == 'del':
	cursor.execute("delete from UserFaceReconStatus where UserId in ({})".format(",".join([str(i) for i in args['userid']])))
	cnxn.commit()
elif op == 'select':
	cursor.execute("select * from UserFaceReconStatus")
	for i in cursor.fetchall():
		print("[INFO]: ",i)



'''

How to execute above code:

1. For select operation

$ python check_datatable.py -o select 


2. To delete opeation for userids (2,13,25)

$ python check_datatable.py -o del -u 2 13 25


'''  