# -*- coding: utf-8 -*-
"""
Модуль *event* позволяет обрабатывать события, происходящие в приложении.

event.py::

	def before_event(error, event):	
		...

	def after_event(event):	
		...
		
	def error_event(event):	
		...

События происходят при изменении данных в приложении пользователем
и программный интерфейс позволяет управлять этими событиями. 
Приложение генерирует события при выполнении
определенных действий. При этом вызываются соответствующие функции
:py:func:`before_event() <event.before_event>`, :py:func:`after_event()<event.after_event>`
или :py:func:`error_event() <event.error_event>` из :ref:`модуля event <capi-templates>`.

События происходят при операциях изменения  данных,
поэтому смысл этих функций сводится к следующему:

* before_event() - действие перед изменением данных;
* after_event() - действие после изменения данных;
* error_event() - обработка ошибки изменения данных.

"""
# Для включения обработки событий переименуйте этот файл в event.py
# Подробнее об обработке событий смотрите в документации - http://cerebrohq.com/documentation/ru/


import cerebro
import visible.src

# Файлы с примерами лежат в папке ./examples
# Чтобы включить тот или иной пример, необходимо раскомментировать строку с вызовом примера

def before_event(event):
	visible.src.event.before_event(event)	
	pass


def after_event(event):	
	pass
	

def error_event(error, event):	
	pass
