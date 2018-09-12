# -*- coding: utf-8 -*-

import cerebro
import datetime
from cerebro.aclasses import Statuses
from cerebro.aclasses import Users
from cerebro.aclasses import AbstractMessage

import pstatuses.py_cerebro as py_cerebro

compose_name = 'Compose'
render_name = 'Render'

compose_status_to = 'paused'
render_status_to = 'could be better'

def get_db():
	db = py_cerebro.database.Database('db.cerebrohq.com', 45432)
	db.connect_from_cerebro_client()

	if not db:
		cerebro.core.print_error("Connect to Cerebro client error!")
		exit(1)

	return db

def after_event(event):
	# Status change
	if event.event_type() == event.EVENT_CHANGING_OF_TASKS_STATUS:
		tasks = event.tasks()
		for task in tasks: # All selected tasks
			status_t = task.status()
			parent_name_t = ''
			if task.parent_id():
				parent_name_t = cerebro.core.task(task.parent_id()).name()

			if parent_name_t.find(compose_name) >= 0:
				if status_t[Statuses.DATA_NAME] == compose_status_to:
					db = get_db()
					links = db.task_links(task.id())

					for link in links:
						tsk = db.task(link[py_cerebro.dbtypes.TASK_LINK_SRC])
						task_id = tsk[py_cerebro.dbtypes.TASK_DATA_ID]
						task_parent_id = tsk[py_cerebro.dbtypes.TASK_DATA_PARENT_ID]
						task_from_parent = ''
						if task_parent_id:
							task_from_parent = cerebro.core.task(task_parent_id).name()

						if task_from_parent.find(render_name) >= 0:
							task = cerebro.core.task(task_id)
							for status in task.possible_statuses():
								if status[Statuses.DATA_NAME] == render_status_to:
									 db.task_set_status(task_id, status[Statuses.DATA_ID])
