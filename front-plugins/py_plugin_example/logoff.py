# -*- coding: utf-8 -*-
"""
The *logoff* module contains the *logoff()* function which handles exit
(log off) from the application.

.. py:function:: logoff()

	Called on Cerebro session termination, returns either True or False. 
	If the function returns True, the session terminates, otherwise the session remains active
	and the application does not shut down.
	
	logoff.py::
	
		def logoff():	
			...
			return True # If the finction returns True, the session terminates,
							# otherwise the session remains active
							# and the application does not shut down.

"""
# Rename this file to logoff.py to turn logoff handling on
# See http://cerebrohq.com/documentation/en/ for more details on logoff handling


import cerebro
import py_plugin_example.examples


# Sample files are located in the./examples folder
# Uncomment a line with an example to activate it

def logoff():
	return py_plugin_example.examples.logoff.logoff()	
	return True # If the finction returns True, the session terminates,
						# otherwise the session remains active
						# and the application does not shut down.
