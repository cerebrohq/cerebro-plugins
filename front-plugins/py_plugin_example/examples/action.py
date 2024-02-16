# -*- coding: utf-8 -*-

import cerebro
import os.path
import pycerebro
import py_plugin_example.xlsxwriter


def main():
	# Добавление меню и действий
	add_menu()

def add_menu():

	# cerebro.core.task_children(0)

	# Путь к иконке
	icon = os.path.dirname(os.path.abspath(__file__)) + '/icon.png'	

	current_user = cerebro.core.user_profile() # получили профиль пользователя
	
	"""Гланое меню"""
	# Добавим в главное меню пользовательское меню
	mainMenu = cerebro.actions.MainMenu() # Получили главное меню
	userMenu = mainMenu.add_menu('Users menu') # добавили пользовательское меню
	userSubmenu = userMenu.add_menu('Users submenu') # добавили в пользовательское меню подменю	

	# В пользовательское меню добавим действия
	userSubmenu.add_action('py_plugin_example.examples.action.hello_user', 'Приветствие', icon) # добавили действие
	adminAction = userSubmenu.add_action('py_plugin_example.examples.action.hello_administrator', 'Приветствие администратора', icon) # добавили действие
	
	userMenu.add_action('py_plugin_example.examples.action.is_debug', 'Отладочное приложение?', icon) # добавили действие
	userMenu.add_action('py_plugin_example.examples.action.verified_ssl', 'Выключить проверку ssl', icon) # добавили действие
	userMenu.add_action('py_plugin_example.examples.logoff.reports', 'Наличие отчетов (запрос+принт)', icon) # добавили действие
	userMenu.add_action('py_plugin_example.examples.action.winput', 'Ввод значений', icon) # добавили действие
	userMenu.add_action('py_plugin_example.examples.action.wpass', 'Пароль', icon) # добавили действие
	
	isadmin = cerebro.core.has_perm_global(cerebro.aclasses.Perm.PERM_GLOBAL_USERS)
	print('isadmin', isadmin)
	# Сделаем кнопку администратора недоступной для пользователя
	if isadmin == False: # проверяем пользователя
		adminAction.set_enabled(False) # Сделали кнопку недоступной
	
	"""Меню и тулбары задач"""
	# action информации по задаче в меню и турбары
	taskInfoAction = cerebro.actions.Action('py_plugin_example.examples.action.task_info_show', 'Информация о задаче', icon)
	
	# Добавим действия в контекстное меню задачи на вкладке навигация
	taskMenu = cerebro.actions.TaskNavigatorMenu() # Получили контестное меню задачи
	taskCheckBox = taskMenu.add_action('py_plugin_example.examples.action.task_info', 'Чекбокс (+ID задачи)')
	taskCheckBox.set_checkable(True) # установили кнопку с чекбоксом
	taskMenu.add_action(taskInfoAction) # добавили действие	
	taskMenu.add_action('py_plugin_example.examples.action.task_menu_remove', 'Удалить/Восстановить пункты выреза', icon, 'Ctrl+Q')
	taskMenu.add_action('py_plugin_example.examples.action.copy_task', 'Копировать задачу с другим именем', icon)

	taskMenu.add_action('py_plugin_example.examples.action.error_from_app', 'Ошибка установки текущей задачи', icon)

	taskMenu.add_action('py_plugin_example.examples.action.add_checks', 'Добавить чек-лист: раз[v], два, три', icon)
	taskMenu.add_action('py_plugin_example.examples.action.add_checks_pycerebro', 'Добавить и установить чек-пункт из pycerebro', icon)
	taskMenu.add_action('py_plugin_example.examples.action.clear_checks', 'Очистить чек-лист', icon)

	taskMenu.add_action('py_plugin_example.examples.action.move_task', 'Переместить задачу на уровень выше', icon)
	
	cerebro.actions.TaskActiveMenu().add_action(taskInfoAction)
	cerebro.actions.TaskActiveMenu().add_separator()
	cerebro.actions.TaskSearchMenu().add_action(taskInfoAction)
	cerebro.actions.TaskSearchMenu().add_separator()
	cerebro.actions.TaskToDoListMenu().add_action(taskInfoAction)	
	cerebro.actions.TaskToDoListMenu().add_separator()

	# Добавим действие в панель инструментов задач
	taskToolBar = cerebro.actions.TaskToolBar() # Получили панель инструментов
	taskToolBar.insert_separator(3)
	taskToolBarUserMenu = taskToolBar.insert_menu(4, 'Меню', icon) # вставим меню на предпоследнюю позицию панели инструментов
	taskToolBar.insert_separator(5)		
	taskToolBarUserMenu.add_action(taskInfoAction) # добавим действие

	"""Меню и тулбар сообщений в форуме"""
	messInfoAction = cerebro.actions.Action('py_plugin_example.examples.action.message_creator', 'Автор сообщения', icon)
	
	# Добавим подменю в контекстное меню сообщения
	messageMenu = cerebro.actions.MessageForumMenu()
	messageMenu.insert_separator(1)
	userMessageMenu = messageMenu.insert_menu(2, 'User Message menu', icon) # вставим меню на первую позицию
	messageMenu.insert_separator(3) # добавили разделитель
	userMessageMenu.add_action(messInfoAction) # добавили действие
	
	messbar = cerebro.actions.MessageForumToolBar()	
	messbar.add_action(messInfoAction)
	messbar.insert_separator(1)

	"""Меню и тулбар файлов в форуме"""
	attachInfoAction = cerebro.actions.Action('py_plugin_example.examples.action.attach_size', 'Размер вложения', icon)
	attachApproveAction = cerebro.actions.Action('py_plugin_example.examples.action.attach_approve', 'Переключить утвержденный статус', icon)

	cerebro.actions.AttachmentEditorMenu().add_action(attachInfoAction)
	cerebro.actions.AttachmentEditorMenu().add_action(attachApproveAction)
	cerebro.actions.AttachmentForumMenu().add_action(attachInfoAction)
	cerebro.actions.AttachmentForumMenu().add_action(attachApproveAction)
	cerebro.actions.AttachmentSearchMenu().add_action(attachInfoAction)
	cerebro.actions.AttachmentSearchMenu().add_action(attachApproveAction)

	cerebro.actions.AttachmentForumToolBar().add_action(attachInfoAction)
	cerebro.actions.AttachmentForumToolBar().add_action(attachApproveAction)
	cerebro.actions.AttachmentSearchToolBar().add_action(attachInfoAction)
	cerebro.actions.AttachmentSearchToolBar().add_action(attachApproveAction)

	
