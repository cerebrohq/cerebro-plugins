# -*- coding: utf-8 -*-
import os

pic_path =			os.path.abspath(os.path.dirname(__file__)) + '/alert.png'

timer_sec =			10000 # 300000 msec = 5 min

report_time =		'18:00' # report after
alert_time =		'18:05' # alert after
alert_tomorrow_time='12:00' # 

alert_text =		'Есть задачи без отчета за сегодня. Хотите отправить отчет?'
btn_one_hour_text =	'Отложить на 1 час'
btn_tomorrow_text =	'Отложить до завтра'
btn_report_text =	'Написать отчет'

alert_statuses =	['in progress', 'pending review']
ignore_groups =		['123', 'for script']
