# -*- coding: utf-8 -*-
"""
The *event* module hanles the events ocurring in the application.

event.py::

	def before_event(error, event):	
		...

	def after_event(event):	
		...
		
	def error_event(event):	
		...

The events occur on application data changes made by a user
and the API allows to control the events. 
The application generates the events by performing 
definite actions. These call the corresponding functions
:py:func:`before_event() <event.before_event>`, :py:func:`after_event()<event.after_event>`
or :py:func:`error_event() <event.error_event>` from :ref:`event module <capi-templates>`.

The events are caused by data changing operations,
therefore the general meanings of these functions are the following:

* before_event() - an action before data changing;
* after_event() - an action after data changing;
* error_event() - handling of error on data changing.

"""
# Rename this file to event.py to turn the event handling on
# See http://cerebrohq.com/documentation/en/ for more details on event handling


import cerebro
import py_plugin_example.examples

# Sample files are located in the./examples folder
# Uncomment a line with an example to activate it

def before_event(event):
	py_plugin_example.examples.event.before_event(event)
	pass
	

def after_event(event):
	py_plugin_example.examples.event.after_event(event)
	pass
	

def error_event(error, event):
	plugin_example.examples.event.error_event(error, event)
	pass
