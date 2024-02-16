# -*- coding: utf-8 -*-
"""
The example shows a function calling timer launch on Cerebro logon.
The function called by timer checks if there are tasks in the user's task list, 
which start shortly. If they are, the user is shown a notification.

Functions:

logon() - is called on Cerebro logon
check_start_tasks() - is called by timer and checks the user's task list
"""

import cerebro
import datetime


def logon():	
	# Starting the timer to call the	check_start_tasks function	
	cerebro.core.start_timer('py_plugin_example.examples.logon.check_start_tasks', 5000) 
	# The check_start_tasks function will be called every 30 minutes
	pass

	
def check_start_tasks():
	
	# getting the current user's task list
	current_user = cerebro.core.user_profile()
	tasks = cerebro.core.to_do_task_list(current_user[cerebro.aclasses.Users.DATA_ID], False)
	if tasks is not None and len(tasks) > 0:
		task = tasks[len(tasks)-1]
		td = task.start() - datetime.datetime.now()
		seconds = td.total_seconds()
		#if seconds >= 0 and seconds < 1800: # if the task has not started yet and it is less than 30 minutes till its start
		message = 'The task: ' + task.name() + ' is starting in  ' + str(round(seconds/60)) + " minutes."
		cerebro.core.notify_user(message,  task.id()) # displaying the notification
	else:
		message = 'Назначенных задач нет'
		cerebro.core.notify_user(message,  None) # displaying the notification	

	# Stopping the timer from calling the check_start_tasks function, previously launched on Cerebro logon (the "logon" module)
	cerebro.core.stop_timer('py_plugin_example.examples.logon.check_start_tasks')	
