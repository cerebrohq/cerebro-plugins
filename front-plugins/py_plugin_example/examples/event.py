# -*- coding: utf-8 -*-

"""
The example shows message creation, task creation and progress altering event handling.
Below we will: 

a) check if a file is being attached while posting a new report;
b) make a newly created task highly prioritized if it starts today;
c) ask a user for a confirmation if he/she is lowering the progress value down.

The functions:

before_event() - the action before changing data
after_event() - the action after changing data
error_event() - data change error handling
"""

import cerebro
import datetime



def before_event(event):
	print('before_event', event.type_str())
	# Checking if a new report being posted contains attachment(-s)
	if event.event_type() == event.EVENT_CREATION_OF_MESSAGE: # if the event type is "Creation of message"
		if event.type() == event.TYPE_REPORT: # if the new message is "Report"
			
			attachs = event.new_attachments() # getting all attachments to the message
			if len(attachs) == 0: # if there are no attachments there, raising an exception
				raise Exception('Please attach a file to your report') 
				# The report will not be posted, the user will be displayed a window with this text instead.
			for a in attachs:
				# Auto approve attached files
				a.set_approved(True)
		elif event.type() == event.TYPE_NOTE:
			# Remove all non-link attachments from note message
			for attach in event.new_attachments():
				if not attach.is_link():
					attach.remove()

	elif event.event_type() == event.EVENT_CHANGING_OF_TASKS_CHECKS:
		print('Check items "{}" {}'.format(event.new_value(), 'added' if event.is_added() else 'removed' ))

	elif event.event_type() == event.EVENT_CHANGING_OF_TASKS_CHECKS_VALUES:
		for ch in event.checks():
			print('Check item "{}" {}'.format(ch.name(), 'set' if event.new_value() else 'unset' ))
			print('Check item val "{}" {}'.format(ch.name(), event.new_value() ))
	
	elif event.event_type() == event.EVENT_CHANGING_OF_ATTACHMENT_APPROVED:
		print('Attachments approved: {}'.format('True' if event.new_value() else 'False'))
	
	# Asking a user for a confirmation when he/she is trying to lower the task progress down
	elif event.event_type() == event.EVENT_CHANGING_OF_TASKS_PROGRESS: # if the event type is "Changing of task progress"
		
		tasks = event.tasks() # getting tasks being changed
		new_progress = event.new_value() # getting the progress value input by user
		for task in tasks: # checking if the new value is higher or lower than the old one
			if new_progress < task.progress(): # if the new progress value is lower, then:
				# asking the user for a confirmation
				q = 'Are you sure you want to lower the "'+task.name()+'" task progress?'
				if cerebro.gui.question_box('Changing of progress',  q) == False: # if the user is not sure, then:
					raise Exception('') 
				# the progress change will not be saved
	elif event.event_type() == event.EVENT_COPY_TASKS:
		tasks = event.tasks()
		dst = event.destination()
		dst_names = event.destination_names()
		
		print('Copy tasks: "{}" to "{}" as "{}"'.format(
			';'.join([t.parent_url() + t.name() for t in tasks])
			, ';'.join([t.parent_url() + t.name() for t in dst])
			, ';'.join(dst_names)
		))


def after_event(event):	
	print('after_event', event.type_str())
	# a newly created task highly prioritized if it starts today
	if event.event_type() == event.EVENT_CREATION_OF_TASK: # if the event type is "Creation of task"
		print('Created task: "{}"'.format(event.parent_url() + event.name()))
		start = event.start() # getting the task starting time
		delta = start - datetime.datetime.now()	
		if delta.days == 0 or delta.days == -1: # if today is the starting date
			event.set_priority(event.PRIORITY_HIGH) # the task is attributed with "High Priority"
	
	elif event.event_type() == event.EVENT_CHANGING_OF_TASKS_CHECKS or event.event_type() == event.EVENT_CHANGING_OF_TASKS_CHECKS_VALUES:
		print( event.type_str())
		for task in event.tasks():
			if len(task.checks()):
				print('Task "{}" Checklist:\n{}'.format(task.name(), '\n'.join(ch.name() + ' {}'.format(ch.value()) for ch in task.checks())))	
			else:
				print('Task has not checklist')


def error_event(error, event):
	print('Event error',  event.type_str(),  error)
