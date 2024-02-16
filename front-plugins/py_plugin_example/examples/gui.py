# -*- coding: utf-8 -*-
import os
import cerebro

panel_main = None
panel_side = None
panel_forum = None

TAB_MAIN = 'Мой таб'
TAB_SIDE = 'Мои свойства'
TAB_FORUM = 'Моя вкладка в форуме'

def main():
	# Добавление меню и действий
	add_menu()
	# Добавление панелей
	add_panels()

def add_panels():
	try:
		from qtpy.QtCore import QUrl
		from qtpy.QtWidgets import QWidget, QLabel, QVBoxLayout
		from qtpy.QtWebEngineWidgets import QWebEngineView
	except ImportError:
		from PyQt5.QtCore import QUrl
		from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
		from PyQt5.QtWebEngineWidgets import QWebEngineView
	
	class MyMainPanel(QWidget):
		def __init__(self, parent = None):
			QWidget.__init__(self, parent)
			
			self.initUI()
		
		def setCurrentTask(self, task_id):
			print("MyMainPanel TASK", task_id)
		
		def setPanelVisible(self, is_visible):
			print("MyMainPanel VISIBLE", is_visible)
			if is_visible and self.we_view.url().isEmpty():
				self.we_view.load(QUrl("https://apps.cerebrohq.com/app/administration/pay"))
		
		def initUI(self):
			vl = QVBoxLayout(self)
			vl.setSpacing(0)
			vl.setContentsMargins(0, 0, 0, 0)
			
			self.we_view = QWebEngineView(self)
			
			vl.addWidget(self.we_view)
			
			self.setLayout(vl)
	
	class MySidePanel(QWidget):
		def __init__(self, parent = None):
			QWidget.__init__(self, parent)
			
			self.initUI()
		
		def setCurrentTask(self, task_id):
			print("MySidePanel TASK", task_id)
			task = cerebro.core.task(task_id)
			if task:
				self.lb_name.setText(task.name())
		
		def setPanelVisible(self, is_visible):
			print("MySidePanel VISIBLE", is_visible)
		
		def initUI(self):
			vl = QVBoxLayout(self)
			vl.setSpacing(0)
			vl.setContentsMargins(0, 0, 0, 0)
			
			self.lb_name = QLabel(self)
			
			vl.addWidget(self.lb_name)
			
			self.setLayout(vl)
	
	class MyForumPanel(QWidget):
		def __init__(self, parent = None):
			QWidget.__init__(self, parent)
			
			self.initUI()
		
		def setCurrentTask(self, task_id):
			print("MyForumPanel TASK", task_id)
			task = cerebro.core.task(task_id)
			if task:
				self.lb_name.setText(task.name())
		
		def setPanelVisible(self, is_visible):
			print("MyForumPanel VISIBLE", is_visible)
		
		def initUI(self):
			vl = QVBoxLayout(self)
			vl.setSpacing(0)
			vl.setContentsMargins(0, 0, 0, 0)
			
			self.lb_name = QLabel(self)
			
			vl.addWidget(self.lb_name)
			
			self.setLayout(vl)
	
	global panel_main
	global panel_side
	global panel_forum
	
	# Путь к иконке
	icon = os.path.dirname(os.path.abspath(__file__)) + '/icon.png'
	
	tabs = cerebro.gui.MainTabWidget()
	panel_main = MyMainPanel()
	my_panel = tabs.add_panel(TAB_MAIN, icon, 'My tab tooltip')
	my_panel.set_widget(panel_main)
	my_panel.add_callback(my_panel.CALLBACK_CURRENTTASK, panel_main.setCurrentTask)
	my_panel.add_callback(my_panel.CALLBACK_PANELVISIBLE, panel_main.setPanelVisible)
	
	tabs = cerebro.gui.SideTabWidget()
	panel_side = MySidePanel()
	my_panel = tabs.add_panel(TAB_SIDE)
	my_panel.set_widget(panel_side)
	my_panel.add_callback(my_panel.CALLBACK_CURRENTTASK, panel_side.setCurrentTask)
	my_panel.add_callback(my_panel.CALLBACK_PANELVISIBLE, panel_side.setPanelVisible)
	
	tabs = cerebro.gui.ForumTabWidget()
	panel_forum = MyForumPanel()
	my_panel = tabs.add_panel(TAB_FORUM)
	my_panel.set_widget(panel_forum)
	my_panel.add_callback(my_panel.CALLBACK_CURRENTTASK, panel_forum.setCurrentTask)
	my_panel.add_callback(my_panel.CALLBACK_PANELVISIBLE, panel_forum.setPanelVisible)


