# -*- coding: utf-8 -*-
"""
The *logon* module contains the *logon()* function, which handles logon
(authorisation) to the application.

.. py:function:: logon()
    
    Called on logon to Cerebro,
    right after authorisation, and on :ref:`Python being restarted
    on debugging <capi_restart_btn>`.
    
    logon.py::
    
        def logon():
            ...

"""
# Rename this file to logon.py to turn logon handling on
# See http://cerebrohq.com/documentation/en/ for more details on logon handling


import cerebro
import py_plugin_example.examples


# Sample files are located in the./examples folder
# Uncomment a line with an example to activate it

def logon():
	py_plugin_example.examples.logon.logon()
	pass
