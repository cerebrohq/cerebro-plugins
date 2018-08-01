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
import py_plugin_example.examples

def init_actions():
	py_plugin_example.examples.action.main()
	pass