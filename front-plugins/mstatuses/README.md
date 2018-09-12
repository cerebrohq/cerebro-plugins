mstatuses - plugin for automatic changing status

Different statuses will be setted for messages types:
- Report message - status 'report_status_name' ('pending review' in example)
- Review message - status 'review_status_name' ('in progress' in example)
- Client review - status 'client_review_status_name' ('could be better' in example)
All this status messages will be removed from task forum

If user post Report to task and task progress less than 'new_task_percent' (5% in example), progress of task set to 'new_task_percent' value
If task status is 'complete_status_name', progress will be set to 100%