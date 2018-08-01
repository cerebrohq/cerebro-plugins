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


def logoff():	
	
	if datetime.datetime.now().hour >= 18: # If it is later than 18:00 o'clock now, the daily report checking starts
		
		database = cerebro.db.Db() # getting a database object to make a query
		
		# Also, we need a current user's ID to make the query
		current_user_id = cerebro.core.user_profile()[cerebro.aclasses.Users.DATA_ID] # current user's ID
		
		# and the period of time to search within. In this case it is today.
		start = datetime.datetime.combine(datetime.datetime.now().date(),  datetime.time(0, 0, 0))
		stop = datetime.datetime.combine(start.date(),  datetime.time(23,  59 ,  59,  999))
		
		# Executing a query to get the amount of hours signed off by the user in his/her today's reports
		reports = database.execute('select sum(declared) from "dumpReportsByUser"($1,$2::text::timestamp with time zone,$3::text::timestamp with time zone)', current_user_id, start.isoformat(),  stop.isoformat())
	
		question = ''
		if len(reports) == 0 or reports[0][0] == None: # if no reports found at all
			question = 'You have not reported today yet.\n Are you sure you want to quit?'
		elif reports[0][0] < 8*60: # if reports found but they contain less than 8 hours all in all
			question = 'You have signed only ' + str(round(reports[0][0]/60, 1)) + ' hours off for today.\n Are you sure you want to quit?'
	
		if question != '': # if a question arises
			# displaying it to the user
			if cerebro.gui.question_box('Cerebro',  question) == False: # if the user cancels to quit
				return False # the session is not terminated and the user can make the daily reporting
			
	
	# Stopping the timer from calling the check_start_tasks function, previously launched on Cerebro logon (the "logon" module)
	cerebro.core.stop_timer('py_plugin_example.examples.logon.check_start_tasks')	
	
	return True
