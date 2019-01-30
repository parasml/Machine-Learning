
*****************************
   check_datatable.py
*****************************



		**Created By**:         Akshay Nevrekar
		
		**Created On**:      	10th December, 2018
		
		**Last Modified On**: 	24th December, 2018

=======================================================================================================================================


**Objective**

	*	To View the entries in table *UserFaceReconStatus*
	*	To delete entries in table (Entries used for Testing Purpose only).
	
	Once it goes live 2nd part should be removed.
	

**Code Block** ::

		import pyodbc


		cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=172.16.1.70;DATABASE=AutomateBanking;UID=sa_admin;PWD=St33p@54321')
		cursor = cnxn.cursor()


		cursor.execute("delete from UserFaceReconStatus where UserId in (2, 10, 13)")
		cnxn.commit()


		cursor.execute("select * from UserFaceReconStatus")

		for i in cursor.fetchall():
			print("[INFO]: ",i)
			


		
**Modules Required**

* pyodbc : To connect SQLServer using python


**Code Explanation** 

* The below code connects to SQLServer using the parameters passed in connect method and creates a *cursor* to deal with DB Operations.

::

		cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=172.16.1.70;DATABASE=AutomateBanking;UID=sa_admin;PWD=St33p@54321')
		cursor = cnxn.cursor()

		
* It deletes the rows from the table for given userid and commit is necessary to update the results in database.

::

		cursor.execute("delete from UserFaceReconStatus where UserId in (2, 10, 13)")
		cnxn.commit()
		

* Select the data and iterate over it to print it.

::
		
		cursor.execute("select * from UserFaceReconStatus")
		for i in cursor.fetchall():
			print("[INFO]: ",i)
