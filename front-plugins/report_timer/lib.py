# -*- coding: utf-8 -*-


import cerebro
from PyQt5 import QtWidgets, QtCore, QtGui

import report_timer.config as config

import datetime, time
import tempfile
import os

def init_timer():
	current_user = cerebro.core.user_profile()

	if not is_user_in_group(current_user[cerebro.aclasses.Users.DATA_ID]):
		cerebro.core.start_timer('report_timer.lib.start', config.timer_sec)
		cerebro.core.print_info('timer "report_timer.lib.start" is registered')
	else:
		cerebro.core.print_info('timer "report_timer.lib.start" is NOT registered! User in IGNORE group')

def get_time_int(time):
	ret = None
	if ':' in time:
		h = time.split(':')[0]
		m = time.split(':')[1]

		try:
			h_i = int(h)
			m_i = int(m)
		except Exception as e:
			raise Exception(e)

		ret = h_i + m_i/60

	return ret

def check_tasks(is_tomorrow=False):
	ret = []

	current_user = cerebro.core.user_profile()
	tasks = cerebro.core.to_do_task_list(current_user[cerebro.aclasses.Users.DATA_ID], False)

	db = cerebro.db.Db()

	for task in tasks:
		if task.status()[1] in config.alert_statuses:
			messs = db.execute('select uid from "_event_list"(%s, false)',  task.id())
			ids = set()
			for mess in messs:
				ids.add(mess[0])

			if len(ids) > 0:
				msgs = db.execute('select * from "eventQuery_08"(%s)',  ids)

			has_report = False 

			for msg in reversed(msgs):
				msg_created = msg[5]
				msg_creator_id = msg[13]
				msg_type = msg[3]
				now_date = datetime.datetime(year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day, hour=int(config.report_time.split(':')[0]), minute=int(config.report_time.split(':')[1]))
				if is_tomorrow:
					now_date = datetime.datetime(year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day, hour=int(config.alert_tomorrow_time.split(':')[0]), minute=int(config.alert_tomorrow_time.split(':')[1]))

				msg_date = datetime.datetime(year=msg_created.year, month=msg_created.month, day=msg_created.day, hour=msg_created.hour, minute=msg_created.minute)

				if now_date > msg_date:
					break

				if msg_creator_id == current_user[cerebro.aclasses.Users.DATA_ID] and msg_type == 2:
					has_report = True

			if not has_report:
				ret.append(task)

	return ret

def is_user_in_group(user_id):
	db = cerebro.db.Db()
	user_groups = db.execute('select name from "listUserGroups_00"(%s)', user_id)
	for group in user_groups:
		if group[0] in config.ignore_groups:
			return True

	return False


def start():
	alert_time = get_time_int(config.alert_time)
	current_time = get_time_int(str(datetime.datetime.now().hour) + ':' + str(datetime.datetime.now().minute))
	current_time_full = time.mktime(datetime.datetime.now().timetuple())

	tmp_file = tempfile.gettempdir() + '/tempCerebro/report_timer'
	is_tomorrow = -1
	tmp_time = 0

	if os.path.exists(tmp_file):
		f = open(tmp_file, 'r')
		tmp_time_str = f.read()
		f.close()

		if tmp_time_str:
			tmp_time_str = tmp_time_str.split(':')
			is_tomorrow = int(tmp_time_str[0])
			tmp_time = float(tmp_time_str[1])

	if current_time > alert_time and is_tomorrow == 1:
		os.remove(tmp_file)
		tmp_time = 0

	cerebro.core.print_info('IS_TOMORROW = ' + str(is_tomorrow))
	cerebro.core.print_info('current_time_full = ' + str(current_time_full))
	cerebro.core.print_info('tmp_time = ' + str(tmp_time))

	if (current_time > alert_time and time.mktime(datetime.datetime.now().timetuple()) > tmp_time) or (is_tomorrow == 1 and current_time_full > tmp_time):
		tasks = check_tasks(is_tomorrow == 1)

		cerebro.core.print_info('TASKS with no reports count = ' + str(len(tasks)))

		if len(tasks) > 0:
			cerebro.core.print_info('Show message')
			class Alert_Dialog(QtWidgets.QDialog): # dialog class
				def __init__(self, parent=None):
					super(Alert_Dialog, self).__init__(parent)

					self.ret = -1
			
					label_alert = QtWidgets.QLabel(config.alert_text)	
					label_pic = QtWidgets.QLabel()
					pixmap = QtGui.QPixmap(config.pic_path)
					label_pic.setPixmap(pixmap)

					textLayout = QtWidgets.QHBoxLayout()
					textLayout.addWidget(label_pic)
					textLayout.addWidget(label_alert)

					textWidget = QtWidgets.QWidget()
					textWidget.setLayout(textLayout)
			
					mainLayout = QtWidgets.QGridLayout()
					mainLayout.addWidget(textWidget)

					btn_one_hour = QtWidgets.QPushButton(config.btn_one_hour_text)
					btn_one_hour.clicked.connect(self.btn_one_hour_clicked)
					btn_tomorrow = QtWidgets.QPushButton(config.btn_tomorrow_text)
					btn_tomorrow.clicked.connect(self.btn_tomorrow_clicked)
					btn_report = QtWidgets.QPushButton(config.btn_report_text)
					btn_report.setDefault(True)
					btn_report.clicked.connect(self.btn_report_clicked)

					buttonsLayout = QtWidgets.QHBoxLayout()
					buttonsLayout.addWidget(btn_report)
					buttonsLayout.addWidget(btn_one_hour)
					buttonsLayout.addWidget(btn_tomorrow)

					buttonsWidget = QtWidgets.QWidget()
					buttonsWidget.setLayout(buttonsLayout)

					mainLayout.addWidget(buttonsWidget)
			
					self.setLayout(mainLayout)	

				def btn_one_hour_clicked(self):
					self.ret = 0
					self.close()

				def btn_tomorrow_clicked(self):
					self.ret = 1
					self.close()

				def btn_report_clicked(self):
					self.ret = 2
					self.close()

			cerebro.core.notify_user(config.alert_text, tasks[0].id())

			dlg = Alert_Dialog()
			dlg.exec_()

			dlg_ret = dlg.ret

			if dlg_ret == 0:
				new_datetime = datetime.datetime.now() + datetime.timedelta(hours=1)
				new_time = time.mktime(new_datetime.timetuple())

				f = open(tmp_file, 'w')
				f.write(str(is_tomorrow) + ':' + str(new_time))
				f.close()

				cerebro.core.print_info('1 HOUR: cur_dt = ' + str(time.mktime(datetime.datetime.now().timetuple())) + ' saved_dt = ' + str(new_time))
			elif dlg_ret == 1:
				new_datetime = datetime.datetime.now() + datetime.timedelta(hours=24)
				new_datetime = new_datetime.replace(hour=int(config.alert_tomorrow_time.split(':')[0]), minute=int(config.alert_tomorrow_time.split(':')[1]), second=0)
				new_time = time.mktime(new_datetime.timetuple())
			
				f = open(tmp_file, 'w')
				f.write('1:' + str(new_time))
				f.close()

				cerebro.core.print_info('TOMORROW: cur_dt = ' + str(time.mktime(datetime.datetime.now().timetuple())) + ' saved_dt = ' + str(new_time))
			elif dlg_ret == 2:
				cerebro.core.set_current_task(tasks[0].id())
				cerebro.gui.message_editor(cerebro.aclasses.AbstractMessage.TYPE_REPORT, tasks[0].id())

	else:
		cerebro.core.print_info('Ignore')


