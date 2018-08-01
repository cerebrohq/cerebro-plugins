# -*- coding: utf-8 -*-

"""
Примеры создания задач.
Этот модуль демонстритует, как можно устанавливать соединение с базой данных,
создавать задачи и связывать их между собой без использования графического интерфейса Cerebro.
Также в модуле продемонстрировано создание сообшений и прикладывание к ним файлов.

Модуль использует пакет py_cerebro (для Python 3.x), который входит в дистрибутив service-tools (http://cerebrohq.com/distribs/service-tools.zip).
Пакет py_cerebro содержит модули для установки соединения с базой данных
и для доступа к файловому хранилищу(Cargador).
Пакет py_cerebro использует сторонний пакет psycopg2 (http://initd.org/psycopg/) 
для осущевстления доступа к базе данных PostgreSQL. Возможно вам придется дополнительно установить этот пакет.
Psycopg2 поставляется в дистрибутиве для всех операционных систем (папка py-site-packages). Также его можно
скачать с сайта разработчика (http://initd.org/psycopg/).

Модуль содержит функции:

create_and_link_tasks - пример создания задач и установления между ними связей.
make_thumnails - для генерации эскизов к видео файлам и изображениям
"""

import fnmatch
import sys
import os
import subprocess
import datetime

local_dir = os.path.realpath(__file__).replace('\\', '/').rsplit('/', 1)[0]
backend_dir = local_dir + '/../..'
sys.path.append(backend_dir)

import py_cerebro
from py_cerebro import dbtypes # в этом модуле описаны различные константы, такие как поля данных, флаги и т.п.


# Переменные, которые вам возможно придется изменить, чтобы преспособить скpипт для вашей сети

#Следующие два параметра, хост и порт - это наш главный сервер с базой данных.
#У вас эти параметры могут быть иными, если вы используете свою базу данных
database_host = 'cerebrohq.com'
database_port = 45432

cargador_host = 'ss' # Cетевой адрес машины, где работает севрис каргадор.
# Может быть задано сетевое имя или IP адрес. 'ss' - это имя нашего сервера, у вас этот параметр скорее всего будет иным.

cargador_xmlrpc_port = 4040 # Порт 4040 - это порт для запросов по xmlrpc протоколу.
#У вас порт может быть иным, подробнее об этом смотрите в комментариях модуля cargador пакета py_cerebro.

cargador_http_port = 4080 # Порт 4080 - это порт для запросов по http протоколу.
#У вас порт может быть иным, подробнее об этом смотрите в комментариях модуля cargador пакета py_cerebro.

project_name = 'Test project' # Имя проекта для тестового добавления задач. 
#Вы можете выбрать любой свой проект

mirada_path = '//ss/front/cerebro/mirada.exe' # Путь, откуда запускать мираду для генерации эскизов.
#У вас этот параметр скорее всего будет иным. Подробнее смотрите в функции

