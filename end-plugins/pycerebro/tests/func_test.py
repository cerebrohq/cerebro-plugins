# -*- coding: utf-8 -*-

import sys, os, datetime

cdir = os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir, os.path.pardir))
if not cdir in sys.path:
	sys.path.append(cdir)

from pycerebro import database

OUT_FILE = "output.txt"

TEST_TASK_ID = 281474979774744
TEST_TASK_URL = "/Test project/Scene/New task"
TEST_TASK_STATUS = 3033778
TEST_MSG_ID = 14073748838674318
TEST_USER_ID = 697
TEST_TEXT = "Test text here"
TEST_TIME = 10
TEST_NAME = "Test name"
TEST_DATETIME = datetime.datetime.now()
TEST_TIMEFLOAT = (datetime.datetime.utcnow() - datetime.datetime(2000, 1, 1)).total_seconds()/(24*60*60)	

TEST_FUNCS = [
	['activities', ()],
	#['add_attachment', ()],
	['add_client_review', (TEST_TASK_ID, None, TEST_TEXT)],
	['add_definition', (TEST_TASK_ID, TEST_TEXT)],
	['add_note', (TEST_TASK_ID, None, TEST_TEXT)],
	#['add_note_user', (TEST_TASK_ID, None, TEST_TEXT, TEST_USER_ID, TEST_DATETIME)],
	['add_report', (TEST_TASK_ID, None, TEST_TEXT, TEST_TIME)],
	#['add_report_user', (TEST_TASK_ID, None, TEST_TEXT, TEST_TIME, TEST_USER_ID, TEST_DATETIME)],
	['add_resource_report', (TEST_TASK_ID, None, None, TEST_TEXT, TEST_TIME)],
	['add_review', (TEST_TASK_ID, None, TEST_TEXT)],
	#['add_task', (TEST_TASK_ID, TEST_NAME)],
	#['attachment_hashtags', ()],
	#['attachment_remove_hashtags', ()],
	#['attachment_set_hashtags', ()],
	#['copy_tasks', ()],
	['current_user_id', ()],
	#['drop_link_tasks', ()],
	['message', (TEST_MSG_ID,)],
	['message_attachments', (TEST_MSG_ID,)],
	['message_hashtags', (TEST_MSG_ID,)],
	#['message_remove_hashtags', ()],
	#['message_set_hashtags', ()],
	['messages', ((TEST_MSG_ID,),)],
	#['project_tags', ()],
	['root_tasks', ()],
	#['set_link_tasks', ()],
	['statuses', ()],
	#['tag_enums', ()],
	['task', (TEST_TASK_ID,)],
	['task_allocated', (TEST_TASK_ID,)],
	['task_attachments', (TEST_TASK_ID,)],
	['task_by_url', (TEST_TASK_URL,)],
	['task_children', (TEST_TASK_ID,)],
	['task_definition', (TEST_TASK_ID,)],
	['task_hashtags', (TEST_TASK_ID,)],
	['task_links', (TEST_TASK_ID,)],
	['task_messages', (TEST_TASK_ID,)],
	['task_possible_statuses', (TEST_TASK_ID,)],
	#['task_remove_allocated', ()],
	#['task_remove_hashtags', ()],
	#['task_set_activity', ()],
	['task_set_allocated', (TEST_TASK_ID, TEST_USER_ID)],
	#['task_set_budget', ()],
	['task_set_finish', (TEST_TASK_ID, TEST_TIMEFLOAT)],
	#['task_set_flag', ()],
	#['task_set_hashtags', ()],
	#['task_set_name', ()],
	#['task_set_planned_time', ()],
	#['task_set_priority', ()],
	#['task_set_progress', ()],
	#['task_set_start', ()],
	['task_set_status', (TEST_TASK_ID, TEST_TASK_STATUS)],
	#['task_set_tag_enum', ()],
	#['task_set_tag_float', ()],
	#['task_set_tag_int', ()],
	#['task_set_tag_string', ()],
	#['task_tag_enums', ()],
	#['task_tag_reset', ()],
	#['task_tags', ()],
	['tasks', ((TEST_TASK_ID,),)],
	['to_do_task_list', (TEST_USER_ID, True)],
	['users', ()]
]

def log(msg):
	print(msg)
	with open(OUT_FILE, 'a') as fh:
		fh.write(msg + '\n')

def execute(db, func_name, args):
	log("[ ? ] Trying function \t{0}".format(func_name))
	if hasattr(db, func_name):
		log("[ + ] Calling \t\t\t{0}".format(func_name))
		log("\twith args \t\t{0}".format(args))
		try:
			ret_value = getattr(db, func_name)(*args)
			log("[ + ] Function returned \t{0}".format(ret_value))
		except Exception as e:
			log("[ - ] EXCEPTION \t\t{0}".format(str(e)))
	else:
		log("[ - ] No such function found")
	log("================================================================")
	
	
def test_all():
	db = database.Database("any", 123)
	db.connect("test_user", "qqq")
	
	f = open(OUT_FILE, 'w')
	f.close()
	
	for f in TEST_FUNCS:
		execute(db, f[0], f[1])
	
	
	
	
	
	
	
test_all()