def add_menu():
	taskMenu = cerebro.actions.MainMenu()
	userMenu = taskMenu.add_menu('Панели')
	userMenu.add_action('py_plugin_example.examples.gui.open_main', 'Переключиться на python-таб', '')
	userMenu.add_action('py_plugin_example.examples.gui.open_side', 'Открыть python-вкладку', '')
	userMenu.add_action('py_plugin_example.examples.gui.open_forum', 'Открыть python-вкладку в форуме', '')
	userMenu.add_action('py_plugin_example.examples.gui.unbind_main', 'Отключить python-таб', '')
	userMenu.add_action('py_plugin_example.examples.gui.unbind_side', 'Отключить python-вкладку', '')
	userMenu.add_action('py_plugin_example.examples.gui.unbind_forum', 'Отключить python-вкладку в форуме', '')
	userMenu.add_action('py_plugin_example.examples.gui.remove_main', 'Удалить python-таб', '')
	userMenu.add_action('py_plugin_example.examples.gui.remove_side', 'Удалить python-вкладку', '')
	userMenu.add_action('py_plugin_example.examples.gui.remove_forum', 'Удалить python-вкладку в форуме', '')


def open_main():
	tabs = cerebro.gui.MainTabWidget()
	my_panel = tabs.panel(TAB_MAIN)
	if my_panel:
		my_panel.set_visible(True)

def open_side():
	tabs = cerebro.gui.SideTabWidget()
	my_panel = tabs.panel(TAB_SIDE)
	if my_panel:
		my_panel.set_visible(True)

def open_forum():
	tabs = cerebro.gui.ForumTabWidget()
	my_panel = tabs.panel(TAB_FORUM)
	if my_panel:
		my_panel.set_visible(True)

def unbind_main():
	global panel_main
	
	tabs = cerebro.gui.MainTabWidget()
	my_panel = tabs.panel(TAB_MAIN)
	if panel_main and my_panel:
		my_panel.remove_callback(my_panel.CALLBACK_CURRENTTASK, panel_main.setCurrentTask)
		my_panel.remove_callback(my_panel.CALLBACK_PANELVISIBLE, panel_main.setPanelVisible)

def unbind_side():
	global panel_side
	
	tabs = cerebro.gui.SideTabWidget()
	my_panel = tabs.panel(TAB_SIDE)
	if panel_side and my_panel:
		my_panel.remove_callback(my_panel.CALLBACK_CURRENTTASK, panel_side.setCurrentTask)
		my_panel.remove_callback(my_panel.CALLBACK_PANELVISIBLE, panel_side.setPanelVisible)

def unbind_forum():
	global panel_forum
	
	tabs = cerebro.gui.ForumTabWidget()
	my_panel = tabs.panel(TAB_FORUM)
	if panel_forum and my_panel:
		my_panel.remove_callback(my_panel.CALLBACK_CURRENTTASK, panel_forum.setCurrentTask)
		my_panel.remove_callback(my_panel.CALLBACK_PANELVISIBLE, panel_forum.setPanelVisible)

def remove_main():
	tabs = cerebro.gui.MainTabWidget()
	tabs.remove_panel(TAB_MAIN)

def remove_side():
	tabs = cerebro.gui.SideTabWidget()
	tabs.remove_panel(TAB_SIDE)

def remove_forum():
	tabs = cerebro.gui.ForumTabWidget()
	tabs.remove_panel(TAB_FORUM)