def create_and_link_tasks(db_user,  db_password):
	"""
	db_user и  db_password это логин и пароль пользователя Cerebro
	
	В этом примере мы создадим в проекте задачу и две подзадачи. 
	У задачи выставим время начала, у подзадач запланируем время исполнения и свяжем их между собой.
	Также мы создадим у подзадач сообщения типа постановка задачи и приложим к ним файлы.
	Мы не будем в этом примере самостоятельно писать sql-запросы, а воспольуемся функцями класса database.Database,
	которые по сути являются обертками над sql-запросами. 
	Описание всех функций смотрите в модуле database пакета py_cerebro.
		
	Пример вызова функции:
	::
		import create_tasks

		create_tasks.create_and_link_tasks('user', 'password')
	::
	"""
	
	def find(f, seq):
		# поиск объектов в списке
		for item in seq:
			if f(item): 
				return item

	try:

		db = py_cerebro.database.Database(database_host, database_port)
		# Устанавливаем соединение с базой данных
		if db.connect_from_cerebro_client() != 0: # пробуем установить соединение с помощью запущенного клиента Cerebro. 
			# Если не выходит, устанавливаем с помощью логина и пароля
			db.connect(db_user, db_password) 
		
		root_tasks = db.root_tasks() # Получаем список корневых задач проектов.
		
		# Ищем нужную корневую задачу проекта в который и будем добовлять задачи
		root_task = find(lambda val: val[dbtypes.TASK_DATA_NAME]  == project_name,  root_tasks)
		
		# Создаем задачу в проекте
		new_task_id = db.add_task(root_task[dbtypes.TASK_DATA_ID],  'New Test Task')
		"""
		Функция add_task принимает на вход два агрумента:
		- идентификатор родительской задачи, в данном случаи идентификатор корневой задачи проекта 
		- имя задачи, Будте внимательны имя задачи имеет ограничения. 
		Подробнее о них смотрите в описании функции add_task.
		
		Результат функции - идентификатор новой задачи.
		"""		
		
		# Устанавливаем время начала задачи в теушее время
		"""
		Время начала задачи устанавливается в днях от 01.01.2000 в UTC
		Подробнее о этом смотрите в описании функции task_set_start.
		"""
		
		datetime_now = datetime.datetime.utcnow()
		datetime_2000 = datetime.datetime(2000, 1, 1)
		timedelta = datetime_now - datetime_2000
		days = timedelta.total_seconds()/(24*60*60)
		
		db.task_set_start(new_task_id,  days)
		
		# Создаем две подзадачи к новой задаче
		new_subtask_id_1 = db.add_task(new_task_id,  'New Test Subtask 1')
		new_subtask_id_2 = db.add_task(new_task_id,  'New Test Subtask 2')
		
		# Добовляем к подзадачам постановки задач с файлами
		def_id_1 = db.add_definition(new_subtask_id_1, 'Do something 1')
		def_id_2 = db.add_definition(new_subtask_id_2, 'Do something 2')

		# Во второй подзадаче создадим еще 5 задач.
		# Для удобства просто создадим 5 копий подзадачи 1
		lst_for_copy = [(new_subtask_id_1, 'Subtask 1'), 
			(new_subtask_id_1, 'Subtask 2'),
			(new_subtask_id_1, 'Subtask 3'),
			(new_subtask_id_1, 'Subtask 4'),
			(new_subtask_id_1, 'Subtask 5'),] # Создадим массив типа [(ID_копируемой задачи, 'Новое имя'), ...]
		new_tasks = db.copy_tasks(new_subtask_id_2, lst_for_copy) # Копируем в подзадачу 2
		
		filename1 = local_dir + '/test.png' # файл для первой подзадачи
		thumbnails1 = make_thumnails(filename1) # генерация эскизов для файла filename1
		filename2 = local_dir + '/test.mp4' # файл для второй подзадачи
		thumbnails2 = make_thumnails(filename2) # генерация эскизов файла filename2
		
		# Создаем объект для добавления файлов в файловое хранилище (Cargador)
		carga = py_cerebro.cargador.Cargador(cargador_host, cargador_xmlrpc_port,  cargador_http_port)
		
		# Добовляем к сообщениям типа постановки задач файлы и, заодно, экспортируем их в хранилище
		db.add_attachment(def_id_1,  carga,  filename1, thumbnails1,  '',  False)		
		db.add_attachment(def_id_2,  carga,  filename2, thumbnails2,  '',  False)
		"""
			Параметр carga, передается для экспортирования файла в файловое хранилише.
			Подробнее об этом смотрите в модуле cargador.
			
			Последний параметр означает, будет ли файл добавлен как линк, без экспорта в хранилище (значение True),
			или же он будет экспортитован (значение False)
			Подробнее об этом смотрите в описании функции add_attachment.
		"""		
		
		# Удаляем сгенерированные эскизы, поскольку мы их уже экспортировали в хранилище
		for f in thumbnails1:
			os.remove(f)
		
		for f in thumbnails2:
			os.remove(f)
			
		
		# Устанавливаем запланированное время на подзадачи
		db.task_set_planned_time(new_subtask_id_1,  12.5) # первой подзадаче устанавливаем 12 с половиной часов
		db.task_set_planned_time(new_subtask_id_2,  30) # второй подзадаче устанавливаем 30 часов
		
		# Связываем подзадачи
		db.set_link_tasks(new_subtask_id_1, new_subtask_id_2)
		"""
		Эта связь значит, что вторая подзадача начнется после окончания первой подзадачи
		"""
		
	except Exception as err:
		print(err)


