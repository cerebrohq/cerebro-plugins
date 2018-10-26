# -*- coding: utf-8 -*-

import os
import re
import socket
import struct
from .cclib import *
from .dbtypes import *
import collections
import time
import requests, json, iso8601, datetime

# PostgreSQL types
TYPES_INT		= {'integer', 'serial', 'smallint', 'int4', 'int2', 'int8'}
TYPES_FLOAT		= {'numeric', 'decimal', 'real', 'double precision', 'float4', 'float8'}
TYPES_DATETIME	= {'timestamptz'}

# Main connection server url
DEFAULT_URL = 'https://cerebrohq.com/dapi/rpc.php'

# PostgreSQL error codes that require another try
RECONNECT_ERROR_CODES = {'08000', '08003', '08006', '08001', '08004', '08007', '08P01'}

def json_serial(obj):
	"""
	json serializer for unsupported by default types.
	"""

	if isinstance(obj, (datetime.datetime, datetime.date)):
		return obj.isoformat()
	elif isinstance(obj, set):
		return list(obj)

	raise TypeError("Type %s is not JSON serializable" % type(obj))

def to_array(obj):
	"""
	Make sure argument is of array-like type.
	"""

	return obj if isinstance(obj, (set, list, tuple)) else [obj]

class Database():
	"""
	:param string db_host: host name.
	:param int db_port: port.
	:param int db_timeout: disconnect timeout (seconds).
	:param int db_reconn_count: reconnect counts.

	The Database class is used for connection to the database,
	it contains a set of methods, executing Cerebro standard queries,
	and enables custom SQL queries.
	
	::

		# Устанавливаем соединение с базой данных

		if db.connect_from_cerebro_client() != 0: # Пробуем установить соединение с помощью запущенного клиента Cerebro.
			# Если не выходит, устанавливаем соединение с помощью логина и пароля
			db.connect('user', 'password')

	.. note:: В классе существуют функции изменяющие свойства задач, которые могут принимать на вход массив
		идентификаторов. Если необходимо установить нескольким задачам одинаковое значение свойства, предпочитайте
		использовать передачу массива идентификаторов в качестве аргумента вместо использования циклов. Это значительно
		повысит производительность.

	::

		# Использование массивов идентификаторов

		to_do_task_list = db.to_do_task_list(db.current_user_id(),  True) # получаем список задач текущего пользователя

		tsks = set()

		for task in to_do_task_list:
			tsks.add(task[dbtypes.TASK_DATA_ID])

		db.task_set_priority(tsks, 
			dbtypes.TASK_PRIORITY_ABOVE_NORMAL) # установили сразу нескольким задачам приоритет выше обычного

	.. rubric:: Methods

	* :py:meth:`activities()                     <py_cerebro.database.Database.activities>`
	* :py:meth:`add_attachment()                 <py_cerebro.database.Database.add_attachment>`
	* :py:meth:`add_client_review()              <py_cerebro.database.Database.add_client_review>`
	* :py:meth:`add_definition()                 <py_cerebro.database.Database.add_definition>`
	* :py:meth:`add_note()                       <py_cerebro.database.Database.add_note>`
	* :py:meth:`add_report()                     <py_cerebro.database.Database.add_report>`
	* :py:meth:`add_resource_report()            <py_cerebro.database.Database.add_resource_report>`
	* :py:meth:`add_review()                     <py_cerebro.database.Database.add_review>`
	* :py:meth:`add_task()                       <py_cerebro.database.Database.add_task>`
	* :py:meth:`attachment_hashtags()                  <py_cerebro.database.Database.attachment_hashtags>`
	* :py:meth:`attachment_remove_hashtags()                  <py_cerebro.database.Database.attachment_remove_hashtags>`
	* :py:meth:`attachment_set_hashtags()                  <py_cerebro.database.Database.attachment_set_hashtags>`
	* :py:meth:`connect()                        <py_cerebro.database.Database.connect>`
	* :py:meth:`connect_from_cerebro_client()    <py_cerebro.database.Database.connect_from_cerebro_client>`
	* :py:meth:`copy_tasks()					 <py_cerebro.database.Database.copy_tasks>`
	* :py:meth:`current_user_id()                <py_cerebro.database.Database.current_user_id>`
	* :py:meth:`drop_link_tasks()                <py_cerebro.database.Database.drop_link_tasks>`
	* :py:meth:`execute()                        <py_cerebro.database.Database.execute>`
	* :py:meth:`message()                        <py_cerebro.database.Database.message>`
	* :py:meth:`message_attachments()            <py_cerebro.database.Database.message_attachments>`
	* :py:meth:`message_hashtags()                  <py_cerebro.database.Database.message_hashtags>`
	* :py:meth:`message_remove_hashtags()                  <py_cerebro.database.Database.message_remove_hashtags>`
	* :py:meth:`message_set_hashtags()                  <py_cerebro.database.Database.message_set_hashtags>`
	* :py:meth:`messages()                        <py_cerebro.database.Database.messages>`
	* :py:meth:`project_tags() 					<py_cerebro.database.Database.project_tags>`
	* :py:meth:`root_tasks()                     <py_cerebro.database.Database.root_tasks>`
	* :py:meth:`set_link_tasks()                 <py_cerebro.database.Database.set_link_tasks>`
	* :py:meth:`statuses()                		<py_cerebro.database.Database.statuses>`
	* :py:meth:`tag_enums()                		<py_cerebro.database.Database.tag_enums>`
	* :py:meth:`task()                           <py_cerebro.database.Database.task>`
	* :py:meth:`task_allocated()                 <py_cerebro.database.Database.task_allocated>`
	* :py:meth:`task_attachments()                 <py_cerebro.database.Database.task_attachments>`
	* :py:meth:`task_by_url()                 <py_cerebro.database.Database.task_by_url>`
	* :py:meth:`task_children()                  <py_cerebro.database.Database.task_children>`
	* :py:meth:`task_definition()                <py_cerebro.database.Database.task_definition>`
	* :py:meth:`task_hashtags()                  <py_cerebro.database.Database.task_hashtags>`
	* :py:meth:`task_links()                     <py_cerebro.database.Database.task_links>`
	* :py:meth:`task_messages()                  <py_cerebro.database.Database.task_messages>`
	* :py:meth:`task_possible_statuses() 	<py_cerebro.database.Database.task_possible_statuses>`
	* :py:meth:`task_remove_allocated()          <py_cerebro.database.Database.task_remove_allocated>`
	* :py:meth:`task_remove_hashtags()                  <py_cerebro.database.Database.task_remove_hashtags>`
	* :py:meth:`task_set_activity()              <py_cerebro.database.Database.task_set_activity>`
	* :py:meth:`task_set_allocated()             <py_cerebro.database.Database.task_set_allocated>`
	* :py:meth:`task_set_budget()                <py_cerebro.database.Database.task_set_budget>`
	* :py:meth:`task_set_finish()                <py_cerebro.database.Database.task_set_finish>`
	* :py:meth:`task_set_flag()                  <py_cerebro.database.Database.task_set_flag>`
	* :py:meth:`task_set_hashtags()                  <py_cerebro.database.Database.task_set_hashtags>`
	* :py:meth:`task_set_name()                  <py_cerebro.database.Database.task_set_name>`
	* :py:meth:`task_set_planned_time()          <py_cerebro.database.Database.task_set_planned_time>`
	* :py:meth:`task_set_priority()              <py_cerebro.database.Database.task_set_priority>`
	* :py:meth:`task_set_progress()              <py_cerebro.database.Database.task_set_progress>`
	* :py:meth:`task_set_start()                 <py_cerebro.database.Database.task_set_start>`
	* :py:meth:`task_set_status()                <py_cerebro.database.Database.task_set_status>`	
	* :py:meth:`task_set_tag_enum()                <py_cerebro.database.Database.task_set_tag_enum>`	
	* :py:meth:`task_set_tag_float()                <py_cerebro.database.Database.task_set_tag_float>`
	* :py:meth:`task_set_tag_int()                <py_cerebro.database.Database.task_set_tag_int>`
	* :py:meth:`task_set_tag_string()                <py_cerebro.database.Database.task_set_tag_string>`
	* :py:meth:`task_tag_enums()                		<py_cerebro.database.Database.task_tag_enums>`
	* :py:meth:`task_tag_reset()                		<py_cerebro.database.Database.task_tag_reset>`
	* :py:meth:`task_tags()                		<py_cerebro.database.Database.task_tags>`
	* :py:meth:`tasks()                           <py_cerebro.database.Database.tasks>`
	* :py:meth:`to_do_task_list()                <py_cerebro.database.Database.to_do_task_list>`
	* :py:meth:`users()                          <py_cerebro.database.Database.users>`
	"""

	def __init__(self, db_host = '', db_port = None, db_timeout = 10, db_reconn_count = 3):
		"""
		:param string db_host: host name.
		:param int db_port: port.
		:param int db_timeout: disconnect timeout (seconds).
		:param int db_reconn_count: reconnect counts.

		Constructor.

		Example::

			db = database.Database('cerebrohq.com', 45432)
		"""

		self.db_timeout = db_timeout
		self.db_reconn_count = db_reconn_count
		self.is_connected_by_client = False

		self.disconnect()

	def is_connected(self):
		"""
		Returns True if current connection is active.
		"""

		return self.sid != -1

	def disconnect(self):
		"""
		Force drop current connection settings.
		"""

		self.sid = -1
		self.query_id = 1
		self.db_url_primary = None
		self.db_url_secondary = None
		
	def connect(self, db_user, db_password, primary_url='', secondary_url=''):
		"""
		Connection and authentification.
		"""

		direct_connection = True
		if primary_url is None or len(primary_url) == 0:
			direct_connection = False
			primary_url = DEFAULT_URL
		
		self.is_connected_by_client = False
		self.db_user = db_user
		self.db_password = db_password

		header = {
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Accept': 'application/json-rpc',
			'Cache-Control': 'no-store'
		}
		payload = {
			'method': 'sessionDirectStart' if direct_connection else 'sessionStart',
			'jsonrpc': '2.0',
			'params': [self.db_user, self.db_password, 0],
			'id': self.query_id
		}

		# Check url format
		connect_url = "{0}{1}{2}".format("" if primary_url.startswith("http") else "http://", primary_url, "" if primary_url.endswith(".php") else "/rpc.php")

		res = None
		error_msg = ""
		for i in range(self.db_reconn_count):
			try:
				response = requests.post(connect_url, headers=header, data=json.dumps(payload, default=json_serial), timeout=30)
				self.query_id += 1
				if response.status_code == 200:
					res = json.loads(response.text)
					err = res.get("error", None)
					if err is None: break
					# Internal server error occured
					res = None
					error_msg = "{0} : {1}".format(err["code"], err["message"])
				else:
					# Http request error occured
					error_msg = "{0} : {1}".format(response.status_code, response.reason)
			except:
				pass

		if res is not None:
			if len(res.get("result", [])) == 0:
				raise Exception('Login is invalid')

			self.sid = int(res["result"][0]["token"])
			#self.db_url_primary = res["result"][len(res["result"]) - 1]["server"]["instances"][0]["addr_jrpc"] + u"/rpc.php"
			if direct_connection:
				self.db_url_primary = self.db_url_secondary = connect_url
			else:
				self.db_url_primary = self.db_url_secondary = res["result"][0]["server"]["primary_server"]["addr_jrpc"] + u"/rpc.php"
		else:
			raise Exception('Connection error: {0}'.format(error_msg))

	def connect_from_cerebro_client(self):
		"""
		Previously authentificated Cerebro user connects to the database.
		Such a connection may be established if the user has logged in Cerebro on the same workstation.
		Unlike the usual :py:func:`Database.connect()<py_cerebro.Database.connect>` which may close the
		concurrent Cerebro client connection (if connected with the same credentials) this function will
		leave the Cerebro client connection alive.
		
		:returns:
		    connection status:
			* 0 - connection established;
			* 1 - connection not established (Cerebro client application is running, but user is not logged in);
			* 2 - connection not established (Cerebro client application is not running).
		
		::
		
			# Establishing connection with the database
			if db.connect_from_cerebro_client() != 0: # Attempting to connect via Cerebro client application. 
				# If failed, connecting with login and password
				db.connect(db_user, db_password)
		
		.. seealso:: :py:meth:`connect() <py_cerebro.database.Database.connect>`.
		"""

		status = 2
		self.is_connected_by_client = True
		try:
			cerebro_port = 51051
			conn = socket.create_connection(('127.0.0.1',  cerebro_port),)

			proto_version = 3
			packet_type = 6

			msg = struct.pack('II',  proto_version,  packet_type)
			header = struct.pack('II', 0xEEEEFF01, len(msg))

			conn.send(header+msg)
			data = conn.recv(1024)

			res = struct.unpack_from('IIQI{0}s'.format(len(data) - 20),  data, 0)
			if res[0] == 0xEEEEFF01:
				session_id = res[2]
				if session_id == 0:
					status = 1
				else:
					status = 0
					urls = json.loads(string_unicode(res[4].strip(b'\x00')))
					self.sid = session_id # устанавливаем идентификатор авторизованного пользователя.
					self.db_url_primary = urls["primary"]
					self.db_url_secondary = urls["secondary"]
					
			conn.close()
			
		except Exception as err:
			print(err)
			
		return status

	def reconnect(self):
		"""
		Try to update connection session with current authentication params.
		"""

		self.disconnect()

		if self.connect_from_cerebro_client:
			self.connect_from_cerebro_client()
		else:
			self.connect(self.db_user, self.db_password)

		return self.is_connected()

	def execute(self, query, *parameters):
		"""
		:param string query: query text.
		:param parameters: query parameters list.
		
		Executes the query and returns the result. The result has a form of a table (list pf tuples).
		"""

		return self.z_execute(False, query, *parameters)

	def z_execute(self, read_only, query, *parameters):
		"""
		:param bool read_only: check if query only reads data from DB.
		:param string query: query text.
		:param parameters: query parameters list.
		
		Executes the query and returns the result. The result has a form of a table (list pf tuples).
		"""
		
		ret = []

		if not self.is_connected() and not self.reconnect():
			raise Exception('Connection error: Reconnect attempt failed')

		args = [query.replace('%s', '?')]
		args.extend(parameters)

		header = {
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Accept': 'application/json-rpc',
			'Cache-Control': 'no-store'
		}
		payload = {
			'method': 'queryMulti',
			'jsonrpc': '2.0',
			'params': args,
			'id': self.query_id
		}
		cookies = {
			'token': str(self.sid)
		}

		res = None
		error_msg = ""
		for i in range(self.db_reconn_count):
			try:
				response = requests.post(self.db_url_secondary if read_only else self.db_url_primary, headers=header, cookies=cookies,
							 data=json.dumps(payload, default=json_serial), timeout=self.db_timeout)
				self.query_id += 1
				if response.status_code == 200:
					res = json.loads(response.text)
					err = res.get("error", None)
					if err is None: break
					# Internal server error occured
					res = None
					error_msg = "{0} : {1}".format(err["code"], err["message"])
					if err["code"] in RECONNECT_ERROR_CODES: continue
					elif err["message"].startswith("sqlmsg--") and err["message"].endswith("#0--"):
						self.reconnect()
						continue
					elif err["message"].startswith("sqlmsg--") and err["message"].endswith("#1--"):
						raise Exception(err["message"][8:-4])
					break
				else:
					# Http request error occured
					error_msg = "Connection error {0} : {1}".format(response.status_code, response.reason)
			except Exception as e:
				error_msg = str(e)

		if res is not None:	
			if len(res.get("result", [])) > 0:
				for i, row in enumerate(res["result"][0]["rows"]):
					ret.append([])
					for j, col in enumerate(row):
						type = res["result"][0]["columns"][j]["type"]
						if col is None:
							ret[i].append(col)
						elif type in TYPES_INT:
							ret[i].append(int(col))
						elif type in TYPES_FLOAT:
							ret[i].append(float(col))
						elif type in TYPES_DATETIME:
							ret[i].append(iso8601.parse_date(col))
						else:
							ret[i].append(col)
		else:
			self.disconnect()
			raise Exception(error_msg)

		return ret

	def current_user_id(self):
		"""
		:returns: the logged in user's ID.
		"""

		user_id = self.z_execute(True, 'select get_usid()')
		if len(user_id) == 1:
			return user_id[0][0]

		return None

	def root_tasks(self):
		"""
		:returns: table of root tasks.
		
		The table fields are described in the module dbtypes: :py:const:`TASK_DATA_...<py_cerebro.dbtypes.TASK_DATA_>`
				
		"""

		tasks = self.z_execute(True, 'select uid from "_task_list_00"(0,0)')

		ids = set()
		for task in tasks:
			ids.add(task[0])

		return self.z_execute(True, 'select * from "taskQuery_11"(?)',  ids)

	def to_do_task_list(self, user_id,  with_done_task):
		"""
		:returns: table of tasks the user is allocated to.
		
		:param user_id: ID of the user or array of user IDs (or of a material resource).
		:type user_id:  int, set(int, ) or list(int, )
		:param bool with_done_task: if "True", then the returned table will include completed tasks (progress = 100%) also, otherwise - with incomplete tasks only.

		The table fields are described in the module dbtypes: :py:const:`TASK_DATA_...<py_cerebro.dbtypes.TASK_DATA_>`
		"""

		tasks = self.z_execute(True, 'select uid from "taskAssigned_byUsers"(?, ?)', to_array(user_id), with_done_task)
		
		ids = set()
		for task in tasks:              
			ids.add(task[0]) 	
		
		return self.z_execute(True, 'select * from "taskQuery_11"(?)',  ids)

	def task(self,  task_id):
		"""
		:param int task_id: task ID.
		:returns: task data.
		
		The table fields are described in the module dbtypes: :py:const:`TASK_DATA_...<py_cerebro.dbtypes.TASK_DATA_>`

		.. seealso:: :py:meth:`tasks() <py_cerebro.database.Database.tasks>`.
		"""		
		
		dset = set()
		dset.add(task_id)
		task = self.z_execute(True, 'select * from "taskQuery_11"(?)', dset)
		if len(task) == 1:
			return task[0]

		return None

	def tasks(self,  task_ids):
		"""
		:param array task_ids: array of task IDs.
		:returns: tasks data.
		
		The table fields are described in the module dbtypes: :py:const:`TASK_DATA_...<py_cerebro.dbtypes.TASK_DATA_>`

		.. seealso:: :py:meth:`task() <py_cerebro.database.Database.task>`.
		"""			
		
		tasks = self.z_execute(True, 'select * from "taskQuery_11"(?)', task_ids)
		if len(tasks) > 0:
			return tasks
			
		return None

	def copy_tasks(self, task_id, tasks_list, \
				flags = COPY_TASKS_SUB_TASKS|COPY_TASKS_INTERNAL_LINKS|COPY_TASKS_TAGS|COPY_TASKS_ASSIGNED_USERS|COPY_TASKS_EVENTS):
		"""
		:param task_id: copied task ID.
		:type task_id:  int, set(int, ) or list(int, )
		:param set tasks_list: list of tuples  [(id1, name1), (id2, name2),].
		:param int flags: flags.
		:returns: IDs of new tasks.

		Copy tasks.

		Full description of flags in dbtypes: :py:const:`COPY_TASKS_...<py_cerebro.dbtypes.COPY_TASKS_>`

		If you need replicate task, you must set tasks_list as list of tuples with one task_id and different names. For example:

		[(123, 'test_task02'), (123, 'test_task03'), (123, 'test_task04'), (123, 'test_task05')]

		123 - copied task ID.
		'test_task02', 'test_task03', ... - names of new tasks.

		::

			# Копируем в задачу 0 задачи 1(2 копии), 2 и 3
			to_do_task_list = db.to_do_task_list(db.current_user_id(),  True)
			lst_copy = [(to_do_task_list[1][dbtypes.TASK_DATA_ID], 'Копия задачи 1(1)'), 
				(to_do_task_list[1][dbtypes.TASK_DATA_ID], 'Копия задачи 1(2)'), 
				(to_do_task_list[2][dbtypes.TASK_DATA_ID], 'Копия задачи 2'), 
				(to_do_task_list[3][dbtypes.TASK_DATA_ID], 'Копия задачи 3')]
			db.copy_tasks(to_do_task_list[0][dbtypes.TASK_DATA_ID], lst_copy)
			# В задачу 0 добавлено 4 новых задачи
		"""

		tids = []
		names = []

		for task_list_id, task_list_name in tasks_list:
			tids.append(task_list_id)
			names.append(task_list_name)
		tasks = self.z_execute(True, 'select "dupVTask"(?,?,?,?)',  tids, names, task_id, flags)
		
		ids = set()
		for task in tasks:              
			ids.add(task[0])

		return ids

	def task_children(self,  task_id):
		"""
		:param int task_id: task ID.
		:returns: subtasks table.
		
		The table fields are described in the module dbtypes: :py:const:`TASK_DATA_...<py_cerebro.dbtypes.TASK_DATA_>`
		"""

		tasks = self.z_execute(True, 'select uid from "_task_list_00"(?,0)',  task_id)

		ids = set()
		for task in tasks:
			ids.add(task[0])

		return self.z_execute(True, 'select * from "taskQuery_11"(?)',  ids)


	def task_allocated(self,  task_id):
		"""
		:param int task_id: task ID.
		:returns: the table of users allocated to the task.
		
		The table fields are described in the module dbtypes: :py:const:`TASK_ALLOCATED_...<py_cerebro.dbtypes.TASK_ALLOCATED_>`
		"""  

		return self.z_execute(True, 'select uid, "userNameDisplay"(uid) as name, "userGetFlags"(uid) as flags from "assignedUsersTask"(?) as uid order by name',  task_id)

	def task_attachments(self,  task_id):
		"""
		:param task_id: task ID or array of task IDs.
		:type task_id:  int, set(int, ) or list(int, )
		:returns: table of files attached to the task(s).
		
		The table fields are described in the module dbtypes: :py:const:`ATTACHMENT_DATA_...<py_cerebro.dbtypes.ATTACHMENT_DATA_>`
		
		One attachment can take 1 to 5 entries in the table.
		The attachment records are grouped by the group ID - :py:const:`ATTACHMENT_DATA_GROUP_ID<py_cerebro.dbtypes.ATTACHMENT_DATA_GROUP_ID>`.
		The records of one attachment are tagged with :py:const:`ATTACHMENT_DATA_TAG<py_cerebro.dbtypes.ATTACHMENT_DATA_TAG>`, and stand for a particular parameter of the attachment.
		
		Attachments fall into two types: a file and a link to a file. In case of file the attachment has 
		a tag :py:const:`ATTACHMENT_TAG_FILE<py_cerebro.dbtypes.ATTACHMENT_TAG_FILE>`, which contains the hash of the file on a Cargador-operated file storage.
		In case of a link, the attachment is tagged with :py:const:`ATTACHMENT_TAG_LINK<py_cerebro.dbtypes.ATTACHMENT_TAG_LINK>`.
		This entry has no hash, it contains a full path to file :py:const:`ATTACHMENT_DATA_FILE_NAME<py_cerebro.dbtypes.ATTACHMENT_DATA_FILE_NAME>` in its name field.
		The entry tagged with :py:const:`ATTACHMENT_TAG_REVIEW<py_cerebro.dbtypes.ATTACHMENT_TAG_REVIEW>` is available only if the file has a Mirada review over it.
		The entry with a thumbnail tag :py:const:`ATTACHMENT_TAG_THUMB...<py_cerebro.dbtypes.ATTACHMENT_TAG_THUMB1>`, is available only if the file is a picture or video.
		If the file is a picture, it has only one entry :py:const:`ATTACHMENT_TAG_THUMB1<py_cerebro.dbtypes.ATTACHMENT_TAG_THUMB1>`, if it is a video -- three entries.
		"""

		return self.z_execute(True, 'select * from "listAttachmentsTasks"(?, false)',  to_array(task_id))

	def task_links(self,  task_id):
		"""
		:param int task_id: task ID.
		:returns: the table of task connections with other tasks.
		
		The table fields are described in the module dbtypes: :py:const:`TASK_LINK_...<py_cerebro.dbtypes.TASK_LINK_>`
		"""	

		return self.z_execute(True, 'select * from "ggLinks_byTask"(?)',  task_id)

	def task_definition(self,  task_id):
		"""
		:param int task_id: task ID.
		:returns: data of *Definition* message type.
		
		The table fields are described in the module dbtypes: :py:const:`MESSAGE_DATA_...<py_cerebro.dbtypes.MESSAGE_DATA_>`
		"""
		
		id = self.z_execute(True, 'select "getTaskDefinitionId"(?)',  task_id)
		if (len(id) == 1  and id[0][0] != None):
			dset = set()
			dset.add(id[0][0])
			definition = self.z_execute(True, 'select * from "eventQuery_08"(?)',  dset)
			if len(definition) == 1:
				return definition[0]

		return None

	def task_messages(self,  task_id):
		"""
		:param int task_id: task ID.
		:returns: the table of messages in the task.
		
		The table fields are described in the module dbtypes: :py:const:`MESSAGE_DATA_...<py_cerebro.dbtypes.MESSAGE_DATA_>`
		The message types are described in the module dbtypes: :py:const:`MESSAGE_TYPE_...<py_cerebro.dbtypes.MESSAGE_TYPE_>`
		"""

		messs = self.z_execute(True, 'select uid from "_event_list"(?, false)',  task_id)
		ids = set()
		for mess in messs:
			ids.add(mess[0])

		return self.z_execute(True, 'select * from "eventQuery_08"(?)',  ids)

	def task_possible_statuses(self,  task_id):
		"""
		:param int task_id: task ID.
		:returns: the table of statuses, which can be set for the task.

		The table fields are described in the module dbtypes: :py:const:`STATUS_DATA_...<py_cerebro.dbtypes.STATUS_DATA_>`
		
		In the Cerebro system for each status, permissions for switching each status are set.
		In addition, each status has a flag of inheritance.
		On the task-containers you can set only the statuses that have this flag enabled.
		Therefore, the list of possible statuses depends on user rights, the current status,
		as well as the presence / lack of sub-tasks in the task.
		"""

		return self.z_execute(True, 'select * from "statusListByTask"(?)',  task_id)

	def message(self,  message_id):
		"""
		:param int message_id: message ID.
		:returns: message data.
		
		The table fields are described in the module dbtypes: :py:const:`MESSAGE_DATA_...<py_cerebro.dbtypes.MESSAGE_DATA_>`
		The message types are described in the module dbtypes: :py:const:`MESSAGE_TYPE_...<py_cerebro.dbtypes.MESSAGE_TYPE_>`
		"""

		dset = set()
		dset.add(message_id)
		mess = self.z_execute(True, 'select * from "eventQuery_08"(?)',  dset)
		if len(mess) == 1:
			return mess[0]

		return None

	def messages(self,  message_ids):
		"""
		:param array message_ids: array of message IDs.
		:returns: messages data.
		
		The table fields are described in the module dbtypes: :py:const:`MESSAGE_DATA_...<py_cerebro.dbtypes.MESSAGE_DATA_>`
		The message types are described in the module dbtypes: :py:const:`MESSAGE_TYPE_...<py_cerebro.dbtypes.MESSAGE_TYPE_>`
		"""
		
		mess = self.z_execute(True, 'select * from "eventQuery_08"(?)',  message_ids)	
		if len(mess) > 0:
			return mess	
		
		return None

	def message_attachments(self,  message_id):
		"""
		:param message_id: message ID or array of message IDs.
		:type message_id:  int, set(int, ) or list(int, )
		:returns: table of files attached to the message(s).
		
		The table fields are described in the module dbtypes: :py:const:`ATTACHMENT_DATA_...<py_cerebro.dbtypes.ATTACHMENT_DATA_>`
		
		One attachment can take 1 to 5 entries in the table.
		The attachment records are grouped by the group ID - :py:const:`ATTACHMENT_DATA_GROUP_ID<py_cerebro.dbtypes.ATTACHMENT_DATA_GROUP_ID>`.
		The records of one attachment are tagged with :py:const:`ATTACHMENT_DATA_TAG<py_cerebro.dbtypes.ATTACHMENT_DATA_TAG>`, and stand for a particular parameter of the attachment.
		
		Attachments fall into two types: a file and a link to a file. In case of file the attachment has 
		a tag :py:const:`ATTACHMENT_TAG_FILE<py_cerebro.dbtypes.ATTACHMENT_TAG_FILE>`, which contains the hash of the file on a Cargador-operated file storage.
		In case of a link, the attachment is tagged with :py:const:`ATTACHMENT_TAG_LINK<py_cerebro.dbtypes.ATTACHMENT_TAG_LINK>`.
		This entry has no hash, it contains a full path to file :py:const:`ATTACHMENT_DATA_FILE_NAME<py_cerebro.dbtypes.ATTACHMENT_DATA_FILE_NAME>` in its name field.
		The entry tagged with :py:const:`ATTACHMENT_TAG_REVIEW<py_cerebro.dbtypes.ATTACHMENT_TAG_REVIEW>` is available only if the file has a Mirada review over it.
		The entry with a thumbnail tag :py:const:`ATTACHMENT_TAG_THUMB...<py_cerebro.dbtypes.ATTACHMENT_TAG_THUMB1>`, is available only if the file is a picture or video.
		If the file is a picture, it has only one entry :py:const:`ATTACHMENT_TAG_THUMB1<py_cerebro.dbtypes.ATTACHMENT_TAG_THUMB1>`, if it is a video -- three entries.
		"""

		return self.z_execute(True, 'select * from "listAttachmentsArray"(?, false)',  to_array(message_id))

	def users(self):
		"""
		:returns: table of users/material resources.
		
		The table fields are described in the module dbtypes: :py:const:`USER_DATA_...<py_cerebro.dbtypes.USER_DATA_>`
		
		A material resource has a flag set :py:const:`USER_FLAG_IS_RESOURCE<py_cerebro.dbtypes.USER_FLAG_IS_RESOURCE>`.
		You can check the state of the flag with the function :py:func:`cclib.has_flag<py_cerebro.cclib.has_flag>`::
		
			if cclib.has_flag(user[dbtypes.USER_DATA_FLAGS], dbtypes.USER_FLAG_IS_RESOURCE): #if it is material resource
				# actions
		"""

		return self.z_execute(True, 'select uid, "userNameDisplay"(uid) as name, "userGetFlags"(uid) as flags' +
									', "userGetLogin"(uid) as lid, "userGetFirstName"(uid) as firstname, "userGetLastName"(uid) as lastname' +
									', "userGetEmail"(uid) as email, "userGetPhone"(uid) as phone, "userGetIcq"(uid) as icq from "userList"() order by name')

	def activities(self):
		"""
		:returns: table of activities.
		
		The table fields are described in the module dbtypes: :py:const:`ACTIVITY_DATA_...<py_cerebro.dbtypes.ACTIVITY_DATA_>`
		"""

		return self.z_execute(True, 'select uid, name from "listActivities"(false)')

	def statuses(self):
		"""
		:returns: the table of all statuses.

		The table fields are described in the module dbtypes: :py:const:`STATUS_DATA_...<py_cerebro.dbtypes.STATUS_DATA_>`		
		"""
		return self.z_execute(True, 'select * from "statusList"()')

	def add_task(self,  parent_id,  name,  activity_id = 0):
		"""
		:param int parent_id: parent task ID.
		:param string name: name of the new task.
		:param int activity_id: activity type ID. Default - '0' (No activity).
		
		:returns: new task ID.
		
		New task creation. The symbols: **\\\\ / # : ? & ' " , + |** cannot be used in a task name.
		
		.. note:: To send a notice to the user about the new task, you must create
			:py:meth:`the "Defenition" type message <py_cerebro.database.Database.add_definition>` in the task.
		"""
		
		match = re.search(r"[\\\\/#:?&'\",|+]+", name)
		if match:
			raise Exception("Name is incorrect. Symbols \\ / # : ? & ' \" , + | are not allowed")
			
		return self.z_execute(False, 'select "newTask_00"(?,?,?,true)',  parent_id,  name,  activity_id)[0][0]

	def task_set_name(self,  task_id,  name):
		"""
		:param int task_id: task ID.
		:param string name: new task name.
		
		Sets a new name for a task.
		It cannot contain the following symbols: **\\\\ / # : ? & ' " , + |**.
		"""
		
		match = re.search(r"[\\\\/#:?&'\",|+]+", name)
		if match:
			raise Exception("Name is incorrect. Symbols \\ / # : ? & ' \" , + | are not allowed")
			
		return self.z_execute(False, 'select "taskSetName"(?,?)',  task_id,  name)[0][0]

	def task_set_activity(self,  task_id,  activity_id):
		"""
		:param task_id: task ID or array of task IDs.
		:type task_id:  int, set(int, ) or list(int, )
		:param int activity_id: activity ID.
		
		Sets an activity type for a task. Activity ID = 0 sets the task activity type to 'No activity'.
		"""

		tasks = self.z_execute(False, 'select "taskSetActivity_a"(?,?)',  to_array(task_id),  activity_id)

		ids = set()
		for task in tasks:              
			ids.add(task[0])

		return ids

	def task_set_status(self,  task_id,  status_id):
		"""
		:param task_id: task ID or array of task IDs.
		:type task_id:  int, set(int, ) or list(int, )
		:param int status_id: status ID.

		Sets a status for a task. Status ID = None sets the task status to 'No Status'.
		"""
		
		tasks = self.z_execute(False, 'select "taskSetStatus_a"(?,?)',  to_array(task_id),  status_id)

		ids = set()
		for task in tasks:              
			ids.add(task[0])

		return ids

	def task_set_priority(self,  task_id,  prior):
		"""
		:param task_id: task ID or array of task IDs.
		:type task_id:  int, set(int, ) or list(int, )
		:param int prior: Task priority value.
		
		Sets task priority level.
		
		Priority values are described in the module dbtypes: :py:const:`TASK_PRIORITY_...<py_cerebro.dbtypes.TASK_PRIORITY_>`
		"""

		tasks = self.z_execute(False, 'select "taskSetPriority_a"(?,?::smallint)',  to_array(task_id),  prior)

		ids = set()
		for task in tasks:              
			ids.add(task[0])

		return ids

	def task_set_flag(self,  task_id,  flag,  is_set):
		"""
		:param task_id: task ID or array of task IDs.
		:type task_id:  int, set(int, ) or list(int, )
		:param int flag: flag value.
		:param bool is_set: current flag setting.
		
		Sets a flag for a task.
		If *is_set* is True, the flag sets, otherwise - resets.
		
		::
		
			# Setting "Closed" status for a task
			db.task_set_flag(task_id, dbtypes.TASK_FLAG_CLOSED, True)
		
		Flag values are described in the module dbtypes: :py:const:`TASK_FLAG_...<py_cerebro.dbtypes.TASK_FLAG_>`
		"""

		newFlag = 0
		if is_set:
			newFlag = 1 << flag
			
		mask	= 1 << flag
			
		self.z_execute(False, 'select "taskSetFlagsMulti"(?,?,?)',  to_array(task_id),  newFlag,  mask)

	def task_set_progress(self,  task_id,  progress):
		"""
		:param task_id: task ID or array of task IDs.
		:type task_id:  int, set(int, ) or list(int, )
		:param int progress: progress value.
		
		Sets progress value for a task.
		If value is 100, the task is considered complete (Done).
		If value is set to None, the task progress value is reset to a sum of progress values of its subtasks.
		"""

		tasks = self.z_execute(False, 'select "taskSetProgress_a"(?,?::smallint)',  to_array(task_id),  progress)

		ids = set()
		for task in tasks:              
			ids.add(task[0])

		return ids

	def task_set_planned_time(self,  task_id,  hours):
		"""
		:param task_id: task ID or array of task IDs.
		:type task_id:  int, set(int, ) or list(int, )
		:param float hours: planned working time (hours).
		
		Sets the time planned to fulfill the task in hours.
		If hours argument is set to None, the planned time is reset.
		After that the planned time is calculated according to calendar time frames and current work schedule of allocated user(s).
		"""	

		tasks = self.z_execute(False, 'select "taskSetPlanned_a"(?,?)',  to_array(task_id),  hours)

		ids = set()
		for task in tasks:              
			ids.add(task[0])

		return ids

	def task_set_start(self,  task_id,  time):
		"""
		:param task_id: task ID or array of task IDs.
		:type task_id: int, set(int, ) or list(int, )
		:param float time: days from 01.01.2000.
		
		Sets the starting moment for a task, in days from 01.01.2000 (UTC time)
		
		If time = None, the start time value is reset.
		After resetting the starting point is calculated according to the task connections and the schedule.
		
		::
		
			db.task_set_start({task_id, task_id1}, 4506.375) # starting point is May 03, 2012 9:00am UTC
		
		An example of setting the starting time equal to current time

		::

			import datetime

			datetime_now = datetime.datetime.utcnow()
			datetime_2000 = datetime.datetime(2000, 1, 1)
			timedelta = datetime_now - datetime_2000
			days = timedelta.total_seconds()/(24*60*60)	
	
			db.task_set_start({task_id, task_id1}, days) 
		"""

		tasks = self.z_execute(False, 'select "ggSetTaskOffset_a"(?,?::double precision)',  to_array(task_id),  time)

		ids = set()
		for task in tasks:              
			ids.add(task[0])

		return ids

	def task_set_finish(self,  task_id,  time):
		"""
		:param task_id: task ID or array of task IDs.
		:type task_id: int, set(int, ) or list(int, )
		:param float time: days from 01.01.2000 (UTC), 
		
		Sets the task finish time, in days from 01.01.2000 (UTC time).
		
		If time = None, the finish time value is reset.
		After resetting the finish time is calculated according to the schedule and the planned working time.
		
		::
		
			db.task_set_finish(task_id, 4506.75) # the finish time is 03.05.2012 18:00 UTC
		
		An example of setting the task finish time in 3 days ahead from current time
		
		::
		
			import datetime
			
			datetime_now = datetime.datetime.utcnow()
			datetime_2000 = datetime.datetime(2000, 1, 1)
			timedelta = datetime_now - datetime_2000
			days = timedelta.total_seconds()/(24*60*60) + 3
			
			db.task_set_finish(task_id, days) 
		"""

		tasks = self.z_execute(False, 'select "ggSetTaskStop_a"(?,?::double precision)', to_array(task_id),  time)

		ids = set()
		for task in tasks:              
			ids.add(task[0])

		return ids


	def task_set_budget(self,  task_id,  budget):
		"""
		:param task_id: task ID or array of task IDs.
		:type task_id: int, set(int, ) or list(int, )
		:param float budget: budgeted amount (in abstract currency units).
		
		Sets the task budget.
		
		If set to None, the current budget value is reset to the sum of its subtask budgets.
		"""

		tasks = self.z_execute(False, 'select "taskSetCosts_a"(?,?)',  to_array(task_id),  budget)

		ids = set()
		for task in tasks:              
			ids.add(task[0])

		return ids

	def task_set_allocated(self,  task_id,  user_id):
		"""
		:param task_id: task ID or array of task IDs.
		:type task_id: int, set(int, ) or list(int, )
		:param user_id: ID of user/material resource or array of ID of user/material resource.
		:type user_id: int, set(int, ) or list(int, )
		
		Allocates a user to a task.
		
		.. note:: To send a notice to the user about the assigned task, you must have 
			:py:meth:`the "Defenition" type message <py_cerebro.database.Database.task_definition>` in the task.
		"""

		tasks = self.z_execute(False, 'select "userAssignmentTask_a"(?,?,?)',  to_array(task_id),  to_array(user_id),  1)

		ids = set()
		for task in tasks:              
			ids.add(task[0])

		return ids

	def task_remove_allocated(self,  task_id,  user_id):
		"""
		:param task_id: task ID or array of task IDs.
		:type task_id: int, set(int, ) or list(int, )
		:param user_id: ID of user/material resource or array of ID of user/material resource.
		:type user_id: int, set(int, ) or list(int, )
		
		Dismisses an allocated user from a task.
		"""	

		tasks = self.z_execute(False, 'select "userAssignmentTask_a"(?,?,?)', to_array(task_id), to_array(user_id),  0)

		ids = set()
		for task in tasks:
			ids.add(task[0])

		return ids

	def task_set_hashtags(self, task_id, hashtags):
		"""
		:param task_id: task ID or array of task IDs.
		:type task_id: int, set(int, ) or list(int, )
		:param hashtags: array of hashtags(every hashtag should be written in one word without spaces).
		:type hashtags: string, set(string, ) or list(string, )

		Sets the task hashtags.
		"""

		tasks = self.z_execute(False, 'select "htSetTask"(?,?,?)', to_array(task_id), hashtags, True)

		ids = set()
		for task in tasks:
			ids.add(task[0])

		return ids

	def task_hashtags(self, task_id):
		"""
		:param task_id: task ID or array of task IDs.
		:type task_id: int, set(int, ) or list(int, )

		Gets the task hashtags.

		::
			# Работа с хэштегами задачи
			to_do_task_list = db.to_do_task_list(db.current_user_id(),  True)
			db.task_set_hashtags(to_do_task_list[0][dbtypes.TASK_DATA_ID], {'хэштег1', 'хэштег2', 'хэштег3'}) # присваиваем задаче массив хэштегов
			db.task_remove_hashtags(to_do_task_list[0][dbtypes.TASK_DATA_ID], 'хэштег2') # удаляем хэштег
			hashtags = db.task_hashtags(to_do_task_list[0][dbtypes.TASK_DATA_ID]) # получаем хэштеги задачи
			print('Хэштеги задачи ',  hashtags) # распечатываем хэштеги

		"""

		#hashtags = '' #self.z_execute(True, 'select "htSetTask"(?,?,?)', task_id), hashtags, True)
		hashtags = self.execute('select "htTask"(?)', task_id)

		return hashtags

	def task_remove_hashtags(self, task_id, hashtags):
		"""
		:param task_id: task ID or array of task IDs.
		:type task_id: int, set(int, ) or list(int, )
		:param hashtags: array of hashtags(every hashtag should be written in one word without spaces).
		:type hashtags: string, set(string, ) or list(string, )

		Removes the task hashtags.
		"""

		tasks = self.z_execute(False, 'select "htSetTask"(?,?,?)', to_array(task_id), to_array(hashtags), False)

		ids = set()
		for task in tasks:
			ids.add(task[0])

		return ids

	def message_set_hashtags(self, message_id, hashtags):
		"""
		:param message_id: message ID or array of message IDs.
		:type message_id: int, set(int, ) or list(int, )
		:param hashtags: array of hashtags(every hashtag should be written in one word without spaces).
		:type hashtags: string, set(string, ) or list(string, )

		Sets the message hashtags.
		"""

		tasks = self.z_execute(False, 'select "htSetEvent"(?,?,?)', to_array(message_id), to_array(hashtags), True)

		ids = set()
		for task in tasks:
			ids.add(task[0])

		return ids

	def message_hashtags(self, message_id):
		"""
		:param message_id: message ID or array of message IDs.
		:type message_id: int, set(int, ) or list(int, )

		Gets the message hashtags.
		"""

		hashtags = ''#self.z_execute(True, 'select "htSetEvent"(?,?,?)', to_array(message_id), to_array(hashtags), True)

		return hashtags

	def message_remove_hashtags(self, message_id, hashtags):
		"""
		:param message_id: message ID or array of message IDs.
		:type message_id: int, set(int, ) or list(int, )
		:param hashtags: array of hashtags(every hashtag should be written in one word without spaces).
		:type hashtags: string, set(string, ) or list(string, )

		Removes the message hashtags.
		"""

		tasks = self.z_execute(False, 'select "htSetEvent"(?,?,?)', to_array(message_id), to_array(hashtags), False)

		ids = set()
		for task in tasks:
			ids.add(task[0])

		return ids

	def attachment_set_hashtags(self, attachment_id, hashtags):
		"""
		:param attachment_id: attachment ID or array of attachment IDs.
		:type attachment_id: int, set(int, ) or list(int, )
		:param hashtags: array of hashtags(every hashtag should be written in one word without spaces).
		:type hashtags: string, set(string, ) or list(string, )

		Sets the attachment hashtags.

		.. note:: Recommended for attachments with tag ATTACHMENT_DATA_TAG value: ATTACHMENT_TAG_FILE or ATTACHMENT_TAG_LINK.
		"""

		tasks = self.z_execute(False, 'select "htSetAttachment"(?,?,?)', to_array(attachment_id), to_array(hashtags), True)

		ids = set()
		for task in tasks:
			ids.add(task[0])

		return ids

	def attachment_hashtags(self, attachment_id):
		"""
		:param attachment_id: attachment ID or array of attachment IDs.
		:type attachment_id: int, set(int, ) or list(int, )

		Gets the attachment hashtags.

		.. note:: Recommended for attachments with tag ATTACHMENT_DATA_TAG value: ATTACHMENT_TAG_FILE or ATTACHMENT_TAG_LINK.
		"""

		hashtags = ''#self.z_execute(True, 'select "htSetAttachment"(?,?,?)', to_array(attachment_id), to_array(hashtags), True)

		return hashtags

	def attachment_remove_hashtags(self, attachment_id, hashtags):
		"""
		:param attachment_id: attachment ID or array of attachment IDs.
		:type attachment_id: int, set(int, ) or list(int, )
		:param hashtags: array of hashtags(every hashtag should be written in one word without spaces).
		:type hashtags: string, set(string, ) or list(string, )

		Removes the attachment hashtags.

		.. note:: Recommended for attachments with tag ATTACHMENT_DATA_TAG value: ATTACHMENT_TAG_FILE or ATTACHMENT_TAG_LINK.
		"""

		tasks = self.z_execute(False, 'select "htSetAttachment"(?,?,?)', to_array(attachment_id), to_array(hashtags), False)

		ids = set()
		for task in tasks:
			ids.add(task[0])

		return ids

	def set_link_tasks(self,  first_task_id,  second_task_id):
		"""
		:param int first_task_id: predecessor task ID.
		:param int second_task_id: follower task ID.
		:returns: connection ID.
		:rtype: int
		
		Creates a sequence of tasks.
		"""

		return self.z_execute(False, 'select "ggLinkAdd_a"(?,?,?)',  to_array(first_task_id),  to_array(second_task_id),  0)[0][0]

	def drop_link_tasks(self,  link_id):
		"""
		:param int link_id: connection ID.
		
		Breaks a sequential connection between tasks.
		"""

		self.z_execute(False, 'select "ggLinkDel_a"(?,?)',  to_array(link_id),  True)

	def add_definition(self,  task_id,  html_text):
		"""
		:param int task_id: task ID.
		:param string html_text: message text in html.
		:returns: new message ID.
		:rtype: int
		
		Adds a message of "Definition" type.
		"""	

		return self.z_execute(False, 'select "eventNew"(?,?,?,?,?,?)',  None,  task_id,  html_text, MESSAGE_TYPE_DEFINITION,  None,  None)[0][0]

	def add_review(self,  task_id,  message_id,  html_text,  minutes = None):
		"""
		:param int task_id: task ID.
		:param int message_id: ID of the message being replied to.
		:param string html_text: message text in html.
		:param int minutes: confirmed working time, minutes.
		:returns: new message ID.
		:rtype: int
		
		Adds a message of "Review" type.
		"""

		return self.z_execute(False, 'select "eventNew"(?,?,?,?,?,?)',  None,  task_id,  html_text, MESSAGE_TYPE_REVIEW,  message_id,  minutes)[0][0]

	def add_client_review(self,  task_id,  message_id,  html_text):
		"""
		:param int task_id: task ID.
		:param int message_id: ID of the message being replied to.
		:param string html_text: message text in html.
		:returns: new message ID.
		:rtype: int
		
		Adds a message of "Client Review" type.
		"""

		return self.z_execute(False, 'select "eventNew"(?,?,?,?,?,?)',  None,  task_id,  html_text, MESSAGE_TYPE_CLIENT_REVIEW,  message_id,  None)[0][0]

	def add_report(self,  task_id,  message_id,  html_text,  minutes):
		"""
		:param int task_id: task ID.
		:param int message_id: ID of the message being replied to.
		:param string html_text: message text in html.
		:param int minutes: signed off working time, minutes.
		:returns: new message ID.
		:rtype: int

		It's very important to set minutes for report. 
		If minutes 0 or None report will not be added to statistic.
		
		Adds a message of "Report" type.
		"""

		if minutes == None:
			minutes = 0

		return self.z_execute(False, 'select "eventNew"(?,?,?,?,?,?)',  None,  task_id,  html_text, MESSAGE_TYPE_REPORT,  message_id,  minutes)[0][0]

	def add_resource_report(self,  task_id,  message_id,  resource_id,  html_text,  minutes):
		"""
		:param int task_id: task ID.
		:param int message_id: ID of the message being replied to.
		:param int resource_id: идентификатор материального ресурса, за который пишется отчет.
		:param string html_text: message text in html.
		:param int minutes: signed off working time, minutes.
		:returns: new message ID.
		:rtype: int
		
		Adds a message of "Resource Report" type.
		"""

		return self.z_execute(False, 'select "eventNew"(?,?,?,?,?,?)',  resource_id,  task_id,  html_text, MESSAGE_TYPE_RESOURCE_REPORT,  message_id,  minutes)[0][0]

	def add_note(self,  task_id,  message_id,  html_text):
		"""
		:param int task_id: task ID.
		:param int message_id: ID of the message being replied to.
		:param string html_text: message text in html.
		:returns: new message ID.
		:rtype: int
		
		Adds a message of "Note" type.
		"""

		return self.z_execute(False, 'select "eventNew"(?,?,?,?,?,?)',  None,  task_id,  html_text, MESSAGE_TYPE_NOTE,  message_id,  None)[0][0]

	def add_attachment(self,  message_id,  carga,  filename,  thumbnails,  description,  as_link, path = ''):
		"""
		:param int message_id: message ID.
		:param py_cerebro.cargador.Cargador carga: object of class :py:class:`cargador.Cargador<py_cerebro.cargador.Cargador>`, to import files to a file storage.
		:param string filename: full path to file.
		:param thumbnails: a list of paths to thumbnail files (3 max). Thumbnail size must be 512x512 pixels. Format - JPG or PNG.
		:param string description: comments to the attachment.
		:param bool as_link: method of file attachment to the message:
			True - file is attached as a link;
			False - file is imported physically to a file storage.
		
		Attaching a file to a message.
		
		**Using for thumbnail generation.**
		
		If a file is a picture or a video, it may have thumbnails to display in Cerebro forum.
		A video file may have up to 3 thumnails (the first frame, the middle frame or the last frame).
		By default thumbnails are generated by Mirada player, bundled with Cerebro.
		
		::
		
			#An example of generating thumbnails with Mirada.
			
			gen_path = os.path.dirname(filename) # Selecting the folder with the attached file as the folder to save thumbnails in
			mirada_path = './mirada' # path to Mirada executable
			
			# Executing Mirada with necessary keys
			res_code = subprocess.call([mirada_path, filename, '-temp', gen_path, '-hide'])				
			#-temp - folder to generate thumbnails to
			#-hide - key to launch Mirada in hidden mode (without GUI) to generate thumbnails.
			
			if res_code != 0:
				raise Exception("Mirada returned bad exit-status.\\n" + mirada_path);
			
			#Searching for thumbnails generated by Mirada.
			#Thumbnail filename is composed from the source file name, date and time of creation - filename_yyyymmdd_hhmmss_thumb[number].jpg
			#For example: test.mov_20120305_112354_thumb1.jpg - the thumbnail of the first frame of the test.mov videofile
			
			thumbnails = list()
			for f in os.listdir(gen_path):
				if fnmatch.fnmatch(f, os.path.basename(filename) + '_*_thumb?.jpg'):
					thumbnails.append(gen_path + '/' + f)
			
			thumbnails.sort()
		
		Beside Mirada, some other software, for instance, ffmpeg, can be used to generate thumbnails.
		
		::
		
			#An example of generating thumbnails with ffmpeg.
			#Prior to generating thumbnails with ffmpeg it is necessary to resolve the duration of video,
			#in order to calculate the middle and the last frame correctly.
			#Let's take, for example, a 30-second long video.
			
			thumbnails = list() # file list for thumbnails
			thumbnails.append(filename + '_thumb1.jpg')
			thumbnails.append(filename + '_thumb2.jpg')
			thumbnails.append(filename + '_thumb3.jpg')
			
			subprocess.call(['ffmpeg', '-i', filename, '-s', '512x512', '-an', '-ss', '00:00:00', '-r', 1, '-vframes', 1, '-y', thumbnails[0]])
			subprocess.call(['ffmpeg', '-i', filename, '-s', '512x512', '-an', '-ss', '15:00:00', '-r', 1, '-vframes', 1, '-y', thumbnails[1]])
			subprocess.call(['ffmpeg', '-i', filename, '-s', '512x512', '-an', '-ss', '30:00:00', '-r', 1, '-vframes', 1, '-y', thumbnails[2]])
			# The key descriptions can be found in ffmpeg documentation
		"""

		if not as_link and not os.path.exists(filename):
			raise Exception('File ' + filename + ' not found')

		"""
		Attaching a file to a message goes in two phases:
		1 - adding the file to Cargador-controlled file storage
			the phase is skipped, if the file is being attached as a link
		2 - adding a corresponding entry(-ies) about the file(-s) to the database
		"""	

		# If the file is attached physically, adding it to Cargador and getting its hash
		hash = ''
		if as_link != True:
			if (carga) is None:
				raise Exception('Cargador connection is NOT established')
			# Query to get text locator of the task
			if path:
				task_url = path
			else:
				rtask_url = self.z_execute(True, 'select "getUrlBody_byTaskId_00"((select taskid from "eventQuery_08"(?)))', to_array(message_id))
				task_url = rtask_url[0][0]
			
			# Importing file to the storage
			hash64 = carga.import_file(filename,  task_url)
			hash = hash64_16(hash64)

			# If hash is unavailable, dropping exception
			if hash == None or len(hash) == 0:
				raise Exception('Hash is unavailable')


		tag = ATTACHMENT_TAG_FILE
		file_size = 0
		file_name = ''
		if as_link == True:
			tag = ATTACHMENT_TAG_LINK
			file_name = filename.replace('\\', '/')
		else:
			file_size = os.stat(filename).st_size
			file_name = os.path.basename(filename)

		"""
		The "tag" parameter is required to define the type of attachment:
		dbtypes.ATTACHMENT_TAG_FILE - file is imported, i.e., it is stored in the Cargador-controlled file storage and it has a hash sum
		dbtypes.ATTACHMENT_TAG_LINK - file/folder is linked.

		file_size - file size, bytes. For  link = 0.

		file_name - file name. For a link - full path to file, for an imported file - just its basic name

		description - text comments to the attachment
		"""

		# Getting a new entry ID to enlist the file into the database
		rnew_attach_id = self.z_execute(False, 'select "getNewAttachmentGroupID"()')
		new_attach_id = rnew_attach_id[0][0]

		# Adding the entry
		self.z_execute(False, 'select "newAtachment_00_"(?::bigint, ?::integer, ?, ?::integer, ?::bigint, ?, ?)',
				message_id, new_attach_id, hash, tag, file_size, file_name, description)
		
		"""
		The added file may have several entries, e.g., it may have thumbnails or reviews.
		The additional entries must use the same ID but the tags must differ.
		If you modify this script for adding several files,
		you have to get a separate new ID for each file.
		"""

		if (carga) is None:
			print('Cargador connection is NOT established')
		else:
			if thumbnails != None and len(thumbnails) > 0:
				# Adding thumbnails to the file storage and getting their hash sums
				hashthumbs = list()
				for f in thumbnails:
					# Importing a thumbnail to the file storage
					th_hash64 = carga.import_file(f,  'thumbnail.cache')
					th_hash = hash64_16(th_hash64)
					hashthumbs.append(th_hash)

				# Adding thumbnail hash sums to the database
				for i in range(len(hashthumbs)):
					if i > 2:
						break
					# Setting a tag for the thumbnail. 1 - first frame, 2 - middle frame, 3 - last frame
					tag = i+1

					# Adding thumbnail entry, executing entry adding query
					self.z_execute(False, 'select "newAtachment_00_"(?::bigint, ?::integer, ?, ?::integer, ?::bigint, ?, ?)',
							message_id, new_attach_id, hashthumbs[i], tag, 0, '', '')
					"""
						Such parameters as file size, file name and text comments make no sense, therefore the corresponding fields are empty
					"""

		return new_attach_id

	def project_tags(self,  project_id):
		"""
		:param int project_id: project ID.
		:returns: project tags table. The table contains all of the tags that can be set on project tasks.

		The table fields are described in the module dbtypes: :py:const:`TAG_DATA_...<py_cerebro.dbtypes.TAG_DATA_>`		
		"""		
		return self.z_execute(True, 'select * from "tagSchemaList_byPrj"(?)',  project_id)
	
	def tag_enums(self,  tag_id):
		"""
		:param int tag_id: tag ID.
		:returns:  tag enumeration table. The table contains enumerations that can be set as the tag value.

		The table fields are described in the module dbtypes: :py:const:`TAG_ENUM_DATA_...<py_cerebro.dbtypes.TAG_ENUM_DATA_>`		
		"""		
		return self.z_execute(True, 'select * from "tagEnumList"(?, false)',  tag_id)

	def task_set_tag_enum(self,  task_id,  enum_id,  is_set):
		"""
		:param task_id: task ID(s).
		:type task_id: int, set(int, ) or list(int, )
		:param enum_id: enumeration ID(s).
		:type enum_id: int, set(int, ) or list(int, )
		:param bool is_set: enumeration set / removed parameter.

		Sets or removes tag value of enumeration or multiple enumeration type for a task(s).
		"""
		
		tasks = self.z_execute(False, 'select "tagTaskSetEnum_a"(?,?,?)',  to_array(enum_id),  to_array(task_id),  is_set)

		ids = set()
		for task in tasks:              
			ids.add(task[0])

		return ids

	def task_set_tag_float(self,  task_id,  tag_id,  value):
		"""
		:param task_id: task ID(s).
		:type task_id: int, set(int, ) or list(int, )
		:param int tag_id: tag ID.
		:param int value: tag value.

		Sets tag value of floating-point number type for a task(s).	
		"""
		
		tasks = self.z_execute(False, 'select "tagTaskSetReal_a"(?,?,?)',  tag_id, to_array(task_id), value)

		ids = set()
		for task in tasks:              
			ids.add(task[0])

		return ids
	
	def task_set_tag_int(self,  task_id,  tag_id,  value):
		"""
		:param task_id: task ID(s).
		:type task_id: int, set(int, ) or list(int, )
		:param int tag_id: tag ID.
		:param int value: tag value.

		Sets tag value of integer number type for a task(s).	
		"""
		
		tasks = self.z_execute(False, 'select "tagTaskSetInt_a"(?,?,?)',  tag_id, to_array(task_id), value)

		ids = set()
		for task in tasks:              
			ids.add(task[0])

		return ids

	def task_set_tag_string(self,  task_id,  tag_id,  value):
		"""
		:param task_id: task ID(s).
		:type task_id: int, set(int, ) or list(int, )
		:param int tag_id: tag ID.
		:param int value: tag value.

		Sets tag value of string type for a task(s).	
		"""
		
		tasks = self.z_execute(False, 'select "tagTaskSetStr_a"(?,?,?)',  tag_id, to_array(task_id), value)

		ids = set()
		for task in tasks:              
			ids.add(task[0])

		return ids
	
	def task_tag_reset(self,  task_id,  tag_id):
		"""
		:param task_id: task ID(s).
		:type task_id: int, set(int, ) or list(int, )
		:param int tag_id: tag ID.

		Removes tag value from a task(s).	
		"""
		
		tasks = self.z_execute(False, 'select "tagTaskReset_a"(?,?)', tag_id, to_array(task_id))

		ids = set()
		for task in tasks:              
			ids.add(task[0])

		return ids

	def task_tag_enums(self,  task_id,  tag_id):
		"""
		:param int task_id: task ID.
		:param int tag_id: tag ID.
		:returns: table of tag enumerations set on a task.

		The table fields are described in the module dbtypes: :py:const:`TASK_TAG_ENUM_...<py_cerebro.dbtypes.TASK_TAG_ENUM_>`
		"""
		return self.z_execute(True, 'select * from "tagTaskEnums"(?,?)',  task_id, tag_id)
	
	def task_tags(self,  task_id):
		"""
		:param int task_id: task ID.
		:returns: table of tag values set on a task.

		The table fields are described in the module dbtypes: :py:const:`TASK_TAG_DATA_...<py_cerebro.dbtypes.TASK_TAG_DATA_>`
		"""
		return self.z_execute(True, 'select * from "tagTaskList"(?)',  task_id)

	def task_by_url(self,  url):
		"""
		:param string url: url of task.
		:returns: task ID.

		Return task ID by url. Url example: '/Test project/test'
		"""
		id = self.z_execute(True, 'select * from "getTaskID_byURL"(?)', url)
		if len(id) == 1:
			return id[0]
			
		return None
