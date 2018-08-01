# -*- coding: utf-8 -*-
"""
Этот пример покажет как работать с элементами меню и кнопками приложения.
В примере рассмотрена работа с главным меню, контексными меню задач, сообщений и вложений.

Функции:

main() - функция для запуска примера
remove_menu() - удаляет и скрывает меню приложения
add_menu() - Создает меню приложения

hello_user() - Приветствие пользователя
hello_administrator() - Приветствие администратора
task_info() - заглушка для действия с чекбоксом
task_info_show() - Показать информацию о сообщении
message_text() - Показать текст сообщения
message_id() - показать ID сообщения
attach_size() - Показать размер вложения
"""

import cerebro


def main():
	# Добавление меню и действий
	add_menu()
	# Удаление меню и действий
	remove_menu()

def add_menu():
	# Путь к иконке
	icon = cerebro.core.python_api_dir() + '/examples/icon.png'

	# Добавим в главное меню пользовательское меню
	mainMenu = cerebro.actions.MainMenu() # Получили главное меню
	userMenu = mainMenu.add_menu('Users menu') # добавили пользовательское меню
	userSubmenu = userMenu.add_menu('Users submenu') # добавили в пользовательское меню подменю

	current_user = cerebro.core.user_profile() # получили профиль пользователя

	# В пользовательское меню добавим действия
	userSubmenu.add_action('py_plugin_example.examples.action.hello_user', 'Приветствие', icon) # добавили действие
	adminAction = userSubmenu.add_action('py_plugin_example.examples.action.hello_administrator', 'Приветствие администратора', icon) # добавили действие
	# Сделаем кнопку администратора недоступной для пользователя
	if current_user[cerebro.aclasses.Users.DATA_LOGIN] != 'Администратор': # проверяем пользователя
		adminAction.set_enabled(False) # Сделали кнопку недоступной

	# Добавим действия в контекстное меню задачи на вкладке навигация
	taskMenu = cerebro.actions.TaskNavigatorMenu() # Получили контестное меню задачи
	taskInfoAction = taskMenu.add_action('py_plugin_example.examples.action.task_info', 'Информация о задаче(ID + Name)') # добавили действие
	# Сформируем действие для его использование в других меню
	act = cerebro.actions.Action('py_plugin_example.examples.action.task_info_show', 'Информация о задаче', icon)
	taskMenu.add_action(act) # добавили действие
	taskInfoAction.set_checkable(True) # установили кнопку с чекбоксом

	# Добавим действие в панель инструментов задач
	taskToolBar = cerebro.actions.TaskToolBar() # Получили панель инструментов
	taskToolBarUserMenu = taskToolBar.insert_menu(taskToolBar.size() - 2, 'Меню', icon) # вставим меню на предпоследнюю позицию панели инструментов
	taskToolBarUserMenu.add_action(act) # добавим действие

	# Добавим подменю в контекстное меню сообщения
	messageMenu = cerebro.actions.MessageForumMenu()
	userMessageMenu = messageMenu.insert_menu(0, 'User Message menu') # вставим меню на первую позицию
	messageMenu.insert_separator(1)
	userMessageMenu.add_action('py_plugin_example.examples.action.message_text', 'Текст сообщения') # добавили действие
	userMessageMenu.add_separator() # добавили разделитель
	userMessageMenu.add_action('py_plugin_example.examples.action.message_creator', 'Автор сообщения') # добавили действие

	# Добавим действие на панель инструментов вложений задачи
	attachToolBar = cerebro.actions.AttachmentForumToolBar() # Получили панель инструментов
	attachToolBar.add_action('py_plugin_example.examples.action.attach_size', 'Размер вложения', icon) # добавили действие

