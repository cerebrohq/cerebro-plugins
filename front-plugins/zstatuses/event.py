# -*- coding: utf-8 -*-

import cerebro
from cerebro.aclasses import Statuses
import datetime

import zstatuses.py_cerebro as py_cerebro

statuses_from_blocked =		['Request']
statuses_to_blocked =		['Done', 'Ready']
statuses_to_stop =			['Done', 'Ready', 'Closed']
statuses_from_reset =		['Not required']
statuses_to_reset =			0 # No Status
message =					'You can not switch status "Request" to status "Done" or "Ready".'

status_ready_to_start =		 'Ready to start'

def get_db():
	db = py_cerebro.database.Database('cerebrohq.com', 45432)
	db.connect_from_cerebro_client()

	if not db:
		cerebro.core.print_error("Connect to Cerebro client error!")
		exit(1)

	return db

def before_event(event):
	if event.event_type() == event.EVENT_CHANGING_OF_TASKS_STATUS:
		has_blocked_status = False
		for task in event.tasks():
			if task.status()[Statuses.DATA_NAME] in statuses_from_blocked:
				has_blocked_status = True
				break

		if (has_blocked_status and event.new_value()[Statuses.DATA_NAME] in statuses_to_blocked):
			raise Exception(message)

		tasks_0 = set()
		tasks_1 = set()

		for task in event.tasks():
			print(event.new_value())
			if event.new_value() != None and event.new_value()[Statuses.DATA_NAME] in statuses_to_stop and task.progress() < 100:
				tasks_0.add(task.id())
			elif (event.new_value() is None or event.new_value()[Statuses.DATA_ID] == statuses_to_reset) and task.status()[Statuses.DATA_NAME] in statuses_from_reset and task.progress() > 99:
				tasks_1.add(task.id())
				
		if len(tasks_0) > 0:
			db = get_db()
			db.task_set_progress(tasks_0, 100.0)

			datetime_now = datetime.datetime.utcnow()
			datetime_2000 = datetime.datetime(2000, 1, 1)
			timedelta = datetime_now - datetime_2000
			days = timedelta.total_seconds()/(24*60*60)
			db.task_set_finish(tasks_0, days)
		
		if len(tasks_1) > 0:
			db = get_db()
			db.task_set_progress(tasks_1, 0.0)	

def get_status_name(db_statuses, id):
	retVal = ''

	for status in db_statuses:
		if status[py_cerebro.dbtypes.STATUS_DATA_ID] == id:
			retVal = status[py_cerebro.dbtypes.STATUS_DATA_NAME]

	return retVal
					
def after_event(event):
	set_start = False

	if event.event_type() == event.EVENT_CHANGING_OF_TASKS_STATUS:

		db = get_db()
		db_statuses = db.statuses()

		tasks_change = set()

		for task in event.tasks():
			if task.status()[Statuses.DATA_NAME] == status_ready_to_start:
				messages = db.task_messages(task.id())
				ready_count = 0
				for message in messages:
					if message[py_cerebro.dbtypes.MESSAGE_DATA_TYPE] == py_cerebro.dbtypes.MESSAGE_TYPE_STATUS_CHANGES:
						if get_status_name(db_statuses, message[py_cerebro.dbtypes.MESSAGE_DATA_STATUS_ID]) == status_ready_to_start:
							ready_count += 1

				if ready_count == 1:
					set_start = True
	
	if event.event_type() == event.EVENT_CREATION_OF_MESSAGE and event.type() == event.TYPE_REPORT:
		task = cerebro.core.task(event.task_id())

		if task.allocated():
			current_user_id = cerebro.core.user_profile()[cerebro.aclasses.Users.DATA_ID]
			allocated_ids = set()

			for user in task.allocated():
				allocated_ids.add(user[cerebro.aclasses.Users.DATA_ID])

			if current_user_id in allocated_ids:
				db = get_db()
				messages = db.task_messages(event.task_id())
				alloc_reports_count = 0

				for message in messages:
					if message[py_cerebro.dbtypes.MESSAGE_DATA_TYPE] == py_cerebro.dbtypes.MESSAGE_TYPE_REPORT and \
					(message[py_cerebro.dbtypes.MESSAGE_DATA_CREATOR_ID] in allocated_ids):
						alloc_reports_count +=1

				if alloc_reports_count <= 1:
					set_start = True

	if set_start:
		datetime_now = datetime.datetime.utcnow()
		datetime_2000 = datetime.datetime(2000, 1, 1)
		timedelta = datetime_now - datetime_2000
		days = timedelta.total_seconds()/(24*60*60)
		task.set_start(days)

def error_event(error, event):	
	pass