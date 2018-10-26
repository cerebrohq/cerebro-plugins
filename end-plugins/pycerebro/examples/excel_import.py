# -*- coding: utf-8 -*-

"""
Пример импорта задач из Excel.

Этот пример демонстрирует импорт задач и свойств задач из Excel.

Для чтения файлов Excel используется сторонний пакет xlrd (https://pypi.python.org/pypi/xlrd)
Для работы с временными зонами используются сторонние пакеты pytz (https://pypi.python.org/pypi/pytz/) и tzlocal (https://pypi.python.org/pypi/tzlocal)

В модуле используются следующие функции:

do_import - Функция импорта. Принимает параметры: Имя пользователя, Пароль пользователя, Путь до задачи, Путь к файлу Excel.
read - Функция, которая записывает свойства задачи и всех вложенных задач из Excel в Cerebro.
connect_db - Функция для соединения с базой данных Cerebro.
write_info, write_error - Функции для логирования.

Пример использования:

do_import('Имя_пользователя', 'Пароль_пользователя', '/Путь/к/Задаче', 'C:/путь/к/файлу.xlsx')

"""

# Имена колонок Excel
columns =		{1: "Описание",	2: "Назначено", 3: "Начало",	4: "Окончание", 5: "Запланировано"}

# Индекс колонки с именем задачи
name_column = 0
# Пропуск 1 строки заголовка
skeep_first_rows = 1
# Разделитель имен задач
tasks_delimeter = '/'

import sys
import os

local_dir = os.path.realpath(__file__).replace('\\', '/').rsplit('/', 1)[0]
backend_dir = local_dir + '/../..'
sys.path.append(backend_dir)

import xlrd
from pycerebro import database, dbtypes
import datetime
import pytz
import tzlocal

def do_import(db_user, db_password, task, file_name):
	"""
	Функция импорта.

	Параметры db_user и db_password - логин и пароль пользователя Cerebro.

	task - тектовый локатор(путь) до задачи, в которую выполняется импорт.

	Формат локатора: '/Проект/Задача 1/Задача 2', то есть по сути путь до задачи.
	Примечание: Имена задач регистрозависимы!

	Пример вызова функции:
	::
		import excel_import

		excel_import.do_import('user', 'password', '/Проект/Задача 1/Задача 2', 'c:/temp/import.xlsx')
	::
	"""
	# Устанавливаем соединение с базой данных
	db = connect_db(db_user, db_password)

	if (db):
		# Открываем файл Excel
		rb = xlrd.open_workbook(file_name)
		if (rb):
			# получаем первый лист
			sheet = rb.sheet_by_index(0)

		if (sheet):
			# Получаем идентификатор задачи (проекта) в которую осуществляется импорт
			task_id = db.task_by_url(task)[0]

			if (task_id):
				read(db, task_id, sheet)
			else:
				write_error('Task (Project) not found')

			write_info('Import finished!')
	else:
		write_error('Can not connect to db: ' + host)

def read(db, task_id, sheet):
	"""
	Функция для чтения данных из Excel и записи данных в Cerebro.

	db - переменная для работы с базой данных.
	task_id - идентификатор задачи.
	sheet - лист Excel.
	"""

	# Получили дату отсчета
	datetime_2000 = datetime.datetime(2000, 1, 1, tzinfo=pytz.utc)

	# Построчно читаем файл
	for rownum in range(sheet.nrows):
		# Пропускаем строку заголовка
		if (rownum +1 > skeep_first_rows):
			# Получили строку
			row = sheet.row_values(rownum)

			# Получили идентификатор задачи, в которую осуществляется импорт
			new_task_id = task_get_create(db, task_id, row[name_column])
			if (new_task_id):
				for col in columns:
					if ('Описание' == columns[col]):
						# Импорт Постановки задачи
						db.add_definition(new_task_id, row[col])
					elif ('Назначено' == columns[col]):
						# Импорт пользователей, нанзаченных на задачу
						alloc_ids = set()
						# Получили список имен пользователей
						user_names = row[col].split('; ')

						for user in db.users():
							# Если пользователь найден в списке пользователей Cerebro, то добавляем его идентификатор в список
							if user[dbtypes.USER_DATA_FULL_NAME] in user_names:
								alloc_ids.add(user[dbtypes.USER_DATA_ID])

						# Назначаем пользователей на задачу
						if (alloc_ids):
							db.task_set_allocated(new_task_id, alloc_ids)
					elif ('Начало' == columns[col]):
						# Импорт даты старта задачи
						if (row[col]):
							# Получаем количество дней от даты отсчета, подробнее в описании функции task_set_start
							date = datetime.datetime.strptime(row[col], '%d.%m.%y %H:%M')
							localtz = tzlocal.get_localzone()
							utcdate = localtz.localize(date)
							timedelta = utcdate - datetime_2000
							days = timedelta.total_seconds()/(24*60*60)

							# Устанавливаем дату старта задачи
							db.task_set_start(new_task_id,  days)
					elif ('Окончание' == columns[col]):
						# Импорт даты окончания
						if (row[col]):
							# Получаем количество дней от даты отсчета, подробнее в описании функции task_set_start
							date = datetime.datetime.strptime(row[col], '%d.%m.%y %H:%M')
							localtz = tzlocal.get_localzone()
							utcdate = localtz.localize(date)
							timedelta = utcdate - datetime_2000
							days = timedelta.total_seconds()/(24*60*60)

							# Устанавливаем дату окончания
							db.task_set_finish(new_task_id,  days)
					elif ('Запланировано' == columns[col]):
						# Импорт запланированных часов
						if (row[col]):
							db.task_set_planned_time(new_task_id, row[col])
						else:
							db.task_set_planned_time(new_task_id, 0.016)

def task_get_create(db, parent_task_id, name):
	"""
	Функция для создания задачи по локатору.
	Если задача существует, то функция вернет идентификатор задачи.

	db - переменная для работы с базой данных.
	parent_task_id - идентификатор задачи, в которой будет создана новая задача.
	name - текстовый локатор задачи.
	"""
	task_id = None
	# Формируем полный путь до задачи
	path = str(db.task(parent_task_id)[dbtypes.TASK_DATA_PARENT_URL]) + str(db.task(parent_task_id)[dbtypes.TASK_DATA_NAME]) + '/' + name

	# Пытаемся получить id задачи
	task_id = db.task_by_url(path)[0]

	if (not task_id):
		# Если задача не существует, создаем ее
		if (name.find(tasks_delimeter) != -1):
			# Получаем список имен задач
			spl_name = name.split(tasks_delimeter)
			t_id = parent_task_id

			# Создаем дерево задач
			for nm in spl_name:
				if (nm):
					t_id = task_get_create(db, t_id, nm)

			# Если хотябы одна задача создана, присваиваем возвращаемой переменной ее идентификатор
			if (t_id != parent_task_id):
				task_id = t_id
		else:
			task_id = db.add_task(parent_task_id, name)
	
	return task_id

def connect_db(user, password):
	"""
	Функция для соединения с базой данных.

	user - имя пользователя cerebro.
	password - пароль пользователя cerebro.
	"""
	# Создаем объект базы данных
	db = database.Database()
	# Соединяемся с базой данных
	db.connect(user, password)

	return db

def write_info(text):
	"""
	Функция для логирования информационных сообщений.

	text - текст сообщения.
	"""
	print('info: ' + text)

def write_error(text):
	"""
	Функция для логирования ошибок.

	text - текст сообщения.
	"""
	print('error: ' + text)
