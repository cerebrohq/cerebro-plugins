# -*- coding: utf-8 -*-

import cerebro
import datetime
from cerebro.aclasses import Statuses
from cerebro.aclasses import Users
from cerebro.aclasses import AbstractMessage

report_status_name = 'pending review' # status after posting Report
review_status_name = 'in progress' # status after posting Review
client_review_status_name = 'could be better' # status after posting Client Review
new_task_percent = 5.0 # new progress % after first Report message
complete_status_name = 'completed' # Complete status name
"""
def change_status(task, to_status):
    for status in task.possible_statuses():
        if status[Statuses.DATA_NAME] == to_status:
            task.set_status(status[Statuses.DATA_ID])
            return True

    return False
"""
def change_status(task, event, to_status):    
    for status in task.possible_statuses():
        if status[Statuses.DATA_NAME] == to_status:
            event.set_new_task_status(status[Statuses.DATA_ID])
            return True

    return False

def task_messages(task_id):		
    db = cerebro.db.Db()
    messs = db.execute('select uid from "_event_list"(%s, false) order by mtm desc limit 1',  task_id)
    ids = set()
    for mess in messs:              
        ids.add(mess[0])

    return db.execute('select * from "eventQuery_08"(%s)',  ids)

def remove_event(msg):
    db = cerebro.db.Db()
    db.execute('select "_event_update"(%s, 1::smallint, 0, 0)', msg[AbstractMessage.DATA_ID])

def before_event(event):
    # change progress on first 
    if event.event_type() == event.EVENT_CREATION_OF_MESSAGE:
         task = cerebro.core.task(event.task_id())
         if event.type() == event.TYPE_REPORT:             
             """has_report = False
             for message in task_messages(event.task_id()):
                 if message[AbstractMessage.DATA_TYPE] == AbstractMessage.TYPE_REPORT:
                     has_report = True
                     break

             task = cerebro.core.task(event.task_id())""" 
             if task.progress() < new_task_percent:  #not has_report and 
                 task.set_progress(new_task_percent)
           
             if event.new_task_status()[cerebro.aclasses.Statuses.DATA_ID] == task.status()[cerebro.aclasses.Statuses.DATA_ID]:
                 change_status(task, event, report_status_name)
         elif event.type() == event.TYPE_REVIEW:
             if event.new_task_status()[cerebro.aclasses.Statuses.DATA_ID] == task.status()[cerebro.aclasses.Statuses.DATA_ID]:
                 change_status(task, event, review_status_name)
         elif event.type() == event.TYPE_CLIENT_REVIEW:
             if event.new_task_status()[cerebro.aclasses.Statuses.DATA_ID] == task.status()[cerebro.aclasses.Statuses.DATA_ID]:
                 change_status(task, event, client_review_status_name)


def after_event(event):
    # Message posting
    if event.event_type() == event.EVENT_CREATION_OF_MESSAGE:
        task = cerebro.core.task(event.task_id())
        status_t = task.status()
        if status_t[Statuses.DATA_NAME] != complete_status_name and (event.type() == event.TYPE_REPORT or event.type() == event.TYPE_REVIEW or event.type() == event.TYPE_CLIENT_REVIEW):
            msgs = task_messages(event.task_id())            
            if msgs and len(msgs):
                 msgdel = msgs[len(msgs) - 1]
                 if (msgdel[1] == AbstractMessage.TYPE_STATUS_CHANGES):
                      remove_event(msgdel)
        
        if status_t[Statuses.DATA_NAME] == complete_status_name:
             task.set_progress(100.0)

    # Status change
    elif event.event_type() == event.EVENT_CHANGING_OF_TASKS_STATUS:
        tasks = event.tasks()
        #user_tasks_lst = None
        for task in tasks: # All selected tasks
            status_t = task.status()
            if status_t[Statuses.DATA_NAME] == complete_status_name:
                task.set_progress(100.0)