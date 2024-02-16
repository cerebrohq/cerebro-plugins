# -*- coding: utf-8 -*-
"""
This example shows a procedure of checking if a user has signed off appropriate amount of his/her today's working time on quitting Cerebro.
If it is later than 18:00 o'clock now and the user signed off less than 8 hours, we are asking if he/she is sure to quit
without appropriate amount of time signed off in his/her daily report(s).

Functions:

logoff() - is called on quitting Cerebro
check_start_tasks() - is called by timer and checks the list of user's tasks
"""

import cerebro
import datetime

def reports():
	database = cerebro.db.Db() # getting a database object to make a query
		
	# Also, we need a current user's ID to make the query
	current_user_id = cerebro.core.user_profile()[cerebro.aclasses.Users.DATA_ID] # current user's ID
	
	# and the period of time to search within. In this case it is today.
	start = datetime.datetime.combine(datetime.datetime.now().date(),  datetime.time(0, 0, 0))
	stop = datetime.datetime.combine(start.date(),  datetime.time(23,  59 ,  59,  999))
	
	# Executing a query to get the amount of hours signed off by the user in his/her today's reports
	reports = database.execute('select sum(declared) from "dumpReportsByUser"(%s,%s::text::timestamp with time zone,%s::text::timestamp with time zone)', current_user_id, start.isoformat(),  stop.isoformat())
	if reports is None or len(reports) == 0 or reports[0][0] == None:
		print("reports hours = 0")
	else:
		print("reports hours = {0}".format(round(reports[0][0]/60, 1)))		

	return reports

def logoff():	
	
	if datetime.datetime.now().hour >= 0: # 18 If it is later than 18:00 o'clock now, the daily report checking starts		
		
		# Executing a query to get the amount of hours signed off by the user in his/her today's reports
		rports = reports()
	
		question = ''
		if rports is None or len(rports) == 0 or rports[0][0] == None: # if no reports found at all
			question = 'You have not reported today yet.\n Are you sure you want to quit?'
		elif rports[0][0] < 8*60: # if reports found but they contain less than 8 hours all in all
			question = 'You have signed only ' + str(round(rports[0][0]/60, 1)) + ' hours off for today.\n Are you sure you want to quit?'
		else:
			question = "Вы хорошо поработали, думаете пора выходить?"
		if question != '': # if a question arises
			# displaying it to the user
			if cerebro.gui.question_box('Cerebro',  question) == False: # if the user cancels to quit
				return False # the session is not terminated and the user can make the daily reporting
			
	return True