def task_menu_remove():	
	taskNavMenu = cerebro.actions.TaskNavigatorMenu() # получили контекстное меню задачи
	if taskNavMenu.has_action('app.action.task.cut'): # проверяем существует ли такой пункт меню
		taskNavMenu.action('app.action.task.cut').set_visible(not taskNavMenu.action('app.action.task.cut').is_visible()) # скрываем меню
	if taskNavMenu.has_action('app.action.task.cut_referense'): # проверяем существует ли такой пункт меню
		taskNavMenu.action('app.action.task.cut_referense').set_visible(not taskNavMenu.action('app.action.task.cut_referense').is_visible()) # скрываем меню

def hello_user(): # Приветствие пользователя
	current_user = cerebro.core.user_profile() # получили профиль пользователя
	msg = 'Hello ' + current_user[cerebro.aclasses.Users.DATA_FULL_NAME] # сформировали сообщение
	cerebro.gui.information_box('Cerebro Python API', msg) # показали сообщение
	"""
	db = pycerebro.database.Database('', '')
	if db.connect_from_cerebro_client() != 0:
		db.connect("superuser", "1234")

	print("db connect")
	"""

def hello_administrator(): # Приветствие администратора
	current_user = cerebro.core.user_profile() # получили профиль пользователя
	msg = 'Hello administrator ' + current_user[cerebro.aclasses.Users.DATA_FULL_NAME] # сформировали сообщение
	cerebro.gui.information_box('Cerebro Python API', msg) # показали сообщение

def task_info(): # заглушка для действия с чекбоксом
	pass

def task_info_show(): # Показать информацию о сообщении
	task = cerebro.core.current_task() # Получили текущую задачу

	# Получим состояние кнопки 'Информация о задаче(ID + Name)'
	taskMenu = cerebro.actions.TaskNavigatorMenu() # Получили контестное меню задачи
	chkAction = taskMenu.action('py_plugin_example.examples.action.task_info')

	# Сформируем сообщение в зависимости от условия
	if chkAction.is_checked():
		msg = 'Имя задачи: ' + task.name() + ', ID задачи: ' + str(task.id()) # Сообщение при включенном пункте 'Информация о задаче(ID + Name)'
	else:
		msg = 'Имя задачи: ' + task.name() # Сообщение при выключенном пункте 'Информация о задаче(ID + Name)'
	cerebro.gui.information_box('Cerebro Python API', msg) # показали сообщение

def verified_ssl():
	db = cerebro.db.Db()
	db.set_verify_ssl(False)
	user_id = db.execute('select get_usid()')
	cerebro.gui.information_box('Cerebro Python API', 'Выполнен запрос на идентификатор пользователя без проверки ssl сертификата.\n Verify ssl {}, User ID {}'.format(str(db.verify_ssl), user_id[0][0])) # показали сообщение


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

def attach_approve(): # Переключить принятый статус
	if cerebro.core.selected_attachments():
		attach = cerebro.core.selected_attachments()[0] # Получили первое выбранное вложение
		attach.set_approved(not attach.is_approved())
		msg = 'Статус вложения: ' + 'Отвергнуто' if attach.is_approved() else 'Принято'  # Сформировали сообщение
		cerebro.core.refresh_tasks()
	else:
		msg = 'Не выбрано ни одного вложения!'  # Сформировали сообщение
	cerebro.gui.information_box('Cerebro Python API', msg) # показали сообщение


def is_debug():
	import py_cerebro_db, sys
	isdebug = py_cerebro_db.is_debug_app()
	msg = ''
	if isdebug:
		msg = 'Да'
	else:
		msg = 'Нет'
	
	print("is_debug", msg)
	
	#print("111111 test 111111", 1/0)
	cerebro.gui.information_box('Cerebro Python API', msg) # показали сообщение

