# -*- coding: utf-8 -*-

"""
Пример экспорта задачи(проекта) со всеми вложенными задачами в Excel.

Этот пример демонстрирует экспорт свойств задачи в Excel.

Для записи в формат Excel используется сторонний пакет xlsxwriter (https://xlsxwriter.readthedocs.org/)
Для праобразования текста в формате html используется сторонний пакет html2text (http://www.aaronsw.com/2002/html2text/).

В модуле используются следующие функции:

do_export - Функция экспорта. Принимает параметры: Имя пользователя, Пароль пользователя, Путь до задачи, Путь к файлу Excel.
write - Функция, которая записывает свойства задачи и всех вложенных задач в файл Excel.
connect_db - Функция для соединения с базой данных Cerebro.
write_info, write_error - Функции для логирования.

Пример использования:

do_export('Имя_пользователя', 'Пароль_пользователя', '/Путь/к/Задаче', 'C:/путь/к/файлу.xlsx')

"""

# Следующие два параметра, хост и порт - это наш главный сервер с базой данных.
# У вас эти параметры могут быть иными, если вы используете свою базу данных
host = 'db.cerebrohq.com'
port = 45432

# Имена колонок Excel
columns =		{ 0: "Задача",	1: "Описание",	2: "Назначено", 3: "Начало",	4: "Окончание", 5: "Запланировано"}
# Ширина колонок
columns_w =		{ 0: 50,		1: 50,			2: 10,			3: 10,			4: 10,			5: 15}
# Высота строк
row_h = 50

import xlsxwriter
from py_cerebro import database, dbtypes
import html2text
import datetime

def do_export(db_user, db_password, task, file_name):
	"""
	Функция экспорта.

	Параметры db_user и db_password - логин и пароль пользователя Cerebro.

	task - тектовый локатор(путь) до задачи.

	Формат локатора: '/Проект/Задача 1/Задача 2', то есть по сути путь до задачи.
	Примечание: Имена задач регистрозависимы!

	Пример вызова функции:
	::
		import excel_export

		excel_export.do_export('user', 'password', '/Проект/Задача 1/Задача 2', 'c:/temp/export.xlsx')
	::
	"""
	# Устанавливаем соединение с базой данных
	db = connect_db(db_user, db_password)

	if (db):
		write_info('Connected to db: ' + host)
		# Создаем файл Excel
		wb = xlsxwriter.Workbook(file_name)
		if (wb):
			# Добавляем лист
			ws = wb.add_worksheet()

		if (ws):
			# Создаем формат для заголовка
			format = wb.add_format()
			format.set_bold(True) # Жирный шрифт
			format.set_align('center_across') # По центру
			for col in columns:
				# Задаем ширину колонок
				ws.set_column(col, col, columns_w[col])
				# Создаем Заголовок
				ws.write(0, col, columns[col], format)

			# Получаем идентификатор задачи (проекта)
			task_id = db.task_by_url(task)[0]

			if (task_id):
				write(db, task_id, ws, wb.add_format())

			write_info('Export finished!')
	else:
		write_error('Can not connect to db: ' + host)

_i = 0

def write(db, task_id, ws, format):
	"""
	Функция для записи свойств задачи и вложенных задач в файл Excel.

	db - переменная для работы с базой данных.
	task_id - идентификатор задачи.
	ws - лист Excel.
	format - переменная форматирования рабочей кники Excel.
	"""
	global _i
	_i += 1

	# Создадим формат для выравнивания по верхней границы ячейки и переноса по словам
	format_top_text_wrap = format
	format_top_text_wrap.set_align('top')
	format_top_text_wrap.set_text_wrap()

	# Устанавливаем высоту строки
	ws.set_row(_i, row_h)

	# Получаем задачу по идентификатору
	task = db.task(task_id)
	# Получаем постановку задачи
	task_def = db.task_definition(task_id)

	# Получаем полный путь к задаче
	name = task[dbtypes.TASK_DATA_PARENT_URL] + task[dbtypes.TASK_DATA_NAME]
	# Записываем полный путь к задаче
	ws.write(_i, 0, name, format_top_text_wrap)

	# Если у задачи есть "Постановка задачи" записываем ее в файл
	if (task_def):
		ws.write(_i, 1, html2text.html2text(task_def[dbtypes.MESSAGE_DATA_TEXT]), format_top_text_wrap)

	# Получаем список пользователей, назначенных на задачу
	user_name = task[dbtypes.TASK_DATA_ALLOCATED]

	# Если есть назначенные на задачу пользователи, сохраняем их в файл
	if (user_name):
		ws.write(_i, 2, user_name, format_top_text_wrap)

	# Получаем начальную дату отсчета
	datetime_2000 = datetime.datetime(2000, 1, 1)

	# Получаем дату старта задачи
	datetime_start = datetime_2000 + datetime.timedelta(task[dbtypes.TASK_DATA_OFFSET])

	# Сохраняем дату старта в файл
	ws.write(_i, 3, datetime_start.strftime('%d.%m.%y %H:%M'), format_top_text_wrap)

	# Получаем дату окончания задачи
	datetime_stop = datetime_start + datetime.timedelta(task[dbtypes.TASK_DATA_DURATION])

	# Сохраняем дату окончания в файл
	ws.write(_i, 4, datetime_stop.strftime('%d.%m.%y %H:%M'), format_top_text_wrap)

	# Сохраняем запланированное время
	ws.write(_i, 5, task[dbtypes.TASK_DATA_PLANNED], format_top_text_wrap)
	
	# Если у задачи есть вложенные задачи, так-же сохраняем их в файл
	for child in db.task_children(task_id):
		write(db, child[dbtypes.TASK_DATA_ID], ws, format)

def connect_db(user, password):
	"""
	Функция для соединения с базой данных.

	user - имя пользователя cerebro.
	password - пароль пользователя cerebro.
	"""
	# Создаем объект базы данных
	db = database.Database(host, port)
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
