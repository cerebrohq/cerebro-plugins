# -*- coding: utf-8 -*-
"""
The sample shows the usage of PyQt5 package (http://www.riverbankcomputing.com/software/pyqt/).
The package is included in Cerebro distribution pack, located in the "py-site-packages" folder.

Functions:

create_menu() - adding menu items calling Qt windows.
show_dialog() - is called on activation of a custom 'Qt dialog' menu item
show_window() - is called on activation of a custom 'Qt window' menu item
"""

import cerebro

def create_menu():	
	# Adding menu items calling Qt windows.	
	
	# Adding the items to the main menu
	main_menu = cerebro.actions.MainMenu() # getting the main menu	
	my_menu = main_menu.insert_menu(main_menu.size() - 2, 'Python Qt') # inserting the submenu into the penultimate position
	
	my_menu.add_action('py_plugin_example.examples.pyqt.show_dialog',  'Qt dialog') # adding the menu item
	my_menu.add_action('py_plugin_example.examples.pyqt.show_window',  'Qt window') # adding the menu item



def show_dialog():
	# A 'Qt Dialog' main menu item activation.
	# Displays a dialog. The main interface is blocked at the moment.		
	from PyQt5 import QtWidgets,  QtCore
	
	class MyDialog(QtWidgets.QDialog): # dialog class

		def __init__(self, parent=None):
			super(MyDialog, self).__init__(parent)
			
			label = QtWidgets.QLabel('Qt dialog')				
			label.setAlignment(QtCore.Qt.AlignCenter)			
			
			mainLayout = QtWidgets.QGridLayout()
			mainLayout.addWidget(label, 0, 0)
			
			self.setLayout(mainLayout)		
	
	
	dialog = MyDialog()
	dialog.setFixedSize(300,  200)
	dialog.exec_() # main application interface remains blocked until the dialog window is closed

	
window = None

def show_window():
	# A 'Qt Window' main menu item activation.
	# The window doesn't cause the main interface to block.		
	from PyQt5 import QtWidgets,  QtCore
	
	global window	
	
	if window == None: # if a window object is not created yet, creating it
		window = QtWidgets.QLabel()
		window.setAlignment(QtCore.Qt.AlignCenter)
		window.setFixedSize(300,  200)
		window.setWindowTitle('Qt window')
		window.setText('Displaying the window for the first time')
	else:
		window.setText('Displaying the window for the next time')
		
	window.show()