def remove_menu():
	# Уберем всем пользователям меню Web conference из главного меню
	mainMenu = cerebro.actions.MainMenu() # Получили главное меню
	mainMenu.remove_menu('conference') # удалили меню Web conference

	# В контестном меню задачи запретим всем пользователям кроме пользователя с логином 'Администратор' вырезать задачи
	taskNavMenu = cerebro.actions.TaskNavigatorMenu() # получили контекстное меню задачи
	current_user = cerebro.core.user_profile() # получили профиль пользователя
	if current_user[cerebro.aclasses.Users.DATA_LOGIN] != 'Администратор': # проверяем пользователя
		if taskNavMenu.has_action('app.action.task.cut'): # проверяем существует ли такой пункт меню
			taskNavMenu.action('app.action.task.cut').set_visible(False) # скрываем меню
		if taskNavMenu.has_action('app.action.task.cut_referense'): # проверяем существует ли такой пункт меню
			taskNavMenu.action('app.action.task.cut_referense').set_visible(False) # скрываем меню

def hello_user(): # Приветствие пользователя
	current_user = cerebro.core.user_profile() # получили профиль пользователя
	msg = 'Hello ' + current_user[cerebro.aclasses.Users.DATA_FULL_NAME] # сформировали сообщение
	cerebro.gui.information_box('Cerebro Python API', msg) # показали сообщение

def hello_administrator(): # Приветствие администратора
	current_user = cerebro.core.user_profile() # получили профиль пользователя
	msg = 'Hello administrator' + current_user[cerebro.aclasses.Users.DATA_FULL_NAME] # сформировали сообщение
	cerebro.gui.information_box('Cerebro Python API', msg) # показали сообщение

def task_info(): # заглушка для действия с чекбоксом
	pass

def task_info_show(): # Показать информацию о сообщении
	task = cerebro.core.current_task() # Получили текущее сообщение

	# Получим состояние кнопки 'Информация о задаче(ID + Name)'
	taskMenu = cerebro.actions.TaskNavigatorMenu() # Получили контестное меню задачи
	chkAction = taskMenu.action('examples.action.task_info')

	# Сформируем сообщение в зависимости от условия
	if chkAction.is_checked():
		msg = 'Имя задачи: ' + task.name() + ', ID задачи: ' + str(task.id()) # Сообщение при включенном пункте 'Информация о задаче(ID + Name)'
	else:
		msg = 'Имя задачи: ' + task.name() # Сообщение при выключенном пункте 'Информация о задаче(ID + Name)'
	cerebro.gui.information_box('Cerebro Python API', msg) # показали сообщение

def message_text(): # Показать текст сообщения
	# Проверяем выбрано ли сообщение
	if cerebro.core.selected_messages():
		message = cerebro.core.selected_messages()[0] # Получили первое выбранное сообщение
		msg = 'Текст сообщения: \n' + message.text_as_plain()  # Сформировали сообщение
	else:
		msg = 'Не выбрано ни одного сообщения!'  # Сформировали сообщение
	cerebro.gui.information_box('Cerebro Python API', msg) # показали сообщение

def message_creator(): # показать ID сообщения
	# Проверяем выбрано ли сообщение
	if cerebro.core.selected_messages():
		message = cerebro.core.selected_messages()[0] # Получили первое выбранное сообщение
		msg = 'Автор сообщения: ' + message.data()[cerebro.aclasses.Message.DATA_CREATOR_NAME] # Сформировали сообщение
	else:
		msg = 'Не выбрано ни одного сообщения!'  # Сформировали сообщение
	cerebro.gui.information_box('Cerebro Python API', msg) # показали сообщение

def attach_size(): # Показать размер вложения
	# Проверяем выбрано ли вложение
	if cerebro.core.selected_attachments():
		attach = cerebro.core.selected_attachments()[0] # Получили первое выбранное вложение
		msg = 'Размер вложения: ' + str(attach.file_size())  # Сформировали сообщение
	else:
		msg = 'Не выбрано ни одного вложения!'  # Сформировали сообщение
	cerebro.gui.information_box('Cerebro Python API', msg) # показали сообщение
