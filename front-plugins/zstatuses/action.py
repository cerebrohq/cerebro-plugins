# -*- coding: utf-8 -*-
"""
The *action* module allows to add user-defined menu items into the application.
New custom menu items can be added to the following elements of the interface:
	
* Main menu
* Task-specific context menu
* Message-specific context menu
* Attachment-specific context menu

.. note::
	the task-specific context menu can be called in several contexts:
	in Navigator, in To-Do list, in Followed list,
	as well as in the Search tab. Custom menu items added 
	into the task-specific menu appear in all of listed above contexts.

	The attachment-specific context menu can be called in Forum alongside with
	the message-specific menu, and while searching the attachments. Custom menu items added
	into the attachment-specific menu appear in Forum
	and in attachment search window.

	Message-specific context menu is called from a task Forum thread.

Each menu item added should be tied to a function of 
a custom user's module. Activation of the menu item calls
the corresponding function.
Besides, the custom user's menu items can have graphic thumbnails
and assigned hot key combinations.

Custom user's menus are added to the *init_actions* functions
from :ref:`menu module <capi-templates>`. 

.. py:function:: init_actions()

	Called on application start and on
	:ref:`Python modules updating on debugging <capi_updating_btn>`.

	action.py::

		def init_actions():
			...

"""

import cerebro

import zstatuses.py_cerebro as py_cerebro

def get_db():
	db = py_cerebro.database.Database('db.cerebrohq.com', 45432)
	db.connect_from_cerebro_client()

	if not db:
		cerebro.core.print_error("Connect to Cerebro client error!")
		exit(1)

	return db

def recalc_dates():
	cur_id = cerebro.core.current_task().id()

	if cur_id:
		db = get_db()
		childr = cerebro.core.task_children(cur_id, True)
		cur_task = db.task(cur_id)

		start = -1
		finish = -1

		for ch in childr:
			ch_task = db.task(ch.id())
			ch_start = ch_task[py_cerebro.dbtypes.TASK_DATA_OFFSET]
			ch_finish = ch_task[py_cerebro.dbtypes.TASK_DATA_OFFSET] + ch_task[py_cerebro.dbtypes.TASK_DATA_DURATION]

			cerebro.core.print_warning('task START: ' + str(ch_task[py_cerebro.dbtypes.TASK_DATA_OFFSET]))
			cerebro.core.print_warning('task FINISH: ' + str(ch_task[py_cerebro.dbtypes.TASK_DATA_OFFSET] + ch_task[py_cerebro.dbtypes.TASK_DATA_DURATION]))

			if start == -1:
				start = ch_task[py_cerebro.dbtypes.TASK_DATA_OFFSET]
			else:
				if ch_task[py_cerebro.dbtypes.TASK_DATA_OFFSET] < start:
					start = ch_task[py_cerebro.dbtypes.TASK_DATA_OFFSET]
			
			if finish == -1:
				finish = ch_task[py_cerebro.dbtypes.TASK_DATA_OFFSET] + ch_task[py_cerebro.dbtypes.TASK_DATA_DURATION]
			else:
				if ch_task[py_cerebro.dbtypes.TASK_DATA_OFFSET] + ch_task[py_cerebro.dbtypes.TASK_DATA_DURATION] > finish:
					finish = ch_task[py_cerebro.dbtypes.TASK_DATA_OFFSET] + ch_task[py_cerebro.dbtypes.TASK_DATA_DURATION]

		cerebro.core.print_warning('')
		cerebro.core.print_warning('CUR task START: ' +  str(cur_task[py_cerebro.dbtypes.TASK_DATA_OFFSET]))
		cerebro.core.print_warning('CUR task FINISH: ' +  str(cur_task[py_cerebro.dbtypes.TASK_DATA_OFFSET] + cur_task[py_cerebro.dbtypes.TASK_DATA_DURATION]))

		cerebro.core.print_warning('')
		cerebro.core.print_warning('NEW START: ' + str(start))
		cerebro.core.print_warning('NEW FINISH: ' + str(finish))
		if start != -1:
			db.task_set_start(cur_id, start)
			cerebro.core.print_warning('START SETTED')

			if finish != -1:
				db.task_set_finish(cur_id, finish)
				cerebro.core.print_warning('FINISH SETTED')

		cerebro.core.refresh_all()

def init_actions():
	cerebro.actions.TaskToolBar().add_action('zstatuses.action.recalc_dates', 'Recalculate dates', '')
	cerebro.actions.TaskNavigatorMenu().add_action('zstatuses.action.recalc_dates', 'Recalculate dates', '')
	pass