def error_from_app():	
	cerebro.core.set_current_task(-1)

def winput():
	
	txt = input('Input text, please\n')
	
	cerebro.gui.information_box('Cerebro Python API', txt) # показали сообщение

def wpass():
	daccount = cerebro.gui.AccountDialog('Сохранение пароля', 'Введите ваш логин и пароль', 'store_key')	
	if len(daccount.login()) > 0:
		cerebro.gui.information_box('Cerebro Python API', 'Сохранённая запись:\n{}\n{}'.format(daccount.login(), daccount.password())) # показали сообщение
		daccount = cerebro.gui.AccountDialog('Сохранение пароля', 'Введите ваш логин и пароль', '')

	res = daccount.execute()
	
	if res == True:
		print('Введенные пользователем логин и пароль', daccount.login(), daccount.password())
		daccount.store('store_key') # сохраняем пароль для последующих вызовов  


def copy_task():
	db = pycerebro.database.Database()
	# Устанавливаем соединение с базой данных
	if db.connect_from_cerebro_client() != 0: # пробуем установить соединение с помощью запущенного клиента Cerebro. 
		cerebro.gui.critical_box('Cerebro Python API', 'Не получилось подключится через клиента') # показали сообщение
		return

	task = cerebro.core.current_task() # Получили текущую задачу
	if task is not None:
		dinput = cerebro.gui.InputDialog(cerebro.gui.InputDialog.TYPE_STRING, 'Имя новой задачи', 'Имя новой задачи')		
		res = dinput.execute()
		if res == True:
			print(task.parent_id(), task.id(), dinput.value())
			db.copy_tasks(task.parent_id(), [(task.id(), dinput.value()),])
			cerebro.core.refresh_tasks()

def add_checks():
	tasks = cerebro.core.selected_tasks() # Получили выделенные задачи
	if len(tasks) == 0:
		cerebro.gui.information_box('Cerebro Python API', 'Задачи не выбраны') # показали сообщение
	else:		
		for task in tasks:
			task.add_checks(['раз', 'два', 'три'])
			for ch in task.checks():
				if ch.name() == 'раз':
					ch.set_value(1)

		cerebro.core.refresh_tasks()

def add_checks_pycerebro():
	db = pycerebro.database.Database()
	# Устанавливаем соединение с базой данных
	if db.connect_from_cerebro_client() != 0: # пробуем установить соединение с помощью запущенного клиента Cerebro. 
		cerebro.gui.critical_box('Cerebro Python API', 'Не получилось подключится через клиента') # показали сообщение
		return

	tasks = cerebro.core.selected_tasks() # Получили выделенные задачи
	if len(tasks) == 0:
		cerebro.gui.information_box('Cerebro Python API', 'Задачи не выбраны') # показали сообщение
	else:
		dinput = cerebro.gui.InputDialog(cerebro.gui.InputDialog.TYPE_STRING, 'Имя чек-пункта', 'Имя нового чек-пункта')		
		res = dinput.execute()
		if res == True:
			task_ids = [task.id() for task in tasks]
			chech_ids = db.task_set_checks(task_ids, dinput.value())
			print(chech_ids)
			db.task_set_checks_value(task_ids, chech_ids, 1)
			cerebro.core.refresh_all()
			cerebro.core.refresh_tasks()

def clear_checks():
	tasks = cerebro.core.selected_tasks() # Получили выделенные задачи
	if len(tasks) == 0:
		cerebro.gui.information_box('Cerebro Python API', 'Задачи не выбраны') # показали сообщение
	else:		
		for task in tasks:
			if len(task.checks()) > 0:
				checks = [ch.name() for ch in task.checks()]
				task.remove_checks(checks)
		cerebro.core.refresh_tasks()


def move_task():
	db = pycerebro.database.Database()
	# Устанавливаем соединение с базой данных
	if db.connect_from_cerebro_client() != 0: # пробуем установить соединение с помощью запущенного клиента Cerebro. 
		cerebro.gui.critical_box('Cerebro Python API', 'Не получилось подключится через клиента') # показали сообщение
		return

	from_id = cerebro.core.current_task().id()
	cur_task = db.task(from_id) # Current task
	if cur_task[pycerebro.dbtypes.TASK_DATA_PARENT_ID] <= 0:
		cerebro.gui.information_box('Cerebro Python API', 'Задача уже на самом верхнем уровне')

	parent_task = db.task(cur_task[pycerebro.dbtypes.TASK_DATA_PARENT_ID]) # Current task
	to_id = parent_task[pycerebro.dbtypes.TASK_DATA_PARENT_ID]
	if to_id <= 0:
		cerebro.gui.information_box('Cerebro Python API', 'Задача уже на самом верхнем уровне')
		return
	
	db.execute('select * from "taskRelinkMulti"(%s, %s)', [from_id], to_id)

	cerebro.core.refresh_tasks()
	cerebro.core.set_current_task(from_id)

	cerebro.gui.information_box('Cerebro Python API', 'Новый путь: ' + cerebro.core.current_task().parent_url())