def make_thumnails(filename):
	"""
	Принимает на вход полный путь до файла видео или изображения и генерирует эскизы к ним
	:returns: список путей до файлов эскизов.	

	Пример вызова функции:
	::	
		import create_tasks

		filename = 'c:/temp/file.mov'
		thumbnails = create_tasks.create_and_link_tasks(filename)		
	::
	
	Генерация эскизов:			
	Если файл является изображением или видео, то можно добавить для него уменшенные эскизы.
	Можно добавить до 3-х эскизов (первый, средний, последний кадры).
	Для генерации эскизов можно использовать программу Mirada.
	Она постовляется вместе с дистрибутивом Cerebro. Можно использовать и другие программы для генерации,
	например, ffmpeg.
	"""
	
	#Пример генерации эскизов с помощью Mirada.	

	if os.path.exists(filename) == False or os.path.exists(mirada_path) == False:
		return list()
	
	gen_path = os.path.dirname(filename) # В качестве директории для генерации эскизов возьмем директорию добавляемого файла

	# Запускаем мираду с необходимыми ключами
	res_code = subprocess.call([mirada_path, filename, '-temp', gen_path, '-hide'])				
	#-temp - директория для генерации эскизов
	#-hide - ключ запуска мирады в скрытом режиме (без загрузки графического интерфейса) для генерации табнейлов.
	
	if res_code != 0:
		raise Exception("Mirada returned bad exit-status.\n" + mirada_path)
	
	#Ищем сгенерированные мирадой эскизы.
	#Имени эскиза формируется из имени файла, даты и времени генерации - filename_yyyymmdd_hhmmss_thumb[number].jpg
	#Например: test.mov_20120305_112354_thumb1.jpg - первый эскиз видео-файла test.mov
	
	thumbnails = list()
	for f in os.listdir(gen_path):
		if fnmatch.fnmatch(f, os.path.basename(filename) + '_*_thumb?.jpg'):
			thumbnails.append(gen_path + '/' + f)

	thumbnails.sort()	
	
	"""
	#Пример генерации эскизов с помощью ffmpeg.
	
	#Для того, чтобы генерить эскизы с помощью ffmpeg, нужно заранее знать длительность видео,
	#чтобы корректно получить средний и последний кадры.
	#Возьмем к примеру ролик длительностью в 30 секунд.

	thumbnails = list() # список файлов для эскизов
	thumbnails.append(filename + '_thumb1.jpg')
	thumbnails.append(filename + '_thumb2.jpg')
	thumbnails.append(filename + '_thumb3.jpg')

	subprocess.call(['ffmpeg', '-i', filename, '-s', '512x512', '-an', '-ss', '00:00:00', '-r', 1, '-vframes', 1, '-y', thumbnails[0]])
	subprocess.call(['ffmpeg', '-i', filename, '-s', '512x512', '-an', '-ss', '15:00:00', '-r', 1, '-vframes', 1, '-y', thumbnails[1]])
	subprocess.call(['ffmpeg', '-i', filename, '-s', '512x512', '-an', '-ss', '30:00:00', '-r', 1, '-vframes', 1, '-y', thumbnails[2]])
	# Описание ключей вы можете посмотреть в документации к ffmpeg
	"""
	
	return thumbnails
